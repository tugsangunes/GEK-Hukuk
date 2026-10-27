<?php
// GEK Hukuk site asistanı: ziyaretçinin sorusunu Claude API'ye iletir ve yanıtı döndürür.
// API anahtarı bu klasörde değil, public_html'in bir üstündeki gek-asistan-config.php dosyasında durur.
// Mesajlar sunucuda saklanmaz; yalnızca IP'nin özetiyle istek sayısı tutulur.
// Bu dosya tools/build.py ile src/api/asistan.php'den üretilir; doğrudan düzenlemeyin.

header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');
header('X-Content-Type-Options: nosniff');

const MODEL = 'claude-opus-5-5';
const MAX_MESSAGES = 12;
const MAX_CHARS = 800;
const PER_IP_PER_HOUR = 30;
const ALL_PER_DAY = 600;
const ALLOWED_HOSTS = ['gekhukuk.com', 'www.gekhukuk.com'];

function fail($code, $msg) {
    http_response_code($code);
    echo json_encode(['error' => $msg], JSON_UNESCAPED_UNICODE);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') fail(405, 'method');

$origin = $_SERVER['HTTP_ORIGIN'] ?? '';
if ($origin !== '' && !in_array(parse_url($origin, PHP_URL_HOST), ALLOWED_HOSTS, true)) fail(403, 'origin');

$config = dirname(__DIR__, 2) . '/gek-asistan-config.php';
if (is_file($config)) require $config;
$key = defined('ANTHROPIC_API_KEY') ? ANTHROPIC_API_KEY : getenv('ANTHROPIC_API_KEY');
if (!$key) fail(503, 'not_configured');

// Basit kullanım sınırı (kişi başı saatlik ve toplam günlük)
function bump($file, $window, $limit) {
    $now = time();
    $fh = fopen($file, 'c+');
    if (!$fh) return true;
    flock($fh, LOCK_EX);
    $times = json_decode(stream_get_contents($fh) ?: '[]', true) ?: [];
    $times = array_values(array_filter($times, function ($t) use ($now, $window) { return $t > $now - $window; }));
    $ok = count($times) < $limit;
    if ($ok) $times[] = $now;
    ftruncate($fh, 0);
    rewind($fh);
    fwrite($fh, json_encode($times));
    flock($fh, LOCK_UN);
    fclose($fh);
    return $ok;
}
$dir = sys_get_temp_dir() . '/gek-asistan';
if (!is_dir($dir)) @mkdir($dir, 0700, true);
$ip = hash('sha256', ($_SERVER['REMOTE_ADDR'] ?? '') . '|gek');
if (!bump("$dir/ip-" . substr($ip, 0, 32), 3600, PER_IP_PER_HOUR)) fail(429, 'rate');
if (!bump("$dir/all", 86400, ALL_PER_DAY)) fail(429, 'rate');

// Gelen konuşmayı doğrula: user ile başlayıp biten, sırayla değişen kısa metinler
$in = json_decode(file_get_contents('php://input'), true);
$msgs = $in['messages'] ?? null;
if (!is_array($msgs) || !$msgs || count($msgs) > MAX_MESSAGES) fail(400, 'messages');
$clean = [];
foreach (array_values($msgs) as $i => $m) {
    $role = $m['role'] ?? '';
    $text = is_string($m['content'] ?? null) ? trim($m['content']) : '';
    if ($role !== ($i % 2 === 0 ? 'user' : 'assistant') || $text === '') fail(400, 'messages');
    if (mb_strlen($text) > ($role === 'user' ? MAX_CHARS : 2000)) fail(400, 'too_long');
    $clean[] = ['role' => $role, 'content' => $text];
}
if (end($clean)['role'] !== 'user') fail(400, 'messages');

$system = <<<'PROMPT'
{{SYSTEM_PROMPT}}
PROMPT;

// Ziyaretçinin bulunduğu sayfanın dili; ziyaretçinin yazdığı dil anlaşılmazsa yanıt bu dilde verilir
const LANG_NAMES = {{LANG_NAMES}};
$lang = $in['lang'] ?? 'tr';
if (!is_string($lang) || !isset(LANG_NAMES[$lang])) $lang = 'tr';
$system .= "\n\nZiyaretçinin bulunduğu sayfanın dili: " . LANG_NAMES[$lang] . " ($lang).";

$body = [
    'model' => MODEL,
    'max_tokens' => 2048,
    'output_config' => ['effort' => 'low'],
    'fallbacks' => 'default',
    'system' => $system,
    'messages' => $clean,
];

$ch = curl_init('https://api.anthropic.com/v1/messages');
curl_setopt_array($ch, [
    CURLOPT_POST => true,
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_TIMEOUT => 60,
    CURLOPT_HTTPHEADER => [
        'content-type: application/json',
        'x-api-key: ' . $key,
        'anthropic-version: 2026-10-21',
        'anthropic-beta: server-side-fallback-2026-07-01',
    ],
    CURLOPT_POSTFIELDS => json_encode($body, JSON_UNESCAPED_UNICODE),
]);
$raw = curl_exec($ch);
$status = curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
curl_close($ch);

$res = $raw ? json_decode($raw, true) : null;
if ($status !== 200 || !is_array($res)) fail(502, 'upstream');
if (($res['stop_reason'] ?? '') === 'refusal') fail(502, 'refusal');

$reply = '';
foreach ($res['content'] ?? [] as $block) {
    if (($block['type'] ?? '') === 'text') $reply .= $block['text'];
}
$reply = trim($reply);
if ($reply === '') fail(502, 'empty');

echo json_encode(['reply' => $reply], JSON_UNESCAPED_UNICODE);

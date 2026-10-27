# GEK Hukuk Bürosu web sitesi

Güneş, Erdil, Karakaya Hukuk Bürosu'nun (gekhukuk.com) statik web sitesi. Derleme adımı yoktur; sayfalar düz HTML ve CSS'tir.

| Dosya | İçerik |
| --- | --- |
| `index.html` | Ana sayfa: Hakkımızda, Çalışma Alanları, Avukatlar, Yayınlar, İletişim |
| `kvkk.html` | KVKK Aydınlatma Metni (doldurulacak) |
| `cerez.html` | Çerez Politikası |
| `CNAME` | GitHub Pages için özel alan adı |

Sarı işaretli (`class="ph"`) alanlar henüz doldurulmamış bilgilerdir.

## İçerik kuralları

Site, Avukatlık Kanunu, TBB Meslek Kuralları ve Reklam Yasağı Yönetmeliği'ne uygun olarak yalnızca bilgilendirme amaçlıdır. Metin eklerken "en iyi", "uzman", başarı oranı gibi iddialar, müvekkil listesi, müvekkil yorumları ve ücret bilgisi kullanılmamalıdır.

## Yayına alma (GitHub Pages)

1. Depoda **Settings → Pages** bölümünde kaynak olarak `main` dalını ve `/ (root)` klasörünü seçin.
2. Alan adı sağlayıcınızın DNS ayarlarında:
   - `gekhukuk.com` için şu dört A kaydını ekleyin: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - `www` için `tugsangunes.github.io` adresine bir CNAME kaydı ekleyin.
3. DNS yayıldıktan sonra Pages ayarlarında **Enforce HTTPS** kutusunu işaretleyin.

Not: Ücretsiz GitHub hesaplarında Pages yalnızca herkese açık depolarda çalışır. Depo gizli kalacaksa GitHub Pro veya Netlify, Cloudflare Pages gibi bir servis gerekir.

Yerelde görmek için `index.html` dosyasını tarayıcıda açmanız yeterlidir.

# GEK Hukuk Bürosu web sitesi

Güneş, Erdil, Karakaya Hukuk Bürosu'nun (gekhukuk.com) statik web sitesi. Sayfalar düz HTML ve CSS'tir; sunucu tarafında çalışan kod yoktur.

## Yapı

| Yol | İçerik |
| --- | --- |
| `src/*.html` | Sayfaların kaynak metinleri (yalnızca sayfa gövdesi) |
| `src/yazilar/*.html` | Yayınlar bölümündeki makaleler; her biri `yazi-<dosya-adı>.html` olarak yayımlanır |
| `tools/build.py` | Büro bilgileri, çalışma alanları (her alanın kendi sayfası dahil) ve avukat bilgileri; üst menü ve alt bilgiyi ekleyip sayfaları üretir |
| `*.html` (kökte) | Üretilmiş sayfalar: ana sayfa, Hakkımızda, Çalışma Alanları, Avukatlarımız, Yayınlar, İletişim, KVKK, Çerez |
| `src/api/asistan.php` | Site asistanının sunucu tarafı (Claude API'ye bağlanır); `api/asistan.php` olarak üretilir |
| `style.css`, `site.js` | Ortak stil; mobil menü ve iletişim formu |
| `fonts/`, `assets/` | Kendi sunucumuzdan sunulan yazı tipleri ve logo |

Kökteki HTML dosyalarını elle düzenlemeyin. `src/` altındaki metni ya da `tools/build.py` içindeki bilgileri değiştirip şunu çalıştırın:

```
python3 tools/build.py
```

Yeni makale eklemek için `src/yazilar/_ornek.html` dosyasını kopyalayıp başındaki `_` olmadan adlandırın, başlık, tarih, yazar ve özet satırlarını doldurun ve sayfaları yeniden üretin. Makaleler Yayınlar sayfasında ve ana sayfada en yeniden eskiye listelenir.

Sarı işaretli (`class="ph"`) kutular yayından önce kontrol edilip silinmesi gereken notlardır.

## İçerik kuralları

Site, Avukatlık Kanunu, TBB Meslek Kuralları ve Reklam Yasağı Yönetmeliği'ne uygun olarak yalnızca bilgilendirme amaçlıdır. Metin eklerken "en iyi", "uzman", başarı oranı gibi iddialar, müvekkil listesi, müvekkil yorumları ve ücret bilgisi kullanılmamalıdır.

## Site asistanı

Asistan, hazır yanıtlı düğmeler ve serbest sorular için yapay zekâdan oluşur. Serbest sorular `api/asistan.php` üzerinden Claude API'ye (model `claude-opus-5-5`) gider. API anahtarı depoda ve `public_html` içinde tutulmaz: hosting'de `public_html` klasörünün bir üstüne `gek-asistan-config.php` adlı bir dosya konur:

```php
<?php
define('ANTHROPIC_API_KEY', 'sk-ant-...');
```

Anahtar yoksa veya API'ye ulaşılamazsa asistan hazır yanıtlara döner. Kötüye kullanıma karşı IP başına saatte 30, toplamda günde 600 soru sınırı vardır (`src/api/asistan.php` başındaki sabitler). Asistanın büro bilgileri ve kuralları `tools/build.py` içindeki `system_prompt()` işlevinden gelir; `ASSISTANT = False` yapılırsa asistan sitede gösterilmez.

## Yayına alma (GoDaddy)

Site GoDaddy hosting üzerinde yayınlanacaktır. Kökteki HTML dosyalarını, `style.css`, `site.js`, `fonts.css`, `favicon.*`, `apple-touch-icon.png` dosyalarını ve `fonts/`, `assets/`, `api/` klasörlerini hosting'in `public_html` klasörüne yükleyin. `src/`, `tools/`, `README.md` ve `CNAME` yüklenmez.

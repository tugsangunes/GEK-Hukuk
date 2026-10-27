# GEK Hukuk Bürosu web sitesi

Güneş, Erdil, Karakaya Hukuk Bürosu'nun (gekhukuk.com) statik web sitesi. Sayfalar düz HTML ve CSS'tir; sunucu tarafında çalışan kod yoktur.

## Yapı

| Yol | İçerik |
| --- | --- |
| `src/*.html` | Sayfaların kaynak metinleri (yalnızca sayfa gövdesi) |
| `tools/build.py` | Büro bilgileri, çalışma alanları ve avukat bilgileri; üst menü ve alt bilgiyi ekleyip sayfaları üretir |
| `*.html` (kökte) | Üretilmiş sayfalar: ana sayfa, Hakkımızda, Çalışma Alanları, Avukatlarımız, Yayınlar, İletişim, KVKK, Çerez |
| `style.css`, `site.js` | Ortak stil; mobil menü ve iletişim formu |
| `fonts/`, `assets/` | Kendi sunucumuzdan sunulan yazı tipleri ve logo |

Kökteki HTML dosyalarını elle düzenlemeyin. `src/` altındaki metni ya da `tools/build.py` içindeki bilgileri değiştirip şunu çalıştırın:

```
python3 tools/build.py
```

Sarı işaretli (`class="ph"`) kutular yayından önce kontrol edilip silinmesi gereken notlardır.

## İçerik kuralları

Site, Avukatlık Kanunu, TBB Meslek Kuralları ve Reklam Yasağı Yönetmeliği'ne uygun olarak yalnızca bilgilendirme amaçlıdır. Metin eklerken "en iyi", "uzman", başarı oranı gibi iddialar, müvekkil listesi, müvekkil yorumları ve ücret bilgisi kullanılmamalıdır.

## Yayına alma (GoDaddy)

Site GoDaddy hosting üzerinde yayınlanacaktır. Kökteki HTML dosyalarını, `style.css`, `site.js`, `fonts.css`, `favicon.*`, `apple-touch-icon.png` dosyalarını ve `fonts/`, `assets/` klasörlerini hosting'in `public_html` klasörüne yükleyin. `src/`, `tools/`, `README.md` ve `CNAME` yüklenmez.

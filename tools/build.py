#!/usr/bin/env python3
"""Sitenin HTML sayfalarını üretir.

Ortak üst bilgi (menü), alt bilgi ve büro bilgileri bu dosyada tek yerde durur.
Sayfa içerikleri src/ klasöründedir. Değişiklikten sonra depo kökünde
`python3 tools/build.py` çalıştırın; kökteki .html dosyaları yeniden yazılır.
"""
import html
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "src"

OFFICE = {
    "name": "GEK Hukuk Bürosu",
    "address_lines": ["Reşatbey Mah. 62006 Sk. No:5", "Arun Apt. Kat:5 Daire:14", "Seyhan / Adana"],
    "phone": "+90 532 292 10 72",
    "email": "info@gekhukuk.com",
    "hours": "Hafta içi 09.00 – 17.00",
    "map": "https://www.google.com/maps/search/?api=1&query=Re%C5%9Fatbey+Mah.+62006+Sk.+No%3A5+Seyhan+Adana",
}

AREAS = [
    ("sirketler", "Şirketler Hukuku",
     "Şirketlerin kuruluşundan tasfiyesine kadar geçen süreçte ortaya çıkan hukuki işlemler.",
     ["Anonim ve limited şirket kuruluşu", "Esas sözleşme değişiklikleri", "Genel kurul ve yönetim kurulu işlemleri",
      "Pay devirleri ve sermaye artırımı", "Birleşme, bölünme ve tür değiştirme"]),
    ("ticaret", "Ticaret Hukuku",
     "Tacirler arasındaki ilişkilerden ve ticari işlerden doğan sözleşme ve uyuşmazlıklar.",
     ["Ticari sözleşmelerin hazırlanması ve incelenmesi", "Kambiyo senetleri", "Ticari alacak uyuşmazlıkları",
      "Haksız rekabet", "Ticari dava şartı arabuluculuk"]),
    ("sirket-danismanligi", "Şirket Danışmanlığı",
     "Şirketlerin günlük işleyişinde ihtiyaç duyduğu sürekli hukuki destek.",
     ["Sözleşme taslaklarının hazırlanması ve incelenmesi", "Şirket içi yönetmelik ve politikalar",
      "Ticari ilişkilerde hukuki görüş", "Uyuşmazlık öncesi risk değerlendirmesi"]),
    ("uyum", "Uyum (Compliance)",
     "Şirketlerin yürürlükteki mevzuata uygun çalışmasına yönelik değerlendirme ve düzenlemeler.",
     ["KVKK uyum süreçleri, aydınlatma metinleri ve envanter", "Şirket içi politika ve prosedürler",
      "Mevzuat değişikliklerinin takibi", "Çalışanlara yönelik bilgilendirme"]),
    ("gayrimenkul", "Gayrimenkul Hukuku",
     "Taşınmazların edinilmesi, kullanılması ve devrine ilişkin işlemler ile uyuşmazlıklar.",
     ["Tapu işlemleri ve tapu iptali-tescil davaları", "Kira sözleşmeleri, tahliye ve kira tespiti",
      "Kat karşılığı inşaat sözleşmeleri", "Ortaklığın giderilmesi", "Kat mülkiyeti uyuşmazlıkları"]),
    ("is", "İş Hukuku",
     "İşçi ile işveren arasındaki iş ilişkisinin kurulması, yürütülmesi ve sona ermesi.",
     ["İş sözleşmelerinin hazırlanması", "Fesih süreçleri ve işe iade", "Kıdem, ihbar ve diğer işçilik alacakları",
      "İş kazası ve meslek hastalığı", "Zorunlu arabuluculuk süreçleri"]),
    ("icra-iflas", "İcra ve İflas Hukuku",
     "Alacakların takibi ve tahsili ile borçlunun mal varlığına yönelik süreçler.",
     ["İlamlı ve ilamsız icra takipleri", "İtirazın iptali ve kaldırılması", "Menfi tespit ve istirdat davaları",
      "Haciz ve satış işlemleri", "İflas ve konkordato süreçleri"]),
    ("aile", "Boşanma ve Aile Hukuku",
     "Evlilik birliği ve aile ilişkilerinden doğan hukuki süreçler.",
     ["Anlaşmalı ve çekişmeli boşanma", "Velayet ve kişisel ilişki", "Nafaka", "Mal rejiminin tasfiyesi",
      "Evlilik sözleşmeleri"]),
    ("miras", "Miras Hukuku",
     "Ölüme bağlı tasarruflar ve mirasın paylaşımına ilişkin işlemler ile davalar.",
     ["Mirasçılık belgesi (veraset ilamı)", "Vasiyetname ve miras sözleşmesi", "Tenkis ve muris muvazaası davaları",
      "Mirasın reddi", "Ortaklığın giderilmesi ve miras paylaşımı"]),
    ("fikri-mulkiyet", "Fikri Mülkiyet Hukuku",
     "Marka, patent, tasarım ve eser sahipliğinden doğan hakların korunması.",
     ["Marka ve tasarım başvuruları", "Marka hakkına tecavüz ve hükümsüzlük davaları", "Telif hakları",
      "Lisans ve devir sözleşmeleri"]),
]

LAWYERS = [
    ("tugsan-gunes", "G", "Av. Tuğsan Güneş", [
        ("Baro", "Adana Barosu"), ("Sicil No", "3428"), ("Telefon", "+90 532 292 10 72"),
        ("Eğitim", "Yeditepe Üniversitesi Hukuk Fakültesi"), ("Diller", "Türkçe, İngilizce")],
     "Büroyu 2014 yılında Adana'da kurmuştur."),
    ("omer-murat-erdil", "E", "Av. Ömer Murat Erdil", [
        ("Baro", "Adana Barosu"), ("Sicil No", "4995"), ("Telefon", "+90 530 965 15 96"),
        ("Diller", "Türkçe, İngilizce")], ""),
    ("adem-karakaya", "K", "Av. Adem Karakaya", [
        ("Baro", "Adana Barosu"), ("Sicil No", "5962"), ("Telefon", "+90 545 413 36 82"),
        ("Eğitim", "Dokuz Eylül Üniversitesi Hukuk Fakültesi"), ("Diller", "Türkçe, İngilizce")], ""),
]

NAV = [
    ("index.html", "Ana Sayfa"),
    ("hakkimizda.html", "Hakkımızda"),
    ("calisma-alanlari.html", "Çalışma Alanları"),
    ("avukatlar.html", "Avukatlarımız"),
    ("yayinlar.html", "Yayınlar"),
    ("iletisim.html", "İletişim"),
]

e = html.escape


def head(title, description, robots=None):
    full = OFFICE["name"] if title == OFFICE["name"] else f"{title} · {OFFICE['name']}"
    extra = f'\n<meta name="robots" content="{robots}">' if robots else ""
    return f"""<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(full)}</title>
<meta name="description" content="{e(description)}">{extra}
<link rel="icon" href="favicon.ico" sizes="48x48">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<meta name="theme-color" content="#0f2340">
<link rel="stylesheet" href="fonts.css">
<link rel="stylesheet" href="style.css">
</head>
<body>
"""


def header(current):
    items = "\n".join(
        f'        <li><a href="{href}"{" aria-current=\"page\"" if href == current else ""}>{label}</a></li>'
        for href, label in NAV if href != "index.html")
    return f"""<a class="skip" href="#icerik">İçeriğe geç</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="index.html"><img src="assets/gek-logo-ters.svg" alt="{OFFICE['name']}" width="363" height="77"></a>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="ana-menu">Menü</button>
    <nav id="ana-menu" aria-label="Ana menü">
      <ul>
{items}
      </ul>
    </nav>
  </div>
</header>
<main id="icerik">
"""


def footer():
    addr = "<br>".join(OFFICE["address_lines"])
    areas = "\n".join(f'          <li><a href="calisma-alanlari.html#{slug}">{name}</a></li>' for slug, name, *_ in AREAS)
    return f"""</main>

<footer class="site-footer">
  <div class="wrap footer-grid">
    <div class="footer-brand">
      <img src="assets/gek-logo-ters.svg" alt="{OFFICE['name']}" width="363" height="77">
      <p>Av. Tuğsan Güneş, Av. Ömer Murat Erdil ve Av. Adem Karakaya. 2014'ten bu yana Adana'da.</p>
    </div>
    <div>
      <h2>İletişim</h2>
      <address>{addr}</address>
      <p>{OFFICE['phone']}<br>{OFFICE['email']}<br>{OFFICE['hours']}</p>
    </div>
    <div>
      <h2>Çalışma Alanları</h2>
      <ul>
{areas}
      </ul>
    </div>
    <div>
      <h2>Büro</h2>
      <ul>
          <li><a href="hakkimizda.html">Hakkımızda</a></li>
          <li><a href="avukatlar.html">Avukatlarımız</a></li>
          <li><a href="yayinlar.html">Yayınlar</a></li>
          <li><a href="iletisim.html">İletişim</a></li>
          <li><a href="kvkk.html">KVKK Aydınlatma Metni</a></li>
          <li><a href="cerez.html">Çerez Politikası</a></li>
      </ul>
    </div>
  </div>
  <div class="wrap footer-legal">
    <p>Bu internet sitesi, Avukatlık Kanunu ve Türkiye Barolar Birliği Meslek Kuralları ile Reklam Yasağı Yönetmeliği çerçevesinde yalnızca bilgilendirme amacıyla hazırlanmıştır. Sitedeki içerikler hukuki görüş veya tavsiye niteliği taşımaz.</p>
    <p>© <span id="year">2026</span> {OFFICE['name']}</p>
  </div>
</footer>
<script src="site.js"></script>
</body>
</html>
"""


def area_cards(link_base="calisma-alanlari.html"):
    return "\n".join(
        f'      <li><a class="area-card" href="{link_base}#{slug}"><h3>{name}</h3><p>{e(summary)}</p></a></li>'
        for slug, name, summary, _ in AREAS)


def person_dl(rows):
    return "".join(f"<dt>{k}</dt><dd>{e(v)}</dd>" for k, v in rows)


def render_template(text):
    replacements = {
        "AREA_CARDS": area_cards(),
        "AREA_COUNT": str(len(AREAS)),
        "AREA_INDEX": "\n".join(f'      <li><a href="#{slug}">{name}</a></li>' for slug, name, *_ in AREAS),
        "LAWYER_COUNT": str(len(LAWYERS)),
        "AREA_SECTIONS": "\n".join(
            f"""  <section class="area-detail" id="{slug}">
    <h2>{name}</h2>
    <p>{e(summary)}</p>
    <ul>{''.join(f'<li>{e(t)}</li>' for t in topics)}</ul>
  </section>""" for slug, name, summary, topics in AREAS),
        "LAWYER_CARDS": "\n".join(
            f"""      <li><a class="person-card" href="avukatlar.html#{slug}"><span class="mono" aria-hidden="true">{ini}</span><span><strong>{name}</strong><span>Adana Barosu · Sicil No {dict(rows)['Sicil No']}</span></span></a></li>"""
            for slug, ini, name, rows, _ in LAWYERS),
        "LAWYER_PROFILES": "\n".join(
            f"""  <article class="profile" id="{slug}">
    <span class="mono" aria-hidden="true">{ini}</span>
    <div>
      <h2>{name}</h2>
      {f'<p>{e(note)}</p>' if note else ''}
      <dl>{person_dl(rows)}</dl>
    </div>
  </article>""" for slug, ini, name, rows, note in LAWYERS),
        "ADDRESS": "<br>".join(OFFICE["address_lines"]),
        "PHONE": OFFICE["phone"],
        "EMAIL": OFFICE["email"],
        "HOURS": OFFICE["hours"],
        "MAP": OFFICE["map"],
    }
    return re.sub(r"\{\{(\w+)\}\}", lambda m: replacements[m.group(1)], text)


def build():
    for src in sorted(SRC.glob("*.html")):
        text = src.read_text(encoding="utf-8")
        meta = dict(re.findall(r"<!-- (\w+): (.*?) -->", text))
        body = re.sub(r"<!-- \w+: .*? -->\n", "", text)
        page = src.name
        out = head(meta["title"], meta.get("description", f"{OFFICE['name']}, Adana."), meta.get("robots"))
        out += header(page) + render_template(body) + footer()
        (ROOT / page).write_text(out, encoding="utf-8")
        print("yazıldı:", page)


if __name__ == "__main__":
    build()

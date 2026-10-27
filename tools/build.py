#!/usr/bin/env python3
"""Sitenin HTML sayfalarını üretir.

Ortak üst bilgi (menü), alt bilgi ve büro bilgileri bu dosyada tek yerde durur.
Sayfa içerikleri src/ klasöründedir. Değişiklikten sonra depo kökünde
`python3 tools/build.py` çalıştırın; kökteki .html dosyaları yeniden yazılır.
"""
import html
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "src"

OFFICE = {
    "name": "GEK Hukuk Bürosu",
    "address_lines": ["Reşatbey Mah. 62006 Sk. No:5", "Arun Apt. Kat:5 Daire:14", "Seyhan / Adana"],
    "phone": "+90 532 292 10 72",
    "whatsapp": "905325569086",
    "whatsapp_label": "+90 532 556 90 86",
    "email": "info@gekhukuk.com",
    "hours": "Hafta içi 09.00 – 17.00",
    "map": "https://www.google.com/maps/search/?api=1&query=Re%C5%9Fatbey+Mah.+62006+Sk.+No%3A5+Seyhan+Adana",
    "map_embed": "https://www.google.com/maps?q=Re%C5%9Fatbey+Mah.+62006+Sk.+No%3A5+Seyhan+Adana&z=16&output=embed",
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
    ("arabuluculuk", "Arabuluculuk ve Uzlaştırmada Temsil",
     "Arabuluculuk ve uzlaştırma süreçlerinde tarafların avukat olarak temsil edilmesi.",
     ["Dava şartı arabuluculuk (iş, ticaret, tüketici ve kira uyuşmazlıkları)", "İhtiyari arabuluculuk",
      "Anlaşma belgesinin hazırlanması ve icra edilebilirlik şerhi", "Ceza muhakemesinde uzlaştırma sürecinde temsil",
      "Anlaşmadan doğan edimlerin takibi"]),
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

# Her alanın kendi sayfası: dosya adı ve sayfadaki giriş paragrafları
AREA_PAGES = {
    "sirketler": ("sirketler-hukuku.html", [
        "Şirketler hukuku, ticaret şirketlerinin kuruluşu, yönetimi, ortaklık yapısındaki değişiklikler ve sona ermesiyle ilgili kuralları kapsar. Türk Ticaret Kanunu'nun öngördüğü şekil şartları ve tescil işlemleri, şirket hayatının her aşamasında dikkat gerektirir.",
        "Anonim ve limited şirketlerin kuruluş ve esas sözleşme işlemlerinde, genel kurul ve yönetim kurulu kararlarının hazırlanmasında, pay devirlerinde ve ortaklar arasındaki uyuşmazlıklarda danışmanlık ve dava takibi hizmeti veriyoruz."]),
    "ticaret": ("ticaret-hukuku.html", [
        "Ticaret hukuku, tacirler arasındaki ilişkileri ve ticari işletmeyle ilgili işleri düzenler. Ticari sözleşmeler, kambiyo senetleri ve haksız rekabet bu alanın başlıca konularıdır.",
        "Ticari sözleşmelerin hazırlanması ve incelenmesinde, alacakların takibinde ve ticari uyuşmazlıklarda, dava şartı olan arabuluculuk süreci de dahil olmak üzere danışmanlık ve dava takibi yapıyoruz."]),
    "sirket-danismanligi": ("sirket-danismanligi.html", [
        "Şirketlerin günlük işleyişinde sözleşmeler, çalışanlarla ilişkiler, tedarikçi ve müşterilerle yazışmalar gibi pek çok konu hukuki değerlendirme gerektirir. Bu konuların uyuşmazlığa dönüşmeden ele alınması, ileride doğabilecek riskleri azaltır.",
        "Sürekli danışmanlık kapsamında şirketlerin sözleşme taslaklarını inceliyor, şirket içi düzenlemeleri hazırlıyor ve ticari kararlar öncesinde hukuki görüş veriyoruz."]),
    "uyum": ("uyum-compliance.html", [
        "Uyum (compliance), bir şirketin faaliyetlerinin yürürlükteki mevzuata ve kendi iç kurallarına uygun yürütülmesine yönelik çalışmaların bütünüdür. Kişisel verilerin korunması mevzuatı bu alanda en sık karşılaşılan konulardan biridir.",
        "Şirketlerin KVKK kapsamındaki yükümlülüklerini değerlendiriyor; aydınlatma metinleri, veri envanteri ve şirket içi politika ve prosedürlerin hazırlanmasında destek veriyoruz."]),
    "gayrimenkul": ("gayrimenkul-hukuku.html", [
        "Gayrimenkul hukuku, taşınmazların mülkiyeti, kullanımı, kiralanması ve devriyle ilgili işlem ve uyuşmazlıkları kapsar. Taşınmaz satışlarında resmi şekil şartı ve tapu sicili kayıtları belirleyici öneme sahiptir.",
        "Tapu iptali ve tescil, kira, tahliye ve kira tespiti, kat karşılığı inşaat sözleşmeleri ve ortaklığın giderilmesi konularında danışmanlık ve dava takibi yapıyoruz."]),
    "is": ("is-hukuku.html", [
        "İş hukuku, işçi ile işveren arasındaki ilişkinin kurulmasından sona ermesine kadar tarafların hak ve yükümlülüklerini düzenler. İşçilik alacakları ve işe iade taleplerinde dava açılmadan önce arabulucuya başvurulması zorunludur.",
        "İşverenlere iş sözleşmeleri ve fesih süreçlerinde danışmanlık veriyor; işçilik alacakları, işe iade ve iş kazasından doğan uyuşmazlıklarda dava takibi yapıyoruz."]),
    "icra-iflas": ("icra-iflas-hukuku.html", [
        "İcra ve iflas hukuku, alacakların devlet eliyle zorla tahsilini ve borçlunun ödeme güçlüğüne düştüğü durumları düzenler. Takip yolunun doğru seçilmesi ve sürelere uyulması bu alanda özellikle önemlidir.",
        "İlamlı ve ilamsız icra takipleri, itirazın iptali ve kaldırılması, menfi tespit ve istirdat davaları ile haciz ve satış işlemlerinde alacaklılara ve borçlulara hizmet veriyoruz."]),
    "aile": ("bosanma-aile-hukuku.html", [
        "Aile hukuku, evlilik birliğinin kurulması, sürmesi ve sona ermesiyle ortaya çıkan kişisel ve mali ilişkileri düzenler. Boşanma süreçlerinde velayet, nafaka ve mal rejiminin tasfiyesi çoğu zaman birlikte ele alınır.",
        "Anlaşmalı ve çekişmeli boşanma davaları, velayet ve kişisel ilişki düzenlemeleri, nafaka talepleri ve mal rejiminin tasfiyesi konularında danışmanlık ve dava takibi yapıyoruz."]),
    "miras": ("miras-hukuku.html", [
        "Miras hukuku, bir kişinin ölümüyle malvarlığının mirasçılarına geçişini ve bu geçişle ilgili işlemleri düzenler. Vasiyetname ve miras sözleşmesi gibi ölüme bağlı tasarruflar, kanunun öngördüğü şekil şartlarına bağlıdır.",
        "Mirasçılık belgesi alınması, vasiyetname düzenlenmesi, mirasın reddi, tenkis ve muris muvazaası davaları ile terekenin paylaşımında danışmanlık ve dava takibi yapıyoruz."]),
    "fikri-mulkiyet": ("fikri-mulkiyet-hukuku.html", [
        "Fikri mülkiyet hukuku; marka, patent, endüstriyel tasarım ve fikir ve sanat eserleri üzerindeki hakları korur. Marka ve tasarım hakları büyük ölçüde Türk Patent ve Marka Kurumu'na yapılan tescil ile korunur.",
        "Marka ve tasarım başvuruları, itiraz süreçleri, tecavüz ve hükümsüzlük davaları, telif hakları ile lisans ve devir sözleşmelerinde danışmanlık ve dava takibi yapıyoruz."]),
    "arabuluculuk": ("arabuluculuk-uzlastirma.html", [
        "Arabuluculuk, tarafların uyuşmazlıklarını tarafsız bir arabulucunun yardımıyla, mahkemeye gitmeden ve kendi iradeleriyle çözmelerini sağlayan bir yöntemdir. İş, ticaret, tüketici ve kira uyuşmazlıkları gibi pek çok alanda dava açılmadan önce arabulucuya başvurulması zorunludur. Ceza muhakemesindeki uzlaştırma ise kanunda sayılan suçlarda şüpheli ile mağdurun bir uzlaştırmacı aracılığıyla anlaşmasına imkân verir.",
        "Arabuluculuk ve uzlaştırma görüşmelerinde müvekkillerimizi temsil ediyor; taleplerin hazırlanmasında, görüşmelerin yürütülmesinde ve varılan anlaşmanın hukuka uygun biçimde belgelenmesinde destek veriyoruz."]),
}

# 24x24 çizgi ikonlar (stroke="currentColor"); alan kartlarında ve alan başlıklarında kullanılır
ICONS = {
    "sirketler": '<path d="M4 21V5l8-3v19M12 8l8 3v10M2 21h20M7 8h2M7 12h2M7 16h2M15 13h2M15 17h2"/>',
    "ticaret": '<rect x="3" y="7" width="18" height="13" rx="1"/><path d="M8 7V4h8v3M3 12h18M11 12v2h2v-2"/>',
    "sirket-danismanligi": '<path d="M4 5h16v11H9l-5 4z"/><path d="M8 9h8M8 12h5"/>',
    "uyum": '<path d="M12 2l8 3v6c0 5-3.5 9-8 11-4.5-2-8-6-8-11V5z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
    "gayrimenkul": '<path d="M3 11l9-8 9 8M5 9.5V21h14V9.5"/><path d="M10 21v-6h4v6"/>',
    "is": '<circle cx="9" cy="7" r="3"/><path d="M3 20c0-3.5 2.7-6 6-6s6 2.5 6 6"/><circle cx="17" cy="8" r="2.5"/><path d="M16 14c3 0 5 2 5 5"/>',
    "icra-iflas": '<path d="M6 2h9l4 4v16H6z"/><path d="M14 2v5h5M9 12h7M9 16h7"/>',
    "aile": '<circle cx="9" cy="13" r="5.5"/><circle cx="15" cy="13" r="5.5"/><path d="M10 4l2-2 2 2"/>',
    "miras": '<path d="M12 22V11M12 15l-4-3M12 13l4-3"/><path d="M12 11a5 5 0 1 0-5-5 4 4 0 0 0 0 .5A4 4 0 1 0 12 11a4 4 0 1 0 5-4.5V6a5 5 0 0 0-5 5z"/>',
    "arabuluculuk": '<path d="M2 12h6M16 12h6M5 9l3 3-3 3M19 9l-3 3 3 3"/><circle cx="12" cy="12" r="2.5"/><path d="M12 3v4M12 17v4"/>',
    "fikri-mulkiyet": '<path d="M9 18h6M10 22h4M12 2a7 7 0 0 0-4 12.7V17h8v-2.3A7 7 0 0 0 12 2z"/>',
}

STEPS = [
    ("İlk görüşme", "Konunuzu dinler, belge ve bilgileri birlikte gözden geçiririz."),
    ("Değerlendirme", "Hukuki durumu, izlenebilecek yolları ve olası sonuçlarını açıkça anlatırız."),
    ("Yol haritası", "Süreç, süreler ve gerekli işlemler konusunda yazılı bir plan oluştururuz."),
    ("Takip", "Dosyanın her aşamasında sizi düzenli olarak bilgilendiririz."),
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


def icon(slug, cls="icon"):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" '
            f'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[slug]}</svg>')


def area_href(slug):
    return AREA_PAGES[slug][0]


def tel(number):
    return f'<a href="tel:{number.replace(" ", "")}">{number}</a>'


WA_ICON = ('<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.7" '
           'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3.5 20.5l1.3-4.2A8.5 8.5 0 1 1 8 19.4z"/>'
           '<path d="M9 8.5c0 3.5 3 6.5 6.5 6.5l1-1.6-2-1-1 .9c-1-.5-2.3-1.8-2.8-2.8l.9-1-1-2z"/></svg>')


# Sohbet asistanı (yapay zekâ bağlantısı kurulana kadar kapalı)
ASSISTANT = False

BOT_ICON = ('<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.7" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 5h16v11H9l-5 4z"/>'
            '<path d="M8.5 10.5h.01M12 10.5h.01M15.5 10.5h.01"/></svg>')


def assistant_data():
    """Sohbet asistanının hazır yanıtlarda kullandığı büro bilgileri (site.js okur)."""
    data = {
        "phone": OFFICE["phone"], "tel": OFFICE["phone"].replace(" ", ""),
        "whatsapp": OFFICE["whatsapp"], "email": OFFICE["email"], "hours": OFFICE["hours"],
        "address": ", ".join(OFFICE["address_lines"]), "map": OFFICE["map"],
        "areas": [{"name": n, "href": area_href(sl), "summary": sm, "keys": [t.lower() for t in tp]}
                  for sl, n, sm, tp in AREAS],
        "lawyers": [{"name": n, "href": f"avukatlar.html#{sl}"} for sl, _, n, _, _ in LAWYERS],
    }
    return json.dumps(data, ensure_ascii=False).replace("</", "<\\/")


def assistant_toggle():
    if not ASSISTANT:
        return ""
    return f'''  <button class="bot-toggle" type="button" aria-expanded="false" aria-controls="asistan" hidden>{BOT_ICON}<span>Asistan</span></button>
'''


def assistant_panel():
    if not ASSISTANT:
        return ""
    return f'''<section class="bot" id="asistan" aria-label="Site asistanı" hidden>
  <header class="bot-head"><strong>GEK Hukuk Asistanı</strong><button class="bot-close" type="button" aria-label="Asistanı kapat">×</button></header>
  <div class="bot-log" role="log" aria-live="polite"></div>
  <form class="bot-input"><input type="text" name="q" placeholder="Sorunuzu yazın…" autocomplete="off" aria-label="Sorunuz"><button class="btn" type="submit">Sor</button></form>
</section>
<script id="asistan-veri" type="application/json">{assistant_data()}</script>
'''


def whatsapp(label=None):
    return f'<a href="https://wa.me/{OFFICE["whatsapp"]}" rel="noopener" target="_blank">{label or OFFICE["whatsapp_label"]}</a>'


def mail(addr):
    return f'<a href="mailto:{addr}">{addr}</a>'


def json_ld():
    data = {
        "@context": "https://schema.org",
        "@type": "LegalService",
        "name": OFFICE["name"],
        "url": "https://gekhukuk.com/",
        "logo": "https://gekhukuk.com/assets/ikon-512.png",
        "telephone": OFFICE["phone"],
        "email": OFFICE["email"],
        "foundingDate": "2014",
        "address": {"@type": "PostalAddress", "streetAddress": "Reşatbey Mah. 62006 Sk. No:5 Arun Apt. K:5 D:14",
                    "addressLocality": "Seyhan", "addressRegion": "Adana", "addressCountry": "TR"},
        "openingHours": "Mo-Fr 09:00-17:00",
        "availableLanguage": ["tr", "en"],
        "employee": [{"@type": "Person", "name": name.replace("Av. ", ""), "jobTitle": "Avukat"}
                     for _, _, name, _, _ in LAWYERS],
    }
    return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>\n'


def head(title, description, robots=None, extra_head=""):
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
{extra_head}</head>
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
    <a class="header-cta" href="tel:{OFFICE['phone'].replace(' ', '')}">{OFFICE['phone']}</a>
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
    areas = "\n".join(f'          <li><a href="{area_href(slug)}">{name}</a></li>' for slug, name, *_ in AREAS)
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
      <p>{tel(OFFICE['phone'])}<br>WhatsApp: {whatsapp()}<br>{mail(OFFICE['email'])}<br>{OFFICE['hours']}</p>
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
<div class="float-actions">
  <a class="wa-float" href="https://wa.me/{OFFICE['whatsapp']}" rel="noopener" target="_blank" aria-label="WhatsApp ile yazın">{WA_ICON}</a>
{assistant_toggle()}</div>
{assistant_panel()}<script src="site.js"></script>
</body>
</html>
"""


def area_cards():
    return "\n".join(
        f'      <li><a class="area-card" href="{area_href(slug)}">{icon(slug)}<h3>{name}</h3><p>{e(summary)}</p></a></li>'
        for slug, name, summary, _ in AREAS)


def area_overview():
    return "\n".join(
        f"""      <li><a class="area-tile" href="{area_href(slug)}">
        {icon(slug)}
        <h2>{name}</h2>
        <p>{e(summary)}</p>
        <ul>{''.join(f'<li>{e(t)}</li>' for t in topics[:3])}</ul>
        <span class="more">Ayrıntılar</span>
      </a></li>""" for slug, name, summary, topics in AREAS)


def crumbs(*parts):
    links = "".join(f'<a href="{href}">{label}</a><span aria-hidden="true">/</span>' for href, label in parts[:-1])
    return f'<nav class="crumbs" aria-label="Konum">{links}{e(parts[-1])}</nav>'


def area_page(i):
    slug, name, summary, topics = AREAS[i]
    href, paras = AREA_PAGES[slug]
    prev_slug, prev_name = AREAS[i - 1][:2]
    next_slug, next_name = AREAS[(i + 1) % len(AREAS)][:2]
    others = "\n".join(
        f'        <li><a href="{area_href(s_)}"{" aria-current=\"page\"" if s_ == slug else ""}>{icon(s_)}{n_}</a></li>'
        for s_, n_, *_ in AREAS)
    body = f"""<div class="page-head"><div class="wrap">{crumbs(("index.html", "Ana Sayfa"), ("calisma-alanlari.html", "Çalışma Alanları"), name)}
  <p class="eyebrow">Çalışma Alanı</p>
  <div class="page-title-icon">{icon(slug)}<h1>{name}</h1></div>
  <p class="lead">{e(summary)}</p>
</div></div>
<div class="wrap area-page page-body">
  <article class="prose">
    {''.join(f'<p>{e(p_)}</p>' for p_ in paras)}
    <h2>Başlıca konular</h2>
    <ul class="topic-list">{''.join(f'<li>{e(t)}</li>' for t in topics)}</ul>
    <div class="cta-box">
      <div>
        <h2>Bu konuda görüşmek için</h2>
        <p>{tel(OFFICE['phone'])} · {whatsapp("WhatsApp")} · {mail(OFFICE['email'])}<br>{OFFICE['hours']}</p>
      </div>
      <a class="btn" href="iletisim.html">Bize yazın</a>
    </div>
  </article>
  <aside class="area-aside">
    <h2>Çalışma alanları</h2>
    <ul>
{others}
    </ul>
  </aside>
</div>
<nav class="wrap pager" aria-label="Diğer alanlar">
  <a href="{area_href(prev_slug)}"><span>Önceki alan</span>{prev_name}</a>
  <a href="{area_href(next_slug)}"><span>Sonraki alan</span>{next_name}</a>
</nav>
"""
    out = head(name, f"{OFFICE['name']}: {summary}")
    return href, out + header("calisma-alanlari.html") + body + footer()


def load_articles():
    """src/yazilar/*.html dosyalarını tarihe göre yeniden eskiye sıralı döndürür (_ ile başlayanlar örnektir)."""
    items = []
    for f in sorted((SRC / "yazilar").glob("*.html")):
        if f.name.startswith("_"):
            continue
        text = f.read_text(encoding="utf-8")
        meta = dict(re.findall(r"<!-- (\w+): (.*?) -->", text))
        meta["body"] = re.sub(r"<!-- \w+: .*? -->\n", "", text)
        meta["href"] = f"yazi-{f.stem}.html"
        items.append(meta)
    return sorted(items, key=lambda m: m["date"], reverse=True)


def tr_date(iso):
    months = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
    y, m, d = iso.split("-")
    return f"{int(d)} {months[int(m) - 1]} {y}"


def article_cards(articles):
    if not articles:
        return """<div class="empty-state">
      <p>İlk yazılarımız hazırlanıyor. Mevzuat değişiklikleri ve güncel içtihatlar üzerine notlarımız yakında bu bölümde yayımlanacak.</p>
    </div>"""
    return '<ul class="article-list">' + "".join(
        f"""<li><a class="article-card" href="{a['href']}"><span class="article-meta">{tr_date(a['date'])} · {e(a['author'])}</span><h3>{e(a['title'])}</h3><p>{e(a['summary'])}</p><span class="more">Devamını okuyun</span></a></li>"""
        for a in articles) + "</ul>"


def article_page(a):
    body = f"""<div class="page-head"><div class="wrap">{crumbs(("index.html", "Ana Sayfa"), ("yayinlar.html", "Yayınlar"), a['title'])}
  <p class="eyebrow">{tr_date(a['date'])} · {e(a['author'])}</p>
  <h1>{e(a['title'])}</h1>
</div></div>
<article class="wrap prose page-body">
{a['body']}
  <p class="form-note">Bu yazı genel bilgilendirme amacı taşır, hukuki görüş veya tavsiye niteliğinde değildir.</p>
</article>
"""
    return head(a["title"], a["summary"]) + header("yayinlar.html") + body + footer()


def person_dl(rows):
    return "".join(f"<dt>{k}</dt><dd>{tel(v) if k == 'Telefon' else e(v)}</dd>" for k, v in rows)


def render_template(text, articles=()):
    replacements = {
        "AREA_OVERVIEW": area_overview(),
        "ARTICLES": article_cards(articles),
        "ARTICLES_LATEST": article_cards(articles[:3]),
        "AREA_CARDS": area_cards(),
        "AREA_COUNT": str(len(AREAS)),
        "LAWYER_COUNT": str(len(LAWYERS)),
        "LAWYER_CARDS": "\n".join(
            f"""      <li><a class="person-card" href="avukatlar.html#{slug}"><span class="mono" aria-hidden="true">{ini}</span><span class="person-card-body"><strong>{name}</strong><span>Avukat · Adana Barosu</span><span>Sicil No {dict(rows)['Sicil No']}{' · ' + dict(rows)['Eğitim'].replace(' Hukuk Fakültesi', '') if 'Eğitim' in dict(rows) else ''}</span><span class="more">Profil</span></span></a></li>"""
            for slug, ini, name, rows, _ in LAWYERS),
        "LAWYER_PROFILES": "\n".join(
            f"""  <article class="profile" id="{slug}">
    <span class="mono" aria-hidden="true">{ini}</span>
    <div>
      <h2>{name}</h2>
      {f'<p>{e(note)}</p>' if note else ''}
      <dl>{person_dl(rows)}</dl>
      <p class="profile-actions"><a class="btn btn-ghost" href="tel:{dict(rows)['Telefon'].replace(' ', '')}">Ara</a> <a class="btn btn-ghost" href="iletisim.html">Mesaj gönderin</a></p>
    </div>
  </article>""" for slug, ini, name, rows, note in LAWYERS),
        "ADDRESS": "<br>".join(OFFICE["address_lines"]),
        "PHONE": tel(OFFICE["phone"]),
        "WHATSAPP": whatsapp("WhatsApp ile yazın"),
        "EMAIL": mail(OFFICE["email"]),
        "STEPS": "\n".join(f'      <li><span class="step-no">{i:02d}</span><h3>{t}</h3><p>{d}</p></li>'
                           for i, (t, d) in enumerate(STEPS, 1)),
        "HOURS": OFFICE["hours"],
        "MAP": OFFICE["map"],
        "MAP_EMBED": OFFICE["map_embed"],
    }
    return re.sub(r"\{\{(\w+)\}\}", lambda m: replacements[m.group(1)], text)


def build():
    articles = load_articles()
    for i in range(len(AREAS)):
        name, page = area_page(i)
        (ROOT / name).write_text(page, encoding="utf-8")
        print("yazıldı:", name)
    for a in articles:
        (ROOT / a["href"]).write_text(article_page(a), encoding="utf-8")
        print("yazıldı:", a["href"])
    for src in sorted(SRC.glob("*.html")):
        text = src.read_text(encoding="utf-8")
        meta = dict(re.findall(r"<!-- (\w+): (.*?) -->", text))
        body = re.sub(r"<!-- \w+: .*? -->\n", "", text)
        page = src.name
        body = body.replace('<div class="page-head"><div class="wrap">',
                            '<div class="page-head"><div class="wrap"><nav class="crumbs" aria-label="Konum">'
                            f'<a href="index.html">Ana Sayfa</a><span aria-hidden="true">/</span>{e(meta["title"])}</nav>', 1)
        extra = json_ld() if page == "index.html" else ""
        out = head(meta["title"], meta.get("description", f"{OFFICE['name']}, Adana."), meta.get("robots"), extra)
        out += header(page) + render_template(body, articles) + footer()
        (ROOT / page).write_text(out, encoding="utf-8")
        print("yazıldı:", page)


if __name__ == "__main__":
    build()

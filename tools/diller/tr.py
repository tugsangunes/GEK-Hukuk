"""Türkçe arayüz metinleri. Çalışma alanları, avukatlar ve adımların Türkçe metni tools/build.py içindedir.

Diğer dillerin dosyaları (en.py, de.py ...) aynı anahtarları taşır; ayrıca AREAS, STEPS, VALUES ve NOTES
ile build.py'deki Türkçe verinin çevirisini verir.
"""

NAME = "Türkçe"
DIR = "ltr"
OFFICE_NAME = "GEK Hukuk Bürosu"
HOURS = "Hafta içi 09.00 – 17.00"
COUNTRY = ""
MONTHS = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
DATE = "{d} {m} {y}"

UI = {
    "nav": {"index.html": "Ana Sayfa", "hakkimizda.html": "Hakkımızda", "calisma-alanlari.html": "Çalışma Alanları",
            "avukatlar.html": "Avukatlarımız", "yayinlar.html": "Yayınlar", "iletisim.html": "İletişim"},
    "skip": "İçeriğe geç",
    "menu": "Menü",
    "main_menu": "Ana menü",
    "language": "Dil",
    "phone": "Telefon",
    "footer_note": "Av. Tuğsan Güneş, Av. Ömer Murat Erdil ve Av. Adem Karakaya. 2014'ten bu yana Adana'da.",
    "contact": "İletişim",
    "areas": "Çalışma Alanları",
    "office": "Büro",
    "kvkk": "KVKK Aydınlatma Metni",
    "cookies": "Çerez Politikası",
    "legal": "Bu internet sitesi, Avukatlık Kanunu ve Türkiye Barolar Birliği Meslek Kuralları ile Reklam Yasağı Yönetmeliği çerçevesinde yalnızca bilgilendirme amacıyla hazırlanmıştır. Sitedeki içerikler hukuki görüş veya tavsiye niteliği taşımaz.",
    "wa_aria": "WhatsApp ile yazın",
    "quick": "Hızlı iletişim",
    "call": "Ara",
    "assistant": "Asistan",
    "write": "Yazın",
    "bot_label": "Site asistanı",
    "bot_title": "GEK Hukuk Asistanı",
    "bot_close": "Asistanı kapat",
    "bot_ph": "Sorunuzu yazın…",
    "bot_q": "Sorunuz",
    "bot_ask": "Sor",
    "crumbs": "Konum",
    "area_eyebrow": "Çalışma Alanı",
    "topics": "Başlıca konular",
    "discuss": "Bu konuda görüşmek için",
    "write_us": "Bize yazın",
    "areas_lower": "Çalışma alanları",
    "other_areas": "Diğer alanlar",
    "prev_area": "Önceki alan",
    "next_area": "Sonraki alan",
    "details": "Ayrıntılar",
    "empty_articles": "İlk yazılarımız hazırlanıyor. Mevzuat değişiklikleri ve güncel içtihatlar üzerine notlarımız yakında bu bölümde yayımlanacak.",
    "read_more": "Devamını okuyun",
    "article_note": "Bu yazı genel bilgilendirme amacı taşır, hukuki görüş veya tavsiye niteliğinde değildir.",
    "in_turkish": "",
    "lawyer_card": "Avukat · Adana Barosu",
    "reg_no": "Sicil No",
    "profile": "Profil",
    "send_msg": "Mesaj gönderin",
    "wa_cta": "WhatsApp ile yazın",
    "job_title": "Avukat",
    "labels": {"Baro": "Baro", "Sicil No": "Sicil No", "Telefon": "Telefon", "Eğitim": "Eğitim", "Diller": "Diller"},
}

# site.js'in kullandığı metinler. {hours}, {address} gibi yer tutucuları site.js doldurur.
JS = {
    "form_invalid": "Lütfen tüm alanları doldurun ve KVKK onay kutusunu işaretleyin.",
    "form_subject": "İletişim talebi: ",
    "form_sent": "E-posta uygulamanız açılmadıysa info@gekhukuk.com adresine yazabilirsiniz.",
    "map_title": "GEK Hukuk Bürosu konumu",
    "typing": "Yazıyor…",
    "rate": "Kısa sürede çok sayıda soru geldi. Lütfen biraz sonra tekrar deneyin ya da bize doğrudan ulaşın:",
    "welcome": "Merhaba, GEK Hukuk Bürosu'na hoş geldiniz. Büromuzla ilgili sorularınızı yanıtlayabilirim; hukuki görüş veya tavsiye veremem.",
    "ai_note": "Yazdığınız sorular, yanıt üretilmesi için yapay zekâ hizmet sağlayıcımız Anthropic'e (ABD) iletilir. Lütfen adınızı, iletişim bilgilerinizi ve uyuşmazlığınızın ayrıntılarını paylaşmayın.",
    "details": "Ayrıntılar",
    "menu_q": "Size nasıl yardımcı olabilirim?",
    "c_call": "Ara", "c_wa": "WhatsApp", "c_form": "İletişim formu",
    "other": "Başka bir konu",
    "m_appt": "Randevu almak istiyorum", "m_areas": "Çalışma alanlarınız", "m_addr": "Adres ve harita",
    "m_hours": "Çalışma saatleri", "m_docs": "İlk görüşmeye ne getirmeliyim?", "m_fee": "Ücretler",
    "appt": "Görüşme için hafta içi 09.00 – 17.00 arasında bizi arayabilir, WhatsApp üzerinden yazabilir ya da iletişim formunu kullanabilirsiniz. Mesajınızda yalnızca konunun başlığını belirtmeniz yeterli; ayrıntıları görüşmede konuşuruz.",
    "areas": "Danışmanlık ve dava takibi yaptığımız alanlar şunlar. Ayrıntı için birini seçin:",
    "area_page": "Alan sayfasına git",
    "area_talk": "Bu konuda görüşmek istiyorum",
    "area_more": "Diğer alanlar",
    "addr": "Büromuzun adresi: {address}.",
    "map_open": "Haritada aç", "contact_page": "İletişim sayfası",
    "hours": "Çalışma saatlerimiz: {hours}.",
    "open": "Şu anda büromuz açık.",
    "closed": "Şu anda mesai saatleri dışındayız; WhatsApp ya da formdan yazarsanız ilk iş gününde dönüş yaparız.",
    "docs": "Konuyla ilgili sözleşme, tapu, tebligat, yazışma ve mahkeme ya da icra dairesinden gelen belgeleri getirmeniz, durumun daha hızlı değerlendirilmesini sağlar. Olayların kısa bir tarih sırası da işe yarar.",
    "fee": "Avukatlık ücreti, işin niteliği ve kapsamına göre birlikte belirlenir ve yazılı sözleşmeye bağlanır. Ücret, Avukatlık Asgari Ücret Tarifesi'nin altında olamaz. Kesin bilgi için görüşmede konuşmak gerekir.",
    "fee_talk": "Görüşme ayarlamak istiyorum",
    "team": "Büromuzda Av. Tuğsan Güneş, Av. Ömer Murat Erdil ve Av. Adem Karakaya birlikte çalışmaktadır. Tamamı Adana Barosu'na kayıtlıdır.",
    "team_link": "Avukatlarımız",
    "lang": "Görüşme, yazışma ve sözleşme çalışmalarını Türkçe ve İngilizce yürütüyoruz. We work in Turkish and English.",
    "unknown": "Bu soruya hazır bir yanıtım yok. Hukuki sorularınızı en doğru şekilde avukatlarımız yanıtlayabilir; bize ulaşmanız için:",
    # Hazır yanıtları seçen anahtar sözcükler (küçük harfe çevrilmiş ve Türkçe harfleri sadeleştirilmiş metinde aranır)
    "rules": {
        "appt": "randevu|gorus|ulas|iletisim|telefon|ara(ma|yin|mak)|whatsapp|yaz(mak|abilir)",
        "addr": "adres|nerede|konum|harita|yol tarif",
        "hours": "saat|acik|kapali|mesai|cumartesi|pazar",
        "fee": "ucret|fiyat|para|masraf|tarife|vekalet",
        "docs": "belge|evrak|getir|hazirla",
        "team": "avukat|kim|ekip|tugsan|omer|adem|erdil|karakaya|gunes",
        "lang": "ingilizce|english|dil",
        "areas": "alan|konu|hizmet|neler",
    },
    # Alan adlarında eşleşmede yok sayılan sözcükler
    "stop": "hukuku|ve",
}

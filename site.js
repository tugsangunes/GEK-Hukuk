// Mobil menü, iletişim formu ve telif yılı
(function () {
  var toggle = document.querySelector('.menu-toggle');
  var nav = document.getElementById('ana-menu');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  var form = document.getElementById('contact-form');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var status = document.getElementById('form-status');
      if (!form.checkValidity()) {
        status.textContent = 'Lütfen tüm alanları doldurun ve KVKK onay kutusunu işaretleyin.';
        return;
      }
      var name = form.elements['name'].value;
      var subject = 'İletişim talebi: ' + name;
      var body = form.elements['message'].value + '\n\n' + name + ' <' + form.elements['email'].value + '>';
      window.location.href = 'mailto:info@gekhukuk.com?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
      status.textContent = 'E-posta uygulamanız açılmadıysa info@gekhukuk.com adresine yazabilirsiniz.';
    });
  }

  // Harita yalnızca ziyaretçi isteyince Google'dan yüklenir
  var mapBtn = document.getElementById('map-load');
  if (mapBtn) {
    mapBtn.addEventListener('click', function () {
      var box = document.getElementById('harita');
      var frame = document.createElement('iframe');
      frame.src = box.getAttribute('data-src');
      frame.title = 'GEK Hukuk Bürosu konumu';
      frame.loading = 'lazy';
      frame.referrerPolicy = 'no-referrer-when-downgrade';
      box.innerHTML = '';
      box.appendChild(frame);
      box.classList.add('loaded');
    });
  }

  // Hazır yanıtlı site asistanı: tarayıcıda çalışır, hiçbir yere veri göndermez
  var botData = document.getElementById('asistan-veri');
  var bot = document.getElementById('asistan');
  var botToggle = document.querySelector('.bot-toggle');
  if (botData && bot && botToggle) {
    var D = JSON.parse(botData.textContent);
    var log = bot.querySelector('.bot-log');
    var started = false;
    botToggle.hidden = false;

    var norm = function (t) {
      return t.toLocaleLowerCase('tr').replace(/ı/g, 'i').replace(/ğ/g, 'g').replace(/ü/g, 'u')
        .replace(/ş/g, 's').replace(/ö/g, 'o').replace(/ç/g, 'c').replace(/â/g, 'a');
    };
    var el = function (tag, cls, text) {
      var n = document.createElement(tag);
      if (cls) n.className = cls;
      if (text) n.textContent = text;
      return n;
    };
    var say = function (who, text, html) {
      var m = el('div', 'bot-msg ' + who);
      if (html) m.innerHTML = html; else m.textContent = text;
      log.appendChild(m);
      log.scrollTop = log.scrollHeight;
      return m;
    };
    var links = function (items) {
      var row = el('div', 'bot-links');
      items.forEach(function (it) {
        var a = el('a', null, it[0]);
        a.href = it[1];
        if (/^https?:/.test(it[1])) { a.target = '_blank'; a.rel = 'noopener'; }
        row.appendChild(a);
      });
      log.appendChild(row);
      log.scrollTop = log.scrollHeight;
    };
    var choices = function (items) {
      var row = el('div', 'bot-choices');
      items.forEach(function (it) {
        var b = el('button', null, it[0]);
        b.type = 'button';
        b.addEventListener('click', function () { row.remove(); say('me', it[0]); setTimeout(it[1], 250); });
        row.appendChild(b);
      });
      log.appendChild(row);
      log.scrollTop = log.scrollHeight;
    };
    var contact = [['Ara', 'tel:' + D.tel], ['WhatsApp', 'https://wa.me/' + D.whatsapp], ['İletişim formu', 'iletisim.html']];
    var openNow = function () {
      var p = new Intl.DateTimeFormat('en-GB', { timeZone: 'Europe/Istanbul', weekday: 'short', hour: '2-digit', minute: '2-digit', hour12: false }).formatToParts(new Date());
      var g = {}; p.forEach(function (x) { g[x.type] = x.value; });
      var mins = parseInt(g.hour, 10) * 60 + parseInt(g.minute, 10);
      return ['Sat', 'Sun'].indexOf(g.weekday) < 0 && mins >= 540 && mins < 1020;
    };
    var more = function () { choices([['Başka bir konu', menu]]); };

    var A = {
      randevu: function () {
        say('bot', 'Görüşme için hafta içi 09.00 – 17.00 arasında bizi arayabilir, WhatsApp üzerinden yazabilir ya da iletişim formunu kullanabilirsiniz. Mesajınızda yalnızca konunun başlığını belirtmeniz yeterli; ayrıntıları görüşmede konuşuruz.');
        links(contact); more();
      },
      alanlar: function () {
        say('bot', 'Danışmanlık ve dava takibi yaptığımız alanlar şunlar. Ayrıntı için birini seçin:');
        choices(D.areas.map(function (a) { return [a.name, function () { A.alan(a); }]; }).concat([['Başka bir konu', menu]]));
      },
      alan: function (a) {
        say('bot', a.name + ': ' + a.summary);
        links([['Alan sayfasına git', a.href]]);
        choices([['Bu konuda görüşmek istiyorum', A.randevu], ['Diğer alanlar', A.alanlar], ['Başka bir konu', menu]]);
      },
      adres: function () {
        say('bot', 'Büromuzun adresi: ' + D.address + '.');
        links([['Haritada aç', D.map], ['İletişim sayfası', 'iletisim.html']]); more();
      },
      saat: function () {
        say('bot', 'Çalışma saatlerimiz: ' + D.hours + '. ' + (openNow() ? 'Şu anda büromuz açık.' : 'Şu anda mesai saatleri dışındayız; WhatsApp ya da formdan yazarsanız ilk iş gününde dönüş yaparız.'));
        links(contact); more();
      },
      belge: function () {
        say('bot', 'Konuyla ilgili sözleşme, tapu, tebligat, yazışma ve mahkeme ya da icra dairesinden gelen belgeleri getirmeniz, durumun daha hızlı değerlendirilmesini sağlar. Olayların kısa bir tarih sırası da işe yarar.');
        more();
      },
      ucret: function () {
        say('bot', 'Avukatlık ücreti, işin niteliği ve kapsamına göre birlikte belirlenir ve yazılı sözleşmeye bağlanır. Ücret, Avukatlık Asgari Ücret Tarifesi\'nin altında olamaz. Kesin bilgi için görüşmede konuşmak gerekir.');
        choices([['Görüşme ayarlamak istiyorum', A.randevu], ['Başka bir konu', menu]]);
      },
      avukat: function () {
        say('bot', 'Büromuzda Av. Tuğsan Güneş, Av. Ömer Murat Erdil ve Av. Adem Karakaya birlikte çalışmaktadır. Tamamı Adana Barosu\'na kayıtlıdır.');
        links([['Avukatlarımız', 'avukatlar.html']]); more();
      },
      dil: function () {
        say('bot', 'Görüşme, yazışma ve sözleşme çalışmalarını Türkçe ve İngilizce yürütüyoruz. We work in Turkish and English.');
        more();
      },
      bilinmiyor: function () {
        say('bot', 'Bu soruya hazır bir yanıtım yok. Hukuki sorularınızı en doğru şekilde avukatlarımız yanıtlayabilir; bize ulaşmanız için:');
        links(contact); more();
      }
    };

    var rules = [
      [/randevu|gorus|ulas|iletisim|telefon|ara(ma|yin|mak)|whatsapp|yaz(mak|abilir)/, A.randevu],
      [/adres|nerede|konum|harita|yol tarif/, A.adres],
      [/saat|acik|kapali|mesai|cumartesi|pazar/, A.saat],
      [/ucret|fiyat|para|masraf|tarife|vekalet/, A.ucret],
      [/belge|evrak|getir|hazirla/, A.belge],
      [/avukat|kim|ekip|tugsan|omer|adem|erdil|karakaya|gunes/, A.avukat],
      [/ingilizce|english|dil/, A.dil],
      [/alan|konu|hizmet|neler/, A.alanlar]
    ];

    var answer = function (q) {
      var n = norm(q);
      for (var i = 0; i < D.areas.length; i++) {
        var a = D.areas[i];
        var words = norm(a.name).replace(/hukuku|ve|\(|\)/g, ' ').split(/\s+/).filter(function (w) { return w.length > 3; });
        var hit = words.some(function (w) { return n.indexOf(w.slice(0, 5)) >= 0; }) ||
          a.keys.some(function (k) { return norm(k).split(/[\s,()]+/).some(function (w) { return w.length > 5 && n.indexOf(w.slice(0, 6)) >= 0; }); });
        if (hit) { A.alan(a); return; }
      }
      for (var j = 0; j < rules.length; j++) if (rules[j][0].test(n)) { rules[j][1](); return; }
      A.bilinmiyor();
    };

    function menu() {
      say('bot', 'Size nasıl yardımcı olabilirim?');
      choices([
        ['Randevu almak istiyorum', A.randevu],
        ['Çalışma alanlarınız', A.alanlar],
        ['Adres ve harita', A.adres],
        ['Çalışma saatleri', A.saat],
        ['İlk görüşmeye ne getirmeliyim?', A.belge],
        ['Ücretler', A.ucret]
      ]);
    }

    var setOpen = function (open) {
      bot.hidden = !open;
      botToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      document.body.classList.toggle('bot-open', open);
      if (open && !started) {
        started = true;
        say('bot', 'Merhaba, GEK Hukuk Bürosu\'na hoş geldiniz. Bu asistan büromuzla ilgili sık sorulan sorulara hazır yanıtlar verir; hukuki görüş veya tavsiye vermez.');
        menu();
      }
      if (open) bot.querySelector('input').focus({ preventScroll: true });
    };
    botToggle.addEventListener('click', function () { setOpen(bot.hidden); });
    bot.querySelector('.bot-close').addEventListener('click', function () { setOpen(false); botToggle.focus(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !bot.hidden) setOpen(false); });
    bot.querySelector('.bot-input').addEventListener('submit', function (e) {
      e.preventDefault();
      var inp = this.elements.q, q = inp.value.trim();
      if (!q) return;
      inp.value = '';
      log.querySelectorAll('.bot-choices').forEach(function (c) { c.remove(); });
      say('me', q);
      setTimeout(function () { answer(q); }, 300);
    });
  }

  // Bölümleri ekrana girerken yumuşakça göster
  var targets = document.querySelectorAll('.block .wrap, .facts-band .wrap, .area-tile, .contact-band .wrap');
  if ('IntersectionObserver' in window && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    document.documentElement.classList.add('reveal-on');
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px' });
    targets.forEach(function (t) { t.classList.add('reveal'); io.observe(t); });
  }

  var year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();
})();

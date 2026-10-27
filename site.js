// Mobil menü, dil seçici, iletişim formu ve telif yılı
(function () {
  // Sayfanın dilindeki arayüz metinleri (tools/diller/<dil>.py içindeki JS sözlüğü)
  var metin = document.getElementById('site-metin');
  var T = metin ? JSON.parse(metin.textContent) : {};
  var lang = document.documentElement.lang || 'tr';
  var fill = function (s, v) { return s.replace(/\{(\w+)\}/g, function (_, k) { return v[k]; }); };

  var toggle = document.querySelector('.menu-toggle');
  var nav = document.getElementById('ana-menu');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // Dil seçici: dışarı tıklanınca veya Esc ile kapanır
  var langSw = document.querySelector('.lang-switch');
  if (langSw) {
    document.addEventListener('click', function (e) { if (langSw.open && !langSw.contains(e.target)) langSw.open = false; });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && langSw.open) { langSw.open = false; langSw.querySelector('summary').focus(); } });
  }

  var form = document.getElementById('contact-form');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var status = document.getElementById('form-status');
      if (!form.checkValidity()) {
        status.textContent = T.form_invalid;
        return;
      }
      var name = form.elements['name'].value;
      var subject = T.form_subject + name;
      var body = form.elements['message'].value + '\n\n' + name + ' <' + form.elements['email'].value + '>';
      window.location.href = 'mailto:info@gekhukuk.com?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
      status.textContent = T.form_sent;
    });
  }

  // Harita yalnızca ziyaretçi isteyince Google'dan yüklenir
  var mapBtn = document.getElementById('map-load');
  if (mapBtn) {
    mapBtn.addEventListener('click', function () {
      var box = document.getElementById('harita');
      var frame = document.createElement('iframe');
      frame.src = box.getAttribute('data-src');
      frame.title = T.map_title;
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
      return t.toLocaleLowerCase(lang).replace(/ı/g, 'i').replace(/ğ/g, 'g').replace(/ü/g, 'u')
        .replace(/ş/g, 's').replace(/ö/g, 'o').replace(/ç/g, 'c').replace(/â/g, 'a');
    };
    var el = function (tag, cls, text) {
      var n = document.createElement(tag);
      if (cls) n.className = cls;
      if (text) n.textContent = text;
      return n;
    };
    var say = function (who, text) {
      var m = el('div', 'bot-msg ' + who.replace(/^bot\b/, 'from-bot').replace(/^me$/, 'from-me'));
      // Yanıttaki sayfa adlarını (ör. is-hukuku.html) bağlantıya çevir
      text.split(/([a-z0-9-]+\.html(?:#[a-z0-9-]+)?)/).forEach(function (part, i) {
        if (i % 2) { var a = el('a', null, part); a.href = part; m.appendChild(a); }
        else m.appendChild(document.createTextNode(part));
      });
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
    var contact = [[T.c_call, 'tel:' + D.tel], [T.c_wa, 'https://wa.me/' + D.whatsapp], [T.c_form, 'iletisim.html']];
    var openNow = function () {
      var p = new Intl.DateTimeFormat('en-GB', { timeZone: 'Europe/Istanbul', weekday: 'short', hour: '2-digit', minute: '2-digit', hour12: false }).formatToParts(new Date());
      var g = {}; p.forEach(function (x) { g[x.type] = x.value; });
      var mins = parseInt(g.hour, 10) * 60 + parseInt(g.minute, 10);
      return ['Sat', 'Sun'].indexOf(g.weekday) < 0 && mins >= 540 && mins < 1020;
    };
    var more = function () { choices([[T.other, menu]]); };

    var A = {
      randevu: function () {
        say('bot', T.appt);
        links(contact); more();
      },
      alanlar: function () {
        say('bot', T.areas);
        choices(D.areas.map(function (a) { return [a.name, function () { A.alan(a); }]; }).concat([[T.other, menu]]));
      },
      alan: function (a) {
        say('bot', a.name + ': ' + a.summary);
        links([[T.area_page, a.href]]);
        choices([[T.area_talk, A.randevu], [T.area_more, A.alanlar], [T.other, menu]]);
      },
      adres: function () {
        say('bot', fill(T.addr, D));
        links([[T.map_open, D.map], [T.contact_page, 'iletisim.html']]); more();
      },
      saat: function () {
        say('bot', fill(T.hours, D) + ' ' + (openNow() ? T.open : T.closed));
        links(contact); more();
      },
      belge: function () {
        say('bot', T.docs);
        more();
      },
      ucret: function () {
        say('bot', T.fee);
        choices([[T.fee_talk, A.randevu], [T.other, menu]]);
      },
      avukat: function () {
        say('bot', T.team);
        links([[T.team_link, 'avukatlar.html']]); more();
      },
      dil: function () {
        say('bot', T.lang);
        more();
      },
      bilinmiyor: function () {
        say('bot', T.unknown);
        links(contact); more();
      }
    };

    var R = T.rules;
    var rules = [
      [R.appt, A.randevu], [R.addr, A.adres], [R.hours, A.saat], [R.fee, A.ucret],
      [R.docs, A.belge], [R.team, A.avukat], [R.lang, A.dil], [R.areas, A.alanlar]
    ].map(function (r) { return [new RegExp(r[0]), r[1]]; });
    var stop = new RegExp('(^|\\s)(' + T.stop + ')(?=\\s|$)|\\(|\\)', 'g');

    var answer = function (q) {
      var n = norm(q);
      for (var i = 0; i < D.areas.length; i++) {
        var a = D.areas[i];
        var words = norm(a.name).replace(stop, ' ').split(/\s+/).filter(function (w) { return w.length > 3 || /[^\u0000-\u024f]/.test(w); });
        var hit = words.some(function (w) { return n.indexOf(w.slice(0, 5)) >= 0; }) ||
          a.keys.some(function (k) { return norm(k).split(/[\s,()]+/).some(function (w) { return w.length > 5 && n.indexOf(w.slice(0, 6)) >= 0; }); });
        if (hit) { A.alan(a); return; }
      }
      for (var j = 0; j < rules.length; j++) if (rules[j][0].test(n)) { rules[j][1](); return; }
      A.bilinmiyor();
    };

    // Serbest sorular yapay zekâya gider; yanıt alınamazsa hazır yanıtlara dönülür
    var history = [];
    var busy = false;
    var ask = function (q) {
      if (busy) return;
      busy = true;
      var typing = say('bot typing', T.typing);
      var sent = history.concat([{ role: 'user', content: q }]).slice(-11);
      if (sent[0].role !== 'user') sent = sent.slice(1);
      fetch(D.api, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages: sent, lang: D.lang })
      }).then(function (r) {
        return r.json().then(function (j) { if (!r.ok || !j.reply) throw new Error(j.error || r.status); return j.reply; });
      }).then(function (reply) {
        typing.remove();
        history = sent.concat([{ role: 'assistant', content: reply }]);
        say('bot', reply);
        more();
      }).catch(function (err) {
        typing.remove();
        if (String(err.message) === 'rate') {
          say('bot', T.rate);
          links(contact); more();
        } else {
          answer(q);
        }
      }).then(function () { busy = false; });
    };

    function menu() {
      say('bot', T.menu_q);
      choices([
        [T.m_appt, A.randevu],
        [T.m_areas, A.alanlar],
        [T.m_addr, A.adres],
        [T.m_hours, A.saat],
        [T.m_docs, A.belge],
        [T.m_fee, A.ucret]
      ]);
    }

    var setOpen = function (open) {
      bot.hidden = !open;
      document.querySelectorAll('.bot-toggle, .bot-toggle-m').forEach(function (t) { t.setAttribute('aria-expanded', open ? 'true' : 'false'); });
      document.body.classList.toggle('bot-open', open);
      if (open && !started) {
        started = true;
        say('bot', T.welcome);
        var note = el('p', 'bot-note', T.ai_note + ' ');
        var more_ = el('a', null, T.details);
        more_.href = 'kvkk.html#yapay-zeka';
        note.appendChild(more_);
        log.appendChild(note);
        menu();
      }
      if (open) bot.querySelector('input').focus({ preventScroll: true });
    };
    botToggle.addEventListener('click', function () { setOpen(bot.hidden); });
    var botToggleM = document.querySelector('.bot-toggle-m');
    if (botToggleM) botToggleM.addEventListener('click', function () { setOpen(bot.hidden); });
    bot.querySelector('.bot-close').addEventListener('click', function () { setOpen(false); botToggle.focus(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !bot.hidden) setOpen(false); });
    bot.querySelector('.bot-input').addEventListener('submit', function (e) {
      e.preventDefault();
      var inp = this.elements.q, q = inp.value.trim();
      if (!q) return;
      inp.value = '';
      log.querySelectorAll('.bot-choices').forEach(function (c) { c.remove(); });
      say('me', q);
      ask(q);
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

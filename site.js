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

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

  var year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();
})();

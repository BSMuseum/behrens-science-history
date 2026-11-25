(function () {
  var views = __VIEWS__;
  var titles = __TITLES__;
  function show() {
    var name = (location.hash || '').replace('#', '');
    var inner = null;
    if (!views[name]) {
      var el = name ? document.getElementById(name) : null;
      var host = el ? el.closest('.view') : null;
      if (host) { inner = el; name = host.id.replace('v-', ''); } else { name = 'home'; }
    }
    Object.keys(views).forEach(function (k) {
      document.getElementById(views[k]).hidden = (k !== name);
    });
    document.title = titles[name];
    if (inner) { inner.scrollIntoView(); } else { window.scrollTo(0, 0); }
  }
  window.addEventListener('hashchange', show);
  show();
})();

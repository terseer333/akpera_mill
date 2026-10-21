/* ==========================================================================
   AKPERA MILL — interactions
   ========================================================================== */
(function () {
  'use strict';

  /* ----------------------------------------------------------------------
     Catalogue data
     ---------------------------------------------------------------------- */
  var PRODUCTS = [
    { id: 'lg50',  kicker: 'LONG GRAIN · 50kg',   name: 'Premium Long Grain', price: '85,000', rating: '4.8', art: 'home-p1' },
    { id: 'pb25',  kicker: 'PARBOILED · 25kg',    name: 'Golden Parboiled',   price: '44,000', rating: '4.8', art: 'home-p2' },
    { id: 'fr10',  kicker: 'FRAGRANT · 10kg',     name: 'Aromatic Fragrant',  price: '24,000', rating: '4.8', art: 'home-p3' },
    { id: 'br5',   kicker: 'BROWN RICE · 5kg',    name: 'Wholegrain Brown',  price: '13,500', rating: '4.8', art: 'home-p4' },
    { id: 'lg25',  kicker: 'LONG GRAIN · 25kg',   name: 'Premium Long Grain', price: '43,000', rating: '4.8', art: 'cat-p5' },
    { id: 'pb50',  kicker: 'PARBOILED · 50kg',    name: 'Golden Parboiled',   price: '86,000', rating: '4.8', art: 'cat-p6' },
    { id: 'lg10',  kicker: 'LONG GRAIN · 10kg',   name: 'Premium Long Grain', price: '18,000', rating: '4.8', art: 'cat-p7' },
    { id: 'fr5',   kicker: 'FRAGRANT · 5kg',      name: 'Aromatic Fragrant',  price: '12,500', rating: '4.8', art: 'cat-p8' }
  ];

  var money = function (n) { return '₦' + n; };

  /* Responsive artwork: the mockups ship different crops per breakpoint. */
  function artTag(base, alt) {
    return '<picture>' +
      '<source media="(max-width: 767px)" srcset="images/' + base + '-m.png">' +
      '<source media="(max-width: 1023px)" srcset="images/' + base + '-t.png">' +
      '<img src="images/' + base + '-d.png" alt="' + alt + '">' +
      '</picture>';
  }

  /* ----------------------------------------------------------------------
     Product card
     ---------------------------------------------------------------------- */
  function cardMarkup(p, cls) {
    return '' +
      '<article class="card ' + (cls || '') + '" data-id="' + p.id + '">' +
        '<div class="card__media">' + artTag(p.art, p.name) + '</div>' +
        '<p class="card__kicker">' + p.kicker + '</p>' +
        '<h3 class="card__name">' + p.name + '</h3>' +
        '<div class="card__meta">' +
          '<span class="card__price">' + money(p.price) + '</span>' +
          '<span class="card__rating"><span class="star">★</span> ' + p.rating + '</span>' +
        '</div>' +
        '<button class="btn btn--sm js-add" data-id="' + p.id + '">Add to Cart +</button>' +
      '</article>';
  }

  function renderHome() {
    var grid = document.getElementById('product-grid');
    if (!grid) return;
    grid.innerHTML = PRODUCTS.slice(0, 4).map(function (p) { return cardMarkup(p); }).join('');
  }

  function renderCatalog() {
    var grid = document.getElementById('catalog-grid');
    if (!grid) return;
    var art = ['cat-p1', 'cat-p2', 'cat-p3', 'cat-p4', 'cat-p5', 'cat-p6', 'cat-p7', 'cat-p8'];
    grid.innerHTML = PRODUCTS.map(function (p, i) {
      var c = Object.assign({}, p, { art: art[i] });
      return cardMarkup(c, 'catalog-card');
    }).join('');
  }

  /* ----------------------------------------------------------------------
     Cart state
     ---------------------------------------------------------------------- */
  var CART_KEY = 'akpera.cart';
  var cart = [];

  function loadCart() {
    try { cart = JSON.parse(localStorage.getItem(CART_KEY)) || []; }
    catch (e) { cart = []; }
  }
  function saveCart() {
    try { localStorage.setItem(CART_KEY, JSON.stringify(cart)); } catch (e) {}
  }

  function addToCart(id) {
    var p = PRODUCTS.filter(function (x) { return x.id === id; })[0];
    if (!p) return;
    var line = cart.filter(function (l) { return l.id === id; })[0];
    if (line) line.qty += 1;
    else cart.push({ id: id, qty: 1 });
    saveCart();
    renderCart();
  }

  function cartTotals() {
    var subtotal = 0, bags = 0, kg = 0, kinds = {};
    cart.forEach(function (l) {
      var p = PRODUCTS.filter(function (x) { return x.id === l.id; })[0];
      if (!p) return;
      var weight = parseInt(p.kicker.replace(/[^0-9]/g, ''), 10) || 0;
      subtotal += parseInt(p.price.replace(/,/g, ''), 10) * l.qty;
      bags += l.qty;
      kg += weight * l.qty;
      kinds[l.id] = 1;
    });
    var delivery = bags ? 5000 : 0;
    return {
      subtotal: subtotal, bags: bags, kg: kg, kinds: Object.keys(kinds).length,
      delivery: delivery, total: subtotal + delivery
    };
  }

  function renderCart() {
    var list = document.getElementById('cart-items');
    if (!list) return;
    var t = cartTotals();
    list.innerHTML = cart.map(function (l) {
      var p = PRODUCTS.filter(function (x) { return x.id === l.id; })[0];
      if (!p) return '';
      var art = 'home-p1';
      return '' +
        '<div class="cart-item" data-id="' + l.id + '">' +
          '<div class="cart-item__media">' + artTag(art, p.name) + '</div>' +
          '<div class="cart-item__body">' +
            '<h3>' + p.name + '</h3>' +
            '<p class="cart-item__meta">' + p.kicker.replace(/ · /, ' sealed bag · ') + ' · ' + money(p.price) + ' each</p>' +
            '<div class="cart-item__row">' +
              '<div class="qty">' +
                '<button class="js-dec" data-id="' + l.id + '">−</button>' +
                '<span>' + l.qty + '</span>' +
                '<button class="js-inc" data-id="' + l.id + '">+</button>' +
              '</div>' +
              '<button class="link js-remove" data-id="' + l.id + '">Remove</button>' +
              '<span class="cart-item__price">' + money(parseInt(p.price.replace(/,/g, ''), 10) * l.qty) + '</span>' +
            '</div>' +
          '</div>' +
        '</div>';
    }).join('');

    set('cart-bags', t.bags + ' bag' + (t.bags === 1 ? '' : 's') + ' · ' + t.kinds + ' product' + (t.kinds === 1 ? '' : 's') + ' · ' + t.kg + 'kg');
    set('cart-subtotal', money(t.subtotal));
    set('cart-delivery', t.delivery ? money(t.delivery) : money(0));
    set('cart-total', money(t.total));
  }

  function set(id, v) {
    var el = document.getElementById(id);
    if (el) el.textContent = v;
  }

  /* ----------------------------------------------------------------------
     Global click handling
     ---------------------------------------------------------------------- */
  document.addEventListener('click', function (e) {
    var t = e.target;

    var add = t.closest && t.closest('.js-add');
    if (add) { addToCart(add.getAttribute('data-id')); return; }

    var inc = t.closest && t.closest('.js-inc');
    if (inc) {
      cart.forEach(function (l) { if (l.id === inc.getAttribute('data-id')) l.qty += 1; });
      saveCart(); renderCart(); return;
    }
    var dec = t.closest && t.closest('.js-dec');
    if (dec) {
      var id = dec.getAttribute('data-id');
      cart.forEach(function (l) { if (l.id === id) l.qty = Math.max(0, l.qty - 1); });
      cart = cart.filter(function (l) { return l.qty > 0; });
      saveCart(); renderCart(); return;
    }
    var rm = t.closest && t.closest('.js-remove');
    if (rm) {
      cart = cart.filter(function (l) { return l.id !== rm.getAttribute('data-id'); });
      saveCart(); renderCart(); return;
    }

    var drawer = t.closest && t.closest('.js-drawer-toggle');
    if (drawer) {
      var panel = document.getElementById('filter-drawer');
      if (panel) panel.classList.toggle('is-open');
      document.body.classList.toggle('drawer-open');
      return;
    }
    var close = t.closest && t.closest('.js-drawer-close');
    if (close) {
      var p2 = document.getElementById('filter-drawer');
      if (p2) p2.classList.remove('is-open');
      document.body.classList.remove('drawer-open');
      return;
    }

    var tab = t.closest && t.closest('.js-tab');
    if (tab) {
      var group = tab.getAttribute('data-group');
      document.querySelectorAll('[data-tab-group="' + group + '"]').forEach(function (b) {
        b.classList.remove('is-on');
      });
      tab.classList.add('is-on');
      var target = tab.getAttribute('data-target');
      document.querySelectorAll('[data-panel-group="' + group + '"]').forEach(function (p3) {
        p3.hidden = p3.getAttribute('data-panel') !== target;
      });
      return;
    }

    var size = t.closest && t.closest('.js-size');
    if (size) {
      document.querySelectorAll('.js-size').forEach(function (b) { b.classList.remove('pdp__size--on'); });
      size.classList.add('pdp__size--on');
      return;
    }

    var promo = t.closest && t.closest('.js-apply');
    if (promo) {
      var input = document.getElementById('promo-code');
      var note = document.getElementById('promo-note');
      if (note) {
        note.textContent = input && input.value.trim()
          ? 'Code "' + input.value.trim() + '" applied.'
          : 'Enter a code to apply a discount.';
      }
      return;
    }
  });

  /* ----------------------------------------------------------------------
     Boot
     ---------------------------------------------------------------------- */
  loadCart();
  renderHome();
  renderCatalog();
  renderCart();

  window.Akpera = { products: PRODUCTS, cart: cart, addToCart: addToCart };
})();

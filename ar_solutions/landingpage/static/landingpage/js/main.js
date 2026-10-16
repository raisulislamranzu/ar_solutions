/**
 * Behavior and interactive features for AR Solutions BD Landing Page
 * Handles: Products rendering, Search, Category filter, Quick View,
 * Direct Order modal, Shopping Cart, Cart Checkout, and Toast notifications.
 */

// -------- State & Data --------
let productsData = [];
let cart = [];
let currentQuickOrderProduct = null;
let selectedDeliveryFee = 0;
let activeCategory = '';

// -------- Utility Functions --------
const fmt = (n) => Number(n).toLocaleString('en-US');

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

const csrftoken = getCookie('csrftoken');

function renderStars(rating) {
  let html = '';
  const full = Math.floor(rating);
  const half = rating - full >= 0.5;
  for (let i = 0; i < 5; i++) {
    if (i < full) html += '<i class="fa-solid fa-star"></i>';
    else if (i === full && half) html += '<i class="fa-solid fa-star-half-stroke"></i>';
    else html += '<i class="fa-regular fa-star"></i>';
  }
  return html;
}

// -------- Product Rendering --------
function renderProducts() {
  const grid = document.getElementById('productGrid');
  const empty = document.getElementById('emptyState');
  const searchInput = document.getElementById('searchInput');
  const q = (searchInput ? searchInput.value : '').toLowerCase().trim();

  const list = productsData.filter(p => {
    const matchCat = !activeCategory || p.category === activeCategory;
    const matchQ = !q || p.title.toLowerCase().includes(q);
    return matchCat && matchQ;
  });

  const countEl = document.getElementById('productCount');
  if (countEl) countEl.innerText = list.length + ' টি পণ্য';

  if (!grid) return;

  if (!list.length) {
    grid.innerHTML = '';
    if (empty) empty.classList.remove('hidden');
    return;
  }

  if (empty) empty.classList.add('hidden');

  grid.innerHTML = list.map(p => {
    const badge = p.badge
      ? `<span class="absolute top-2 left-2 bg-brand-accent text-white text-[10px] font-bold px-2 py-0.5 rounded-full font-bn">${p.badge}</span>`
      : '';
    const disc = p.discountPercent
      ? `<span class="absolute top-2 right-2 bg-red-500 text-white text-[10px] font-bold px-2 py-0.5 rounded-full">${p.discountPercent}% ছাড়</span>`
      : '';
    const img = p.image ? p.image : 'https://via.placeholder.com/400x300?text=No+Image';

    return `
    <div class="bg-white rounded-2xl border border-gray-100 shadow-sm hover:shadow-lg transition overflow-hidden flex flex-col">
      <div class="relative">
        <img src="${img}" alt="${p.title}" class="w-full h-40 sm:h-48 object-cover cursor-pointer" onclick="openProductQuickView(${p.id})">
        ${badge}${disc}
      </div>
      <div class="p-3 sm:p-4 flex flex-col flex-1">
        ${p.category ? `<span class="text-[11px] text-brand-green font-semibold font-bn mb-1">${p.category}</span>` : ''}
        <h4 class="font-bold text-sm text-brand-teal font-bn leading-snug line-clamp-2 mb-1.5 cursor-pointer hover:text-brand-green" onclick="openProductQuickView(${p.id})">${p.title}</h4>
        <div class="flex items-center gap-1 mb-2 text-brand-accent text-xs">${renderStars(p.rating)}<span class="text-gray-400 ml-1">(${p.reviewsCount})</span></div>
        <div class="flex items-end gap-2 mb-3 mt-auto">
          <span class="text-lg font-extrabold text-brand-green">৳${fmt(p.price)}</span>
          ${p.oldPrice && p.oldPrice > p.price ? `<span class="text-gray-400 line-through text-xs">৳${fmt(p.oldPrice)}</span>` : ''}
        </div>
        <div class="flex gap-2">
          <button onclick="triggerDirectOrder(${p.id})" class="flex-1 bg-brand-green hover:bg-brand-greenHover text-white py-2 rounded-lg text-xs font-bold font-bn transition">অর্ডার করুন</button>
          <button onclick="addToCart(${p.id})" title="কার্টে যোগ করুন" class="w-9 shrink-0 bg-brand-teal hover:bg-brand-tealLight text-white rounded-lg transition"><i class="fa-solid fa-cart-plus text-xs"></i></button>
        </div>
      </div>
    </div>`;
  }).join('');
}

// -------- Quick View Modal --------
function openProductQuickView(productId) {
  const product = productsData.find(p => p.id === productId);
  if (!product) return;

  const qvImage = document.getElementById('qvImage');
  const qvTitle = document.getElementById('qvTitle');
  const qvCategory = document.getElementById('qvCategory');
  const qvPrice = document.getElementById('qvPrice');
  const qvOldPrice = document.getElementById('qvOldPrice');
  const qvDescription = document.getElementById('qvDescription');
  const qvRating = document.getElementById('qvRating');
  const qvReviews = document.getElementById('qvReviews');
  const qvDiscountBadge = document.getElementById('qvDiscountBadge');
  const qvHighlights = document.getElementById('qvHighlights');
  const qvDirectOrderBtn = document.getElementById('qvDirectOrderBtn');
  const qvAddToCartBtn = document.getElementById('qvAddToCartBtn');

  if (qvImage) qvImage.src = product.image || 'https://via.placeholder.com/400x300?text=No+Image';
  if (qvTitle) qvTitle.innerText = product.title;
  if (qvCategory) qvCategory.innerText = product.category || 'General';
  if (qvPrice) qvPrice.innerText = '৳ ' + fmt(product.price);
  if (qvOldPrice) qvOldPrice.innerText = (product.oldPrice && product.oldPrice > product.price) ? '৳ ' + fmt(product.oldPrice) : '';
  if (qvDescription) qvDescription.innerText = product.description;
  if (qvRating) qvRating.innerHTML = renderStars(product.rating);
  if (qvReviews) qvReviews.innerText = `${product.rating} (${product.reviewsCount} জন গ্রাহক ভেরিফাইড রিভিউ দিয়েছেন)`;

  if (qvDiscountBadge) {
    qvDiscountBadge.innerText = product.discountPercent ? `${product.discountPercent}% ছাড়` : '';
    qvDiscountBadge.style.display = product.discountPercent ? '' : 'none';
  }

  if (qvHighlights) {
    qvHighlights.innerHTML = (product.highlights && product.highlights.length)
      ? product.highlights.map(h => `<li class="flex items-start gap-2"><i class="fa-solid fa-circle-check text-brand-green mt-1 text-xs"></i><span>${h}</span></li>`).join('')
      : '<li class="text-gray-400">কোনো বিবরণ যোগ করা হয়নি।</li>';
  }

  if (qvDirectOrderBtn) {
    qvDirectOrderBtn.onclick = () => {
      closeProductQuickView();
      triggerDirectOrder(productId);
    };
  }

  if (qvAddToCartBtn) {
    qvAddToCartBtn.onclick = () => {
      addToCart(productId);
    };
  }

  const modal = document.getElementById('productQuickViewModal');
  if (modal) modal.classList.remove('hidden');
}

function closeProductQuickView() {
  const modal = document.getElementById('productQuickViewModal');
  if (modal) modal.classList.add('hidden');
}

// -------- Direct / Quick Order Modal --------
function triggerDirectOrder(productId) {
  currentQuickOrderProduct = productsData.find(p => p.id === productId);
  if (!currentQuickOrderProduct) return;

  const productIdInput = document.getElementById('orderProductId');
  const modalImg = document.getElementById('modalProductImage');
  const modalTitle = document.getElementById('modalProductTitle');
  const qtyInput = document.getElementById('orderQuantity');
  const insideRadio = document.querySelector('input[name="deliveryArea"][value="Inside Dhaka"]');

  if (productIdInput) productIdInput.value = productId;
  if (modalImg) modalImg.src = currentQuickOrderProduct.image || 'https://via.placeholder.com/100x100';
  if (modalTitle) modalTitle.innerText = currentQuickOrderProduct.title;
  if (qtyInput) qtyInput.value = 1;
  if (insideRadio) insideRadio.checked = true;

  selectDeliveryArea('Inside Dhaka');

  const modal = document.getElementById('quickOrderModal');
  if (modal) modal.classList.remove('hidden');
}

function selectDeliveryArea(area) {
  if (!currentQuickOrderProduct) return;
  selectedDeliveryFee = (area === 'Outside Dhaka')
    ? currentQuickOrderProduct.deliveryOutside
    : currentQuickOrderProduct.deliveryInside;

  const activeCls = 'border-brand-green bg-brand-greenLight/30';
  const idleCls = 'border-gray-200';

  const labelDhaka = document.getElementById('labelDhaka');
  const labelOutside = document.getElementById('labelOutside');

  if (labelDhaka) {
    labelDhaka.className = 'flex items-center gap-2 p-2.5 border rounded-xl cursor-pointer hover:bg-gray-50 transition ' +
      (area === 'Inside Dhaka' ? activeCls : idleCls);
  }
  if (labelOutside) {
    labelOutside.className = 'flex items-center gap-2 p-2.5 border rounded-xl cursor-pointer hover:bg-gray-50 transition ' +
      (area === 'Outside Dhaka' ? activeCls : idleCls);
  }

  updateOrderModalCalculations();
}

function changeQty(delta) {
  const input = document.getElementById('orderQuantity');
  if (!input) return;
  input.value = Math.max(1, (parseInt(input.value, 10) || 1) + delta);
  updateOrderModalCalculations();
}

function updateOrderModalCalculations() {
  if (!currentQuickOrderProduct) return;
  const price = currentQuickOrderProduct.price;
  const qtyEl = document.getElementById('orderQuantity');
  const qty = parseInt(qtyEl ? qtyEl.value : 1, 10) || 1;
  const grandTotal = (price * qty) + selectedDeliveryFee;

  const priceTotalEl = document.getElementById('modalProductPriceTotal');
  const priceTotal2El = document.getElementById('modalProductPriceTotal2');
  const deliveryFeeEl = document.getElementById('modalDeliveryFeeText');
  const grandTotalEl = document.getElementById('modalGrandTotal');

  if (priceTotalEl) priceTotalEl.innerText = fmt(price * qty);
  if (priceTotal2El) priceTotal2El.innerText = fmt(price * qty);
  if (deliveryFeeEl) deliveryFeeEl.innerText = fmt(selectedDeliveryFee);
  if (grandTotalEl) grandTotalEl.innerText = fmt(grandTotal);
}

function closeQuickOrderModal() {
  const modal = document.getElementById('quickOrderModal');
  if (modal) modal.classList.add('hidden');
}

// -------- Shopping Cart --------
function addToCart(productId) {
  const product = productsData.find(p => p.id === productId);
  if (!product) return;

  const existing = cart.find(i => i.id === productId);
  if (existing) {
    existing.qty += 1;
  } else {
    cart.push({
      id: product.id,
      title: product.title,
      price: product.price,
      image: product.image,
      qty: 1
    });
  }

  updateCartUI();
  showToast('পণ্যটি কার্টে যোগ করা হয়েছে।');
}

function cartQtyChange(productId, delta) {
  const item = cart.find(i => i.id === productId);
  if (!item) return;

  item.qty += delta;
  if (item.qty < 1) {
    cart = cart.filter(i => i.id !== productId);
  }
  updateCartUI();
}

function cartRemove(productId) {
  cart = cart.filter(i => i.id !== productId);
  updateCartUI();
}

function updateCartUI() {
  const count = cart.reduce((s, i) => s + i.qty, 0);
  const cartCountEl = document.getElementById('cartCount');
  const cartTotalEl = document.getElementById('cartTotal');
  const box = document.getElementById('cartItems');

  if (cartCountEl) cartCountEl.innerText = count;
  if (cartTotalEl) cartTotalEl.innerText = fmt(cart.reduce((s, i) => s + (i.price * i.qty), 0));

  if (!box) return;

  if (!cart.length) {
    box.innerHTML = '<div class="text-center text-gray-400 py-16 font-bn"><i class="fa-solid fa-cart-shopping text-4xl mb-3 block"></i>আপনার কার্ট খালি।</div>';
    return;
  }

  box.innerHTML = cart.map(i => `
    <div class="flex items-center gap-3 bg-gray-50 rounded-xl p-3">
      <img src="${i.image || 'https://via.placeholder.com/60'}" class="w-14 h-14 object-cover rounded-lg" alt="">
      <div class="flex-1 min-w-0">
        <p class="font-bold text-sm text-brand-teal font-bn truncate">${i.title}</p>
        <p class="text-brand-green font-bold text-sm">৳${fmt(i.price * i.qty)}</p>
      </div>
      <div class="flex items-center border border-gray-200 rounded-lg bg-white">
        <button onclick="cartQtyChange(${i.id}, -1)" class="px-2 py-1 text-gray-600"><i class="fa-solid fa-minus text-[10px]"></i></button>
        <span class="px-2 text-sm">${i.qty}</span>
        <button onclick="cartQtyChange(${i.id}, 1)" class="px-2 py-1 text-gray-600"><i class="fa-solid fa-plus text-[10px]"></i></button>
      </div>
      <button onclick="cartRemove(${i.id})" class="text-red-400 hover:text-red-600 px-1"><i class="fa-solid fa-trash text-sm"></i></button>
    </div>`).join('');
}

function toggleCart() {
  const d = document.getElementById('cartDrawer');
  if (!d) return;
  d.classList.toggle('hidden');
  if (!d.classList.contains('hidden')) updateCartUI();
}

// -------- Cart Checkout Modal --------
function checkoutCart() {
  if (!cart.length) {
    showToast('আপনার কার্ট খালি।');
    return;
  }
  const drawer = document.getElementById('cartDrawer');
  const checkoutModal = document.getElementById('checkoutModal');
  if (drawer) drawer.classList.add('hidden');
  if (checkoutModal) checkoutModal.classList.remove('hidden');
}

function closeCheckout() {
  const checkoutModal = document.getElementById('checkoutModal');
  if (checkoutModal) checkoutModal.classList.add('hidden');
}

// -------- Toast Notification --------
function showToast(msg) {
  const toast = document.getElementById('toastNotification');
  if (!toast) return;
  const msgEl = document.getElementById('toastMessage');
  if (msgEl) msgEl.innerText = msg;
  toast.classList.remove('translate-y-24', 'opacity-0');
  toast.classList.add('translate-y-0', 'opacity-100');
  setTimeout(() => {
    toast.classList.add('translate-y-24', 'opacity-0');
    toast.classList.remove('translate-y-0', 'opacity-100');
  }, 3500);
}

// -------- Event Listeners & Initialization --------
document.addEventListener('DOMContentLoaded', () => {
  // 1. Load products data from embedded json_script tag
  const scriptTag = document.getElementById('products-data');
  if (scriptTag) {
    try {
      productsData = JSON.parse(scriptTag.textContent) || [];
    } catch (e) {
      console.error('Failed to parse products data:', e);
      productsData = [];
    }
  }

  // 2. Category filter
  const categoryFilter = document.getElementById('categoryFilter');
  if (categoryFilter) {
    categoryFilter.addEventListener('click', (e) => {
      const btn = e.target.closest('.cat-btn');
      if (!btn) return;
      document.querySelectorAll('.cat-btn').forEach(b => {
        b.classList.remove('bg-brand-teal', 'text-white');
        b.classList.add('bg-gray-100', 'text-gray-600');
      });
      btn.classList.add('bg-brand-teal', 'text-white');
      btn.classList.remove('bg-gray-100', 'text-gray-600');
      activeCategory = btn.dataset.cat || '';
      renderProducts();
    });
  }

  // 3. Search inputs
  const searchInput = document.getElementById('searchInput');
  const searchInputMobile = document.getElementById('searchInputMobile');
  if (searchInput) {
    searchInput.addEventListener('input', renderProducts);
  }
  if (searchInputMobile) {
    searchInputMobile.addEventListener('input', (e) => {
      if (searchInput) searchInput.value = e.target.value;
      renderProducts();
    });
  }

  // 4. Quick order form submit
  const quickOrderForm = document.getElementById('quickOrderForm');
  if (quickOrderForm) {
    quickOrderForm.addEventListener('submit', function (e) {
      e.preventDefault();
      const areaEl = document.querySelector('input[name="deliveryArea"]:checked');
      const payload = {
        product_id: document.getElementById('orderProductId').value,
        name: document.getElementById('orderCustomerName').value,
        phone: document.getElementById('orderCustomerPhone').value,
        address: document.getElementById('orderCustomerAddress').value,
        area: areaEl ? areaEl.value : 'Inside Dhaka',
        quantity: parseInt(document.getElementById('orderQuantity').value, 10) || 1,
      };

      fetch('/order/create/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken') || ''
        },
        body: JSON.stringify(payload),
      })
        .then(r => r.json().then(data => ({ ok: r.ok, data })))
        .then(({ ok, data }) => {
          if (ok && data.success) {
            closeQuickOrderModal();
            showToast(data.message || 'ধন্যবাদ! আপনার অর্ডারটি সফলভাবে গ্রহণ করা হয়েছে।');
            quickOrderForm.reset();
          } else {
            showToast(data.message || 'অনুগ্রহ করে সব তথ্য সঠিকভাবে পূরণ করুন।');
          }
        })
        .catch(() => showToast('দুঃখিত, অর্ডারটি নেওয়া যায়নি। আবার চেষ্টা করুন।'));
    });
  }

  // 5. Cart checkout form submit (Home page cart drawer modal)
  const cartCheckoutForm = document.getElementById('checkoutForm');
  if (cartCheckoutForm && document.getElementById('coName')) {
    cartCheckoutForm.addEventListener('submit', function (e) {
      e.preventDefault();
      const areaEl = document.querySelector('input[name="coArea"]:checked');
      const payload = {
        name: document.getElementById('coName').value,
        phone: document.getElementById('coPhone').value,
        address: document.getElementById('coAddress').value,
        area: areaEl ? areaEl.value : 'Inside Dhaka',
        items: cart.map(i => ({ product_id: i.id, quantity: i.qty })),
      };

      fetch('/order/checkout/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken') || ''
        },
        body: JSON.stringify(payload),
      })
        .then(r => r.json().then(data => ({ ok: r.ok, data })))
        .then(({ ok, data }) => {
          if (ok && data.success) {
            closeCheckout();
            showToast(data.message || 'ধন্যবাদ! আপনার অর্ডারটি সফলভাবে গ্রহণ করা হয়েছে।');
            cart = [];
            updateCartUI();
            renderProducts();
          } else {
            showToast(data.message || 'অনুগ্রহ করে সব তথ্য সঠিকভাবে পূরণ করুন।');
          }
        })
        .catch(() => showToast('দুঃখিত, অর্ডারটি নেওয়া যায়নি। আবার চেষ্টা করুন।'));
    });
  }

  // 6. Dynamic Year
  const yearEl = document.getElementById('year');
  if (yearEl) yearEl.innerText = new Date().getFullYear();

  // 7. Initial renders
  renderProducts();
  updateCartUI();

  // 8. Single Page Module Initializer
  initSinglePage();
});

// ==========================================================================
// Single Landing Page Interactive Features (Gallery, Autoplay, Checkout)
// ==========================================================================
let currentSinglePageGalleryIndex = 0;
let singlePageGalleryImages = [];
let singlePageAutoScrollTimer = null;

function switchMainImage(src, btn, index) {
  const mainImg = document.getElementById('mainProductImage');
  if (mainImg) {
    mainImg.classList.add('opacity-30');
    setTimeout(() => {
      mainImg.src = src;
      mainImg.classList.remove('opacity-30');
    }, 140);
  }
  if (typeof index !== 'undefined') {
    currentSinglePageGalleryIndex = index;
  }
  // Update thumbnails active state
  document.querySelectorAll('.gallery-thumb').forEach(t => {
    t.classList.remove('border-brand-green', 'ring-2', 'ring-brand-green/30', 'scale-105', 'shadow-sm');
    t.classList.add('border-slate-200', 'opacity-60');
  });
  if (btn) {
    btn.classList.add('border-brand-green', 'ring-2', 'ring-brand-green/30', 'scale-105', 'shadow-sm');
    btn.classList.remove('border-slate-200', 'opacity-60');
    // Scroll only the thumbnail container horizontally, NEVER scroll the window/page
    const container = document.getElementById('galleryThumbnails') || btn.parentElement;
    if (container && typeof container.scrollTo === 'function') {
      const containerRect = container.getBoundingClientRect();
      const btnRect = btn.getBoundingClientRect();
      const scrollOffset = (btnRect.left - containerRect.left) + container.scrollLeft - (container.clientWidth / 2) + (btn.offsetWidth / 2);
      container.scrollTo({ left: Math.max(0, scrollOffset), behavior: 'smooth' });
    }
  }
  // Update dot indicators
  const dots = document.querySelectorAll('.gallery-dot');
  dots.forEach((dot, idx) => {
    if (idx === currentSinglePageGalleryIndex) {
      dot.classList.add('bg-brand-green', 'w-4');
      dot.classList.remove('bg-white/70', 'w-2');
    } else {
      dot.classList.remove('bg-brand-green', 'w-4');
      dot.classList.add('bg-white/70', 'w-2');
    }
  });
}

function navigateGallery(direction) {
  if (!singlePageGalleryImages.length) {
    const thumbs = document.querySelectorAll('.gallery-thumb img');
    if (thumbs.length) {
      singlePageGalleryImages = Array.from(thumbs).map(img => img.src);
    }
  }
  if (!singlePageGalleryImages.length) return;
  currentSinglePageGalleryIndex = (currentSinglePageGalleryIndex + direction + singlePageGalleryImages.length) % singlePageGalleryImages.length;
  const thumbs = document.querySelectorAll('.gallery-thumb');
  const targetThumb = thumbs[currentSinglePageGalleryIndex];
  switchMainImage(singlePageGalleryImages[currentSinglePageGalleryIndex], targetThumb, currentSinglePageGalleryIndex);
}

function startAutoScroll() {
  const galleryBox = document.getElementById('heroGalleryBox');
  if (!galleryBox) return;
  const autoScrollEnabled = galleryBox.dataset.autoscroll !== 'false';
  const intervalSeconds = parseFloat(galleryBox.dataset.interval) || 3;
  if (!autoScrollEnabled) return;

  if (!singlePageGalleryImages.length) {
    const thumbs = document.querySelectorAll('.gallery-thumb img');
    if (thumbs.length) {
      singlePageGalleryImages = Array.from(thumbs).map(img => img.src);
    }
  }
  if (singlePageGalleryImages.length <= 1) return;

  stopAutoScroll();
  singlePageAutoScrollTimer = setInterval(() => {
    navigateGallery(1);
  }, intervalSeconds * 1000);
}

function stopAutoScroll() {
  if (singlePageAutoScrollTimer) {
    clearInterval(singlePageAutoScrollTimer);
    singlePageAutoScrollTimer = null;
  }
}

function calculateSinglePageTotal() {
  const bundleRadios = document.querySelectorAll('input[name="bundle_id"]');
  let bundlePrice = 0;
  let bundleName = "";

  bundleRadios.forEach(radio => {
    const label = radio.closest('.bundle-label') || radio.closest('label');
    const dot = label ? label.querySelector('.radio-dot') : null;
    const circle = label ? label.querySelector('.radio-circle') : null;

    if (radio.checked) {
      bundlePrice = parseFloat(radio.getAttribute('data-price') || 0);
      bundleName = radio.getAttribute('data-name') || "";
      if (dot) dot.classList.remove('hidden');
      if (circle) {
        circle.classList.add('border-brand-green');
        circle.classList.remove('border-slate-300');
      }
      if (label) {
        label.classList.add('is-selected', 'border-brand-green', 'bg-emerald-50/70', 'shadow-sm');
        label.classList.remove('border-slate-200');
      }
    } else {
      if (dot) dot.classList.add('hidden');
      if (circle) {
        circle.classList.remove('border-brand-green');
        circle.classList.add('border-slate-300');
      }
      if (label) {
        label.classList.remove('is-selected', 'border-brand-green', 'bg-emerald-50/70', 'shadow-sm');
        label.classList.add('border-slate-200');
      }
    }
  });

  if (bundlePrice === 0 && bundleRadios.length > 0) {
    bundlePrice = parseFloat(bundleRadios[0].getAttribute('data-price') || 0);
    bundleName = bundleRadios[0].getAttribute('data-name') || "";
  }

  const deliveryRadios = document.querySelectorAll('input[name="delivery_area"]');
  let deliveryCharge = 60;

  deliveryRadios.forEach(radio => {
    const label = radio.closest('.delivery-label') || radio.closest('label');
    if (radio.checked) {
      deliveryCharge = parseFloat(radio.getAttribute('data-charge') || 0);
      if (label) {
        label.classList.add('is-selected', 'border-brand-green', 'bg-emerald-50/70', 'shadow-sm');
        label.classList.remove('border-slate-200');
      }
    } else {
      if (label) {
        label.classList.remove('is-selected', 'border-brand-green', 'bg-emerald-50/70', 'shadow-sm');
        label.classList.add('border-slate-200');
      }
    }
  });

  const total = bundlePrice + deliveryCharge;

  const nameEl = document.getElementById('bundleNameDisplay');
  const priceEl = document.getElementById('bundlePriceDisplay');
  const chargeEl = document.getElementById('deliveryChargeDisplay');
  const totalEl = document.getElementById('totalPriceDisplay');

  if (nameEl && bundleName) nameEl.innerText = bundleName;
  if (priceEl) priceEl.innerText = '৳ ' + Math.round(bundlePrice);
  if (chargeEl) chargeEl.innerText = '৳ ' + Math.round(deliveryCharge);
  if (totalEl) totalEl.innerText = '৳ ' + Math.round(total);
}

function initSinglePage() {
  const galleryBox = document.getElementById('heroGalleryBox');
  const singleOrderForm = document.getElementById('singlePageOrderForm') || document.getElementById('checkoutForm');
  const bundleContainer = document.getElementById('bundleOptionsContainer');
  if (!galleryBox && !singleOrderForm && !bundleContainer) return;

  // 1. Collect gallery images from DOM
  const thumbImgs = document.querySelectorAll('.gallery-thumb img');
  if (thumbImgs.length) {
    singlePageGalleryImages = Array.from(thumbImgs).map(img => img.src);
  } else {
    const mainImg = document.getElementById('mainProductImage');
    if (mainImg && mainImg.src) {
      singlePageGalleryImages = [mainImg.src];
    }
  }

  // 2. Setup hover & touch auto-scroll listeners + pause when off-screen
  if (galleryBox) {
    galleryBox.addEventListener('mouseenter', stopAutoScroll);
    galleryBox.addEventListener('mouseleave', startAutoScroll);
    galleryBox.addEventListener('touchstart', stopAutoScroll, { passive: true });
    galleryBox.addEventListener('touchend', startAutoScroll, { passive: true });

    if ('IntersectionObserver' in window) {
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            startAutoScroll();
          } else {
            stopAutoScroll();
          }
        });
      }, { threshold: 0.1 });
      observer.observe(galleryBox);
    } else {
      startAutoScroll();
    }
  }

  // 3. Setup package click & change listeners
  document.querySelectorAll('.bundle-label').forEach(label => {
    label.addEventListener('click', function (e) {
      const radio = this.querySelector('input[name="bundle_id"]');
      if (radio) {
        radio.checked = true;
        calculateSinglePageTotal();
      }
    });
  });

  document.querySelectorAll('input[name="bundle_id"]').forEach(input => {
    input.addEventListener('change', calculateSinglePageTotal);
    input.addEventListener('input', calculateSinglePageTotal);
  });

  // 4. Setup delivery area click & change listeners
  document.querySelectorAll('.delivery-label').forEach(label => {
    label.addEventListener('click', function () {
      const radio = this.querySelector('input[name="delivery_area"]');
      if (radio) {
        radio.checked = true;
        calculateSinglePageTotal();
      }
    });
  });

  document.querySelectorAll('input[name="delivery_area"]').forEach(input => {
    input.addEventListener('change', calculateSinglePageTotal);
    input.addEventListener('input', calculateSinglePageTotal);
  });

  // 5. Initial calculation
  calculateSinglePageTotal();

  // 6. Single page form submit feedback
  if (singleOrderForm) {
    singleOrderForm.addEventListener('submit', function () {
      const btn = document.getElementById('submitBtn');
      if (btn) {
        btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> প্রসেসিং হচ্ছে...';
        btn.classList.add('opacity-75');
      }
    });
  }
}

// Global Aliases so template inline handlers (onclick, onchange) work in all contexts
window.calculateTotal = calculateSinglePageTotal;
window.calculateSinglePageTotal = calculateSinglePageTotal;
window.switchMainImage = switchMainImage;
window.navigateGallery = navigateGallery;
window.startAutoScroll = startAutoScroll;
window.stopAutoScroll = stopAutoScroll;
window.initSinglePage = initSinglePage;

// In case DOM is already parsed when main.js executes
if (document.readyState === 'complete' || document.readyState === 'interactive') {
  initSinglePage();
}


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
          'X-CSRFToken': csrftoken
        },
        body: JSON.stringify(payload),
      })
        .then(r => r.json())
        .then(data => {
          closeQuickOrderModal();
          showToast(data.message || 'ধন্যবাদ! আপনার অর্ডারটি সফলভাবে গ্রহণ করা হয়েছে।');
          quickOrderForm.reset();
        })
        .catch(() => showToast('দুঃখিত, অর্ডারটি নেওয়া যায়নি। আবার চেষ্টা করুন।'));
    });
  }

  // 5. Cart checkout form submit
  const checkoutForm = document.getElementById('checkoutForm');
  if (checkoutForm) {
    checkoutForm.addEventListener('submit', function (e) {
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
          'X-CSRFToken': csrftoken
        },
        body: JSON.stringify(payload),
      })
        .then(r => r.json())
        .then(data => {
          closeCheckout();
          showToast(data.message || 'ধন্যবাদ! আপনার অর্ডারটি সফলভাবে গ্রহণ করা হয়েছে।');
          cart = [];
          updateCartUI();
          renderProducts();
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
});

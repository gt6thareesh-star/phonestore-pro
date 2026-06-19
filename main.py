import os
from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

PRODUCTS = [
    { "id": 1, "name": "iPhone 15 Pro Max", "brand": "Apple", "price": 1199, "rating": 4.9, "badge": "HOT", "storage": "256GB", "specs": "A17 Pro Chip, Titanium Body, 5x Telephoto Camera" },
    { "id": 2, "name": "Samsung Galaxy S24 Ultra", "brand": "Samsung", "price": 1299, "rating": 4.8, "badge": "NEW", "storage": "512GB", "specs": "Snapdragon 8 Gen 3, S-Pen Included, 200MP Camera" },
    { "id": 3, "name": "Google Pixel 8 Pro", "brand": "Google", "price": 999, "rating": 4.7, "badge": "SALE", "storage": "128GB", "specs": "Tensor G3, Magic Eraser, Best-in-class AI Camera" },
    { "id": 4, "name": "OnePlus 12", "brand": "OnePlus", "price": 799, "rating": 4.6, "badge": "HOT", "storage": "256GB", "specs": "100W Fast Charging, Hasselblad Camera, Fluid AMOLED" },
    { "id": 5, "name": "Xiaomi 14 Ultra", "brand": "Xiaomi", "price": 1099, "rating": 4.8, "badge": "NEW", "storage": "512GB", "specs": "Leica Optic Lenses, 1-inch Main Sensor, Premium Ceramic" },
    { "id": 6, "name": "Sony Xperia 1 VI", "brand": "Sony", "price": 1399, "rating": 4.5, "badge": "NEW", "storage": "256GB", "specs": "4K OLED 120Hz Screen, Dedicated Shutter Key, Jack 3.5mm" },
    { "id": 7, "name": "Motorola Edge 50 Ultra", "brand": "Motorola", "price": 849, "rating": 4.4, "badge": "SALE", "storage": "512GB", "specs": "Real Wooden Back Panel, Pantone Validated Screen" },
    { "id": 8, "name": "Asus ROG Phone 8 Pro", "brand": "Asus", "price": 1199, "rating": 4.9, "badge": "HOT", "storage": "512GB", "specs": "AeroActive Cooler, AniMe Vision LED Matrix, Game Genie" },
    { "id": 9, "name": "iPhone 15 Plus", "brand": "Apple", "price": 899, "rating": 4.6, "badge": "NONE", "storage": "128GB", "specs": "Dynamic Island, A16 Bionic, Longest Battery Life" },
    { "id": 10, "name": "Samsung Galaxy Z Fold 5", "brand": "Samsung", "price": 1599, "rating": 4.7, "badge": "HOT", "storage": "512GB", "specs": "7.6-inch Foldable Display, Flex Mode, Multi-window Pro" },
    { "id": 11, "name": "Google Pixel 8a", "brand": "Google", "price": 499, "rating": 4.5, "badge": "NEW", "storage": "128GB", "specs": "Affordable Flagship AI, Smooth 120Hz, Long Support" },
    { "id": 12, "name": "Nothing Phone (2)", "brand": "OnePlus", "price": 649, "rating": 4.6, "badge": "SALE", "storage": "256GB", "specs": "Unique Glyph LED Interface, Transparent Back, Nothing OS" },
    { "id": 13, "name": "Xiaomi Redmi Note 13 Pro+", "brand": "Xiaomi", "price": 399, "rating": 4.4, "badge": "SALE", "storage": "256GB", "specs": "200MP OIS Camera, 120W Charging, Curved AMOLED" },
    { "id": 14, "name": "Sony Xperia 5 V", "brand": "Sony", "price": 899, "rating": 4.3, "badge": "NONE", "storage": "128GB", "specs": "Compact Premium Build, High Fidelity Sound, Exmor T Sensor" },
    { "id": 15, "name": "Motorola Razr 50 Ultra", "brand": "Motorola", "price": 999, "rating": 4.7, "badge": "NEW", "storage": "256GB", "specs": "Largest Cover Display, Retro Pocket Styling, Vegan Leather" },
    { "id": 16, "name": "Asus Zenfone 11 Ultra", "brand": "Asus", "price": 899, "rating": 4.5, "badge": "NONE", "storage": "256GB", "specs": "Gimbal Stabilizer 3.0, AI Noise Cancellation, Minimalist Look" },
    { "id": 17, "name": "iPhone 13 Mini", "brand": "Apple", "price": 599, "rating": 4.5, "badge": "NONE", "storage": "128GB", "specs": "Pocket Size Powerhouse, Super Retina XDR, Light Weight" },
    { "id": 18, "name": "Samsung Galaxy S24 FE", "brand": "Samsung", "price": 649, "rating": 4.4, "badge": "NEW", "storage": "128GB", "specs": "Exynos 2400e, ProVisual Engine, Epic Nightography" },
    { "id": 19, "name": "OnePlus Nord 4", "brand": "OnePlus", "price": 429, "rating": 4.3, "badge": "SALE", "storage": "128GB", "specs": "All-Metal Slim Design, Ultra-Fast OxygenOS, 5500mAh Battery" },
    { "id": 20, "name": "Poco F6 Pro", "brand": "Xiaomi", "price": 549, "rating": 4.6, "badge": "HOT", "storage": "512GB", "specs": "WQHD+ Flow AMOLED, Snapdragon 8 Gen 2, WildBoost Opt 3.0" }
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PhoneStore Pro - Premium Tech Shop</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@400;500;700&family=Syne:wght@700;800&display=swap');
        body { font-family: 'DM Sans', sans-serif; background-color: #0B0F19; color: #F3F4F6; }
        h1, h2, h3, .font-syne { font-family: 'Syne', sans-serif; }
        .font-mono { font-family: 'DM Mono', sans-serif; }
        .glow-box:hover { box-shadow: 0 0 20px rgba(37, 99, 235, 0.25); border-color: rgba(37, 99, 235, 0.4); }
        .glow-text { text-shadow: 0 0 10px rgba(37, 99, 235, 0.6); }
    </style>
</head>
<body class="relative min-h-screen overflow-x-hidden">
    <div id="toast-container" class="fixed top-5 right-5 z-50 flex flex-col gap-2"></div>
    <nav class="sticky top-0 bg-[#0F172A]/80 backdrop-blur-md border-b border-gray-800 z-40 px-6 py-4 flex justify-between items-center">
        <h1 class="text-2xl font-extrabold tracking-tight text-white flex items-center gap-2">
            <span class="text-blue-500 glow-text">📱</span> PHONE<span class="text-blue-500">STORE</span>
        </h1>
        <div class="relative w-full max-w-md mx-4">
            <input type="text" id="search-input" oninput="applyFilters()" placeholder="Search by name or brand..." class="w-full bg-[#1E293B] border border-gray-700 rounded-xl px-4 py-2 pl-10 text-sm focus:outline-none focus:border-blue-500 transition text-gray-200">
            <span class="absolute left-3 top-2.5">🔍</span>
        </div>
        <button onclick="toggleCart(true)" class="relative bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-xl text-sm font-semibold flex items-center gap-2 transition">
            🛒 Cart <span id="cart-badge" class="bg-white text-blue-600 px-2 py-0.5 rounded-full text-xs font-bold">0</span>
        </button>
    </nav>
    <div class="bg-[#0B0F19] px-6 py-3 flex gap-2 overflow-x-auto border-b border-gray-900 scrollbar-none">
        <button onclick="filterByBrand('All')" class="brand-chip bg-blue-600 text-white px-4 py-1.5 rounded-full text-xs font-medium transition whitespace-nowrap">All Brands</button>
        <button onclick="filterByBrand('Apple')" class="brand-chip bg-[#1E293B] text-gray-300 px-4 py-1.5 rounded-full text-xs font-medium transition whitespace-nowrap">Apple</button>
        <button onclick="filterByBrand('Samsung')" class="brand-chip bg-[#1E293B] text-gray-300 px-4 py-1.5 rounded-full text-xs font-medium transition whitespace-nowrap">Samsung</button>
        <button onclick="filterByBrand('Google')" class="brand-chip bg-[#1E293B] text-gray-300 px-4 py-1.5 rounded-full text-xs font-medium transition whitespace-nowrap">Google</button>
        <button onclick="filterByBrand('OnePlus')" class="brand-chip bg-[#1E293B] text-gray-300 px-4 py-1.5 rounded-full text-xs font-medium transition whitespace-nowrap">OnePlus</button>
        <button onclick="filterByBrand('Xiaomi')" class="brand-chip bg-[#1E293B] text-gray-300 px-4 py-1.5 rounded-full text-xs font-medium transition whitespace-nowrap">Xiaomi</button>
        <button onclick="filterByBrand('Sony')" class="brand-chip bg-[#1E293B] text-gray-300 px-4 py-1.5 rounded-full text-xs font-medium transition whitespace-nowrap">Sony</button>
        <button onclick="filterByBrand('Motorola')" class="brand-chip bg-[#1E293B] text-gray-300 px-4 py-1.5 rounded-full text-xs font-medium transition whitespace-nowrap">Motorola</button>
        <button onclick="filterByBrand('Asus')" class="brand-chip bg-[#1E293B] text-gray-300 px-4 py-1.5 rounded-full text-xs font-medium transition whitespace-nowrap">Asus</button>
    </div>
    <div class="flex flex-col lg:flex-row p-6 gap-6">
        <aside class="w-full lg:w-64 bg-[#0F172A] p-6 rounded-2xl border border-gray-800 space-y-6 h-fit">
            <div>
                <h3 class="text-xs font-bold text-gray-400 uppercase tracking-wider mb-3">Sort By</h3>
                <select id="sort-select" onchange="applyFilters()" class="w-full bg-[#1E293B] border border-gray-700 rounded-xl p-2.5 text-sm text-gray-200 focus:outline-none">
                    <option value="featured">Featured</option>
                    <option value="low-high">Price: Low to High</option>
                    <option value="high-low">Price: High to Low</option>
                    <option value="top-rated">Top Rated</option>
                </select>
            </div>
            <div>
                <h3 class="text-xs font-bold text-gray-400 uppercase tracking-wider mb-3">Price Range ($)</h3>
                <input type="range" id="price-slider" min="200" max="1600" value="1600" oninput="updatePriceLabel(this.value)" class="w-full accent-blue-500">
                <div class="flex justify-between text-xs text-gray-400 mt-1 font-mono">
                    <span>$200</span><span id="price-label" class="text-blue-400 font-bold">$1600</span>
                </div>
            </div>
        </aside>
        <main class="flex-1">
            <div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-6" id="grid-container"></div>
        </main>
    </div>
    <div id="cart-drawer" class="fixed inset-y-0 right-0 w-full max-w-md bg-[#0F172A] border-l border-gray-800 shadow-2xl z-50 transform translate-x-full transition-transform duration-300 flex flex-col">
        <div class="p-6 border-b border-gray-800 flex justify-between items-center bg-[#1E293B]/50">
            <h2 class="text-lg font-bold text-white">Your Tech Cart</h2>
            <button onclick="toggleCart(false)" class="text-gray-400 hover:text-white text-xl">&times;</button>
        </div>
        <div class="flex-1 overflow-y-auto p-6 space-y-4" id="cart-items-container"></div>
        <div class="p-6 border-t border-gray-800 bg-[#1E293B]/30 space-y-4">
            <div class="flex justify-between items-center text-sm">
                <span class="text-gray-400">Subtotal:</span>
                <span id="cart-subtotal" class="text-xl font-bold text-blue-400 font-mono">$0.00</span>
            </div>
            <button onclick="showToast('Secure checkout processed successfully!')" class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold p-3 rounded-xl transition text-sm">Secure Checkout</button>
        </div>
    </div>
    <div id="details-modal" class="fixed inset-0 bg-black/70 backdrop-blur-sm hidden items-center justify-center z-50 p-4">
        <div class="bg-[#0F172A] border border-gray-800 rounded-2xl max-w-lg w-full overflow-hidden shadow-2xl relative">
            <button onclick="closeDetailsModal()" class="absolute top-4 right-4 text-gray-400 hover:text-white text-2xl z-10">&times;</button>
            <div class="p-6 space-y-4" id="modal-content-area"></div>
        </div>
    </div>
    <script>
        let products = [];
        let cart = [];
        let selectedBrand = "All";

        document.addEventListener("DOMContentLoaded", () => {
            fetch('/api/products')
                .then(res => res.json())
                .then(data => {
                    products = data;
                    renderGrid(products);
                });
        });

        function showToast(message) {
            const container = document.getElementById("toast-container");
            const toast = document.createElement("div");
            toast.className = "bg-[#1E293B] border border-blue-500/50 text-white px-4 py-3 rounded-xl shadow-lg text-xs font-mono";
            toast.innerText = `⚡ ${message}`;
            container.appendChild(toast);
            setTimeout(() => toast.remove(), 2500);
        }

        function renderGrid(dataList) {
            const container = document.getElementById("grid-container");
            if(dataList.length === 0) {
                container.innerHTML = `<div class="text-gray-500 col-span-full text-center py-10">No premium devices match your filters.</div>`;
                return;
            }
            container.innerHTML = dataList.map(p => `
                <div class="bg-[#0F172A] border border-gray-800 rounded-2xl p-5 transition-all duration-300 hover:-translate-y-2 glow-box flex flex-col justify-between group">
                    <div>
                        <div class="flex justify-between items-start mb-4">
                            ${p.badge !== 'NONE' ? `<span class="bg-blue-600/10 text-blue-400 border border-blue-500/30 text-[10px] font-bold px-2 py-0.5 rounded-md font-mono">${p.badge}</span>` : '<span></span>'}
                            <button onclick="showToast('Added to Wishlist!')" class="text-gray-500 hover:text-red-500">❤️</button>
                        </div>
                        <div onclick="openDetailsModal(${p.id})" class="cursor-pointer">
                            <span class="text-xs text-blue-500 font-semibold font-mono">${p.brand}</span>
                            <h3 class="text-lg font-bold text-white group-hover:text-blue-400 mt-1 transition">${p.name}</h3>
                            <div class="text-xs text-amber-500 mt-1">⭐ ${p.rating} / 5.0</div>
                        </div>
                    </div>
                    <div class="mt-6 flex justify-between items-center border-t border-gray-900 pt-4">
                        <span class="text-xl font-bold text-white font-mono">$${p.price}</span>
                        <button onclick="addToCart(${p.id})" class="bg-[#1E293B] hover:bg-blue-600 border border-gray-700 text-gray-200 hover:text-white px-3 py-2 rounded-xl text-xs transition">Add +</button>
                    </div>
                </div>
            `).join('');
        }

        function filterByBrand(brand) {
            selectedBrand = brand;
            document.querySelectorAll(".brand-chip").forEach(btn => {
                btn.classList.replace("bg-blue-600", "bg-[#1E293B]");
                btn.classList.replace("text-white", "text-gray-300");
            });
            event.target.classList.replace("bg-[#1E293B]", "bg-blue-600");
            event.target.classList.replace("text-gray-300", "text-white");
            applyFilters();
        }

        function updatePriceLabel(val) {
            document.getElementById("price-label").innerText = `$${val}`;
            applyFilters();
        }

        function applyFilters() {
            const searchVal = document.getElementById("search-input").value.toLowerCase();
            const maxPrice = parseInt(document.getElementById("price-slider").value);
            const sortBy = document.getElementById("sort-select").value;

            let filtered = products.filter(p => {
                const matchesSearch = p.name.toLowerCase().includes(searchVal) || p.brand.toLowerCase().includes(searchVal);
                const matchesBrand = selectedBrand === "All" || p.brand === selectedBrand;
                const matchesPrice = p.price <= maxPrice;
                return matchesSearch && matchesBrand && matchesPrice;
            });

            if (sortBy === "low-high") filtered.sort((a,b) => a.price - b.price);
            else if (sortBy === "high-low") filtered.sort((a,b) => b.price - a.price);
            else if (sortBy === "top-rated") filtered.sort((a,b) => b.rating - a.rating);

            renderGrid(filtered);
        }

        function toggleCart(open) {
            document.getElementById("cart-drawer").style.transform = open ? "translateX(0)" : "translateX(100%)";
        }

        function addToCart(id) {
            const product = products.find(p => p.id === id);
            const exist = cart.find(item => item.id === id);
            if (exist) { exist.qty++; } else { cart.push({ ...product, qty: 1 }); }
            showToast(`${product.name} added to cart!`);
            updateCartUI();
        }

        function changeQty(id, delta) {
            const item = cart.find(i => i.id === id);
            if (!item) return;
            item.qty += delta;
            if (item.qty <= 0) cart = cart.filter(i => i.id !== id);
            updateCartUI();
        }

        function updateCartUI() {
            const container = document.getElementById("cart-items-container");
            document.getElementById("cart-badge").innerText = cart.reduce((s, i) => s + i.qty, 0);
            
            container.innerHTML = cart.map(item => `
                <div class="flex justify-between items-center bg-[#1E293B]/60 p-4 rounded-xl border border-gray-800">
                    <div>
                        <h4 class="text-sm font-bold text-white">${item.name}</h4>
                        <span class="text-xs text-blue-400 font-mono">$${item.price}</span>
                    </div>
                    <div class="flex items-center gap-2">
                        <button onclick="changeQty(${item.id}, -1)" class="bg-[#0F172A] border border-gray-700 px-2 py-0.5 rounded text-xs text-white">-</button>
                        <span class="text-sm font-mono text-white">${item.qty}</span>
                        <button onclick="changeQty(${item.id}, 1)" class="bg-[#0F172A] border border-gray-700 px-2 py-0.5 rounded text-xs text-white">+</button>
                    </div>
                </div>
            `).join('');

            const subtotal = cart.reduce((sum, item) => sum + (item.price * item.qty), 0);
            document.getElementById("cart-subtotal").innerText = `$${subtotal.toFixed(2)}`;
        }

        function openDetailsModal(id) {
            const p = products.find(item => item.id === id);
            const area = document.getElementById("modal-content-area");
            area.innerHTML = `
                <div class="border-b border-gray-800 pb-3">
                    <span class="text-xs font-mono text-blue-500 uppercase">${p.brand} Flagship Series</span>
                    <h2 class="text-2xl font-bold text-white mt-1">${p.name}</h2>
                </div>
                <div class="space-y-3 pt-2 text-sm">
                    <div class="flex justify-between font-mono bg-[#1E293B]/40 p-2.5 rounded-xl"><span class="text-gray-400">Retail Price:</span> <span class="text-emerald-400 font-bold">$${p.price}</span></div>
                    <div class="flex justify-between font-mono bg-[#1E293B]/40 p-2.5 rounded-xl"><span class="text-gray-400">Storage Config:</span> <span class="text-white">${p.storage}</span></div>
                    <div class="flex justify-between font-mono bg-[#1E293B]/40 p-2.5 rounded-xl"><span class="text-gray-400">Global Score:</span> <span class="text-amber-400">⭐ ${p.rating} / 5.0</span></div>
                    <p class="text-gray-400 text-xs font-mono bg-[#1E293B]/20 p-3 rounded-xl leading-relaxed">${p.specs}</p>
                </div>
                <button onclick="addToCart(${p.id}); closeDetailsModal();" class="w-full bg-blue-600 hover:bg-blue-700 text-white p-3 rounded-xl font-bold transition text-xs mt-4">ADD TO CART</button>
            `;
            document.getElementById("details-modal").style.display = "flex";
        }

        function closeDetailsModal() { document.getElementById("details-modal").style.display = "none"; }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/products')
def get_products():
    return jsonify(PRODUCTS)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

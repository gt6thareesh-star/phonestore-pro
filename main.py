import os
from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# താൽക്കാലികമായി ഡാറ്റ സൂക്ഷിക്കാൻ (Sample Product Data)
products = [
    {"id": 1, "name": "Bleu de Chanel", "category": "Perfume", "stock": 15, "price": 120},
    {"id": 2, "name": "Sauvage Dior", "category": "Perfume", "stock": 8, "price": 115},
    {"id": 3, "name": "Creed Aventus", "category": "Luxury Perfume", "stock": 5, "price": 250},
    {"id": 4, "name": "Acqua Di Gio", "category": "Perfume", "stock": 22, "price": 95},
    {"id": 5, "name": "Tom Ford Oud Wood", "category": "Luxury Perfume", "stock": 3, "price": 180}
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fragorium Inventory Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 font-sans antialiased">

    <div class="max-w-6xl mx-auto p-4 md:p-8">
        <div class="flex items-center space-x-3 mb-8">
            <span class="text-3xl">📊</span>
            <h1 class="text-2xl md:text-3xl font-bold text-gray-800">Fragorium Inventory Dashboard</h1>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
                <p class="text-sm font-medium text-gray-500 uppercase">Total Items In Stock</p>
                <p class="text-3xl font-bold text-blue-600 mt-2">{{ total_items }}</p>
            </div>
            <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
                <p class="text-sm font-medium text-gray-500 uppercase">Unique Products</p>
                <p class="text-3xl font-bold text-indigo-600 mt-2">{{ unique_products }}</p>
            </div>
            <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
                <p class="text-sm font-medium text-gray-500 uppercase">Low Stock Alerts</p>
                <p class="text-3xl font-bold text-red-600 mt-2">{{ low_stock_count }}</p>
            </div>
        </div>

        <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-200 mb-8">
            <h2 class="text-lg font-bold text-gray-800 mb-4">➕ Add New Product</h2>
            <form action="/add" method="POST" class="grid grid-cols-1 md:grid-cols-4 gap-4">
                <input type="text" name="name" placeholder="Product Name" required class="border p-2 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
                <input type="text" name="category" placeholder="Category (e.g. Perfume)" required class="border p-2 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
                <input type="number" name="price" placeholder="Price ($)" required class="border p-2 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
                <input type="number" name="stock" placeholder="Initial Stock" required class="border p-2 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
                <button type="submit" class="md:col-span-4 bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 rounded-lg transition text-sm">Add Product to Inventory</button>
            </form>
        </div>

        <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
            <div class="overflow-x-auto">
                <table class="w-full text-left border-collapse">
                    <thead>
                        <tr class="bg-gray-800 text-white text-sm">
                            <th class="p-4 font-semibold">ID</th>
                            <th class="p-4 font-semibold">Product Name</th>
                            <th class="p-4 font-semibold">Category</th>
                            <th class="p-4 font-semibold">Price</th>
                            <th class="p-4 font-semibold">Stock Qty</th>
                            <th class="p-4 font-semibold">Status</th>
                            <th class="p-4 font-semibold text-center">Actions</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-200 text-sm text-gray-700">
                        {% for prod in products %}
                        <tr class="hover:bg-gray-50">
                            <td class="p-4 font-mono text-gray-500">#{{ prod.id }}</td>
                            <td class="p-4 font-bold text-gray-900">{{ prod.name }}</td>
                            <td class="p-4"><span class="bg-gray-100 px-2 py-1 rounded text-xs">{{ prod.category }}</span></td>
                            <td class="p-4 font-medium">${{ prod.price }}</td>
                            <td class="p-4 font-bold">{{ prod.stock }}</td>
                            <td class="p-4">
                                {% if prod.stock <= 5 %}
                                <span class="bg-red-100 text-red-800 px-2.5 py-0.5 rounded-full text-xs font-semibold">Low Stock</span>
                                {% else %}
                                <span class="bg-green-100 text-green-800 px-2.5 py-0.5 rounded-full text-xs font-semibold">In Stock</span>
                                {% endif %}
                            </td>
                            <td class="p-4 text-center space-x-2">
                                <a href="/stock_in/{{ prod.id }}" class="bg-green-500 hover:bg-green-600 text-white px-3 py-1 rounded font-bold text-xs transition">+ Stock In</a>
                                <a href="/stock_out/{{ prod.id }}" class="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded font-bold text-xs transition">- Stock Out</a>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>

</body>
</html>
"""

@app.route('/')
def dashboard():
    total_items = sum(p['stock'] for p in products)
    unique_products = len(products)
    low_stock_count = sum(1 for p in products if p['stock'] <= 5)
    
    return render_template_string(
        HTML_TEMPLATE, 
        products=products, 
        total_items=total_items, 
        unique_products=unique_products, 
        low_stock_count=low_stock_count
    )

@app.route('/add', methods=['POST'])
def add_product():
    if request.method == 'POST':
        new_id = max([p['id'] for p in products]) + 1 if products else 1
        new_prod = {
            "id": new_id,
            "name": request.form['name'],
            "category": request.form['category'],
            "price": int(request.form['price']),
            "stock": int(request.form['stock'])
        }
        products.append(new_prod)
    return redirect(url_for('dashboard'))

@app.route('/stock_in/<int:product_id>')
def stock_in(product_id):
    for p in products:
        if p['id'] == product_id:
            p['stock'] += 1
            break
    return redirect(url_for('dashboard'))

@app.route('/stock_out/<int:product_id>')
def stock_out(product_id):
    for p in products:
        if p['id'] == product_id and p['stock'] > 0:
            p['stock'] -= 1
            break
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)


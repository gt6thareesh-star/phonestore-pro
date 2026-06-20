import os
from flask import Flask, render_template_string, request, redirect

url_counts = {}

app = Flask(__name__)

# Sample Product Data (For Fragorium Inventory Bot Testing)
products = [
    {"id": 1, "name": "Bleu de Chanel", "category": "Perfume", "stock": 15, "price": 120},
    {"id": 2, "name": "Sauvage Dior", "category": "Perfume", "stock": 8, "price": 115},
    {"id": 3, "name": "Creed Aventus", "category": "Luxury Perfume", "stock": 5, "price": 250},
    {"id": 4, "name": "Acqua Di Gio", "category": "Perfume", "stock": 22, "price": 95},
    {"id": 5, "name": "Tom Ford Oud Wood", "category": "Luxury Perfume", "stock": 3, "price": 180}
]

# HTML Template Embedded Directly
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fragorium Inventory Control Pro</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f6f9; margin: 0; padding: 20px; }
        .container { max-width: 900px; margin: 0 auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        h1 { color: #1e293b; border-bottom: 2px solid #e2e8f0; padding-bottom: 10px; margin-bottom: 20px; text-align: center; }
        .stats-box { display: flex; justify-content: space-between; margin-bottom: 25px; background: #f8fafc; padding: 15px; border-radius: 8px; border: 1px solid #e2e8f0; }
        .stat-item { text-align: center; flex: 1; font-weight: bold; color: #475569; }
        .stat-item span { display: block; font-size: 24px; color: #2563eb; }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; }
        th, td { padding: 14px; text-align: left; border-bottom: 1px solid #e2e8f0; }
        th { background-color: #0f172a; color: white; border-top-left-radius: 4px; border-top-right-radius: 4px; }
        tr:hover { background-color: #f8fafc; }
        .badge { padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: bold; }
        .badge-instock { background-color: #dcfce7; color: #15803d; }
        .badge-low { background-color: #fee2e2; color: #b91c1c; }
        .btn { background-color: #2563eb; color: white; padding: 6px 12px; border: none; border-radius: 6px; cursor: pointer; text-decoration: none; font-size: 13px; }
        .btn:hover { background-color: #1d4ed8; }
        .footer { margin-top: 30px; text-align: center; font-size: 12px; color: #94a3b8; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Fragorium Inventory Dashboard</h1>
        
        <div class="stats-box">
            <div class="stat-item">Total Items<span>{{ total_stock }}</span></div>
            <div class="stat-item">Unique Products<span>{{ products|length }}</span></div>
            <div class="stat-item">Low Stock Alert<span>{{ low_stock_count }}</span></div>
        </div>

        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Product Name</th>
                    <th>Category</th>
                    <th>Price ($)</th>
                    <th>Stock Qty</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                {% for item in products %}
                <tr>
                    <td>#{{ item.id }}</td>
                    <td><strong>{{ item.name }}</strong></td>
                    <td>{{ item.category }}</td>
                    <td>${{ item.price }}</td>
                    <td>{{ item.stock }}</td>
                    <td>
                        {% if item.stock > 5 %}
                        <span class="badge badge-instock">In Stock</span>
                        {% else %}
                        <span class="badge badge-low">Low Stock</span>
                        {% endif %}
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        
        <div class="footer">
            Fragorium Store Management System v1.0 • Connected via GitHub
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    total_stock = sum(item['stock'] for item in products)
    low_stock_count = sum(1 for item in products if item['stock'] <= 5)
    return render_template_string(HTML_TEMPLATE, products=products, total_stock=total_stock, low_stock_count=low_stock_count)

if __name__ == '__main__':
    # Bind to PORT specified by deployment platforms, default to 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

import os
import csv
from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)
CSV_FILE = 'inventory.csv'

def load_inventory():
    if not os.path.exists(CSV_FILE):
        return []
    
    entries = []
    with open(CSV_FILE, mode='r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # വരിയിൽ ഡാറ്റ ഉണ്ടെന്ന് ഉറപ്പുവരുത്തുന്നു
            if row.get("Sl No") and not row.get("Sl No").startswith('...'):
                entries.append({
                    "sl_no": row.get("Sl No", "").strip(),
                    "date": row.get("Date", "").strip(),
                    "item": row.get("Item Description", "").strip(),
                    "qty": row.get("Quantity", "").strip(),
                    "issued_to": row.get("Issued To", "").strip()
                })
    return entries

def save_entry(sl_no, date, item, qty, issued_to):
    file_exists = os.path.exists(CSV_FILE)
    with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Sl No", "Date", "Item Description", "Quantity", "Issued To"])
        writer.writerow([sl_no, date, item, qty, issued_to])

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fragorium Stock Issue Ledger</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50 font-sans antialiased">

    <div class="max-w-6xl mx-auto p-4 md:p-8">
        <div class="flex items-center space-x-3 mb-8 bg-white p-6 rounded-xl shadow-sm border border-gray-100">
            <span class="text-4xl">📦</span>
            <div>
                <h1 class="text-2xl font-bold text-gray-800">Fragorium Stock Issue Ledger</h1>
                <p class="text-sm text-gray-500">Real-time Factory Inventory Tracking</p>
            </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-200 border-l-4 border-blue-500">
                <p class="text-sm font-medium text-gray-500 uppercase">Total Transactions</p>
                <p class="text-3xl font-bold text-gray-800 mt-1">{{ total_transactions }}</p>
            </div>
            <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-200 border-l-4 border-emerald-500">
                <p class="text-sm font-medium text-gray-500 uppercase">Latest Update</p>
                <p class="text-xl font-bold text-gray-800 mt-2">{% if latest_date %}{{ latest_date }}{% else %}N/A{% endif %}</p>
            </div>
        </div>

        <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-200 mb-8">
            <h2 class="text-base font-bold text-gray-800 mb-4 flex items-center">
                <span class="mr-2">📝</span> Log New Stock Issue
            </h2>
            <form action="/add" method="POST" class="grid grid-cols-1 md:grid-cols-4 gap-4">
                <input type="text" name="date" placeholder="Date (DD/MM/YYYY)" required class="border p-2.5 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
                <input type="text" name="item" placeholder="Item Description" required class="border p-2.5 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
                <input type="text" name="qty" placeholder="Quantity (e.g. 1 Box)" required class="border p-2.5 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
                <input type="text" name="issued_to" placeholder="Issued To (Name/Dept)" required class="border p-2.5 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
                <button type="submit" class="md:col-span-4 bg-blue-600 hover:bg-blue-700 text-white font-medium py-2.5 rounded-lg transition text-sm shadow-sm">Save Transaction</button>
            </form>
        </div>

        <div class="mb-4">
            <input type="text" id="searchInput" placeholder="🔍 Type to search item description or staff name..." class="w-full border p-3 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white shadow-sm">
        </div>

        <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
            <div class="overflow-x-auto">
                <table class="w-full text-left border-collapse" id="ledgerTable">
                    <thead>
                        <tr class="bg-gray-800 text-white text-xs uppercase tracking-wider">
                            <th class="p-4 font-semibold w-20">Sl No</th>
                            <th class="p-4 font-semibold w-32">Date</th>
                            <th class="p-4 font-semibold">Item Description</th>
                            <th class="p-4 font-semibold w-32">Quantity</th>
                            <th class="p-4 font-semibold w-48">Issued To</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-200 text-sm text-gray-700">
                        {% for entry in inventory_data %}
                        <tr class="hover:bg-gray-50 transition-colors">
                            <td class="p-4 font-mono text-gray-400">#{{ entry.sl_no }}</td>
                            <td class="p-4 text-gray-600 font-medium">{{ entry.date }}</td>
                            <td class="p-4 font-bold text-gray-900">{{ entry.item }}</td>
                            <td class="p-4"><span class="bg-blue-50 text-blue-700 px-2 py-1 rounded text-xs font-semibold">{{ entry.qty }}</span></td>
                            <td class="p-4 text-gray-600 font-medium">{{ entry.issued_to }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <script>
    document.getElementById("searchInput").addEventListener("keyup", function() {
        var filter = this.value.toUpperCase();
        var rows = document.querySelectorAll("#ledgerTable tbody tr");
        
        rows.forEach(function(row) {
            var text = row.textContent || row.innerText;
            if (text.toUpperCase().indexOf(filter) > -1) {
                row.style.display = "";
            } else {
                row.style.display = "none";
            }
        });
    });
    </script>
</body>
</html>
"""

@app.route('/')
def dashboard():
    data = load_inventory()
    total_transactions = len(data)
    latest_date = data[-1]['date'] if data else ""
    
    return render_template_string(
        HTML_TEMPLATE, 
        inventory_data=reversed(data), 
        total_transactions=total_transactions,
        latest_date=latest_date
    )

@app.route('/add', methods=['POST'])
def add_entry():
    if request.method == 'POST':
        data = load_inventory()
        
        try:
            next_sl = max([int(e['sl_no']) for e in data if e['sl_no'].isdigit()]) + 1 if data else 1
        except ValueError:
            next_sl = len(data) + 1
            
        date = request.form['date']
        item = request.form['item']
        qty = request.form['qty']
        issued_to = request.form['issued_to']
        
        save_entry(next_sl, date, item, qty, issued_to)
        
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)

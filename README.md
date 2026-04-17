# Real-Time E-Commerce Data Pipeline 🛒

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=flat&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=flat&logo=sqlite&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Charts-3F4F75?style=flat&logo=plotly&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)

A fully functional **real-time data pipeline** that simulates e-commerce user events, processes and stores them in SQLite, and visualises live analytics through a dark-themed Flask dashboard powered by Plotly.

---

## 🖥️ Dashboard Preview

> Dark-themed analytics dashboard with animated metric cards and live-updating charts.

---

## ⚙️ Architecture

```
┌─────────────────┐     ┌──────────────────────┐     ┌──────────────────┐
│  Data Generator │────▶│  Pipeline (ETL)      │────▶│  Dashboard       │
│  (Faker + RNG)  │     │  Process → SQLite DB │     │  Flask + Plotly  │
└─────────────────┘     └──────────────────────┘     └──────────────────┘
```

---

## 📁 Project Structure

```
ecommerce-pipeline/
├── data/                    # SQLite database (auto-created)
│   └── ecommerce.db
├── dashboard/               # Web dashboard
│   └── app.py               # Flask server + premium dark UI
├── src/                     # Core pipeline
│   ├── data_generator.py    # Fake e-commerce event generator
│   └── pipeline.py          # ETL: process + store + aggregate
├── requirements.txt
├── run_pipeline.py          # CLI runner (batch / continuous / dashboard)
├── setup.bat                # One-click Windows setup
└── README.md
```

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/SandeepTech11/ecommerce-pipeline.git
cd ecommerce-pipeline
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Seed the Database (Batch Mode)

```bash
python run_pipeline.py --mode batch --batch-size 100
```

### 4. Start the Dashboard

```bash
python dashboard/app.py
```

Open **http://localhost:5000** in your browser.

### ⚡ One-Click Setup (Windows)

```bat
setup.bat
```

---

## 🎛️ Run Modes

| Mode | Command | Description |
|------|---------|-------------|
| **Batch** | `python run_pipeline.py --mode batch --batch-size 100` | Generate N events once |
| **Continuous** | `python run_pipeline.py --mode continuous --interval 2` | Stream events every N seconds |
| **Dashboard** | `python run_pipeline.py --mode dashboard` | Launch the web dashboard |

---

## 📊 Dashboard Features

- **4 Live Metric Cards** — Total Events, Purchases, Revenue, Unique Users
- **Sales by Category** — Animated bar chart (Electronics, Sports, Home)
- **Event Distribution** — Donut chart (Purchases vs Other Events)
- **Auto-refresh** every 5 seconds with animated number transitions
- **Dark theme** with glassmorphism-inspired cards and gradient accents

---

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Web dashboard |
| `/api/metrics` | GET | JSON metrics data |

**Sample `/api/metrics` Response:**
```json
{
  "total_events": 1423,
  "total_purchases": 175,
  "total_revenue": 14382.75,
  "unique_users": 1380,
  "category_sales": [["Electronics", 72], ["Sports", 64], ["Home", 39]]
}
```

---

## 📦 Sample Events Generated

| Field | Examples |
|-------|---------|
| **Event Types** | page_view, add_to_cart, purchase, remove_from_cart |
| **Products** | Wireless Headphones, Running Shoes, Coffee Maker, Desk Lamp |
| **Categories** | Electronics, Sports, Home |
| **Payment** | credit_card, paypal, debit_card, apple_pay |
| **Users** | Unique UUID-based user & session IDs |

---

## 🛠️ Customisation

- **Add products** → edit `PRODUCTS` list in `src/data_generator.py`
- **Change event weights** → edit `weights` in `DataGenerator.generate_event()`
- **Add new metrics** → extend `get_metrics()` in `src/pipeline.py`
- **Style the dashboard** → edit CSS variables in `dashboard/app.py`

---

## 🧑‍💻 Author

**Sandeep Reddy** — [GitHub](https://github.com/SandeepTech11)

---

## 📄 License

This project is licensed under the MIT License.

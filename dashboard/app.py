
import sys
import os
from pathlib import Path

# Robust path fix — works from any working directory
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'src'))

from flask import Flask, jsonify, render_template_string
from pipeline import ECommercePipeline

app = Flask(__name__)

# Use absolute path for the database
db_path = str(Path(__file__).resolve().parent.parent / 'data' / 'ecommerce.db')
pipeline = ECommercePipeline(db_path=db_path)

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>E-Commerce Analytics Dashboard</title>
    <meta name="description" content="Real-time e-commerce data pipeline analytics dashboard with live metrics and charts.">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
    <style>
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

        :root {
            --bg-primary:   #0d0f1a;
            --bg-card:      #131626;
            --bg-card2:     #1a1e35;
            --border:       rgba(255,255,255,0.07);
            --accent1:      #6c63ff;
            --accent2:      #a78bfa;
            --accent3:      #38bdf8;
            --accent4:      #f472b6;
            --accent5:      #34d399;
            --text-primary: #f1f5f9;
            --text-muted:   #94a3b8;
            --glow:         rgba(108,99,255,0.25);
        }

        body {
            font-family: 'Inter', sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
            overflow-x: hidden;
        }

        /* Animated background blobs */
        body::before {
            content: '';
            position: fixed;
            top: -200px; left: -200px;
            width: 600px; height: 600px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(108,99,255,0.12) 0%, transparent 70%);
            pointer-events: none;
            animation: blobMove 12s ease-in-out infinite alternate;
        }
        body::after {
            content: '';
            position: fixed;
            bottom: -200px; right: -200px;
            width: 500px; height: 500px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(56,189,248,0.10) 0%, transparent 70%);
            pointer-events: none;
            animation: blobMove 15s ease-in-out infinite alternate-reverse;
        }
        @keyframes blobMove {
            from { transform: translate(0,0) scale(1); }
            to   { transform: translate(60px,40px) scale(1.15); }
        }

        /* ── Top Bar ── */
        .topbar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 18px 40px;
            border-bottom: 1px solid var(--border);
            background: rgba(13,15,26,0.85);
            backdrop-filter: blur(14px);
            position: sticky; top: 0; z-index: 100;
        }
        .topbar-brand {
            display: flex; align-items: center; gap: 12px;
        }
        .topbar-icon {
            width: 36px; height: 36px;
            background: linear-gradient(135deg, var(--accent1), var(--accent2));
            border-radius: 10px;
            display: flex; align-items: center; justify-content: center;
            font-size: 18px;
        }
        .topbar-title {
            font-size: 1.1rem; font-weight: 700;
            background: linear-gradient(90deg, var(--accent2), var(--accent3));
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }
        .topbar-status {
            display: flex; align-items: center; gap: 8px;
            font-size: 0.78rem; color: var(--text-muted);
        }
        .status-dot {
            width: 8px; height: 8px; border-radius: 50%;
            background: var(--accent5);
            box-shadow: 0 0 8px var(--accent5);
            animation: pulse 2s ease-in-out infinite;
        }
        @keyframes pulse {
            0%,100% { opacity:1; transform:scale(1); }
            50%      { opacity:0.5; transform:scale(1.4); }
        }

        /* ── Main Content ── */
        .main { padding: 36px 40px; max-width: 1400px; margin: 0 auto; }

        /* ── Metric Cards ── */
        .metrics {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 20px;
            margin-bottom: 32px;
        }
        .metric-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 24px 28px;
            position: relative;
            overflow: hidden;
            transition: transform 0.25s ease, box-shadow 0.25s ease;
            cursor: default;
        }
        .metric-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 40px rgba(0,0,0,0.4);
        }
        .metric-card::before {
            content: '';
            position: absolute; top: 0; left: 0; right: 0; height: 3px;
            border-radius: 18px 18px 0 0;
        }
        .metric-card:nth-child(1)::before { background: linear-gradient(90deg,#6c63ff,#a78bfa); }
        .metric-card:nth-child(2)::before { background: linear-gradient(90deg,#38bdf8,#818cf8); }
        .metric-card:nth-child(3)::before { background: linear-gradient(90deg,#34d399,#6ee7b7); }
        .metric-card:nth-child(4)::before { background: linear-gradient(90deg,#f472b6,#fb923c); }

        .metric-icon {
            font-size: 1.6rem; margin-bottom: 12px;
        }
        .metric-value {
            font-size: 2.4rem; font-weight: 800;
            letter-spacing: -1px;
            line-height: 1;
        }
        .metric-card:nth-child(1) .metric-value { color: var(--accent2); }
        .metric-card:nth-child(2) .metric-value { color: var(--accent3); }
        .metric-card:nth-child(3) .metric-value { color: var(--accent5); }
        .metric-card:nth-child(4) .metric-value { color: var(--accent4); }

        .metric-label {
            font-size: 0.78rem; font-weight: 500; text-transform: uppercase;
            letter-spacing: 1px; color: var(--text-muted); margin-top: 8px;
        }

        /* ── Toolbar ── */
        .toolbar {
            display: flex; align-items: center; justify-content: space-between;
            margin-bottom: 24px;
        }
        .toolbar-title {
            font-size: 1rem; font-weight: 600; color: var(--text-muted);
        }
        #refresh-btn {
            display: flex; align-items: center; gap: 8px;
            padding: 10px 24px;
            background: linear-gradient(135deg, var(--accent1), var(--accent2));
            color: white; border: none; border-radius: 50px;
            cursor: pointer; font-size: 0.88rem; font-weight: 600;
            font-family: 'Inter', sans-serif;
            transition: opacity 0.2s, transform 0.2s;
            box-shadow: 0 4px 20px var(--glow);
        }
        #refresh-btn:hover { opacity:0.88; transform:scale(1.04); }
        #refresh-btn:active { transform:scale(0.97); }
        #refresh-btn svg { width:16px; height:16px; }

        /* ── Charts ── */
        .charts {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(440px, 1fr));
            gap: 24px;
        }
        .chart-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 24px;
            transition: transform 0.25s ease, box-shadow 0.25s ease;
        }
        .chart-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 36px rgba(0,0,0,0.35);
        }
        .chart-title {
            font-size: 0.9rem; font-weight: 600; color: var(--text-muted);
            margin-bottom: 16px; text-transform: uppercase; letter-spacing: 0.8px;
        }

        /* ── Footer ── */
        .footer {
            text-align: center; padding: 32px 40px;
            font-size: 0.75rem; color: var(--text-muted);
            border-top: 1px solid var(--border); margin-top: 48px;
        }

        /* Loading shimmer */
        @keyframes shimmer {
            from { background-position: -400px 0; }
            to   { background-position: 400px 0; }
        }
    </style>
</head>
<body>

<!-- Top Bar -->
<header class="topbar">
    <div class="topbar-brand">
        <div class="topbar-icon">🛒</div>
        <span class="topbar-title">E-Commerce Analytics</span>
    </div>
    <div class="topbar-status">
        <div class="status-dot"></div>
        Live · Auto-refreshing every 5 s
    </div>
</header>

<!-- Main -->
<main class="main">

    <!-- Metric Cards -->
    <div class="metrics">
        <div class="metric-card">
            <div class="metric-icon">📦</div>
            <div class="metric-value" id="total-events">—</div>
            <div class="metric-label">Total Events</div>
        </div>
        <div class="metric-card">
            <div class="metric-icon">🛍️</div>
            <div class="metric-value" id="total-purchases">—</div>
            <div class="metric-label">Purchases</div>
        </div>
        <div class="metric-card">
            <div class="metric-icon">💰</div>
            <div class="metric-value" id="total-revenue">—</div>
            <div class="metric-label">Revenue</div>
        </div>
        <div class="metric-card">
            <div class="metric-icon">👤</div>
            <div class="metric-value" id="unique-users">—</div>
            <div class="metric-label">Unique Users</div>
        </div>
    </div>

    <!-- Toolbar -->
    <div class="toolbar">
        <span class="toolbar-title" id="last-updated">Fetching data…</span>
        <button id="refresh-btn" onclick="loadData()">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="23 4 23 10 17 10"></polyline>
                <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"></path>
            </svg>
            Refresh
        </button>
    </div>

    <!-- Charts -->
    <div class="charts">
        <div class="chart-card">
            <div class="chart-title">Sales by Category</div>
            <div id="category-chart" style="height:320px;"></div>
        </div>
        <div class="chart-card">
            <div class="chart-title">Event Distribution</div>
            <div id="event-chart" style="height:320px;"></div>
        </div>
    </div>

</main>

<footer class="footer">
    Real-Time E-Commerce Data Pipeline &mdash; Built with Flask &amp; Plotly
</footer>

<script>
    const PLOTLY_LAYOUT = {
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor:  'rgba(0,0,0,0)',
        font: { family: 'Inter, sans-serif', color: '#94a3b8' },
        margin: { t: 10, b: 40, l: 40, r: 20 },
    };

    async function loadData() {
        try {
            const response = await fetch('/api/metrics');
            const data = await response.json();

            // Animate number updates
            animateValue('total-events',    data.total_events);
            animateValue('total-purchases', data.total_purchases);
            animateValue('unique-users',    data.unique_users);
            document.getElementById('total-revenue').textContent =
                '$' + data.total_revenue.toLocaleString('en-US', {maximumFractionDigits:2});

            // Update timestamp
            const now = new Date();
            document.getElementById('last-updated').textContent =
                'Last updated: ' + now.toLocaleTimeString();

            // Category bar chart
            const categories = data.category_sales.map(x => x[0]);
            const values     = data.category_sales.map(x => x[1]);

            Plotly.react('category-chart', [{
                x: categories, y: values, type: 'bar',
                marker: {
                    color: ['#6c63ff','#a78bfa','#38bdf8','#f472b6','#34d399'],
                    opacity: 0.9,
                },
                text: values,
                textposition: 'outside',
                textfont: { color: '#f1f5f9', size: 13 },
                hovertemplate: '<b>%{x}</b><br>Sales: %{y}<extra></extra>',
            }], {
                ...PLOTLY_LAYOUT,
                xaxis: { gridcolor: 'rgba(255,255,255,0.06)', zerolinecolor: 'rgba(255,255,255,0.06)' },
                yaxis: { gridcolor: 'rgba(255,255,255,0.06)', zerolinecolor: 'rgba(255,255,255,0.06)' },
            }, { responsive: true, displayModeBar: false });

            // Event distribution donut
            const purchases = data.total_purchases;
            const others    = data.total_events - purchases;
            Plotly.react('event-chart', [{
                values: [purchases, others],
                labels: ['Purchases', 'Other Events'],
                type: 'pie', hole: 0.55,
                marker: { colors: ['#34d399','#6c63ff'] },
                textinfo: 'label+percent',
                textfont: { color: '#f1f5f9', size: 13 },
                hovertemplate: '<b>%{label}</b><br>Count: %{value}<br>%{percent}<extra></extra>',
            }], {
                ...PLOTLY_LAYOUT,
                showlegend: true,
                legend: { font: { color: '#94a3b8' } },
            }, { responsive: true, displayModeBar: false });

        } catch (err) {
            console.error('Failed to fetch metrics:', err);
            document.getElementById('last-updated').textContent = 'Connection error — retrying…';
        }
    }

    function animateValue(id, target) {
        const el = document.getElementById(id);
        const start = parseInt(el.textContent.replace(/[^0-9]/g, '')) || 0;
        const diff  = target - start;
        const steps = 20;
        let step = 0;
        const timer = setInterval(() => {
            step++;
            el.textContent = Math.round(start + (diff * step / steps)).toLocaleString();
            if (step >= steps) clearInterval(timer);
        }, 16);
    }

    loadData();
    setInterval(loadData, 5000);
</script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(DASHBOARD_HTML)

@app.route('/api/metrics')
def metrics():
    return jsonify(pipeline.get_metrics())

if __name__ == '__main__':
    print("=" * 50)
    print("  E-Commerce Analytics Dashboard")
    print("  http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, port=5000)

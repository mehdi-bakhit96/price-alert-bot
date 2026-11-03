# 🚀 Price & Inventory Monitoring Bot

A robust, modular, and asynchronous Python-based bot designed to track product prices and stock availability in real-time. Built with fault-tolerance in mind, featuring local state persistence and multi-channel notification dispatchers.

---

## 🛠️ Key Features

- **Asynchronous Architecture:** Powered by `asyncio` and `httpx` for high-performance, non-blocking HTTP requests.
- **Fault-Tolerant Notifier:** Gracefully handles network restrictions/timeouts and falls back to local logging and console alerts.
- **Local State Persistence:** Tracks price fluctuations and stock changes securely using structured JSON storage (`storage_state.json` & `alerts_history.json`).
- **Modular Design:** Clean separation of concerns across configuration, tracking, storage, and notification modules.
- **Environment-based Config:** Secure configuration management using `python-dotenv`.

---

## 📂 Project Structure
```text
price_alert_bot/
│
├── data/
│   ├── alerts_history.json    # Historical log of price/stock changes
│   └── storage_state.json     # Current tracked item states
│
├── src/
│   ├── __init__.py
│   ├── alert_logic.py         # Price & stock comparison logic
│   ├── config.py              # Environment and settings parser
│   ├── logger.py              # Centralized logging configuration
│   ├── main.py                # Application entry point & async loop
│   ├── notifier.py            # Multi-channel notification handler (Console/File/API)
│   ├── storage.py             # Local JSON state persistence manager
│   └── tracker.py             # Asynchronous API fetcher & tracker
│
├── .env.example               # Template for environment variables
├── requirements.txt           # Project dependencies
└── README.md                  # Project documentation

 Installation & Setup
1.Clone the repository:
   git clone https://github.com/YOUR_USERNAME/price-alert-bot.git
   cd price_alert_bot
   
2.Create and activate a virtual environment:
   python -m venv .venv
   # On Windows (PowerShell):
   .\.venv\Scripts\Activate.ps1
   
3.Install dependencies:
   pip install -r requirements.txt
   
4.Configure environment variables:

   Copy .env.example to .env
   Set your desired check interval and API target.

5.Run the bot:
   python -m src.main
   
 Use Cases
E-commerce price tracking and competitor analysis.
Out-of-stock inventory alerts for high-demand products.
Automated data pipeline feeding into local storage or dashboards.

Author
Mahdi

Python Automation & Backend Developer

# CropChain — Blockchain-Based Fair Trade Prototype

> Streamlit prototype demonstrating a blockchain-like ledger for fair trade and product traceability  
> (Farmer → Distributor → Retailer → Consumer)

---

## Project overview

This repository contains a lightweight Streamlit application that simulates a blockchain-powered fair trade system. It allows:
- Farmers to register products (ProductID, name, base price).
- Distributors to purchase from farmers and update price/ownership.
- Retailers to stock items and set final consumer prices.
- Consumers to verify product authenticity and view the full ownership history.

All transactions are recorded into a session-based ledger representing an immutable log for demo purposes. The core app is `app/streamlit_app.py`. The original prototype code used for this repo is included (see file reference). :contentReference[oaicite:2]{index=2}

---

## Quick demo (local)

1. Clone the repo:
```bash
git clone https://github.com/Silverfang180/CropChain-blockchain-fairtrade-system.git
cd CropChain-blockchain-fairtrade-system
```
2. Create and activate a Python virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Run the Streamlit app:
```bash
streamlit run app/streamlit_app.py
```
5. Open the provided URL (usually http://localhost:8501) and use the left column to register, transfer, and verify sample products.

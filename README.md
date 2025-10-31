<h1 align="center"> All-India APMC Market Intelligence Tool</h1>

<p align="center">
  🚜 <b>Empowering Farmers with Data — Real-Time Commodity Insights Across India</b>
</p>

<p align="center">
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white" /></a>
  <a href="https://pandas.pydata.org/"><img src="https://img.shields.io/badge/pandas-Data%20Analysis-blue?logo=pandas&logoColor=white" /></a>
  <a href="https://www.selenium.dev/"><img src="https://img.shields.io/badge/Selenium-Web%20Scraping-brightgreen?logo=selenium&logoColor=white" /></a>
  <a href="#"><img src="https://img.shields.io/badge/License-MIT-green.svg" /></a>
</p>

---

> 📈 A Python-based command-line tool that provides **real-time agricultural market intelligence** across India using live data scraped from the **Government’s Agmarknet portal**.  
> Designed to empower **farmers, traders, and analysts** with up-to-date, actionable price insights for better decision-making.

---

## 🧩 Overview

Farmers across India often face a critical challenge — the **lack of accessible, consolidated, and timely market information**.  
Even within the same state, prices for identical commodities can vary widely between markets (mandis).  
While government portals like Agmarknet provide this data, they are often **slow**, **inconsistent**, and **hard to compare**.

This tool bridges that gap by:
- **Automating data collection** from Agmarknet using Selenium  
- **Analyzing live and historical price data** with pandas  
- **Delivering a clean, real-time report** directly in the terminal  

With this, farmers and traders can instantly identify **price trends**, **best-performing markets**, and **commodity movement** — without manual lookup.

---

## ✨ Key Features

✅ **All-India Coverage**  
Scrapes market data for **any state or Union Territory** in India.  

⚡ **On-Demand Analysis**  
Fetches and analyzes the **latest available prices** in real-time whenever you run the script.  

🧠 **Smart Input Recognition**  
Accepts flexible user input (e.g., `banana`, `Banana`, or `BANANA`) and automatically matches it to official Agmarknet entries.  

📊 **Live Market Report**  
For the most recent day with data, the tool provides:
- **Average price** for the commodity in the selected state  
- **Market with the highest price**  
- **Market with the lowest price**  

📈 **Trend Analysis**  
Compares the latest average price with the previous day’s average and reports whether the trend is **UP 📈** or **DOWN 📉**.  

🕸️ **Robust Web Scraping**  
Uses **Selenium** to navigate the government’s complex **ASP.NET-based** Agmarknet portal seamlessly.  

🎯 **Accurate State Filtering**  
Includes a built-in reference of **all Indian districts** to precisely filter data and ensure accurate state-specific results.  

---

## ⚙️ How It Works

1. **User Input:**  
   Prompts for a **state** and **commodity** (supports fuzzy matching for flexible spelling).  

2. **Live Scraping:**  
   Opens a **headless Selenium browser** and fetches the latest and last 4 days of data from the Agmarknet portal.  

3. **Data Cleaning:**  
   Converts prices to numeric types, standardizes date formats, and removes incomplete records using `pandas`.  

4. **Filtering:**  
   Filters only the relevant data for the selected state using an internal state–district mapping.  

5. **Analysis:**  
   Determines:
   - Average, highest, and lowest prices  
   - The latest two available dates  
   - Trend direction (UP/DOWN)  

6. **Report Generation:**  
   Prints a clean, formatted summary report directly to your terminal, for example:

   ```
   ───────────────────────────────────────────────
   📅 Date: 30 Oct 2025
   🌾 Commodity: Tomato
   🗺️ State: Maharashtra

   ▪ Average Price: ₹2,850 / Quintal
   ▪ Highest Price: ₹3,200 at Pune Market
   ▪ Lowest Price: ₹2,400 at Nashik Market
   ▪ Trend: UP 📈 (compared to previous day)
   ───────────────────────────────────────────────
   ```

---

## 🚀 How to Use

### 1️⃣ Clone the Repository
```bash
git clone <your-repository-url>
cd <your-repository-name>
```

### 2️⃣ Create a Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

*(This will install `pandas` and `selenium`.)*

### 4️⃣ Run the Tool
```bash
python live_market_analyzer.py
```

---

## 🧰 Tech Stack

| Layer | Tools & Libraries |
|-------|-------------------|
| **Language** | Python 3.10+ |
| **Data Handling** | pandas |
| **Web Scraping** | Selenium (headless mode) |
| **Automation** | fuzzywuzzy (for flexible text matching) |
| **Platform** | Agmarknet (Government of India portal) |

---

## 📈 Example Use Case

> “A farmer in Karnataka wants to check the latest prices for onions.  
> With a single command, they get a summary showing which mandi is paying the highest price, what the current trend is, and how today’s prices compare to yesterday’s — enabling smarter market decisions.”

---

## 🧭 Future Enhancements

- Add **state-wise price charts** using Matplotlib  
- Enable **SMS or WhatsApp notifications** for daily updates  
- Build a **web dashboard** version of this CLI  
- Introduce **AI-powered price forecasting**  

---

## 👨‍💻 Author

**Viswateja Chitturi**  
💼 Data & AI Enthusiast | Machine Learning Developer  

---

## ⭐ Support

If you found this tool useful, please **⭐ star this repository**!  
Your support helps farmers and dev

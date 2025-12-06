SMARTWORTH – Market Value Analyzer
A lightweight CLI tool for scraping product prices, storing them in a local database, and providing simple trend analysis.
Developed as a group assignment by
Eda • Melis • Tuana • Gamze • Nisa

1. Overview
SMARTWORTH is a small but functional price-tracking and analysis tool.
It collects product prices from online sources, saves them into an SQLite database, and generates insights such as value scores, simple trends, and similar product suggestions.
The project allowed us to practice:
Web scraping
SQL database management
Object-oriented programming
Basic price analysis
CLI menu design
Robust error handling

2. Purpose of the Project
The system is designed to:
Retrieve price information from multiple websites
Store data in a structured SQLite database
Track how prices evolve over time
Calculate simple analytics (value score, trends, comparisons)
Suggest similar products using name token matching
Practice OOP by dividing logic into analyzers, scrapers, and utilities
Although the code lives inside a single file (smartpy.py), we structured it logically into modules for readability.

3. Features
👤 User System
Account creation & login
Password hashing (basic, for educational use)
🌍 Web Scraping
Google scraping → approximate price ranges
Trendyol scraping → real product prices
Optional Scrapy spider (scraper_spider.py) for advanced users
📊 Price Analysis
Minimum, maximum, average price
Category-specific analyzer logic (Electronics, Clothing, Books, General)
Simple trend estimation
“Value Score” calculation
🕒 Price History
Every search is saved with:
Timestamp
Price list
Source website
ASCII-based price trend chart
🔍 Similar Products
Uses name token comparison to suggest related items.

4. Project Structure
 SMARTWORTH/
│
├── smartpy.py           # Main project file (all logic inside)
├── smartworth.db        # Auto-generated SQLite database
├── scraper_spider.py    # Optional Scrapy spider
└── README.md
Internal Logical Modules (inside smartpy.py):
UserAuth — login/registration
Database Layer — SQLite operations
Scrapers — Google & Trendyol scrapers
Analyzers — category-based scoring
Utils — cleaning, logging, helpers

5. Installation & Running
Clone the repo
git clone <repo-link>
cd SMARTWORTH

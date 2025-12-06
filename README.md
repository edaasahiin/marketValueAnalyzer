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
git clone <https://github.com/edaasahiin/marketValueAnalyzer.git>
cd smartworth.py

Install dependencies
pip install requests beautifulsoup4 sqlalchemy

(Optional) Install Scrapy
pip install scrapy

Run the program
python smartpy.py

6. How to Use the Program
Upon launching, you will see:
Log in
Register
Exit
After logging in, the main menu appears:
| Menu Item                | Description                   |
| ------------------------ | ----------------------------- |
| Analyze a product        | Scrapes prices & saves result |
| View price history       | Shows past price entries      |
| Compare two products     | Min/avg/max comparison        |
| List saved products      | Shows all user products       |
| Show product detail card | Analyzer outputs & info       |
| Find similar products    | Suggests related products     |
| Delete a product         | Removes from DB               |
| Run Scrapy spider        | Optional web-scraping test    |
| Exit                     | Close program                 |

Entirely runs via CLI.

7. Price History ASCII Chart
The tool prints a mini bar chart, helping visualize price trends without graphical libraries.
Example:
Price Trend:
100 | ████
120 | ██████
90  | ███

8. Value Score (Simplified)
score = (average_price / (min_price + max_price)) * 100
Each category analyzer modifies this base formula with its own weights.

9. Code Quality — Pylint
We used pylint throughout development:
Initial score: 8.30/10
After cleanup: fixed unused imports, line lengths, spacing issues
This directly aligns with the instructor’s grading rubric for readability.

<img width="614" height="76" alt="Ekran Resmi 2025-12-06 17 57 16" src="https://github.com/user-attachments/assets/d43580af-25dd-4d43-bc2e-3b67cad54ae6" />

10. Robustness & Testing
We prepared basic handling for likely issues:
Scraping errors
Missing prices
Database failures
Empty inputs
Unavailable URLs
Manual test cases were added for login, product analysis, and error scenarios.

11. Known Issues
Google/Trendyol markup may change
Password hashing is not secure for real-world use
Long product names reduce similarity accuracy
Scrapy is optional and not guaranteed to work on all systems

12. Future Improvements
Proper unit tests
Stronger password hashing (bcrypt/argon2)
Split modules into separate files
Add caching for repeated searches
More informative error messages

13. Out-of-the-Box Functionality
The project works instantly on any clean environment:
✔ Database auto-creates
✔ No extra configuration
✔ Scrapers run without external tools
✔ Scrapy optional
✔ All menu features functional

14. Conclusion
SMARTWORTH demonstrates how a simple CLI tool can combine:
Web scraping
OOP principles
SQL databases
Data analysis
CLI menus
Error handling
This project helped our team gain hands-on experience with real programming workflows and collaborative development.




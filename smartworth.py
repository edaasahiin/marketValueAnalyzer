"""
SMARTWORTH - Market Value Analyzer
Student Version (Revised)

This project was prepared for basic web scpraping, price analysis,
simple trend calculation, and product tracking over SQLite.
The code is kept simple enough for a student-level implementation.
"""

# ----------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------

import requests
from bs4 import BeautifulSoup
import subprocess
from datetime import datetime
from sqlalchemy import (
    create_engine, MetaData, Table,
    Column, Integer, String, Float, Text
)
from sqlalchemy.sql import select, insert, delete
from abc import ABC, abstractmethod
from dataclasses import dataclass

# -------------------------------------------------------------------------------
# DATABASE INITIALIZATION
#--------------------------------------------------------------------------------

DB_NAME = "smartworth.db)
engine = create_engine(f"sqlite:///{DB_NAME]", echo=False, future=True)
metadata = MetaData()

# USERS TABLE
users_table = Table(
   "users",
   metadata,
   Column("id", Integer, primary_key=True),
   Column("username", String, unique=True),
   Column("password_hash", String),
   Column("role", String),
)

# PRODUCTS TABLE
products_table = Table(
    "products",
     metadata,
     Column("id", Intiger, primary_key=True),
     Column("user_id", Intiger, primary_key=True),
     Column("name", String),
     Column("category", String),
     Column("avg_price", Float),
     Column("min_price", Float),
     Column("max_price", Float),
     Column("price_spread", Float),
     Column("value_score", Integer),
     Column("trend", String),
     Column("description", Text),
     Column("supply_level", String),
     Column("consistency", Float),
     Column("date_added", String),
)

# HISTORY TABLE
history_table = Table(
    "history",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("product_name", String),
    Column("price", Float),
    Column("source", String),
    Column("date", String),
)

metadata.create_all(engine)

# ----------------------------------------------------------------------------------------
#LOGGING
# ----------------------------------------------------------------------------------------

def write_log(message: str) -> None:
    """Simple log writer."""
    try:
        with open("smartworth_logs.txt", "a", encoding="utf-8) as f:
             now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
             f.write(f"[{now}] {message}\n")
    except Exception:
        pass

# ----------------------------------------------------------------------------------------
# UTILITY FUNCTIONS
# ----------------------------------------------------------------------------------------

def normalize_price_text(text: str) -> float:
    """
    Converts different currency formats to float TL.
    Simple converter used for student-level parsing.
    """
    t = (
        text.lower()
        .replace("tl", "")
        .replace("₺", "")
        .replace(" ", "")
        .replace(".", "")
        .replace(",", ".")
        .strip()
    )

    if not t:
        return 0.0

    try:
        if "usd" in t or "$" in t:
            return float(t.replace("usd", "").replace("$", "")) * 35
        return float(t)
    except Exception:
        return 0.0


jef simple_hash(text: str) -> str:
    """Very simple password hashing."""
    total = 0
    for ch in text:
        total = (total * 31 + ord(ch)) % 10_000_000
    return str(total)

# ---------------------------------------------------------------------------------------
# USER AUTHENTICATION
# ---------------------------------------------------------------------------------------

class UserAuth:
    """Handles user registration and login."""

    def __init__(self):
        self.engine = engine

    def register(self, username: str, password: str, role="user")
        if not username or not password:
            print("Username and password cannot be empty.")
            return False

        pw = simple_hash(password)

        try:
            with self.engine.begin() as conn:
                conn.execute(
                    insert(users_table).values(
                        username=username,
                        password_hash=pw,
                        role=role,
                    )
                )
            write_log(f"User registered: {username}")
            return True
        except Exeception as e:
            write_log(f"Registration failed: {e}")
            print("This username may already exist.")
            return False

    def login(self, username: str, password: str):
        if not username or not password:
            print("Empty login is not allowed.")
            return None, None

        pw = simple_hash(password)

        with self.engine.connect() as conn:
            row = conn.execute(
                select(
                    users_table.c.id,
                    users_table.c.username,
                    users_table.c.role,
                    users_table.c.password_hash,
                ).where(users_table.c.username == username)
            ).fetchone()

        if row and row.password_hash == pw:
            write_log(f"Login failed: {username}")
            return row.id, row.role

        write_log(f"Login failed: {username}")
        print("Incorrect username or password.")
        return None, None 


#  DATABASE  WRAPPER
        
        
class Database:
    """Centralized wrapper for DB operations."""

    def __init__(self):
        self.engine = engine

    def save_history(self, name: str, prices_by_source: dict):
        now = datetime.now().strftime("%d-%m-%Y %H:%M")
        with self.engine.begin() as conn:
            for source, lst in prices_by_source.items():
                for p in lst:
                    conn.execute(
                        insert(history_table).values(
                            product_name=name,
                            price=p,
                            source=source,
                            date=now,
                        )
                    )

    def add_product(self, user_id: int, product, score, trend, supply, consistency):
        spread = product.max_price - product.min_price
        with self.engine.begin() as conn:
            conn.execute(
                insert(products_table).values(
                    user_id=user_id,
                    name=product.name,
                    category=product.category,
                    avg_price=product.avg_price,
                    min_price=product.min_price,
                    max_price=product.max_price,
                    price_spread=spread,
                    value_score=score,
                    trend=trend,
                    description=product.description,
                    supply_level=supply,
                    consistency=consistency,
                    date_added=datetime.now().strftime("%d-%m-%Y %H:%M"),
                )
            )

    def list_products(self, user_id: int):
        with self.engine.connect() as conn:
            rows = conn.execute(
                select(
                    products_table.c.id,
                    products_table.c.name,
                    products_table.c.category,
                    products_table.c.avg_price,
                    products_table.c.value_score,
                    products_table.c.trend,
                ).where(products_table.c.user_id == user_id)
            ).fetchall()

        print("\n--- SAVED PRODUCTS ---\n")
        if not rows:
            print("No saved products.")
            return

        for r in rows:
            print(
                f"[{r.id}] {r.name} - {r.category} | "
                f"Avg: {r.avg_price:.2f} TL | Score: %{r.value_score} | Trend: {r.trend}"
            )

    def get_history(self, name: str):
        """Returns price history for a product."""
        with self.engine.connect() as conn:
            rows = conn.execute(
                select(
                    history_table.c.price,
                    history_table.c.source,
                    history_table.c.date,
                ).where(history_table.c.product_name == name)
                .order_by(history_table.c.id.asc())
            ).fetchall()
        return rows

    def delete_product(self, product_id: int):
        """Deletes a product by ID."""
        with self.engine.begin() as conn:
            conn.execute(
                delete(products_table).where(products_table.c.id == product_id)
            )

    def get_product_by_id(self, product_id: int):
        """Returns a single product by ID."""
        with self.engine.connect() as conn:
            row = conn.execute(
                select(products_table).where(products_table.c.id == product_id)
            ).fetchone()
        return row

    def get_all_products_for_similarity(self, user_id: int):
        """Returns all products for similarity comparison."""
        with self.engine.connect() as conn:
            rows = conn.execute(
                select(
                    products_table.c.id,
                    products_table.c.name,
                    products_table.c.category,
                    products_table.c.avg_price,
                    products_table.c.min_price,
                    products_table.c.max_price,
                    products_table.c.value_score,
                    products_table.c.trend,
                ).where(products_table.c.user_id == user_id)
                .order_by(products_table.c.id.asc())
            ).fetchall()
        return rows

# DOMAIN MODEL


@dataclass
class Product:
    """Simple product structure."""
    name: str
    category: str
    prices: list
    avg_price: float
    min_price: float
    max_price: float
    description: str


# ANALYZERS


class AnalyzerBase(ABC):
    """Base class for product analyzers."""

    @abstractmethod
    def calculate_value_score(self, product: Product) -> int:
        pass

    @abstractmethod
    def estimate_trend(self, product: Product) -> str:
        pass


class ElectronicsAnalyzer(AnalyzerBase):
    """Basic analyzer fine-tuned for electronic items."""

    def calculate_value_score(self, p: Product) -> int:
        score = 55
        spread = p.max_price - p.min_price

        if p.avg_price > 0 and spread > p.avg_price * 0.2:
            score -= 8

        text = p.description.lower()
        if "new" in text or "2023" in text or "2024" in text:
            score += 10
        if "old model" in text:
            score -= 8

        if p.min_price < p.avg_price * 0.9:
            score += 5

        return max(0, min(score, 100))

    def estimate_trend(self, p: Product) -> str:
        if p.avg_price == 0:
            return "Unknown"

        ratio = (p.max_price - p.min_price) / p.avg_price
        if ratio < 0.06:
            return "Stable"
        if ratio < 0.15:
            return "May decrease"
        return "Uncertain"


class ClothingAnalyzer(AnalyzerBase):
    """Lightweight analyzer for clothing products."""

def calculate_value_score(self, p: Product) -> int:
        score = 50
        text = p.description.lower()

        if "new season" in text:
            score += 15
        if "last season" in text:
            score -= 5

        if p.min_price < p.avg_price * 0.85:
            score += 5

        return max(0, min(score, 100))

    def estimate_trend(self, p: Product) -> str:
        return "Seasonal"


class BookAnalyzer(AnalyzerBase):
    """Simple analyzer for books."""

    def calculate_value_score(self, p: Product) -> int:
        score = 60
        text = p.description.lower()

        if "used" in text:
            score -= 10
        if "new edition" in text:
            score += 8

        return max(0, min(score, 100))

    def estimate_trend(self, p: Product) -> str:
        return "Stable"


class GeneralAnalyzer(AnalyzerBase):
    """Fallback analyzer when category is unclear."""

    def calculate_value_score(self, p: Product) -> int:
        score = 50
        spread = p.max_price - p.min_price

        if p.avg_price > 0 and spread > p.avg_price * 0.25:
            score -= 8
        if p.min_price < p.avg_price * 0.9:
            score += 5

        return max(0, min(score, 100))

    def estimate_trend(self, p: Product) -> str:
        if p.avg_price == 0:
            return "Unknown"

        ratio = (p.max_price - p.min_price) / p.avg_price
        if ratio < 0.05:
            return "Stable"
        return "Uncertain"



# SUPPLY / DEMAND ANALYZER


class SupplyDemandAnalyzer:
    """Extracts supply level hints from product description."""

    def _init_(self):
        self.high_words = ["limited stock", "only a few left", "low stock"]
        self.medium_words = ["in stock", "available", "ready to ship"]
        self.low_words = ["pre-order", "coming soon", "out of stock"]

    def analyze_supply_level(self, text: str) -> str:
        t = text.lower()
        score = 0

        for w in self.high_words:
            if w in t:
                score += 2
        for w in self.medium_words:
            if w in t:
                score += 1
        for w in self.low_words:
            if w in t:
                score -= 2

        if score >= 2:
            return "High"
        if score <= -2:
            return "Low"
        return "Medium"

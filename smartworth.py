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




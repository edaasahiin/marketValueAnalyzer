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
  


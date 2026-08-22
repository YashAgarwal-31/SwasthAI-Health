"""SQLite persistence for the local SwasthAI portfolio demo."""
from __future__ import annotations
import sqlite3
from pathlib import Path
from typing import Any

DB_PATH = Path(__file__).resolve().parents[1] / "data" / "swasthai.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE NOT NULL, password_hash TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS profiles (user_id INTEGER PRIMARY KEY, name TEXT, age INTEGER, gender TEXT, height REAL, weight REAL, conditions TEXT, allergies TEXT, goal TEXT, diet TEXT, emergency_contact TEXT);
CREATE TABLE IF NOT EXISTS health_logs (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, logged_on TEXT NOT NULL, weight REAL, water REAL, sleep REAL, steps INTEGER, systolic REAL, diastolic REAL, glucose REAL, heart_rate REAL, spo2 REAL, stress INTEGER, note TEXT);
CREATE TABLE IF NOT EXISTS reports (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, uploaded_on TEXT NOT NULL, filename TEXT NOT NULL, extracted_text TEXT, summary TEXT);
CREATE TABLE IF NOT EXISTS appointments (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, scheduled_for TEXT NOT NULL, doctor TEXT, specialty TEXT, purpose TEXT);
CREATE TABLE IF NOT EXISTS chats (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, created_on TEXT NOT NULL, role TEXT NOT NULL, message TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS predictions (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, created_on TEXT NOT NULL, model TEXT, probability REAL, risk TEXT, factors TEXT);
"""

def connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:
    with connect() as conn:
        conn.executescript(SCHEMA)

def execute(sql: str, params: tuple[Any, ...] = ()) -> None:
    with connect() as conn:
        conn.execute(sql, params)

def one(sql: str, params: tuple[Any, ...] = ()) -> sqlite3.Row | None:
    with connect() as conn:
        return conn.execute(sql, params).fetchone()

def all_rows(sql: str, params: tuple[Any, ...] = ()) -> list[sqlite3.Row]:
    with connect() as conn:
        return conn.execute(sql, params).fetchall()

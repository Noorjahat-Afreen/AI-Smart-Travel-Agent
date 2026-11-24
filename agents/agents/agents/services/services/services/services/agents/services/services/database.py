
import sqlite3
import json
import os
from datetime import datetime

DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "travel_agent.db"
)


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():

    with get_connection() as conn:

        conn.execute("""
            CREATE TABLE IF NOT EXISTS travel_plans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT NOT NULL,
                destination TEXT NOT NULL,
                departure_date TEXT,
                return_date TEXT,
                budget REAL,
                travellers INTEGER,
                travel_mode TEXT,
                plan_data TEXT,
                created_at TEXT
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS collected_places (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT,
                latitude REAL,
                longitude REAL,
                address TEXT,
                website TEXT,
                source TEXT,
                collected_at TEXT
            )
        """)


def save_travel_plan(request, plan_data):

    initialize_database()

    with get_connection() as conn:

        cursor = conn.execute("""
            INSERT INTO travel_plans (
                source,
                destination,
                departure_date,
                return_date,
                budget,
                travellers,
                travel_mode,
                plan_data,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            request.get("source"),
            request.get("destination"),
            request.get("departure_date"),
            request.get("return_date"),
            request.get("budget"),
            request.get("travellers"),
            request.get("travel_mode"),
            json.dumps(plan_data, ensure_ascii=False, default=str),
            datetime.now().isoformat()
        ))

        return cursor.lastrowid


def save_places(places):

    initialize_database()
    saved_count = 0

    with get_connection() as conn:

        for place in places:

            if not isinstance(place, dict):
                continue

            if not place.get("name"):
                continue

            conn.execute("""
                INSERT INTO collected_places (
                    name,
                    category,
                    latitude,
                    longitude,
                    address,
                    website,
                    source,
                    collected_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                place.get("name"),
                place.get("category"),
                place.get("latitude"),
                place.get("longitude"),
                place.get("address"),
                place.get("website"),
                place.get("source"),
                datetime.now().isoformat()
            ))

            saved_count += 1

    return saved_count


def get_recent_travel_plans(limit=10):

    initialize_database()

    with get_connection() as conn:

        rows = conn.execute("""
            SELECT *
            FROM travel_plans
            ORDER BY id DESC
            LIMIT ?
        """, (limit,)).fetchall()

        return [dict(row) for row in rows]


def get_saved_places(category=None):

    initialize_database()

    with get_connection() as conn:

        if category:
            rows = conn.execute("""
                SELECT *
                FROM collected_places
                WHERE category = ?
                ORDER BY id DESC
            """, (category,)).fetchall()
        else:
            rows = conn.execute("""
                SELECT *
                FROM collected_places
                ORDER BY id DESC
            """).fetchall()

        return [dict(row) for row in rows]

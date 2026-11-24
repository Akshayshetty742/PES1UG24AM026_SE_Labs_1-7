
"""Dairy milk collection ledger for recording and reviewing deliveries."""

import hashlib
import sqlite3


def create_database(connection):
    """Create the table used to store milk collection records."""
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS milk (
            id INTEGER PRIMARY KEY,
            farmer TEXT,
            litres REAL,
            fat REAL,
            day TEXT
        )
        """
    )


def record_milk(connection, farmer, litres, fat, day):
    """Record one farmer's milk delivery."""
    connection.execute(
        """
        INSERT INTO milk (farmer, litres, fat, day)
        VALUES (?, ?, ?, ?)
        """,
        (farmer, litres, fat, day),
    )
    connection.commit()


def farmer_token(farmer):
    """Generate a SHA-256 digest for a farmer's name."""
    return hashlib.sha256(farmer.encode("utf-8")).hexdigest()


def daily_total(connection, day):
    """Return the total litres collected on a given day."""
    rows = connection.execute(
        "SELECT litres FROM milk WHERE day = ?",
        (day,),
    ).fetchall()
    total = sum(row[0] for row in rows)
    return f"Total: {total:.1f} litres"


def top_farmer(connection):
    """Return the farmer with the highest total milk delivery."""
    rows = connection.execute(
        """
        SELECT farmer, SUM(litres)
        FROM milk
        GROUP BY farmer
        ORDER BY SUM(litres) DESC
        LIMIT 1
        """
    ).fetchone()

    if rows is None:
        return "No collections recorded"

    return rows[0]


def print_slip(farmer):
    """Print a simple collection-slip message."""
    print(f"Printing slip for {farmer}")


def low_fat(connection):
    """Return farmers whose milk fat is missing or below 3.5."""
    rows = connection.execute(
        "SELECT farmer, fat FROM milk"
    ).fetchall()

    return [
        farmer
        for farmer, fat in rows
        if fat is None or fat < 3.5
    ]


def main():
    """Run a short demonstration of the dairy collection ledger."""
    with sqlite3.connect(":memory:") as connection:
        create_database(connection)

        record_milk(connection, "Gopal", 12.5, 4.1, "Mon")
        record_milk(connection, "Lata", 20.0, 3.2, "Mon")

        print(
            daily_total(connection, "Mon"),
            top_farmer(connection),
            low_fat(connection),
        )
        print_slip("Gopal")
        print(farmer_token("Lata"))


if __name__ == "__main__":
    main()

"""
Create a sample SQLite database with global power plant data for demoing
Datasette Agent's conversational data exploration capabilities.
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "power_plants.db")


def create_database():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE power_plants (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            country TEXT NOT NULL,
            region TEXT NOT NULL,
            fuel_type TEXT NOT NULL,
            capacity_mw REAL NOT NULL,
            commissioned_year INTEGER,
            latitude REAL,
            longitude REAL
        )
    """)

    plants = [
        ("Three Gorges Dam", "China", "Asia", "Hydro", 22500, 2003, 30.82, 111.00),
        ("Itaipu Dam", "Brazil", "South America", "Hydro", 14000, 1984, -25.41, -54.59),
        ("Kashiwazaki-Kariwa", "Japan", "Asia", "Nuclear", 7965, 1985, 37.43, 138.60),
        ("Guri Dam", "Venezuela", "South America", "Hydro", 10235, 1978, 7.77, -62.97),
        ("Tucurui Dam", "Brazil", "South America", "Hydro", 8370, 1984, -3.83, -49.72),
        ("Surgut-2", "Russia", "Europe", "Gas", 5597, 1985, 61.25, 73.38),
        ("Grand Coulee", "United States", "North America", "Hydro", 6809, 1942, 47.95, -118.98),
        ("Longtan Dam", "China", "Asia", "Hydro", 6426, 2007, 24.83, 107.05),
        ("Sayano-Shushenskaya", "Russia", "Europe", "Hydro", 6400, 1978, 52.83, 91.37),
        ("Bruce Nuclear", "Canada", "North America", "Nuclear", 6232, 1977, 44.33, -81.60),
        ("Zaporizhzhia", "Ukraine", "Europe", "Nuclear", 5700, 1984, 47.51, 34.58),
        ("Gansu Wind Farm", "China", "Asia", "Wind", 5160, 2009, 40.30, 96.70),
        ("Robert-Bourassa", "Canada", "North America", "Hydro", 5616, 1981, 53.78, -77.45),
        ("Shoaiba", "Saudi Arabia", "Middle East", "Oil", 5600, 2003, 20.68, 39.50),
        ("Taichung", "Taiwan", "Asia", "Coal", 5500, 1992, 24.21, 120.48),
        ("Belchatow", "Poland", "Europe", "Coal", 5354, 1981, 51.27, 19.33),
        ("Jamnagar", "India", "Asia", "Gas", 5000, 2000, 22.47, 70.07),
        ("Eesti Energia", "Estonia", "Europe", "Oil Shale", 4600, 1973, 59.28, 27.41),
        ("Bhadla Solar Park", "India", "Asia", "Solar", 2245, 2018, 27.53, 71.91),
        ("Noor-Ouarzazate", "Morocco", "Africa", "Solar", 580, 2016, 31.05, -6.86),
        ("Olkaria", "Kenya", "Africa", "Geothermal", 791, 2014, -0.88, 36.29),
        ("Alto Maipo", "Chile", "South America", "Hydro", 531, 2021, -33.80, -70.10),
        ("Hornsea One", "United Kingdom", "Europe", "Wind", 1218, 2020, 53.88, 1.79),
        ("Walney Extension", "United Kingdom", "Europe", "Wind", 659, 2018, 54.05, -3.53),
        ("Topaz Solar", "United States", "North America", "Solar", 550, 2014, 35.38, -120.04),
        ("Ivanpah", "United States", "North America", "Solar", 392, 2014, 35.56, -115.47),
        ("Tengger Desert Solar", "China", "Asia", "Solar", 1547, 2019, 37.55, 104.95),
        ("Pampa Wind Farm", "Argentina", "South America", "Wind", 100, 2019, -38.00, -63.00),
        ("Lake Turkana", "Kenya", "Africa", "Wind", 310, 2019, 2.43, 36.79),
        ("Medupi", "South Africa", "Africa", "Coal", 4764, 2015, -23.68, 27.55),
    ]

    c.executemany(
        "INSERT INTO power_plants (name, country, region, fuel_type, capacity_mw, commissioned_year, latitude, longitude) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        plants,
    )

    conn.commit()
    conn.close()
    return DB_PATH


if __name__ == "__main__":
    path = create_database()
    print(f"Created database: {path}")

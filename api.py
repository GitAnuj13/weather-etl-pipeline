import requests
import pandas as pd
from datetime import datetime

import pyodbc
import logging

logging.basicConfig(
    filename='weather_etl.log',
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)
def connect_to_db():
    logging.info("Connecting to SQL Server")
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost;"
        "DATABASE=WeatherETL;"
        "Trusted_Connection=yes;"
)

    return conn


def extract_weather():
    logging.info("Extracting weather data from API")
    url = (
        "https://api.open-meteo.com/v1/forecast"
        "?latitude=28.4595"
        "&longitude=77.0266"
        "&hourly=temperature_2m,wind_speed_10m"
    )

    response = requests.get(url)
    response.raise_for_status()

    data = response.json()
    logging.info(f"{len(data)} records extracted")

    return pd.DataFrame(data["hourly"])


def transform_weather(df):
    logging.info("Starting transformation")
    df = df.copy()

    df.rename(
        columns={
            "time": "ObservationTime",
            "temperature_2m": "Temperature",
            "wind_speed_10m": "WindSpeed"
        },
        inplace=True
    )

    df["ObservationTime"] = pd.to_datetime(
        df["ObservationTime"],
        errors="coerce"
    )

    df["City"] = "Gurgaon"
    df["LoadTimestamp"] = datetime.now()
    logging.info("Transformation completed")
    return df

def load_weather(conn, new_data):

    cursor = conn.cursor()

    insert_query = """
    INSERT INTO fact_weather
    (
        ObservationTime,
        Temperature,
        WindSpeed,
        City,
        LoadTimestamp
    )
    VALUES (?, ?, ?, ?, ?)
    """

    for _, row in new_data.iterrows():

        cursor.execute(
            insert_query,
            row["ObservationTime"],
            row["Temperature"],
            row["WindSpeed"],
            row["City"],
            row["LoadTimestamp"]
        )

    conn.commit()


def get_last_loaded_time(conn):
    

    query = """
    SELECT MAX(ObservationTime)
    FROM fact_weather
    """

    cursor = conn.cursor()
    cursor.execute(query)

    result = cursor.fetchone()
    logging.info(
    f"Last loaded timestamp: {result[0]}"
)
    return result[0]


def get_new_records(df, last_loaded_time):

    if last_loaded_time is None:

        logging.info(
            f"First run detected. Loading {len(df)} records."
        )

        return df

    new_data = df[
        df["ObservationTime"] > last_loaded_time
    ]

    logging.info(
        f"New records identified: {len(new_data)}"
    )

    return new_data


def run_pipeline():
    logging.info("Pipeline started")

    conn = connect_to_db()

    try:

        # Extract
        df = extract_weather()

        # Transform
        df = transform_weather(df)

        # Get checkpoint
        last_loaded_time = get_last_loaded_time(conn)

        # Incremental filter
        new_data = get_new_records(
            df,
            last_loaded_time
        )

        # No new records
        if len(new_data) == 0:
            print("No new records found.")
            return

        print(f"New records found: {len(new_data)}")

        # Load
        load_weather(
            conn,
            new_data
        )

        logging.info("Pipeline completed successfully")

    finally:
        conn.close()
new_data = run_pipeline()

def get_latest_weather():

    conn = connect_to_db()

    query = """
    SELECT TOP 20
        ObservationTime,
        Temperature,
        WindSpeed,
        City
    FROM fact_weather
    ORDER BY ObservationTime DESC
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df

if new_data is not None:
    print(new_data.head())


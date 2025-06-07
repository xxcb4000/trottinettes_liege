import requests
import pandas as pd
from datetime import datetime
import os

URL = "https://gbfs.api.ridedott.com/public/v2/liege/free_bike_status.json"
FICHIER = "dott_positions.csv"

def collect_and_save():
    raw = requests.get(URL, timeout=10).json()
    bikes = pd.json_normalize(raw["data"]["bikes"])
    bikes["datetime"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    write_header = not os.path.exists(FICHIER)
    bikes.to_csv(FICHIER, mode='a', header=write_header, index=False, encoding='utf-8-sig')

if __name__ == "__main__":
    collect_and_save()
    print("Capture réalisée :", datetime.utcnow())

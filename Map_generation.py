# %%
import pandas as pd
import numpy as np
#df = pd.read_csv('dott_positions_20250608.csv')
df = pd.read_csv('https://raw.githubusercontent.com/xxcb4000/trottinettes_liege/refs/heads/main/dott_positions.csv')
df



# %%
df = df.drop_duplicates(subset=['bike_id', 'lat', 'lon']).sort_values(by=['bike_id', 'datetime'])
df = df.sort_values(['bike_id', 'datetime'])
df['lat_prev'] = df.groupby('bike_id')['lat'].shift(1)
df['lon_prev'] = df.groupby('bike_id')['lon'].shift(1)
df['longueur_trajet'] = np.sqrt(((df['lat'] - df['lat_prev'])*111000)**2 + ((df['lon'] - df['lon_prev'])*71700)**2)
df['battery_level'] = np.where(df['current_fuel_percent'] > 0.7, 'High', np.where(df['current_fuel_percent'] >= 0.3, 'Medium', 'Low'))
#df.groupby(['bike_id', 'lat', 'lon']).count().head(50)
df.sort_values('longueur_trajet' , ascending = False)


# %%
import folium

m = folium.Map(location=[50.633, 5.567], zoom_start=13, tiles="CartoDB positron")
previous_row = None
df.sort_values(['bike_id', 'datetime'])

for _, row in df.iterrows():
    if row['battery_level'] == 'High':
        coulor = 'Green'
    elif row['battery_level'] == 'Medium':
        coulor = 'Orange'
    else:
        coulor = 'Red',

    folium.CircleMarker(
        [row["lat"], row["lon"]],
        radius=3,
        tooltip=f'Battery : {row["current_fuel_percent"]} - ID : {row["bike_id"]} - Datetime: {row["datetime"]}',
        color = coulor,
        fill=True,
        fill_opacity=0.7
    ).add_to(m)
    if previous_row is not None :
        if previous_row['bike_id'] == row['bike_id'] and row['longueur_trajet'] > 40:
            folium.PolyLine(
                locations = [(previous_row['lat'], previous_row['lon']), (row['lat'], row['lon'])],
                tooltip=f'Date time:{row["datetime"]}',
                color='black',
                weight=3,
                opacity=0.8
            ).add_to(m)
    previous_row = row

m.save("trotinettes_liege_20250608.html")
print("Carte enregistrée : trotinettes_liege_20250608.html")






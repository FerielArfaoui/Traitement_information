from influxdb import InfluxDBClient
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.cluster import KMeans

# Connexion à InfluxDB
client = InfluxDBClient(
    host='localhost',
    port=8087,
    username='Feriel',
    password='admin123',
    database='events'
)

# Récupération des données de la mesure user_event
query = "SELECT * FROM user_event"
result = client.query(query)

# Conversion en DataFrame
points = list(result.get_points())
df = pd.DataFrame(points)

print(f"Nombre total de lignes chargées : {len(df)}")
print(f"Nombre total d'utilisateurs uniques : {df['user'].nunique()}\n")

# Fonction de segmentation KMeans
def kmeans_segmentation(df, features, n_clusters=3):
    df_seg = df.copy()
    X = df_seg[features]

    for col in features:
        if X[col].dtype == 'object':
            le = LabelEncoder()
            X.loc[:, col] = le.fit_transform(X[col])  # Correction du warning

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(X_scaled)
    df_seg['cluster'] = clusters

    return df_seg

# 1) Segmentation par comportement (event_type)
print("Segmentation par comportement (event_type):")
seg1 = df.groupby('user').agg({'event_type': lambda x: x.mode()[0]}).reset_index()
seg1 = kmeans_segmentation(seg1, ['event_type'], n_clusters=3)
print(f"Nombre d'utilisateurs : {seg1['user'].nunique()}")
print(f"Nombre de clusters obtenus : {seg1['cluster'].nunique()}")
print(seg1[['user', 'cluster']])
print("\n" + "-"*50 + "\n")

# 2) Segmentation par système (system)
print("Segmentation par système (system):")
seg2 = df.groupby('user').agg({'system': lambda x: x.mode()[0]}).reset_index()
seg2 = kmeans_segmentation(seg2, ['system'], n_clusters=3)
print(f"Nombre d'utilisateurs : {seg2['user'].nunique()}")
print(f"Nombre de clusters obtenus : {seg2['cluster'].nunique()}")
print(seg2[['user', 'cluster']])
print("\n" + "-"*50 + "\n")

# 3) Segmentation par durée d'écran moyenne (screen_duration)
print("Segmentation par durée d'écran moyenne:")
seg3 = df.groupby('user').agg({'screen_duration': 'mean'}).reset_index()
seg3 = kmeans_segmentation(seg3, ['screen_duration'], n_clusters=3)
print(f"Nombre d'utilisateurs : {seg3['user'].nunique()}")
print(f"Nombre de clusters obtenus : {seg3['cluster'].nunique()}")
print(seg3[['user', 'cluster']])
print("\n" + "-"*50 + "\n")

# 4) Segmentation par fabricant (manufacturer)
print("Segmentation par fabricant (manufacturer):")
if 'manufacturer' in df.columns:
    seg4 = df.groupby('user').agg({'manufacturer': lambda x: x.mode()[0]}).reset_index()
    seg4 = kmeans_segmentation(seg4, ['manufacturer'], n_clusters=3)
    print(f"Nombre d'utilisateurs : {seg4['user'].nunique()}")
    print(f"Nombre de clusters obtenus : {seg4['cluster'].nunique()}")
    print(seg4[['user', 'cluster']])
else:
    print("La colonne 'manufacturer' n'existe pas dans les données.")
print("\n" + "-"*50 + "\n")

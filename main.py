import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

# Örnek veri oluşturma
example_data = {
    "Year": [2020, 2021, 2021, 2022],
    "GTIP": [1234, 5678, 5678, 1234],
    "Product": ["Elektronik", "Otomobil", "Otomobil", "Elektronik"],
    "Country": ["Almanya", "Fransa", "Fransa", "ABD"],
    "Export_Value": [10000, 20000, 25000, 15000],
    "Import_Value": [5000, 10000, 12000, 7000],
}

df = pd.DataFrame(example_data)
df.to_csv("trade_data.csv", index=False)  # Dosyayı kaydedin

# 1. Veriyi Yükleme
# Örnek veri dosyası adını girin. Gerçek projede, CSV veya Excel dosyasından veriyi yükleyeceksiniz.
data_file = "trade_data.csv"
data = pd.read_csv(data_file)

# Veriye hızlı bir göz atma
print(data.head())

# 2. Veri Ön İşleme
# Eksik değerlerin kontrolü ve doldurulması
print(data.isnull().sum())
data.fillna(0, inplace=True)

# Verinin doğru formatta olduğunu kontrol etme
data['Year'] = pd.to_datetime(data['Year'], format='%Y')

# 3. Ürün Bazında Analiz
# GTIP kodlarına göre ihracat miktarlarının toplamı
product_exports = data.groupby(['GTIP', 'Product'])['Export_Value'].sum().reset_index()
product_exports = product_exports.sort_values(by='Export_Value', ascending=False)

# Görselleştirme: En Çok İhraç Edilen Ürünler
plt.figure(figsize=(10, 6))
plt.bar(product_exports['Product'][:10], product_exports['Export_Value'][:10], color='skyblue')
plt.title('En Çok İhraç Edilen Ürünler')
plt.xlabel('Ürün')
plt.ylabel('İhracat Değeri')
plt.xticks(rotation=45)
plt.show()

# 4. Ülkelere Göre Ticaret Hacmi Dağılımı
# Ülkelere göre toplam ticaret hacmi
country_trade = data.groupby(['Country'])[['Export_Value', 'Import_Value']].sum().reset_index()

# Görselleştirme: Harita Üzerinde Dağılım
fig = px.choropleth(
    country_trade,
    locations="Country",
    locationmode="country names",
    color="Export_Value",
    title="Ülkelere Göre İhracat Değeri",
    color_continuous_scale=px.colors.sequential.Plasma
)
fig.show()

# 5. Yıllara Göre İhracat ve İthalat Trend Grafikleri
# Yıllara göre trend analizi
yearly_trends = data.groupby(data['Year'].dt.year)[['Export_Value', 'Import_Value']].sum().reset_index()

# Görselleştirme: Çizgi Grafiği
plt.figure(figsize=(12, 6))
plt.plot(yearly_trends['Year'], yearly_trends['Export_Value'], marker='o', label='İhracat Değeri')
plt.plot(yearly_trends['Year'], yearly_trends['Import_Value'], marker='o', label='İthalat Değeri')
plt.title('Yıllara Göre İhracat ve İthalat Trendleri')
plt.xlabel('Yıl')
plt.ylabel('Değer')
plt.legend()
plt.grid(True)
plt.show()

import requests
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

headers = {
    "Origin": "https://www.mgm.gov.tr",
    "Referer": "https://www.mgm.gov.tr/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}

def mgm_hava_tahmini_grafik(sehir):
    url = f"https://servis.mgm.gov.tr/web/merkezler?il={sehir}"
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("API'den veri alınamadı.")
        return
    
    merkezler = response.json()
    if not merkezler:
        print("Şehir bulunamadı veya merkez verisi boş.")
        return
    
    ist_no = merkezler[0]['saatlikTahminIstNo']
    print("İstasyon Numarası:", ist_no)
    
    tahmin_url = f"https://servis.mgm.gov.tr/web/tahminler/saatlik?istno={ist_no}"
    tahmin_response = requests.get(tahmin_url, headers=headers)
    if tahmin_response.status_code != 200:
        print("Tahmin verisi alınamadı.")
        return
    
    tahmin_data = tahmin_response.json()
    if not tahmin_data:
        print("Tahmin verisi boş.")
        return
    
    tahminler = tahmin_data[0]['tahmin']
    
    saatler = [datetime.fromisoformat(t["tarih"].replace("Z", "+00:00")).strftime("%H:%M") for t in tahminler]
    sicakliklar = [t["sicaklik"] for t in tahminler]
    ruzgar_hizlari = [t["ruzgarHizi"] for t in tahminler]


    korelasyon = np.corrcoef(sicakliklar, ruzgar_hizlari)[0, 1]
    print(f"Sıcaklık ile rüzgar hızı arasındaki Pearson korelasyon katsayısı: {korelasyon:.3f}")
    

    fig, ax1 = plt.subplots(figsize=(10,5))
    ax1.set_xlabel("Saat (UTC)")
    ax1.set_ylabel("Sıcaklık (°C)", color="tab:red")
    ax1.plot(saatler, sicakliklar, color="tab:red", marker="o", label="Sıcaklık (°C)")
    ax1.tick_params(axis='y', labelcolor="tab:red")
    ax1.grid(True)
    
    ax2 = ax1.twinx()
    ax2.set_ylabel("Rüzgar Hızı (km/saat)", color="tab:blue")
    ax2.plot(saatler, ruzgar_hizlari, color="tab:blue", marker="x", linestyle="--", label="Rüzgar Hızı (km/saat)")
    ax2.tick_params(axis='y', labelcolor="tab:blue")
    
    plt.title(f"{sehir.capitalize()} 5 Saatlik Hava Tahmini")
    fig.tight_layout()
    plt.show()


    plt.figure(figsize=(7,5))
    plt.scatter(sicakliklar, ruzgar_hizlari, color='purple')
    plt.xlabel("Sıcaklık (°C)")
    plt.ylabel("Rüzgar Hızı (km/saat)")
    plt.title(f"{sehir.capitalize()} - Sıcaklık ve Rüzgar Hızı İlişkisi")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    while True:
        sehir_adi = input("Şehir adı giriniz (büyük harfle, örn: MALATYA) veya '0' ile çıkış yapınız: ")
        if sehir_adi == "0":
            break
        mgm_hava_tahmini_grafik(sehir_adi)

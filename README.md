# Karınca Kolonisi Algoritması ile Yol Optimizasyonu

## 📋 Proje Açıklaması

Bu proje, Antalya'nın Muratpaşa ilçesindeki bir kargo firmasının 20 farklı mağazaya en kısa rotayla ulaşması için **Karınca Kolonisi Optimizasyonu (ACO)** algoritması kullanmaktadır. Proje, Google Maps API ile gerçek yol mesafelerini hesaplayarak, Streamlit web arayüzü üzerinden interaktif bir şekilde rota optimizasyonu yapmaktadır.

## 🎯 Senaryo

**Senaryo 4:** Antalya'nın Muratpaşa ilçesindeki bir kargo firması 20 farklı mağazaya günde 1 kez uğramak zorundadır. En kısa rotayı seçiniz.

## 🚀 Özellikler

- ✅ **Google Maps API Entegrasyonu**: Gerçek yol mesafeleri (driving distance) hesaplama
- ✅ **ACO Algoritması**: En kısa rotayı bulan optimizasyon algoritması
- ✅ **İnteraktif Harita**: Folium ile rota görselleştirme
- ✅ **Yakınsama Grafiği**: Algoritmanın performansını izleme
- ✅ **Parametre Ayarlama**: Algoritma parametrelerini dinamik olarak değiştirme
- ✅ **Google Drive Entegrasyonu**: Veri setini Google Drive'dan yükleme
- ✅ **Google Colab Uyumlu**: Colab ortamında çalıştırılabilir

## 📁 Proje Yapısı

```
aco_yol_optimizasyonu/
├── main.py                      # Streamlit ana uygulama
├── config.py                    # ACO parametre ayarları
├── requirements.txt             # Gerekli kütüphaneler
├── ACO_Rota_Optimizasyonu.ipynb # Google Colab notebook
├── README.md                    # Proje dokümantasyonu
├── .gitignore                   # Git ignore dosyası
├── data/
│   └── coordinates.py          # Şehir/mağaza verileri ve Google Drive entegrasyonu
├── core/
│   ├── haversine.py            # Haversine mesafe hesaplama
│   ├── matrix_utils.py         # Mesafe matrisi oluşturma
│   └── ant_algorithm.py        # ACO algoritması
├── visual/
│   └── plotting.py             # Harita ve grafik çizimi
├── .streamlit/
│   └── secrets.toml            # Streamlit API key (örnek)
└── figure/                     # Grafik çıktıları (gitignore'da)
    ├── rota.png
    └── convergence.png
```

## 🔧 Kurulum

### 1. Gereksinimler

```bash
pip install -r requirements.txt
```

### 2. Google Maps API Key

Google Maps API key'inizi almak için:
1. [Google Cloud Console](https://console.cloud.google.com/)'a gidin
2. Yeni bir proje oluşturun veya mevcut projeyi seçin
3. "APIs & Services" > "Library" bölümünden "Distance Matrix API" ve "Maps JavaScript API"yi etkinleştirin
4. "Credentials" bölümünden API key oluşturun

### 3. API Key Yapılandırması

API key'inizi aşağıdaki yöntemlerden biriyle ekleyebilirsiniz:

**Yöntem 1: Streamlit Secrets (Önerilen)**
`.streamlit/secrets.toml` dosyasına ekleyin:
```toml
google_maps_api_key = "YOUR_API_KEY_HERE"
```

**Yöntem 2: .env Dosyası**
Proje kök dizininde `.env` dosyası oluşturun:
```
GOOGLE_MAPS_API_KEY=YOUR_API_KEY_HERE
```

**Yöntem 3: Streamlit Arayüzü**
Uygulamayı çalıştırdıktan sonra sidebar'dan API key girebilirsiniz.

## 💻 Kullanım

### Yerel Ortamda Çalıştırma

```bash
streamlit run main.py
```

Tarayıcınızda `http://localhost:8501` adresine gidin.

### Google Colab'da Çalıştırma

1. `ACO_Rota_Optimizasyonu.ipynb` dosyasını Google Colab'a yükleyin
2. Hücreleri sırayla çalıştırın
3. Google Drive bağlantısını yapın
4. API key'inizi girin
5. Streamlit uygulamasını başlatın

## 📊 Kullanım Adımları

1. **Veri Yükleme**
   - Google Drive'dan veri yükleyin veya örnek veri kullanın
   - 20 mağaza + 1 depo (başlangıç noktası) yüklenir

2. **Mesafe Matrisi Hesaplama**
   - Google Maps API ile gerçek yol mesafeleri hesaplanır
   - API key yoksa Haversine formülü kullanılır

3. **ACO Parametrelerini Ayarlama**
   - Karınca sayısı (10-200)
   - İterasyon sayısı (10-500)
   - Alpha (α): Feromon önem katsayısı
   - Beta (β): Mesafe önem katsayısı
   - Buharlaşma oranı

4. **Algoritmayı Çalıştırma**
   - "ACO Algoritmasını Çalıştır" butonuna tıklayın
   - Algoritma en kısa rotayı bulur

5. **Sonuçları İnceleme**
   - Harita üzerinde rota görselleştirmesi
   - Yakınsama grafiği
   - Rota detayları ve mesafe bilgisi

## 🧮 ACO Algoritması Parametreleri

- **Alpha (α)**: Feromon önem katsayısı. Yüksek değer, karıncaların feromon izlerini daha çok takip etmesini sağlar.
- **Beta (β)**: Mesafe önem katsayısı. Yüksek değer, kısa mesafelerin tercih edilmesini sağlar.
- **Buharlaşma Oranı**: Feromonun zamanla azalma oranı. Yüksek değer, eski çözümlerin daha hızlı unutulmasını sağlar.
- **Karınca Sayısı**: Her iterasyonda çözüm üreten karınca sayısı.
- **İterasyon Sayısı**: Algoritmanın çalışacağı toplam iterasyon sayısı.

## 📈 Sonuçlar

Proje çalıştırıldığında:
- En kısa rota harita üzerinde gösterilir
- Yakınsama grafiği oluşturulur
- Rota detayları ve mesafe bilgisi görüntülenir
- Sonuçlar `figure/` klasörüne kaydedilir

## 🔒 Güvenlik

- API key'ler `.gitignore` dosyasına eklenmiştir
- `.env` ve `.streamlit/secrets.toml` dosyaları Git'e eklenmez
- Gerçek API key'ler repository'de saklanmamalıdır

## 📚 Teknolojiler

- **Python 3.8+**
- **Streamlit**: Web arayüzü
- **Google Maps API**: Mesafe hesaplama
- **Folium**: Harita görselleştirme
- **NumPy, Pandas**: Veri işleme
- **Matplotlib**: Grafik çizimi
- **PyDrive2**: Google Drive entegrasyonu

## 🤝 Katkıda Bulunma

Bu bir öğrenci projesidir. Katkılarınız için teşekkürler!

## 📝 Lisans

Bu proje eğitim amaçlıdır.

## 👤 Yazar

[Adınız Soyadınız]
[Okul Numaranız]

## 🔗 GitHub Repository

https://github.com/kullanici_adi/aco_yol_optimizasyonu

---

**Not:** Bu proje, Yapay Zeka Sistemleri dersi kapsamında hazırlanmıştır.



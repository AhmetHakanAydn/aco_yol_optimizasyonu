"""
Streamlit Ana Uygulama
Antalya Muratpaşa Kargo Firması Rota Optimizasyonu
Google Colab uyumlu
"""
import streamlit as st
import numpy as np
import pandas as pd
import os
import sys
from pathlib import Path

# Proje yollarını ekle
sys.path.append(str(Path(__file__).parent))

from data.coordinates import load_data_from_drive, get_coordinates_from_dataframe, create_sample_data
from core.matrix_utils import calculate_distance_matrix_google_maps, calculate_distance_matrix_haversine, get_api_key
from core.ant_algorithm import AntColonyOptimizer
from visual.plotting import create_route_map, plot_convergence
import config

# Sayfa yapılandırması
st.set_page_config(
    page_title="ACO Rota Optimizasyonu",
    page_icon="🐜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Başlık
st.title("🐜 Karınca Kolonisi Algoritması ile Rota Optimizasyonu")
st.markdown("### Antalya Muratpaşa Kargo Firması - 20 Mağaza Rota Optimizasyonu")

# Sidebar - Parametreler
st.sidebar.header("⚙️ Algoritma Parametreleri")

# ACO Parametreleri
n_ants = st.sidebar.slider("Karınca Sayısı", min_value=10, max_value=200, 
                          value=config.DEFAULT_ANT_COUNT, step=10)
n_iterations = st.sidebar.slider("İterasyon Sayısı", min_value=10, max_value=500, 
                                 value=config.DEFAULT_ITERATIONS, step=10)
alpha = st.sidebar.slider("Alpha (α) - Feromon Önemi", min_value=0.1, max_value=5.0, 
                         value=config.DEFAULT_ALPHA, step=0.1)
beta = st.sidebar.slider("Beta (β) - Mesafe Önemi", min_value=0.1, max_value=5.0, 
                        value=config.DEFAULT_BETA, step=0.1)
evaporation_rate = st.sidebar.slider("Buharlaşma Oranı", min_value=0.1, max_value=0.9, 
                                    value=config.DEFAULT_EVAPORATION_RATE, step=0.05)

# Google Maps API Key girişi
st.sidebar.header("🔑 API Ayarları")
api_key_input = st.sidebar.text_input("Google Maps API Key", type="password", 
                                      help="API key'inizi girin (opsiyonel - Haversine kullanılabilir)")

# Veri yükleme seçenekleri
st.sidebar.header("📊 Veri Kaynağı")
data_source = st.sidebar.radio(
    "Veri kaynağını seçin:",
    ["Google Drive", "Örnek Veri (Demo)"],
    help="Google Drive'dan veri yüklemek için kimlik doğrulama gerekebilir"
)

# Ana içerik
tab1, tab2, tab3 = st.tabs(["🗺️ Harita ve Rota", "📈 Yakınsama Grafiği", "ℹ️ Bilgiler"])

with tab1:
    st.header("Rota Optimizasyonu")
    
    # Veri yükleme
    if 'data_loaded' not in st.session_state:
        st.session_state.data_loaded = False
        st.session_state.df = None
        st.session_state.coordinates = None
        st.session_state.names = None
        st.session_state.distance_matrix = None
    
    if st.button("🔄 Veriyi Yükle", type="primary"):
        with st.spinner("Veri yükleniyor..."):
            try:
                if data_source == "Google Drive":
                    df = load_data_from_drive(config.GOOGLE_DRIVE_FOLDER_ID)
                else:
                    df = create_sample_data()
                
                names, latitudes, longitudes = get_coordinates_from_dataframe(df)
                coordinates = list(zip(latitudes, longitudes))
                
                st.session_state.df = df
                st.session_state.coordinates = coordinates
                st.session_state.names = names
                st.session_state.data_loaded = True
                
                st.success(f"✅ {len(coordinates)} nokta yüklendi!")
                st.dataframe(df.head(10))
                
            except Exception as e:
                st.error(f"Veri yükleme hatası: {e}")
                st.info("Örnek veri kullanılıyor...")
                df = create_sample_data()
                names, latitudes, longitudes = get_coordinates_from_dataframe(df)
                coordinates = list(zip(latitudes, longitudes))
                st.session_state.df = df
                st.session_state.coordinates = coordinates
                st.session_state.names = names
                st.session_state.data_loaded = True
    
    # Mesafe matrisi hesaplama
    if st.session_state.data_loaded and st.session_state.distance_matrix is None:
        if st.button("📏 Mesafe Matrisini Hesapla"):
            with st.spinner("Mesafe matrisi hesaplanıyor (bu işlem biraz zaman alabilir)..."):
                try:
                    # API key kontrolü
                    if api_key_input:
                        os.environ['GOOGLE_MAPS_API_KEY'] = api_key_input
                        client = None
                        try:
                            from core.matrix_utils import initialize_google_maps_client
                            client = initialize_google_maps_client()
                            distance_matrix, duration_matrix = calculate_distance_matrix_google_maps(
                                st.session_state.coordinates, client
                            )
                            st.success("✅ Google Maps API ile mesafe matrisi oluşturuldu!")
                        except Exception as e:
                            st.warning(f"Google Maps API hatası: {e}. Haversine formülü kullanılıyor...")
                            from core.matrix_utils import calculate_distance_matrix_haversine
                            distance_matrix = calculate_distance_matrix_haversine(st.session_state.coordinates)
                    else:
                        st.info("API key girilmedi. Haversine formülü kullanılıyor...")
                        from core.matrix_utils import calculate_distance_matrix_haversine
                        distance_matrix = calculate_distance_matrix_haversine(st.session_state.coordinates)
                    
                    st.session_state.distance_matrix = distance_matrix
                    st.success("✅ Mesafe matrisi hazır!")
                    
                except Exception as e:
                    st.error(f"Mesafe matrisi hesaplama hatası: {e}")
    
    # ACO algoritmasını çalıştır
    if st.session_state.data_loaded and st.session_state.distance_matrix is not None:
        if st.button("🚀 ACO Algoritmasını Çalıştır", type="primary"):
            with st.spinner("ACO algoritması çalışıyor..."):
                try:
                    # ACO optimizer oluştur
                    optimizer = AntColonyOptimizer(
                        distance_matrix=st.session_state.distance_matrix,
                        n_ants=n_ants,
                        n_iterations=n_iterations,
                        alpha=alpha,
                        beta=beta,
                        evaporation_rate=evaporation_rate
                    )
                    
                    # Algoritmayı çalıştır
                    best_path, best_distance, iteration_distances = optimizer.solve(start_city=0)
                    
                    # Sonuçları session state'e kaydet
                    st.session_state.best_path = best_path
                    st.session_state.best_distance = best_distance
                    st.session_state.iteration_distances = iteration_distances
                    
                    st.success(f"✅ Algoritma tamamlandı! En kısa rota: {best_distance:.2f} km")
                    
                except Exception as e:
                    st.error(f"Algoritma hatası: {e}")
    
    # Sonuçları göster
    if 'best_path' in st.session_state and st.session_state.best_path is not None:
        st.subheader("📍 En Kısa Rota")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Harita oluştur
            route_map = create_route_map(
                st.session_state.coordinates,
                st.session_state.best_path,
                st.session_state.names,
                st.session_state.best_distance
            )
            st_folium(route_map, width=700, height=500)
        
        with col2:
            st.metric("Toplam Mesafe", f"{st.session_state.best_distance:.2f} km")
            st.metric("Ziyaret Edilen Nokta", len(st.session_state.best_path) - 1)
            
            # Rota detayları
            st.subheader("Rota Sırası")
            route_details = []
            for i, city_idx in enumerate(st.session_state.best_path):
                if i < len(st.session_state.best_path) - 1:
                    route_details.append({
                        'Sıra': i + 1,
                        'Mağaza': st.session_state.names[city_idx],
                        'Koordinat': f"({st.session_state.coordinates[city_idx][0]:.4f}, {st.session_state.coordinates[city_idx][1]:.4f})"
                    })
            st.dataframe(pd.DataFrame(route_details))

with tab2:
    st.header("Yakınsama Grafiği")
    
    if 'iteration_distances' in st.session_state and st.session_state.iteration_distances:
        # Grafik oluştur
        fig = plot_convergence(st.session_state.iteration_distances)
        
        # Streamlit'te göster
        import matplotlib.pyplot as plt
        plt.figure(figsize=(10, 6))
        plt.plot(range(1, len(st.session_state.iteration_distances) + 1), 
                st.session_state.iteration_distances, 
                linewidth=2, color='blue', marker='o', markersize=3)
        plt.xlabel('İterasyon', fontsize=12, fontweight='bold')
        plt.ylabel('En İyi Mesafe (km)', fontsize=12, fontweight='bold')
        plt.title('ACO Algoritması Yakınsama Grafiği', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        st.pyplot(plt)
        plt.close()
        
        # İstatistikler
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Başlangıç Mesafe", f"{st.session_state.iteration_distances[0]:.2f} km")
        with col2:
            st.metric("Bitiş Mesafe", f"{st.session_state.iteration_distances[-1]:.2f} km")
        with col3:
            improvement = ((st.session_state.iteration_distances[0] - st.session_state.iteration_distances[-1]) / 
                          st.session_state.iteration_distances[0]) * 100
            st.metric("İyileşme", f"{improvement:.2f}%")
        with col4:
            st.metric("Toplam İterasyon", len(st.session_state.iteration_distances))
    else:
        st.info("Lütfen önce algoritmayı çalıştırın.")

with tab3:
    st.header("Proje Hakkında")
    
    st.markdown("""
    ### 📋 Proje Açıklaması
    
    Bu proje, Antalya'nın Muratpaşa ilçesindeki bir kargo firmasının 20 farklı mağazaya 
    en kısa rotayla ulaşması için Karınca Kolonisi Optimizasyonu (ACO) algoritması kullanmaktadır.
    
    ### 🎯 Özellikler
    
    - **Google Maps API Entegrasyonu**: Gerçek yol mesafeleri hesaplama
    - **ACO Algoritması**: En kısa rotayı bulan optimizasyon algoritması
    - **İnteraktif Harita**: Folium ile rota görselleştirme
    - **Yakınsama Grafiği**: Algoritmanın performansını izleme
    - **Parametre Ayarlama**: Algoritma parametrelerini dinamik olarak değiştirme
    
    ### 🔧 Kullanım
    
    1. **Veri Yükleme**: Google Drive'dan veya örnek veri ile başlayın
    2. **Mesafe Matrisi**: Google Maps API veya Haversine formülü ile hesaplayın
    3. **Algoritma Çalıştırma**: Parametreleri ayarlayıp ACO'yu çalıştırın
    4. **Sonuçları İnceleme**: Harita ve grafiklerde sonuçları görüntüleyin
    
    ### 📚 Teknolojiler
    
    - Python 3.8+
    - Streamlit (Web Arayüzü)
    - Google Maps API (Mesafe Hesaplama)
    - Folium (Harita Görselleştirme)
    - NumPy, Pandas (Veri İşleme)
    - Matplotlib (Grafik Çizimi)
    """)
    
    st.subheader("📊 Mevcut Durum")
    if st.session_state.data_loaded:
        st.success(f"✅ {len(st.session_state.coordinates)} nokta yüklendi")
    else:
        st.warning("⚠️ Henüz veri yüklenmedi")
    
    if st.session_state.distance_matrix is not None:
        st.success("✅ Mesafe matrisi hazır")
    else:
        st.warning("⚠️ Mesafe matrisi henüz hesaplanmadı")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("### 📝 Notlar")
st.sidebar.info(
    "Google Maps API kullanmak için API key gerekir. "
    "API key olmadan Haversine formülü kullanılacaktır."
)



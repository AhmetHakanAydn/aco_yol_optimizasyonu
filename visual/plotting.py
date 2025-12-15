"""
Görselleştirme fonksiyonları
Harita çizimi ve grafik oluşturma
"""
import folium
import matplotlib.pyplot as plt
import numpy as np
from streamlit_folium import st_folium

def create_route_map(coordinates, path, names, best_distance):
    """
    Folium haritası üzerinde rotayı çizer
    
    Args:
        coordinates: [(lat, lon), ...] formatında koordinat listesi
        path: Şehir ziyaret sırası (indeks listesi)
        names: Şehir/mağaza isimleri
        best_distance: En iyi mesafe (km)
    
    Returns:
        folium.Map: Harita nesnesi
    """
    # Harita merkezini belirle
    center_lat = np.mean([coord[0] for coord in coordinates])
    center_lon = np.mean([coord[1] for coord in coordinates])
    
    # Harita oluştur
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=12,
        tiles='OpenStreetMap'
    )
    
    # Rota çizgisi için koordinatlar
    route_coords = [coordinates[i] for i in path]
    
    # Rota çizgisini ekle
    folium.PolyLine(
        route_coords,
        color='blue',
        weight=4,
        opacity=0.7,
        popup=f'En Kısa Rota: {best_distance:.2f} km'
    ).add_to(m)
    
    # Her noktayı işaretle
    for i, (coord, name) in enumerate(zip(coordinates, names)):
        # Başlangıç noktası (depo) farklı renkte
        if i == path[0]:
            color = 'red'
            icon = 'home'
            popup_text = f'<b>{name}</b><br>Depo (Başlangıç)'
        else:
            color = 'green'
            icon = 'shopping-cart'
            popup_text = f'<b>{name}</b><br>Sıra: {path.index(i) if i in path else "N/A"}'
        
        folium.Marker(
            location=coord,
            popup=folium.Popup(popup_text, max_width=200),
            icon=folium.Icon(color=color, icon=icon, prefix='fa'),
            tooltip=name
        ).add_to(m)
    
    # Harita başlığı
    title_html = f'''
    <h3 align="center" style="font-size:20px">
        <b>En Kısa Rota: {best_distance:.2f} km</b>
    </h3>
    '''
    m.get_root().html.add_child(folium.Element(title_html))
    
    return m

def plot_convergence(iteration_distances, save_path='figure/convergence.png'):
    """
    İterasyonlara göre mesafe değişimini grafikle gösterir
    
    Args:
        iteration_distances: Her iterasyondaki en iyi mesafe listesi
        save_path: Grafik kayıt yolu
    """
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, len(iteration_distances) + 1), iteration_distances, 
             linewidth=2, color='blue', marker='o', markersize=3)
    plt.xlabel('İterasyon', fontsize=12, fontweight='bold')
    plt.ylabel('En İyi Mesafe (km)', fontsize=12, fontweight='bold')
    plt.title('ACO Algoritması Yakınsama Grafiği', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Grafik kaydet
    import os
    os.makedirs(os.path.dirname(save_path) if os.path.dirname(save_path) else '.', exist_ok=True)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return plt

def plot_route_comparison(coordinates, paths, distances, names):
    """
    Birden fazla rotayı karşılaştırmalı gösterir
    
    Args:
        coordinates: Koordinat listesi
        paths: Rota listesi (her biri bir çözüm)
        distances: Mesafe listesi
        names: Şehir isimleri
    """
    fig, axes = plt.subplots(1, len(paths), figsize=(15, 5))
    if len(paths) == 1:
        axes = [axes]
    
    for idx, (path, distance) in enumerate(zip(paths, distances)):
        ax = axes[idx]
        
        # Koordinatları çiz
        route_coords = [coordinates[i] for i in path]
        lats = [coord[0] for coord in route_coords]
        lons = [coord[1] for coord in route_coords]
        
        ax.plot(lons, lats, 'o-', linewidth=2, markersize=8, label='Rota')
        ax.scatter(lons[0], lats[0], c='red', s=200, marker='s', 
                  label='Başlangıç', zorder=5)
        
        ax.set_xlabel('Boylam', fontsize=10)
        ax.set_ylabel('Enlem', fontsize=10)
        ax.set_title(f'Rota {idx+1}: {distance:.2f} km', fontsize=11, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend()
    
    plt.tight_layout()
    return fig



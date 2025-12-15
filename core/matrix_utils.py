"""
Mesafe matrisi oluşturma ve yönetim fonksiyonları
Google Maps API kullanarak driving distance hesaplama
"""
import googlemaps
import numpy as np
import pandas as pd
from config import GOOGLE_MAPS_API_KEY
import os
from dotenv import load_dotenv
import streamlit as st

# .env dosyasını yükle
load_dotenv()

def get_api_key():
    """API anahtarını farklı kaynaklardan al"""
    # Önce Streamlit secrets'tan dene
    try:
        if hasattr(st, 'secrets') and 'google_maps_api_key' in st.secrets:
            return st.secrets['google_maps_api_key']
    except:
        pass
    
    # Sonra .env dosyasından dene
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    if api_key:
        return api_key
    
    # Son olarak config'den dene
    if GOOGLE_MAPS_API_KEY:
        return GOOGLE_MAPS_API_KEY
    
    return None

def initialize_google_maps_client():
    """Google Maps API istemcisini başlat"""
    api_key = get_api_key()
    if not api_key:
        raise ValueError(
            "Google Maps API anahtarı bulunamadı. "
            "Lütfen .streamlit/secrets.toml veya .env dosyasına ekleyin."
        )
    return googlemaps.Client(key=api_key)

def calculate_distance_matrix_google_maps(coordinates, client=None):
    """
    Google Maps API kullanarak mesafe matrisi oluşturur
    
    Args:
        coordinates: [(lat, lon), ...] formatında koordinat listesi
        client: Google Maps API istemcisi (None ise yeni oluşturulur)
    
    Returns:
        numpy.ndarray: Mesafe matrisi (km cinsinden)
        numpy.ndarray: Süre matrisi (saniye cinsinden)
    """
    if client is None:
        client = initialize_google_maps_client()
    
    n = len(coordinates)
    distance_matrix = np.zeros((n, n))
    duration_matrix = np.zeros((n, n))
    
    # Koordinatları string formatına çevir
    origins = [f"{lat},{lon}" for lat, lon in coordinates]
    destinations = origins.copy()
    
    # Google Maps API'de maksimum 25 origin/destination desteklenir
    # Büyük matrisler için batch işleme
    batch_size = 25
    
    for i in range(0, n, batch_size):
        batch_origins = origins[i:min(i+batch_size, n)]
        
        for j in range(0, n, batch_size):
            batch_destinations = destinations[j:min(j+batch_size, n)]
            
            try:
                # Distance Matrix API çağrısı
                result = client.distance_matrix(
                    origins=batch_origins,
                    destinations=batch_destinations,
                    mode="driving",
                    units="metric",
                    language="tr"
                )
                
                # Sonuçları matrise yaz
                for idx_i, row in enumerate(result['rows']):
                    for idx_j, element in enumerate(row['elements']):
                        if element['status'] == 'OK':
                            distance_matrix[i + idx_i, j + idx_j] = element['distance']['value'] / 1000.0  # km
                            duration_matrix[i + idx_i, j + idx_j] = element['duration']['value']  # saniye
                        else:
                            # Hata durumunda Haversine mesafesi kullan
                            from core.haversine import haversine_distance
                            dist = haversine_distance(
                                coordinates[i + idx_i],
                                coordinates[j + idx_j]
                            )
                            distance_matrix[i + idx_i, j + idx_j] = dist
                            duration_matrix[i + idx_i, j + idx_j] = dist * 60  # Yaklaşık süre (km başına 1 dakika)
            
            except Exception as e:
                print(f"API hatası (i={i}, j={j}): {e}")
                # Hata durumunda Haversine kullan
                from core.haversine import haversine_distance
                for idx_i in range(len(batch_origins)):
                    for idx_j in range(len(batch_destinations)):
                        dist = haversine_distance(
                            coordinates[i + idx_i],
                            coordinates[j + idx_j]
                        )
                        distance_matrix[i + idx_i, j + idx_j] = dist
                        duration_matrix[i + idx_i, j + idx_j] = dist * 60
    
    return distance_matrix, duration_matrix

def calculate_distance_matrix_haversine(coordinates):
    """
    Haversine formülü kullanarak mesafe matrisi oluşturur (fallback)
    
    Args:
        coordinates: [(lat, lon), ...] formatında koordinat listesi
    
    Returns:
        numpy.ndarray: Mesafe matrisi (km cinsinden)
    """
    from core.haversine import haversine_distance
    
    n = len(coordinates)
    distance_matrix = np.zeros((n, n))
    
    for i in range(n):
        for j in range(n):
            if i != j:
                distance_matrix[i, j] = haversine_distance(coordinates[i], coordinates[j])
    
    return distance_matrix

def save_distance_matrix(distance_matrix, filename='distance_matrix.npy'):
    """Mesafe matrisini kaydet"""
    np.save(filename, distance_matrix)

def load_distance_matrix(filename='distance_matrix.npy'):
    """Mesafe matrisini yükle"""
    return np.load(filename)



"""
Haversine formülü ile mesafe hesaplama
Google Maps API kullanılamadığında fallback olarak kullanılır
"""
import numpy as np

def haversine_distance(coord1, coord2):
    """
    İki koordinat arasındaki mesafeyi Haversine formülü ile hesaplar
    
    Args:
        coord1: (latitude, longitude) tuple
        coord2: (latitude, longitude) tuple
    
    Returns:
        float: Mesafe (kilometre cinsinden)
    """
    # Dünya yarıçapı (km)
    R = 6371.0
    
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    
    # Dereceleri radyana çevir
    lat1_rad = np.radians(lat1)
    lon1_rad = np.radians(lon1)
    lat2_rad = np.radians(lat2)
    lon2_rad = np.radians(lon2)
    
    # Farklar
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    # Haversine formülü
    a = np.sin(dlat / 2)**2 + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(dlon / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    
    distance = R * c
    
    return distance



"""
Google Drive'dan mağaza koordinatlarını yükleyen modül
Antalya Muratpaşa ilçesindeki 20 mağaza için
"""
import pandas as pd
import numpy as np
import os

# Google Colab kontrolü
try:
    import google.colab
    IN_COLAB = True
except ImportError:
    IN_COLAB = False

if not IN_COLAB:
    try:
        from pydrive2.auth import GoogleAuth
        from pydrive2.drive import GoogleDrive
    except ImportError:
        GoogleAuth = None
        GoogleDrive = None

def authenticate_google_drive():
    """Google Drive kimlik doğrulaması"""
    if IN_COLAB:
        # Colab'da Google Drive zaten mount edilmiş
        return None
    
    if GoogleAuth is None or GoogleDrive is None:
        raise ImportError("PyDrive2 kütüphanesi yüklü değil")
    
    gauth = GoogleAuth()
    # Colab ortamında otomatik kimlik doğrulama
    gauth.LoadCredentialsFile("credentials.json")
    if gauth.credentials is None:
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()
    gauth.SaveCredentialsFile("credentials.json")
    return GoogleDrive(gauth)

def load_data_from_drive(folder_id, filename=None):
    """
    Google Drive'dan veri yükler
    
    Args:
        folder_id: Google Drive klasör ID'si
        filename: Yüklenecek dosya adı (None ise tüm CSV/Excel dosyalarını arar)
    
    Returns:
        pandas.DataFrame: Yüklenen veri
    """
    try:
        if IN_COLAB:
            # Colab'da Google Drive mount edilmişse doğrudan dosya yolu kullan
            drive_path = f"/content/drive/MyDrive"
            # Klasör ID'sinden dosya yolu oluşturulamaz, bu yüzden PyDrive kullan
            # Alternatif: Kullanıcı dosyayı manuel olarak yükleyebilir
            print("Colab ortamında Google Drive API kullanılıyor...")
        
        drive = authenticate_google_drive()
        
        if drive is None and IN_COLAB:
            # Colab'da PyDrive kullan
            try:
                from pydrive2.auth import GoogleAuth
                from pydrive2.drive import GoogleDrive
                gauth = GoogleAuth()
                gauth.LoadClientConfigFile("client_secrets.json")
                gauth.LocalWebserverAuth()
                drive = GoogleDrive(gauth)
            except:
                print("Google Drive API kimlik doğrulaması başarısız. Örnek veri kullanılıyor.")
                return create_sample_data()
        
        if drive is None:
            raise ValueError("Google Drive bağlantısı kurulamadı")
        
        # Klasördeki dosyaları listele
        file_list = drive.ListFile({'q': f"'{folder_id}' in parents and trashed=false"}).GetList()
        
        if filename:
            # Belirli bir dosya aranıyor
            for file in file_list:
                if file['title'] == filename:
                    file.GetContentFile(file['title'])
                    if filename.endswith('.csv'):
                        return pd.read_csv(filename)
                    elif filename.endswith(('.xlsx', '.xls')):
                        return pd.read_excel(filename)
        else:
            # İlk CSV veya Excel dosyasını bul
            for file in file_list:
                if file['title'].endswith(('.csv', '.xlsx', '.xls')):
                    file.GetContentFile(file['title'])
                    if file['title'].endswith('.csv'):
                        return pd.read_csv(file['title'])
                    elif file['title'].endswith(('.xlsx', '.xls')):
                        return pd.read_excel(file['title'])
        
        raise FileNotFoundError("Google Drive'da uygun bir veri dosyası bulunamadı")
    
    except Exception as e:
        print(f"Google Drive'dan veri yüklenirken hata: {e}")
        print("Örnek veri kullanılıyor...")
        # Fallback: Örnek veri oluştur
        return create_sample_data()

def create_sample_data():
    """
    Örnek mağaza verisi oluşturur (Google Drive erişimi yoksa)
    Antalya Muratpaşa ilçesinde 20 mağaza için örnek koordinatlar
    """
    # Antalya Muratpaşa merkez koordinatları: 36.8841, 30.7056
    center_lat, center_lon = 36.8841, 30.7056
    
    # 20 mağaza için rastgele koordinatlar oluştur (Muratpaşa sınırları içinde)
    np.random.seed(42)
    n_stores = 20
    
    # Muratpaşa ilçesi yaklaşık 0.1 derece (10km) yarıçapında
    stores = []
    for i in range(n_stores):
        # Merkez etrafında rastgele koordinatlar
        lat = center_lat + np.random.uniform(-0.05, 0.05)
        lon = center_lon + np.random.uniform(-0.05, 0.05)
        stores.append({
            'id': i + 1,
            'name': f'Mağaza {i + 1}',
            'latitude': lat,
            'longitude': lon,
            'address': f'Muratpaşa, Antalya - Mağaza {i + 1}'
        })
    
    # Depo/başlangıç noktası (Muratpaşa merkez)
    stores.insert(0, {
        'id': 0,
        'name': 'Depo (Başlangıç)',
        'latitude': center_lat,
        'longitude': center_lon,
        'address': 'Muratpaşa, Antalya - Depo'
    })
    
    return pd.DataFrame(stores)

def get_coordinates_from_dataframe(df):
    """
    DataFrame'den koordinatları çıkarır
    
    Args:
        df: Mağaza bilgilerini içeren DataFrame
    
    Returns:
        tuple: (names, latitudes, longitudes) listeleri
    """
    # Koordinat sütunlarını bul (farklı isimler olabilir)
    lat_col = None
    lon_col = None
    name_col = None
    
    for col in df.columns:
        col_lower = col.lower()
        if 'lat' in col_lower or 'enlem' in col_lower:
            lat_col = col
        elif 'lon' in col_lower or 'boylam' in col_lower or 'lng' in col_lower:
            lon_col = col
        elif 'name' in col_lower or 'isim' in col_lower or 'mağaza' in col_lower:
            name_col = col
    
    if lat_col is None or lon_col is None:
        raise ValueError("DataFrame'de koordinat sütunları bulunamadı")
    
    names = df[name_col].values if name_col else [f"Mağaza {i+1}" for i in range(len(df))]
    latitudes = df[lat_col].values
    longitudes = df[lon_col].values
    
    return names, latitudes, longitudes


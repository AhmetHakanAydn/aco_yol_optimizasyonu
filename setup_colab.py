"""
Google Colab için otomatik kurulum scripti
Bu dosyayı Colab'da çalıştırarak projeyi hızlıca kurabilirsiniz
"""
import os
import subprocess
import sys

def install_requirements():
    """Gerekli kütüphaneleri yükle"""
    print("📦 Gerekli kütüphaneler yükleniyor...")
    subprocess.check_call([
        sys.executable, "-m", "pip", "install", "-q",
        "streamlit", "googlemaps", "pandas", "numpy", 
        "matplotlib", "folium", "streamlit-folium", 
        "python-dotenv", "PyDrive2", "pyngrok"
    ])
    print("✅ Kütüphaneler yüklendi!")

def setup_directories():
    """Gerekli klasörleri oluştur"""
    print("📁 Klasörler oluşturuluyor...")
    directories = ['figure', 'data', 'core', 'visual', '.streamlit']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    print("✅ Klasörler oluşturuldu!")

def check_google_drive():
    """Google Drive bağlantısını kontrol et"""
    print("🔍 Google Drive bağlantısı kontrol ediliyor...")
    if os.path.exists('/content/drive'):
        print("✅ Google Drive bağlı!")
        return True
    else:
        print("⚠️ Google Drive bağlı değil. Lütfen drive.mount('/content/drive') çalıştırın.")
        return False

if __name__ == "__main__":
    print("🚀 Google Colab Kurulum Başlatılıyor...\n")
    
    install_requirements()
    setup_directories()
    check_google_drive()
    
    print("\n✅ Kurulum tamamlandı!")
    print("\n📝 Sonraki adımlar:")
    print("1. Google Drive'ı bağlayın: drive.mount('/content/drive')")
    print("2. API key'inizi ayarlayın")
    print("3. main.py'yi çalıştırın veya notebook'u kullanın")



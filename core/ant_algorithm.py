"""
Karınca Kolonisi Optimizasyonu (ACO) Algoritması
TSP (Traveling Salesman Problem) için uygulama
"""
import numpy as np
import random

class AntColonyOptimizer:
    """
    Karınca Kolonisi Optimizasyonu sınıfı
    """
    
    def __init__(self, distance_matrix, n_ants=50, n_iterations=100, 
                 alpha=1.0, beta=2.0, evaporation_rate=0.5, q=100):
        """
        Args:
            distance_matrix: Mesafe matrisi (n x n)
            n_ants: Karınca sayısı
            n_iterations: İterasyon sayısı
            alpha: Feromon önem katsayısı
            beta: Mesafe önem katsayısı
            evaporation_rate: Feromon buharlaşma oranı
            q: Feromon miktarı sabiti
        """
        self.distance_matrix = np.array(distance_matrix)
        self.n_cities = len(distance_matrix)
        self.n_ants = n_ants
        self.n_iterations = n_iterations
        self.alpha = alpha
        self.beta = beta
        self.evaporation_rate = evaporation_rate
        self.q = q
        
        # Feromon matrisi (başlangıçta küçük bir değer)
        self.pheromone = np.ones((self.n_cities, self.n_cities)) * 0.1
        
        # En iyi çözüm
        self.best_path = None
        self.best_distance = float('inf')
        
        # İterasyon geçmişi (görselleştirme için)
        self.iteration_distances = []
        
    def calculate_probability(self, current_city, unvisited_cities):
        """
        Bir sonraki şehir seçme olasılıklarını hesaplar
        
        Args:
            current_city: Mevcut şehir indeksi
            unvisited_cities: Ziyaret edilmemiş şehirler listesi
        
        Returns:
            numpy.ndarray: Olasılık vektörü
        """
        if len(unvisited_cities) == 0:
            return np.array([])
        
        probabilities = np.zeros(len(unvisited_cities))
        
        for idx, city in enumerate(unvisited_cities):
            # Feromon değeri
            pheromone_value = self.pheromone[current_city, city] ** self.alpha
            
            # Mesafe değeri (küçük mesafe = yüksek tercih)
            distance_value = (1.0 / (self.distance_matrix[current_city, city] + 1e-10)) ** self.beta
            
            probabilities[idx] = pheromone_value * distance_value
        
        # Normalize et
        total = np.sum(probabilities)
        if total > 0:
            probabilities = probabilities / total
        else:
            probabilities = np.ones(len(unvisited_cities)) / len(unvisited_cities)
        
        return probabilities
    
    def select_next_city(self, current_city, unvisited_cities):
        """
        Olasılıklara göre bir sonraki şehri seçer
        
        Args:
            current_city: Mevcut şehir indeksi
            unvisited_cities: Ziyaret edilmemiş şehirler listesi
        
        Returns:
            int: Seçilen şehir indeksi
        """
        probabilities = self.calculate_probability(current_city, unvisited_cities)
        
        if len(probabilities) == 0:
            return None
        
        # Rastgele seçim (olasılıklara göre)
        return np.random.choice(unvisited_cities, p=probabilities)
    
    def construct_solution(self, start_city=0):
        """
        Bir karınca için çözüm oluşturur
        
        Args:
            start_city: Başlangıç şehri indeksi (depo)
        
        Returns:
            list: Şehir ziyaret sırası
            float: Toplam mesafe
        """
        path = [start_city]
        unvisited = list(range(self.n_cities))
        unvisited.remove(start_city)
        current_city = start_city
        
        # Tüm şehirleri ziyaret et
        while len(unvisited) > 0:
            next_city = self.select_next_city(current_city, unvisited)
            if next_city is None:
                break
            path.append(next_city)
            unvisited.remove(next_city)
            current_city = next_city
        
        # Depoya geri dön
        path.append(start_city)
        
        # Toplam mesafeyi hesapla
        total_distance = 0
        for i in range(len(path) - 1):
            total_distance += self.distance_matrix[path[i], path[i + 1]]
        
        return path, total_distance
    
    def update_pheromone(self, paths, distances):
        """
        Feromon matrisini günceller
        
        Args:
            paths: Tüm karıncaların yolları
            distances: Tüm karıncaların mesafeleri
        """
        # Buharlaşma
        self.pheromone *= (1 - self.evaporation_rate)
        
        # Her karınca için feromon bırakma
        for path, distance in zip(paths, distances):
            if distance > 0:
                pheromone_deposit = self.q / distance
                for i in range(len(path) - 1):
                    self.pheromone[path[i], path[i + 1]] += pheromone_deposit
    
    def solve(self, start_city=0):
        """
        ACO algoritmasını çalıştırır
        
        Args:
            start_city: Başlangıç şehri indeksi (depo)
        
        Returns:
            list: En iyi yol
            float: En iyi mesafe
            list: İterasyon geçmişi
        """
        for iteration in range(self.n_iterations):
            # Tüm karıncalar için çözüm oluştur
            paths = []
            distances = []
            
            for ant in range(self.n_ants):
                path, distance = self.construct_solution(start_city)
                paths.append(path)
                distances.append(distance)
                
                # En iyi çözümü güncelle
                if distance < self.best_distance:
                    self.best_distance = distance
                    self.best_path = path.copy()
            
            # Feromon güncelle
            self.update_pheromone(paths, distances)
            
            # İterasyon geçmişi
            iteration_best = min(distances)
            self.iteration_distances.append(iteration_best)
            
            # İlerleme bilgisi (her 10 iterasyonda bir)
            if (iteration + 1) % 10 == 0:
                print(f"İterasyon {iteration + 1}/{self.n_iterations}: En iyi mesafe = {self.best_distance:.2f} km")
        
        return self.best_path, self.best_distance, self.iteration_distances



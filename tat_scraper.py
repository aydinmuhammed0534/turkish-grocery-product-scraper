#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TAT Ürün Görselleri Çekici
Bu script TAT'ın ürün sayfalarındaki tüm ürün görsellerini kategorilere göre indirir.
"""

import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin, urlparse
import time
from pathlib import Path
import mimetypes
import json
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class TatScraper:
    def __init__(self, base_url="https://www.tat.com.tr/"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
        })
        
        # Çıktı dizini oluştur
        self.output_dir = Path("tat_images")
        self.output_dir.mkdir(exist_ok=True)
        
        # TAT ürün kategorileri
        self.categories = {
            'salca': 'Salça',
            'domates_urunleri': 'Domates Ürünleri',
            'soslar': 'Soslar',
            'corba': 'Çorba',
            'organik_urunler': 'Organik Ürünler',
            'sebze_konservesi': 'Sebze Konservesi',
            'haslanmis_urunler': 'Haşlanmış Ürünler',
            'hazir_yemek': 'Hazır Yemek',
            'meze_soslar': 'Meze ve Ekmek Üstü Soslar',
            'tursu': 'Turşu',
            'recel_marmelat': 'Reçel & Marmelat',
            'genel': 'Genel'
        }
        
        # Kategori dizinleri oluştur
        for category_key in self.categories.keys():
            category_dir = self.output_dir / category_key
            category_dir.mkdir(exist_ok=True)
        
    def setup_driver(self):
        """Chrome WebDriver'ı kurar"""
        options = Options()
        options.add_argument('--headless')  # Tarayıcıyı görünmez modda çalıştır
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')
        
        try:
            driver = webdriver.Chrome(options=options)
            return driver
        except Exception as e:
            print(f"Chrome WebDriver kurulamadı: {e}")
            print("Lütfen ChromeDriver'ın yüklü olduğundan emin olun.")
            return None
    
    def get_category_urls(self, driver):
        """Kategori URL'lerini toplar"""
        category_urls = {}
        
        try:
            print("Ana sayfa yükleniyor...")
            driver.get(self.base_url)
            time.sleep(3)
            
            # Ürünler menüsüne hover yapma
            try:
                products_menu = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'tat Ürünleri') or contains(text(), 'Ürünler')]"))
                )
                driver.execute_script("arguments[0].scrollIntoView(true);", products_menu)
                
                # JavaScript ile hover simülasyonu
                driver.execute_script("""
                    var event = new MouseEvent('mouseover', {
                        view: window,
                        bubbles: true,
                        cancelable: true
                    });
                    arguments[0].dispatchEvent(event);
                """, products_menu)
                
                time.sleep(2)
                
                print("Ürünler menüsü açıldı, kategoriler aranıyor...")
                
            except TimeoutException:
                print("Ürünler menüsü bulunamadı.")
            
            # Kategori linkleri bul
            category_links = driver.find_elements(By.XPATH, "//a[contains(@href, '/urun') or contains(@href, '/kategori') or contains(@href, '/product')]")
            
            for link in category_links:
                try:
                    href = link.get_attribute('href')
                    text = link.text.strip()
                    
                    if href and text and len(text) > 2:
                        # Kategori adını normalleştir
                        category_key = self.normalize_category_name(text)
                        if category_key:
                            category_urls[category_key] = {
                                'url': href,
                                'name': text
                            }
                            print(f"Kategori bulundu: {text} -> {href}")
                except Exception as e:
                    continue
            
            # Eğer hover menüden bulamazsak, sayfadaki tüm kategori linklerini ara
            if not category_urls:
                print("Hover menüden kategori bulunamadı, sayfadaki tüm linkler kontrol ediliyor...")
                all_links = driver.find_elements(By.TAG_NAME, "a")
                
                for link in all_links:
                    try:
                        href = link.get_attribute('href')
                        text = link.text.strip()
                        
                        if href and text:
                            # TAT ürün kategorilerini kontrol et
                            category_key = self.normalize_category_name(text)
                            if category_key:
                                category_urls[category_key] = {
                                    'url': href,
                                    'name': text
                                }
                                print(f"Kategori bulundu: {text} -> {href}")
                    except Exception as e:
                        continue
            
        except Exception as e:
            print(f"Kategori URL'leri alınırken hata: {e}")
        
        return category_urls
    
    def normalize_category_name(self, category_name):
        """Kategori adını normalleştirir"""
        category_lower = category_name.lower()
        
        # Kategori eşleştirmeleri
        if any(word in category_lower for word in ['salça', 'salca']):
            return 'salca'
        elif any(word in category_lower for word in ['domates']):
            return 'domates_urunleri'
        elif any(word in category_lower for word in ['sos', 'ketçap', 'mayonez', 'hardal']):
            return 'soslar'
        elif any(word in category_lower for word in ['çorba', 'corba']):
            return 'corba'
        elif any(word in category_lower for word in ['organik']):
            return 'organik_urunler'
        elif any(word in category_lower for word in ['sebze', 'konserve', 'fasulye', 'bezelye', 'bamya']):
            return 'sebze_konservesi'
        elif any(word in category_lower for word in ['haşlanmış', 'haslanmis', 'nohut']):
            return 'haslanmis_urunler'
        elif any(word in category_lower for word in ['hazır', 'hazir', 'yemek', 'pilav']):
            return 'hazir_yemek'
        elif any(word in category_lower for word in ['meze', 'ekmek', 'makarna']):
            return 'meze_soslar'
        elif any(word in category_lower for word in ['turşu', 'tursu']):
            return 'tursu'
        elif any(word in category_lower for word in ['reçel', 'recel', 'marmelat']):
            return 'recel_marmelat'
        
        return None
    
    def get_page_content(self, url):
        """Sayfanın HTML içeriğini alır"""
        try:
            print(f"Sayfa içeriği alınıyor: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            response.encoding = 'utf-8'
            return response.text
        except requests.RequestException as e:
            print(f"Sayfa alınırken hata oluştu: {e}")
            return None
    
    def extract_product_images(self, html_content, category_key):
        """HTML içeriğinden ürün görsellerini çıkarır"""
        soup = BeautifulSoup(html_content, 'html.parser')
        image_data = []
        
        # Ürün görsel konteynerlerini bul
        product_containers = soup.find_all(['div', 'article', 'section'], 
                                         class_=lambda x: x and any(word in x.lower() for word in 
                                         ['product', 'urun', 'item', 'card']))
        
        print(f"Ürün konteyneri bulundu: {len(product_containers)}")
        
        # Tüm img etiketlerini kontrol et
        all_images = soup.find_all('img')
        print(f"Toplam img etiketi: {len(all_images)}")
        
        for img in all_images:
            # src özelliğini kontrol et
            src = img.get('src')
            alt = img.get('alt', '')
            
            if src and self.is_valid_product_image(src, alt):
                full_url = urljoin(self.base_url, src)
                image_data.append({
                    'url': full_url,
                    'alt': alt,
                    'category': category_key
                })
                print(f"Ürün görseli bulundu: {full_url}")
            
            # data-src özelliğini kontrol et (lazy loading)
            data_src = img.get('data-src')
            if data_src and self.is_valid_product_image(data_src, alt):
                full_url = urljoin(self.base_url, data_src)
                image_data.append({
                    'url': full_url,
                    'alt': alt,
                    'category': category_key
                })
                print(f"Lazy load ürün görseli bulundu: {full_url}")
        
        # CSS background-image özelliklerini bul
        style_elements = soup.find_all(attrs={"style": True})
        for element in style_elements:
            style = element.get('style', '')
            if 'background-image' in style:
                urls = re.findall(r'url\(["\']?([^"\']*)["\']?\)', style)
                for url in urls:
                    if self.is_valid_product_image(url):
                        full_url = urljoin(self.base_url, url)
                        image_data.append({
                            'url': full_url,
                            'alt': '',
                            'category': category_key
                        })
                        print(f"CSS background ürün görseli bulundu: {full_url}")
        
        return image_data
    
    def is_valid_product_image(self, url, alt=""):
        """URL'nin geçerli bir ürün görseli olup olmadığını kontrol eder"""
        if not url or url.startswith('data:'):
            return False
        
        # Gereksiz URL'leri filtrele
        exclude_patterns = ['icon', 'logo', 'placeholder', 'loading', 'spinner', 'banner', 'slider']
        url_lower = url.lower()
        alt_lower = alt.lower()
        
        # Exclude patterns kontrolü
        if any(pattern in url_lower for pattern in exclude_patterns):
            return False
        
        # TAT ürünü görseli olabilecek pattern'lar
        product_patterns = ['urun', 'product', 'tat', 'jpg', 'jpeg', 'png', 'webp']
        
        # Görsel uzantılarını kontrol et
        valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg']
        parsed_url = urlparse(url)
        path = parsed_url.path.lower()
        
        has_valid_extension = any(path.endswith(ext) for ext in valid_extensions)
        has_product_pattern = any(pattern in url_lower or pattern in alt_lower for pattern in product_patterns)
        
        return has_valid_extension or has_product_pattern
    
    def get_filename_from_url(self, url, category):
        """URL'den dosya adı çıkarır"""
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        
        # Eğer dosya adı yoksa veya uzantısı yoksa, URL'den oluştur
        if not filename or '.' not in filename:
            filename = f"{category}_product_{hash(url) % 10000}.jpg"
        
        return filename
    
    def download_image(self, image_data):
        """Tek bir görseli indirir"""
        url = image_data['url']
        category = image_data['category']
        filename = self.get_filename_from_url(url, category)
        
        try:
            response = self.session.get(url, timeout=30, stream=True)
            response.raise_for_status()
            
            # İçerik türünü kontrol et
            content_type = response.headers.get('content-type', '')
            if not content_type.startswith('image/'):
                print(f"Bu URL bir görsel değil: {url} (Content-Type: {content_type})")
                return False
            
            # Dosya uzantısını content-type'a göre ayarla
            if not any(filename.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg']):
                ext = mimetypes.guess_extension(content_type.split(';')[0])
                if ext:
                    filename += ext
            
            # Kategori dizinine kaydet
            category_dir = self.output_dir / category
            file_path = category_dir / filename
            
            # Eğer dosya zaten varsa, sayı ekle
            counter = 1
            original_path = file_path
            while file_path.exists():
                stem = original_path.stem
                suffix = original_path.suffix
                file_path = category_dir / f"{stem}_{counter}{suffix}"
                counter += 1
            
            # Dosyayı kaydet
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"✓ İndirildi ({category}): {file_path.name}")
            return True
            
        except requests.RequestException as e:
            print(f"✗ İndirme hatası {url}: {e}")
            return False
        except Exception as e:
            print(f"✗ Dosya kaydetme hatası {filename}: {e}")
            return False
    
    def scrape_category(self, category_info, category_key):
        """Belirli bir kategoriyi scrape eder"""
        print(f"\n{'='*60}")
        print(f"Kategori scraping başlıyor: {category_info['name']}")
        print(f"URL: {category_info['url']}")
        print(f"{'='*60}")
        
        # Kategori sayfası içeriğini al
        html_content = self.get_page_content(category_info['url'])
        if not html_content:
            print(f"Kategori sayfası içeriği alınamadı: {category_info['name']}")
            return 0
        
        # Ürün görsellerini çıkar
        image_data = self.extract_product_images(html_content, category_key)
        
        if not image_data:
            print(f"Bu kategoride ürün görseli bulunamadı: {category_info['name']}")
            return 0
        
        print(f"Bu kategoride {len(image_data)} ürün görseli bulundu")
        
        # Görselleri indir
        successful_downloads = 0
        for i, data in enumerate(image_data, 1):
            print(f"[{i}/{len(image_data)}] İndiriliyor: {data['url']}")
            
            if self.download_image(data):
                successful_downloads += 1
            
            # İstekler arasında kısa bekleme
            time.sleep(0.5)
        
        print(f"Kategori tamamlandı: {category_info['name']}")
        print(f"Başarılı indirme: {successful_downloads}/{len(image_data)}")
        
        return successful_downloads
    
    def scrape_all_categories(self):
        """Tüm kategorileri scrape eder"""
        print("TAT Ürün Görselleri Çekici Başlatıldı")
        print("=" * 60)
        
        # WebDriver'ı kur
        driver = self.setup_driver()
        if not driver:
            print("WebDriver kurulamadı, manuel URL'lerle devam ediliyor...")
            return self.scrape_with_manual_urls()
        
        try:
            # Kategori URL'lerini al
            category_urls = self.get_category_urls(driver)
            
            if not category_urls:
                print("Hiç kategori URL'si bulunamadı!")
                return
            
            print(f"\nToplam {len(category_urls)} kategori bulundu:")
            for key, info in category_urls.items():
                print(f"  - {info['name']}: {info['url']}")
            
            # Her kategoriyi scrape et
            total_downloads = 0
            for category_key, category_info in category_urls.items():
                downloads = self.scrape_category(category_info, category_key)
                total_downloads += downloads
                
                # Kategoriler arası bekleme
                time.sleep(2)
            
            print("\n" + "=" * 60)
            print(f"Tüm kategoriler tamamlandı!")
            print(f"Toplam başarılı indirme: {total_downloads}")
            print(f"Görseller '{self.output_dir}' klasörüne kategorilere göre ayrılarak kaydedildi")
            
            # Kategori özetini göster
            print("\nKategori özetleri:")
            for category_key, category_name in self.categories.items():
                category_dir = self.output_dir / category_key
                if category_dir.exists():
                    file_count = len(list(category_dir.glob('*')))
                    if file_count > 0:
                        print(f"  - {category_name}: {file_count} dosya")
        
        finally:
            driver.quit()
    
    def scrape_with_manual_urls(self):
        """Manuel URL'lerle scraping yapmaya çalışır"""
        print("Manuel URL'lerle scraping deneniyor...")
        
        # TAT'ın bilinen ürün sayfaları
        manual_urls = {
            'salca': 'https://www.tat.com.tr/salca-urunleri',
            'soslar': 'https://www.tat.com.tr/sos-urunleri',
            'domates_urunleri': 'https://www.tat.com.tr/domates-urunleri',
            'genel': 'https://www.tat.com.tr/urunler'
        }
        
        total_downloads = 0
        for category_key, url in manual_urls.items():
            category_info = {'name': self.categories[category_key], 'url': url}
            downloads = self.scrape_category(category_info, category_key)
            total_downloads += downloads
            time.sleep(2)
        
        print(f"\nManuel scraping tamamlandı! Toplam: {total_downloads} dosya")

def main():
    """Ana fonksiyon"""
    scraper = TatScraper()
    scraper.scrape_all_categories()

if __name__ == "__main__":
    main()
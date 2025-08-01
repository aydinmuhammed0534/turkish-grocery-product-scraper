#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teksüt Ürünler Sayfası Görsel Çekici
Bu script Teksüt'ün ürünler sayfasındaki tüm görselleri indirir.
"""

import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin, urlparse
import time
from pathlib import Path
import mimetypes

class TeksutImageScraper:
    def __init__(self, base_url="https://teksut.com.tr/urunler/"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Çıktı dizini oluştur
        self.output_dir = Path("teksut_images")
        self.output_dir.mkdir(exist_ok=True)
        
    def get_page_content(self):
        """Sayfanın HTML içeriğini alır"""
        try:
            print(f"Sayfa içeriği alınıyor: {self.base_url}")
            response = self.session.get(self.base_url, timeout=30)
            response.raise_for_status()
            response.encoding = 'utf-8'
            return response.text
        except requests.RequestException as e:
            print(f"Sayfa alınırken hata oluştu: {e}")
            return None
    
    def extract_image_urls(self, html_content):
        """HTML içeriğinden görsel URL'lerini çıkarır"""
        soup = BeautifulSoup(html_content, 'html.parser')
        image_urls = set()
        
        # img etiketlerini bul
        img_tags = soup.find_all('img')
        print(f"Bulunan img etiketi sayısı: {len(img_tags)}")
        
        for img in img_tags:
            # src özelliğini kontrol et
            src = img.get('src')
            if src:
                # Göreceli URL'leri tam URL'ye çevir
                full_url = urljoin(self.base_url, src)
                image_urls.add(full_url)
                print(f"Görsel URL bulundu: {full_url}")
            
            # data-src özelliğini kontrol et (lazy loading için)
            data_src = img.get('data-src')
            if data_src:
                full_url = urljoin(self.base_url, data_src)
                image_urls.add(full_url)
                print(f"Lazy load görsel URL bulundu: {full_url}")
        
        # CSS background-image özelliklerini bul
        style_tags = soup.find_all(attrs={"style": True})
        for tag in style_tags:
            style = tag.get('style', '')
            if 'background-image' in style:
                # URL'yi çıkar
                import re
                urls = re.findall(r'url\(["\']?([^"\']*)["\']?\)', style)
                for url in urls:
                    full_url = urljoin(self.base_url, url)
                    image_urls.add(full_url)
                    print(f"CSS background görsel URL bulundu: {full_url}")
        
        return list(image_urls)
    
    def get_filename_from_url(self, url):
        """URL'den dosya adı çıkarır"""
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        
        # Eğer dosya adı yoksa veya uzantısı yoksa, URL'den oluştur
        if not filename or '.' not in filename:
            filename = f"image_{hash(url) % 10000}.jpg"
        
        return filename
    
    def download_image(self, url, filename):
        """Tek bir görseli indirir"""
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
            
            file_path = self.output_dir / filename
            
            # Eğer dosya zaten varsa, sayı ekle
            counter = 1
            original_path = file_path
            while file_path.exists():
                stem = original_path.stem
                suffix = original_path.suffix
                file_path = self.output_dir / f"{stem}_{counter}{suffix}"
                counter += 1
            
            # Dosyayı kaydet
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"✓ İndirildi: {file_path}")
            return True
            
        except requests.RequestException as e:
            print(f"✗ İndirme hatası {url}: {e}")
            return False
        except Exception as e:
            print(f"✗ Dosya kaydetme hatası {filename}: {e}")
            return False
    
    def scrape_images(self):
        """Ana scraping fonksiyonu"""
        print("Teksüt Görsel Çekici Başlatıldı")
        print("=" * 50)
        
        # Sayfa içeriğini al
        html_content = self.get_page_content()
        if not html_content:
            print("Sayfa içeriği alınamadı!")
            return
        
        # Görsel URL'lerini çıkar
        print("\nGörsel URL'leri çıkarılıyor...")
        image_urls = self.extract_image_urls(html_content)
        
        if not image_urls:
            print("Hiç görsel URL'si bulunamadı!")
            return
        
        print(f"\nToplam {len(image_urls)} görsel URL'si bulundu")
        print("İndirme işlemi başlatılıyor...\n")
        
        # Görselleri indir
        successful_downloads = 0
        for i, url in enumerate(image_urls, 1):
            print(f"[{i}/{len(image_urls)}] İndiriliyor: {url}")
            filename = self.get_filename_from_url(url)
            
            if self.download_image(url, filename):
                successful_downloads += 1
            
            # İstekler arasında kısa bekleme
            time.sleep(0.5)
        
        print("\n" + "=" * 50)
        print(f"İşlem tamamlandı!")
        print(f"Başarılı indirme: {successful_downloads}/{len(image_urls)}")
        print(f"Görseller '{self.output_dir}' klasörüne kaydedildi")

def main():
    """Ana fonksiyon"""
    scraper = TeksutImageScraper()
    scraper.scrape_images()

if __name__ == "__main__":
    main()

"""
 .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------. 
| .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. |
| | _____  _____ | || |      __      | || |  _________   | || |     ______   | || |  ____  ____  | || |   _____      | || |     _____    | || |    _______   | || |  _________   | |
| ||_   _||_   _|| || |     /  \     | || | |  _   _  |  | || |   .' ___  |  | || | |_   ||   _| | || |  |_   _|     | || |    |_   _|   | || |   /  ___  |  | || | |  _   _  |  | |
| |  | | /\ | |  | || |    / /\ \    | || | |_/ | | \_|  | || |  / .'   \_|  | || |   | |__| |   | || |    | |       | || |      | |     | || |  |  (__ \_|  | || | |_/ | | \_|  | |
| |  | |/  \| |  | || |   / ____ \   | || |     | |      | || |  | |         | || |   |  __  |   | || |    | |   _   | || |      | |     | || |   '.___`-.   | || |     | |      | |
| |  |   /\   |  | || | _/ /    \ \_ | || |    _| |_     | || |  \ `.___.'\  | || |  _| |  | |_  | || |   _| |__/ |  | || |     _| |_    | || |  |`\____) |  | || |    _| |_     | |
| |  |__/  \__|  | || ||____|  |____|| || |   |_____|    | || |   `._____.'  | || | |____||____| | || |  |________|  | || |    |_____|   | || |  |_______.'  | || |   |_____|    | |
| |              | || |              | || |              | || |              | || |              | || |              | || |              | || |              | || |              | |
| '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' |
 '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'                                                                                   
"""                                                                             
                                                                                      


import sys
import subprocess
import os

def install_dependencies():
    required_packages = [
        'undetected-chromedriver',
        'selenium',
        'customtkinter',
        'pillow',
        'qrcode',
        'psutil',
        'pyngrok'
    ]
    
    print("🔧 Installing dependencies...")
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            print(f"📦 Installing {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package, '--quiet'])
    print("✅ Dependencies ready!\n")

install_dependencies()

import customtkinter as ctk
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
from threading import Lock, Thread
import pickle
import webbrowser
import psutil
import qrcode
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
from PIL import Image
import tempfile
import shutil

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

file_lock = Lock()

class BrowserDetector:
    @staticmethod
    def find_browsers():
        browsers = {}
        
        chrome_paths = [
            os.path.expandvars(r'%LOCALAPPDATA%\Google\Chrome\User Data'),
            os.path.expandvars(r'%USERPROFILE%\AppData\Local\Google\Chrome\User Data'),
        ]
        for path in chrome_paths:
            if os.path.exists(path):
                browsers['Chrome'] = path
                break
        
        edge_paths = [
            os.path.expandvars(r'%LOCALAPPDATA%\Microsoft\Edge\User Data'),
            os.path.expandvars(r'%USERPROFILE%\AppData\Local\Microsoft\Edge\User Data'),
        ]
        for path in edge_paths:
            if os.path.exists(path):
                browsers['Edge'] = path
                break
        
        opera_paths = [
            os.path.expandvars(r'%APPDATA%\Opera Software\Opera Stable'),
            os.path.expandvars(r'%APPDATA%\Opera Software\Opera GX Stable'),
        ]
        for path in opera_paths:
            if os.path.exists(path):
                browsers['Opera/OperaGX'] = path
                break
        
        brave_paths = [
            os.path.expandvars(r'%LOCALAPPDATA%\BraveSoftware\Brave-Browser\User Data'),
        ]
        for path in brave_paths:
            if os.path.exists(path):
                browsers['Brave'] = path
                break
        
        return browsers

    @staticmethod
    def close_browser_processes(browser_name):
        process_map = {
            'Chrome': ['chrome.exe', 'chromedriver.exe'],
            'Edge': ['msedge.exe', 'msedgedriver.exe'],
            'Opera/OperaGX': ['opera.exe', 'OperaGX.exe'],
            'Brave': ['brave.exe']
        }
        
        processes = process_map.get(browser_name, [])
        killed = 0
        for proc in psutil.process_iter(['name']):
            try:
                if proc.info['name'] in processes:
                    proc.kill()
                    killed += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        time.sleep(3)
        return killed

class ConfigManager:
    CONFIG_FILE = 'data/config.json'
    
    @staticmethod
    def load_config():
        if os.path.exists(ConfigManager.CONFIG_FILE):
            try:
                with open(ConfigManager.CONFIG_FILE, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    @staticmethod
    def save_config(email, password, ngrok_token, anime_limit):
        config = {
            'email': email,
            'password': password,
            'ngrok_token': ngrok_token,
            'anime_limit': anime_limit
        }
        with open(ConfigManager.CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=4)

class CookieManager:
    COOKIE_FILE = 'data/cookies.pkl'
    
    @staticmethod
    def save_cookies(driver):
        try:
            with open(CookieManager.COOKIE_FILE, 'wb') as f:
                pickle.dump(driver.get_cookies(), f)
            return True
        except:
            return False
    
    @staticmethod
    def load_cookies(driver):
        if os.path.exists(CookieManager.COOKIE_FILE):
            try:
                with open(CookieManager.COOKIE_FILE, 'rb') as f:
                    cookies = pickle.load(f)
                    for cookie in cookies:
                        try:
                            driver.add_cookie(cookie)
                        except:
                            pass
                return True
            except:
                pass
        return False

class AniWorldScraper:
    def __init__(self, browser_name, browser_path, log_callback):
        self.browser_name = browser_name
        self.browser_path = browser_path
        self.log = log_callback
        self.driver = None
        self.temp_profile = None
    
    def init_driver(self, headless=False, use_temp_profile=False):
        try:
            self.log(f"🔧 Creating {self.browser_name} driver...")
            
            if self.browser_name == 'Edge':
                from selenium import webdriver
                from selenium.webdriver.edge.options import Options as EdgeOptions
                
                edge_options = EdgeOptions()
                
                if use_temp_profile:
                    self.temp_profile = tempfile.mkdtemp(prefix="edge_profile_")
                    edge_options.add_argument(f'--user-data-dir={self.temp_profile}')
                else:
                    edge_options.add_argument(f'--user-data-dir={self.browser_path}')
                
                edge_options.add_argument('--no-sandbox')
                edge_options.add_argument('--disable-dev-shm-usage')
                edge_options.add_argument('--disable-blink-features=AutomationControlled')
                edge_options.add_argument('--start-maximized')
                edge_options.add_argument('--disable-infobars')
                edge_options.add_argument('--disable-notifications')
                edge_options.add_argument('--disable-images')
                edge_options.add_argument('--blink-settings=imagesEnabled=false')
                edge_options.page_load_strategy = 'eager'
                
                if headless:
                    edge_options.add_argument('--headless=new')
                
                edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
                edge_options.add_experimental_option('useAutomationExtension', False)
                edge_options.add_experimental_option("prefs", {
                    "profile.managed_default_content_settings.images": 2,
                    "profile.default_content_setting_values.notifications": 2
                })
                
                try:
                    self.log("⏳ Starting Edge WebDriver...")
                    self.driver = webdriver.Edge(options=edge_options)
                    self.log("✅ Edge driver ready")
                except Exception as edge_error:
                    self.log(f"❌ Edge failed: {str(edge_error)}")
                    self.log("💡 Make sure Edge WebDriver is installed")
                    raise
            else:
                options = uc.ChromeOptions()
                
                if use_temp_profile:
                    self.log("📁 Using temporary profile...")
                    self.temp_profile = tempfile.mkdtemp(prefix="chrome_profile_")
                    options.add_argument(f'--user-data-dir={self.temp_profile}')
                else:
                    self.log("📁 Using existing profile...")
                    options.add_argument(f'--user-data-dir={self.browser_path}')
                
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument('--disable-blink-features=AutomationControlled')
                options.add_argument('--start-maximized')
                options.add_argument('--disable-infobars')
                options.add_argument('--disable-notifications')
                options.add_argument('--remote-debugging-port=9222')
                options.add_argument('--disable-images')
                options.add_argument('--blink-settings=imagesEnabled=false')
                options.page_load_strategy = 'eager'
                
                if headless:
                    options.add_argument('--headless=new')
                
                options.add_experimental_option("prefs", {
                    "profile.managed_default_content_settings.images": 2,
                    "profile.default_content_setting_values.notifications": 2
                })
                
                self.log("⏳ Detecting ChromeDriver version...")
                self.log("⏳ Starting Chrome (this may take 15-30 seconds)...")
                
                try:
                    self.driver = uc.Chrome(
                        options=options, 
                        version_main=None, 
                        use_subprocess=True,
                        driver_executable_path=None,
                        browser_executable_path=None
                    )
                    self.log(f"✅ {self.browser_name} driver ready")
                except Exception as chrome_error:
                    self.log(f"⚠️ Failed with profile: {str(chrome_error)[:100]}")
                    self.log("🔄 Retrying with temporary profile...")
                    if not use_temp_profile:
                        return self.init_driver(headless=headless, use_temp_profile=True)
                    raise
            
            self.driver.set_page_load_timeout(15)
            self.driver.set_script_timeout(15)
            self.driver.implicitly_wait(3)
            return self.driver
        except Exception as e:
            raise Exception(f"Driver init failed: {str(e)}")
    
    def check_login_status(self):
        try:
            current_url = self.driver.current_url
            if "watchlist" in current_url or "account" in current_url:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, ".anime-item, .col-md-15, .seriesListContainer, [class*='anime'], [class*='series']")
                    return len(elements) > 0
                except:
                    pass
            return False
        except:
            return False
    
    def login(self, email, password):
        self.log("🔐 Starting login...")
        
        try:
            self.driver.get("https://aniworld.to/login")
            time.sleep(4)
            
            self.log("📧 Entering email...")
            email_field = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.NAME, "email"))
            )
            email_field.clear()
            time.sleep(0.5)
            email_field.send_keys(email)
            time.sleep(1.5)
            
            self.log("🔒 Entering password...")
            password_field = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.NAME, "password"))
            )
            password_field.clear()
            time.sleep(0.5)
            password_field.send_keys(password)
            time.sleep(1.5)
            
            try:
                self.log("☑️ Checking remember me...")
                checkbox = self.driver.find_element(By.CSS_SELECTOR, ".icheckbox_square-blue input[type='checkbox']")
                self.driver.execute_script("arguments[0].click();", checkbox)
                time.sleep(0.5)
            except:
                pass
            
            self.log("🚀 Submitting...")
            submit_button = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input.button.blue[type='submit'], button[type='submit']"))
            )
            self.driver.execute_script("arguments[0].click();", submit_button)
            
            time.sleep(6)
            
            CookieManager.save_cookies(self.driver)
            self.log("✅ Login complete!")
            return True
                    
        except Exception as e:
            self.log(f"❌ Login error: {str(e)}")
            return False
    
    def get_watchlist_items(self, preference, anime_limit=None):
        self.log("📋 Loading watchlist page...")
        
        try:
            self.driver.get("https://aniworld.to/account/watchlist")
            time.sleep(2)
            
            self.log("🔍 Extracting anime data...")
            
            anime_elements = self.driver.find_elements(By.CSS_SELECTOR, ".seriesListContainer .col-md-15")
            
            if not anime_elements:
                self.log("⚠️ No items found!")
                return []
            
            if anime_limit and anime_limit > 0:
                anime_elements = anime_elements[:anime_limit]
                self.log(f"🎯 Limited to {anime_limit} anime")
            
            anime_data = []
            for elem in anime_elements:
                try:
                    name = elem.find_element(By.CSS_SELECTOR, "h3").text.strip()
                    link = elem.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                    cover_img = elem.find_element(By.CSS_SELECTOR, "img").get_attribute("src")
                    anime_data.append({
                        "name": name,
                        "link": link,
                        "cover_image": cover_img
                    })
                except:
                    continue
            
            total = len(anime_data)
            self.log(f"📊 Found {total} anime")
            
            if preference == 'both':
                self.log(f"⚡ Detecting types for all anime (~{int(total * 2 / 60)} min)")
            else:
                self.log(f"⚡ Fast mode: ~2 seconds per anime = ~{int(total * 2 / 60)} minutes total")
            
            anime_list = []
            
            for idx, anime in enumerate(anime_data, 1):
                try:
                    if idx % 20 == 0:
                        self.log(f"📊 Progress: {idx}/{total} ({int(idx/total*100)}%)")
                    
                    self.log(f"⏳ {idx}/{total}: {anime['name'][:40]}...")
                    
                    self.driver.get(anime['link'])
                    
                    try:
                        wait = WebDriverWait(self.driver, 5)
                        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".hosterSiteDirectNav")))
                    except:
                        self.log(f"   ⚠️ Timeout, skipping")
                        continue
                    
                    filme_link = self.driver.find_elements(By.CSS_SELECTOR, ".hosterSiteDirectNav a[href*='/filme']")
                    staffel_links = self.driver.find_elements(By.CSS_SELECTOR, ".hosterSiteDirectNav a[href*='/staffel-']")
                    
                    has_movies = len(filme_link) > 0
                    has_seasons = len(staffel_links) > 0
                    
                    if has_movies and not has_seasons:
                        anime_type = "Movie"
                    elif has_seasons and not has_movies:
                        anime_type = "Series"
                    elif has_movies and has_seasons:
                        anime_type = "Series+Movies"
                    else:
                        anime_type = "Unknown"
                    
                    if preference == 'both':
                        anime_list.append({
                            "name": anime['name'],
                            "link": anime['link'],
                            "cover_image": anime['cover_image'],
                            "type": anime_type,
                            "episodes": len(staffel_links) if has_seasons else 0
                        })
                        self.log(f"   ✅ {anime_type}")
                    elif preference == 'series' and anime_type in ["Series", "Series+Movies"]:
                        anime_list.append({
                            "name": anime['name'],
                            "link": anime['link'],
                            "cover_image": anime['cover_image'],
                            "type": anime_type,
                            "episodes": len(staffel_links)
                        })
                        self.log(f"   ✅ {anime_type} ({len(staffel_links)})")
                    elif preference == 'movies' and anime_type in ["Movie", "Series+Movies"]:
                        anime_list.append({
                            "name": anime['name'],
                            "link": anime['link'],
                            "cover_image": anime['cover_image'],
                            "type": anime_type,
                            "episodes": 0
                        })
                        self.log(f"   ✅ {anime_type}")
                    else:
                        self.log(f"   ⭕ {anime_type}")
                        
                except Exception as e:
                    self.log(f"   ⚠️ Error: {str(e)[:50]}")
            
            return anime_list
            
        except Exception as e:
            self.log(f"❌ Watchlist load failed: {str(e)}")
            return []
    
    def close(self):
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
        if self.temp_profile and os.path.exists(self.temp_profile):
            try:
                shutil.rmtree(self.temp_profile, ignore_errors=True)
            except:
                pass

class FileExporter:
    @staticmethod
    def export_all(anime_list):
        FileExporter.export_txt(anime_list)
        FileExporter.export_json(anime_list)
        FileExporter.export_markdown(anime_list)
        FileExporter.export_html(anime_list)
        FileExporter.export_html_gallery(anime_list)
    
    @staticmethod
    def export_txt(anime_list):
        with open("exports/watchlist.txt", "w", encoding="utf-8") as f:
            f.write("=" * 60 + "\n")
            f.write("ANIME WATCHLIST\n")
            f.write("=" * 60 + "\n\n")
            for idx, anime in enumerate(anime_list, 1):
                f.write(f"{idx}. {anime['name']}\n")
                f.write(f"   Type: {anime.get('type', 'Unknown')}\n")
                if anime.get('episodes', 0) > 0:
                    f.write(f"   Episodes: {anime['episodes']}\n")
                f.write(f"   Link: {anime['link']}\n")
                f.write(f"\n")
    
    @staticmethod
    def export_json(anime_list):
        with open("exports/watchlist.json", "w", encoding="utf-8") as f:
            json.dump({
                "total": len(anime_list),
                "exported_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "anime": anime_list
            }, f, indent=2, ensure_ascii=False)
    
    @staticmethod
    def export_markdown(anime_list):
        with open("exports/watchlist.md", "w", encoding="utf-8") as f:
            f.write("# 🎬 My Anime Watchlist Collection\n\n")
            f.write(f"**Total Anime:** {len(anime_list)} • **Last Updated:** {time.strftime('%B %d, %Y')}\n\n")
            f.write("---\n\n")
            
            for i, anime in enumerate(anime_list):
                emojis = ["🌟", "✨", "💫", "⭐", "🎯", "🎬", "🎥", "🌸", "🔥", "⚡"]
                emoji = emojis[i % len(emojis)]
                
                f.write(f"## {emoji} {anime['name']}\n\n")
                f.write(f"**Type:** {anime.get('type', 'Unknown')}")
                if anime.get('episodes', 0) > 0:
                    f.write(f" • **Episodes:** {anime['episodes']}")
                f.write("\n\n")
                f.write(f"[![{anime['name']}]({anime['cover_image']})]({anime['link']})\n\n")
                f.write(f"[▶️ Watch Now]({anime['link']}) • [🔗 Copy Link]({anime['link']})\n\n")
                f.write("---\n\n")
            
            f.write(f"\n<div align='center'>\n\n")
            f.write(f"*✨ Generated with ❤️ by AniWorld Watchlist Manager V2 ✨*\n\n")
            f.write(f"**{len(anime_list)} Anime** • **{time.strftime('%Y')}**\n\n")
            f.write(f"*Made by [TheHolyOneZ](https://github.com/TheHolyOneZ)*\n\n")
            f.write("</div>")
    
    @staticmethod
    def export_html(anime_list):
        series_count = sum(1 for a in anime_list if a.get('type') in ['Series', 'Series+Movies'])
        movie_count = sum(1 for a in anime_list if a.get('type') in ['Movie', 'Series+Movies'])
        series_only_count = sum(1 for a in anime_list if a.get('type') == 'Series')
        movie_only_count = sum(1 for a in anime_list if a.get('type') == 'Movie')
        both_count = sum(1 for a in anime_list if a.get('type') == 'Series+Movies')
        
        html_cards = []
        for anime in anime_list:
            anime_type = anime.get('type', 'Unknown')
            episodes_info = ""
            
            if anime_type == 'Series':
                type_badge = '<span class="badge type-series">📺 Series</span>'
                if anime.get('episodes', 0) > 0:
                    episodes_info = f'<span class="badge episodes">{anime.get("episodes", 0)} Seasons</span>'
            elif anime_type == 'Movie':
                type_badge = '<span class="badge type-movie">🎬 Movie</span>'
            elif anime_type == 'Series+Movies':
                type_badge = '<span class="badge type-both">📺🎬 Series + Movies</span>'
                if anime.get('episodes', 0) > 0:
                    episodes_info = f'<span class="badge episodes">{anime.get("episodes", 0)} Seasons</span>'
            else:
                type_badge = f'<span class="badge type-unknown">❓ {anime_type}</span>'
            
            html_cards.append(f'''
                <div class="anime-card" data-type="{anime_type.lower()}">
                    <div class="anime-poster">
                        <img src="{anime['cover_image']}" alt="{anime['name']}" loading="lazy" onerror="this.src='data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%22250%22 height=%22350%22%3E%3Crect fill=%22%23667eea%22 width=%22250%22 height=%22350%22/%3E%3Ctext fill=%22white%22 x=%2250%25%22 y=%2250%25%22 text-anchor=%22middle%22 dy=%22.3em%22 font-size=%2220%22%3ENo Image%3C/text%3E%3C/svg%3E'">
                        <div class="anime-overlay">
                            <a href="{anime['link']}" class="watch-btn" target="_blank">
                                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <polygon points="5 3 19 12 5 21 5 3"></polygon>
                                </svg>
                                Watch Now
                            </a>
                        </div>
                    </div>
                    <div class="anime-info">
                        <h3 class="anime-title">{anime['name']}</h3>
                        <div class="anime-meta">
                            {type_badge}
                            {episodes_info}
                        </div>
                    </div>
                </div>
            ''')
        
        html_template = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Anime Collection • {len(anime_list)} Titles</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        :root {{
            --primary: #667eea;
            --primary-light: #7c93f5;
            --secondary: #764ba2;
            --accent: #f093fb;
            --bg-main: #0a0e27;
            --bg-card: #151932;
            --bg-hover: #1e2442;
            --text-primary: #ffffff;
            --text-secondary: #9ca3bc;
            --text-muted: #6b7280;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
            --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.1);
            --shadow-md: 0 8px 24px rgba(0, 0, 0, 0.15);
            --shadow-lg: 0 20px 60px rgba(0, 0, 0, 0.3);
            --shadow-xl: 0 30px 90px rgba(0, 0, 0, 0.5);
        }}
        
        @keyframes gradientShift {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}
        
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(-45deg, #0a0e27, #1a1535, #0f1729, #1e1b4b);
            background-size: 400% 400%;
            animation: gradientShift 15s ease infinite;
            color: var(--text-primary);
            min-height: 100vh;
            padding: 40px 20px 80px;
            line-height: 1.6;
            position: relative;
        }}
        
        body::before {{
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: radial-gradient(circle at 20% 80%, rgba(102, 126, 234, 0.15) 0%, transparent 50%),
                        radial-gradient(circle at 80% 20%, rgba(118, 75, 162, 0.15) 0%, transparent 50%);
            pointer-events: none;
            z-index: 0;
        }}
        
        .credit {{
            position: fixed;
            top: 20px;
            right: 20px;
            background: rgba(21, 25, 50, 0.9);
            backdrop-filter: blur(20px);
            padding: 12px 24px;
            border-radius: 50px;
            border: 1px solid rgba(102, 126, 234, 0.3);
            z-index: 1000;
            font-size: 0.9rem;
            font-weight: 600;
            transition: all 0.3s ease;
        }}
        
        .credit:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);
            border-color: var(--primary);
        }}
        
        .credit a {{
            color: var(--primary-light);
            text-decoration: none;
            transition: color 0.3s ease;
        }}
        
        .credit a:hover {{
            color: var(--accent);
        }}
        
        .container {{
            max-width: 1600px;
            margin: 0 auto;
            position: relative;
            z-index: 1;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 50px;
            animation: fadeInDown 0.8s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        .header h1 {{
            font-size: clamp(2.5rem, 6vw, 4.5rem);
            font-weight: 900;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 15px;
            letter-spacing: -0.03em;
            line-height: 1.1;
        }}
        
        .header-subtitle {{
            font-size: 1.1rem;
            color: var(--text-secondary);
            font-weight: 400;
            margin-bottom: 40px;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            max-width: 1000px;
            margin: 40px auto;
        }}
        
        .stat-card {{
            background: var(--bg-card);
            backdrop-filter: blur(20px);
            padding: 25px;
            border-radius: 20px;
            border: 1px solid rgba(102, 126, 234, 0.15);
            text-align: center;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
            border-color: rgba(102, 126, 234, 0.4);
            box-shadow: var(--shadow-lg);
        }}
        
        .stat-number {{
            font-size: 2.5rem;
            font-weight: 800;
            background: linear-gradient(135deg, var(--primary), var(--accent));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
        }}
        
        .stat-label {{
            font-size: 0.85rem;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.1em;
            font-weight: 600;
        }}
        
        .search-filter-container {{
            max-width: 800px;
            margin: 0 auto 40px;
        }}
        
        .search-box-wrapper {{
            position: relative;
            margin-bottom: 25px;
        }}
        
        .search-box {{
            width: 100%;
            padding: 18px 55px 18px 25px;
            background: rgba(21, 25, 50, 0.8);
            backdrop-filter: blur(20px);
            border: 2px solid rgba(102, 126, 234, 0.2);
            border-radius: 16px;
            color: var(--text-primary);
            font-size: 1rem;
            font-family: 'Inter', sans-serif;
            font-weight: 500;
            transition: all 0.3s ease;
            outline: none;
        }}
        
        .search-box:focus {{
            border-color: var(--primary);
            box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
            background: rgba(21, 25, 50, 1);
        }}
        
        .search-box::placeholder {{
            color: var(--text-muted);
            font-weight: 400;
        }}
        
        .search-icon {{
            position: absolute;
            right: 22px;
            top: 50%;
            transform: translateY(-50%);
            pointer-events: none;
            opacity: 0.5;
        }}
        
        .filter-tabs {{
            display: flex;
            justify-content: center;
            gap: 12px;
            flex-wrap: wrap;
        }}
        
        .filter-tab {{
            padding: 12px 28px;
            background: rgba(21, 25, 50, 0.6);
            backdrop-filter: blur(10px);
            border: 2px solid rgba(102, 126, 234, 0.15);
            border-radius: 50px;
            color: var(--text-secondary);
            font-weight: 600;
            font-size: 0.9rem;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            font-family: 'Inter', sans-serif;
        }}
        
        .filter-tab:hover {{
            background: rgba(102, 126, 234, 0.1);
            border-color: var(--primary);
            color: var(--text-primary);
            transform: translateY(-2px);
        }}
        
        .filter-tab.active {{
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            border-color: transparent;
            color: white;
            box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);
        }}
        
        .anime-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
            gap: 30px;
            padding: 20px 0;
        }}
        
        .anime-card {{
            background: var(--bg-card);
            border-radius: 24px;
            overflow: hidden;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            border: 1px solid rgba(255, 255, 255, 0.05);
            animation: fadeInUp 0.6s ease backwards;
        }}
        
        .anime-card.hidden {{
            display: none;
        }}
        
        .anime-card:hover {{
            transform: translateY(-12px) scale(1.02);
            box-shadow: var(--shadow-xl);
            border-color: rgba(102, 126, 234, 0.3);
        }}
        
        .anime-poster {{
            position: relative;
            width: 100%;
            height: 380px;
            overflow: hidden;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
        }}
        
        .anime-poster img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        .anime-card:hover .anime-poster img {{
            transform: scale(1.1);
        }}
        
        .anime-overlay {{
            position: absolute;
            inset: 0;
            background: linear-gradient(to top, rgba(0,0,0,0.95) 0%, rgba(0,0,0,0.4) 40%, transparent 100%);
            display: flex;
            align-items: flex-end;
            justify-content: center;
            padding: 30px;
            opacity: 0;
            transition: opacity 0.3s ease;
        }}
        
        .anime-card:hover .anime-overlay {{
            opacity: 1;
        }}
        
        .watch-btn {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            color: white;
            padding: 12px 28px;
            border-radius: 50px;
            text-decoration: none;
            font-weight: 600;
            font-size: 0.95rem;
            transition: all 0.3s ease;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        }}
        
        .watch-btn:hover {{
            transform: scale(1.08);
            box-shadow: 0 15px 40px rgba(102, 126, 234, 0.6);
        }}
        
        .anime-info {{
            padding: 20px;
        }}
        
        .anime-title {{
            font-size: 1.05rem;
            font-weight: 700;
            margin-bottom: 14px;
            line-height: 1.4;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
            color: var(--text-primary);
        }}
        
        .anime-meta {{
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }}
        
        .badge {{
            display: inline-flex;
            align-items: center;
            padding: 6px 12px;
            border-radius: 8px;
            font-size: 0.7rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        
        .badge.type-series {{
            background: linear-gradient(135deg, #3b82f6, #2563eb);
            color: white;
        }}
        
        .badge.type-movie {{
            background: linear-gradient(135deg, #ec4899, #d946ef);
            color: white;
        }}
        
        .badge.type-both {{
            background: linear-gradient(135deg, #8b5cf6, #6366f1);
            color: white;
        }}
        
        .badge.type-unknown {{
            background: rgba(107, 114, 128, 0.2);
            color: var(--text-secondary);
        }}
        
        .badge.episodes {{
            background: rgba(102, 126, 234, 0.15);
            color: var(--primary-light);
            border: 1px solid rgba(102, 126, 234, 0.3);
        }}
        
        .no-results {{
            text-align: center;
            padding: 80px 20px;
            display: none;
        }}
        
        .no-results.show {{
            display: block;
        }}
        
        .no-results-icon {{
            width: 80px;
            height: 80px;
            margin: 0 auto 20px;
            opacity: 0.3;
        }}
        
        .no-results-text {{
            font-size: 1.2rem;
            color: var(--text-secondary);
            font-weight: 500;
        }}
        
        @keyframes fadeInDown {{
            from {{
                opacity: 0;
                transform: translateY(-40px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        @keyframes fadeInUp {{
            from {{
                opacity: 0;
                transform: translateY(30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        .anime-card:nth-child(1) {{ animation-delay: 0.05s; }}
        .anime-card:nth-child(2) {{ animation-delay: 0.1s; }}
        .anime-card:nth-child(3) {{ animation-delay: 0.15s; }}
        .anime-card:nth-child(4) {{ animation-delay: 0.2s; }}
        .anime-card:nth-child(5) {{ animation-delay: 0.25s; }}
        .anime-card:nth-child(6) {{ animation-delay: 0.3s; }}
        
        @media (max-width: 768px) {{
            .credit {{
                top: 10px;
                right: 10px;
                font-size: 0.75rem;
                padding: 8px 16px;
            }}
            
            .anime-grid {{
                grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
                gap: 20px;
            }}
            
            .anime-poster {{
                height: 240px;
            }}
            
            .header h1 {{
                font-size: 2rem;
            }}
            
            .stats-grid {{
                grid-template-columns: repeat(2, 1fr);
                gap: 15px;
            }}
            
            .stat-card {{
                padding: 20px 15px;
            }}
            
            .stat-number {{
                font-size: 2rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="credit">
        Made by <a href="https://github.com/TheHolyOneZ" target="_blank">TheHolyOneZ</a>
    </div>
    
    <div class="container">
        <div class="header">
            <h1>🎬 Anime Collection</h1>
            <p class="header-subtitle">Your personal anime library, beautifully organized</p>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">{len(anime_list)}</div>
                    <div class="stat-label">Total Anime</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{series_only_count}</div>
                    <div class="stat-label">Series Only</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{movie_only_count}</div>
                    <div class="stat-label">Movies Only</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{both_count}</div>
                    <div class="stat-label">Series + Movies</div>
                </div>
            </div>
        </div>
        
        <div class="search-filter-container">
            <div class="search-box-wrapper">
                <input type="text" class="search-box" id="searchInput" placeholder="Search your collection..." autocomplete="off">
                <svg class="search-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="11" cy="11" r="8"></circle>
                    <path d="m21 21-4.35-4.35"></path>
                </svg>
            </div>
            
            <div class="filter-tabs">
                <button class="filter-tab active" data-filter="all">All ({len(anime_list)})</button>
                <button class="filter-tab" data-filter="series">📺 Series ({series_only_count})</button>
                <button class="filter-tab" data-filter="movie">🎬 Movies ({movie_only_count})</button>
                <button class="filter-tab" data-filter="series+movies">📺🎬 Both ({both_count})</button>
            </div>
        </div>
        
        <div class="anime-grid" id="animeGrid">
            {''.join(html_cards)}
        </div>
        
        <div class="no-results" id="noResults">
            <svg class="no-results-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <circle cx="11" cy="11" r="8"></circle>
                <path d="m21 21-4.35-4.35"></path>
            </svg>
            <div class="no-results-text">No anime found matching your search</div>
        </div>
    </div>
    
    <script>
        const searchInput = document.getElementById('searchInput');
        const animeGrid = document.getElementById('animeGrid');
        const noResults = document.getElementById('noResults');
        const filterTabs = document.querySelectorAll('.filter-tab');
        const cards = document.querySelectorAll('.anime-card');
        
        let currentFilter = 'all';
        
        function updateVisibility() {{
            const searchTerm = searchInput.value.toLowerCase().trim();
            let visibleCount = 0;
            
            cards.forEach(card => {{
                const title = card.querySelector('.anime-title').textContent.toLowerCase();
                const type = card.getAttribute('data-type');
                
                const matchesSearch = title.includes(searchTerm);
                const matchesFilter = currentFilter === 'all' || type === currentFilter;
                
                const isVisible = matchesSearch && matchesFilter;
                card.classList.toggle('hidden', !isVisible);
                if (isVisible) visibleCount++;
            }});
            
            noResults.classList.toggle('show', visibleCount === 0);
        }}
        
        searchInput.addEventListener('input', updateVisibility);
        
        filterTabs.forEach(btn => {{
            btn.addEventListener('click', () => {{
                filterTabs.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                currentFilter = btn.dataset.filter;
                updateVisibility();
            }});
        }});
        
        searchInput.addEventListener('keydown', (e) => {{
            if (e.key === 'Escape') {{
                searchInput.value = '';
                updateVisibility();
            }}
        }});
        
        document.addEventListener('keydown', (e) => {{
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {{
                e.preventDefault();
                searchInput.focus();
            }}
        }});
    </script>
</body>
</html>'''
        
        with open('exports_website/watchlist_preview.html', 'w', encoding='utf-8') as f:
            f.write(html_template)
    
    @staticmethod
    def export_html_gallery(anime_list):
        with open('exports_website/watchlist_gallery.html', 'w', encoding='utf-8') as f:
            f.write('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Anime Gallery View</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #000;
            color: #fff;
            overflow-x: hidden;
        }
        .credit {
            position: fixed;
            top: 20px;
            right: 20px;
            background: rgba(0, 0, 0, 0.8);
            backdrop-filter: blur(10px);
            padding: 10px 20px;
            border-radius: 50px;
            border: 1px solid #667eea;
            z-index: 1000;
            font-size: 0.9rem;
            font-weight: 600;
        }
        .credit a {
            color: #667eea;
            text-decoration: none;
            transition: color 0.3s ease;
        }
        .credit a:hover {
            color: #f093fb;
        }
        .gallery {
            column-count: 4;
            column-gap: 15px;
            padding: 20px;
        }
        .gallery-item {
            break-inside: avoid;
            margin-bottom: 15px;
            position: relative;
            border-radius: 10px;
            overflow: hidden;
            cursor: pointer;
            transition: transform 0.3s;
        }
        .gallery-item:hover { transform: scale(1.05); }
        .gallery-item img { width: 100%; display: block; }
        .gallery-item .info {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            background: linear-gradient(to top, rgba(0,0,0,0.9), transparent);
            padding: 20px;
            transform: translateY(100%);
            transition: transform 0.3s;
        }
        .gallery-item:hover .info { transform: translateY(0); }
        @media (max-width: 1200px) { .gallery { column-count: 3; } }
        @media (max-width: 768px) { 
            .gallery { column-count: 2; }
            .credit {
                top: 10px;
                right: 10px;
                font-size: 0.75rem;
                padding: 8px 16px;
            }
        }
        @media (max-width: 480px) { .gallery { column-count: 1; } }
    </style>
</head>
<body>
    <div class="credit">
        Made by <a href="https://github.com/TheHolyOneZ" target="_blank">TheHolyOneZ</a>
    </div>
    <div class="gallery">''')
            
            for anime in anime_list:
                f.write(f'''
        <div class="gallery-item">
            <img src="{anime['cover_image']}" alt="{anime['name']}" loading="lazy">
            <div class="info">
                <h3 style="font-size: 1rem; margin-bottom: 5px;">{anime['name']}</h3>
                <a href="{anime['link']}" target="_blank" style="color: #667eea; text-decoration: none;">Watch Now →</a>
            </div>
        </div>''')
            
            f.write('''
    </div>
</body>
</html>''')

class ShareManager:
    @staticmethod
    def generate_qr_and_share(ngrok_token, callback):
        try:
            port = 8000
            script_dir = os.path.dirname(os.path.abspath(__file__))
            os.chdir(script_dir)
            
            server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
            thread = threading.Thread(target=server.serve_forever)
            thread.daemon = True
            thread.start()
            
            if ngrok_token and ngrok_token.strip():
                try:
                    from pyngrok import ngrok
                    ngrok.set_auth_token(ngrok_token)
                    public_url = ngrok.connect(port).public_url
                    share_url = f"{public_url}/watchlist_preview.html"
                    
                    qr = qrcode.QRCode(version=1, box_size=10, border=5)
                    qr.add_data(share_url)
                    qr.make(fit=True)
                    qr_image = qr.make_image(fill_color="black", back_color="white")
                    qr_image.save("watchlist_qr.png")
                    
                    callback(share_url, "watchlist_qr.png")
                    return
                except Exception as ngrok_error:
                    pass
            
            import socket
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            share_url = f"http://{local_ip}:{port}/watchlist_preview.html"
            
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(share_url)
            qr.make(fit=True)
            qr_image = qr.make_image(fill_color="black", back_color="white")
            qr_image.save("watchlist_qr.png")
            
            callback(share_url, "watchlist_qr.png", local_mode=True)
            
        except Exception as e:
            callback(None, None, str(e))

class ModernUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("AniWorld Watchlist Manager V2")
        self.geometry("1100x900")
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.browsers = BrowserDetector.find_browsers()
        self.config = ConfigManager.load_config()
        
        self.create_main_ui()
    
    def create_main_ui(self):
        main_frame = ctk.CTkFrame(self)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        main_frame.grid_columnconfigure(0, weight=1)
        
        top_bar = ctk.CTkFrame(main_frame, fg_color="transparent")
        top_bar.grid(row=0, column=0, sticky="ew", pady=(20, 5))
        top_bar.grid_columnconfigure(0, weight=1)
        
        title_label = ctk.CTkLabel(
            top_bar, 
            text="🎬 AniWorld Watchlist Manager V2",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title_label.pack(side="left", padx=20)
        
        info_btn = ctk.CTkButton(
            top_bar,
            text="ℹ️ Info",
            command=self.show_info,
            width=80,
            height=35,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=["#3B8ED0", "#1F6AA5"]
        )
        info_btn.pack(side="right", padx=20)
        
        subtitle_label = ctk.CTkLabel(
            main_frame,
            text="Extract and share your anime watchlist with style",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        subtitle_label.grid(row=1, column=0, pady=(0, 25))
        
        config_frame = ctk.CTkFrame(main_frame)
        config_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=10)
        config_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(config_frame, text="🔧 Email:", font=ctk.CTkFont(size=13, weight="bold")).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.email_entry = ctk.CTkEntry(config_frame, width=300, placeholder_text="your@email.com")
        self.email_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.email_entry.insert(0, self.config.get('email', ''))
        
        ctk.CTkLabel(config_frame, text="🔒 Password:", font=ctk.CTkFont(size=13, weight="bold")).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.password_entry = ctk.CTkEntry(config_frame, width=300, show="*", placeholder_text="Your password")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.password_entry.insert(0, self.config.get('password', ''))
        
        ctk.CTkLabel(config_frame, text="🌐 Ngrok Token:", font=ctk.CTkFont(size=13, weight="bold")).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        ngrok_frame = ctk.CTkFrame(config_frame, fg_color="transparent")
        ngrok_frame.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        ngrok_frame.grid_columnconfigure(0, weight=1)
        
        self.ngrok_entry = ctk.CTkEntry(ngrok_frame, placeholder_text="Optional - for sharing feature")
        self.ngrok_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.ngrok_entry.insert(0, self.config.get('ngrok_token', ''))
        
        help_label = ctk.CTkLabel(ngrok_frame, text="ℹ️ Optional", font=ctk.CTkFont(size=11), text_color="gray")
        help_label.grid(row=0, column=1)
        
        browser_frame = ctk.CTkFrame(main_frame)
        browser_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=10)
        browser_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(browser_frame, text="🌐 Browser:", font=ctk.CTkFont(size=13, weight="bold")).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        default_browser = "Chrome" if "Chrome" in self.browsers else (list(self.browsers.keys())[0] if self.browsers else "No browsers found")
        self.browser_var = ctk.StringVar(value=default_browser)
        self.browser_menu = ctk.CTkOptionMenu(
            browser_frame,
            variable=self.browser_var,
            values=list(self.browsers.keys()) if self.browsers else ["No browsers found"],
            width=300
        )
        self.browser_menu.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        ctk.CTkLabel(browser_frame, text="🎯 Filter:", font=ctk.CTkFont(size=13, weight="bold")).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.preference_var = ctk.StringVar(value="both")
        preference_frame = ctk.CTkFrame(browser_frame, fg_color="transparent")
        preference_frame.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        
        ctk.CTkRadioButton(preference_frame, text="Series Only", variable=self.preference_var, value="series", font=ctk.CTkFont(size=12)).pack(side="left", padx=15)
        ctk.CTkRadioButton(preference_frame, text="Movies Only", variable=self.preference_var, value="movies", font=ctk.CTkFont(size=12)).pack(side="left", padx=15)
        ctk.CTkRadioButton(preference_frame, text="Both (Recommended)", variable=self.preference_var, value="both", font=ctk.CTkFont(size=12)).pack(side="left", padx=15)
        
        ctk.CTkLabel(browser_frame, text="🎯 Anime Limit:", font=ctk.CTkFont(size=13, weight="bold")).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        limit_frame = ctk.CTkFrame(browser_frame, fg_color="transparent")
        limit_frame.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        limit_frame.grid_columnconfigure(0, weight=1)
        
        self.limit_entry = ctk.CTkEntry(limit_frame, placeholder_text="Leave empty for unlimited", width=200)
        self.limit_entry.grid(row=0, column=0, sticky="w")
        stored_limit = self.config.get('anime_limit', '')
        if stored_limit:
            self.limit_entry.insert(0, str(stored_limit))
        
        limit_help = ctk.CTkLabel(limit_frame, text="ℹ️ Enter number (e.g., 20) to limit anime processed", font=ctk.CTkFont(size=11), text_color="gray")
        limit_help.grid(row=0, column=1, padx=(10, 0))
        
        profile_frame = ctk.CTkFrame(browser_frame, fg_color="transparent")
        profile_frame.grid(row=3, column=1, padx=10, pady=10, sticky="w")
        
        self.use_temp_profile = ctk.CTkCheckBox(
            profile_frame,
            text="⚡ Fast Mode (Temporary Profile - Recommended)",
            font=ctk.CTkFont(size=12)
        )
        self.use_temp_profile.select()
        self.use_temp_profile.pack(side="left")
        
        help_label2 = ctk.CTkLabel(profile_frame, text="ℹ️ Much faster startup, requires manual login", font=ctk.CTkFont(size=10), text_color="gray")
        help_label2.pack(side="left", padx=10)
        
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.grid(row=4, column=0, sticky="ew", padx=20, pady=25)
        button_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        self.extract_btn = ctk.CTkButton(
            button_frame,
            text="🚀 Extract Watchlist",
            command=self.start_extraction,
            font=ctk.CTkFont(size=16, weight="bold"),
            height=45,
            corner_radius=10
        )
        self.extract_btn.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        self.preview_btn = ctk.CTkButton(
            button_frame,
            text="👁️ Preview HTML",
            command=self.preview_html,
            font=ctk.CTkFont(size=16, weight="bold"),
            height=45,
            corner_radius=10,
            state="disabled",
            fg_color="gray40"
        )
        self.preview_btn.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        self.share_btn = ctk.CTkButton(
            button_frame,
            text="📱 Share via QR",
            command=self.share_watchlist,
            font=ctk.CTkFont(size=16, weight="bold"),
            height=45,
            corner_radius=10,
            state="disabled",
            fg_color="gray40"
        )
        self.share_btn.grid(row=0, column=2, padx=10, pady=10, sticky="ew")
        
        log_frame = ctk.CTkFrame(main_frame)
        log_frame.grid(row=5, column=0, sticky="nsew", padx=20, pady=10)
        log_frame.grid_columnconfigure(0, weight=1)
        log_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_rowconfigure(5, weight=1)
        
        ctk.CTkLabel(log_frame, text="📄 Activity Log", font=ctk.CTkFont(size=13, weight="bold")).grid(row=0, column=0, sticky="w", padx=15, pady=(10, 5))
        
        self.log_textbox = ctk.CTkTextbox(
            log_frame, 
            height=200, 
            font=ctk.CTkFont(size=12), 
            wrap="word",
            activate_scrollbars=True
        )
        self.log_textbox.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        
        self.progress_bar = ctk.CTkProgressBar(main_frame, height=8)
        self.progress_bar.grid(row=6, column=0, sticky="ew", padx=20, pady=(10, 20))
        self.progress_bar.set(0)
        
        status_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        status_frame.grid(row=7, column=0, sticky="ew", padx=20, pady=(0, 10))
        
        self.status_label = ctk.CTkLabel(status_frame, text="Ready to extract", font=ctk.CTkFont(size=12), text_color="gray")
        self.status_label.pack(side="left")
        
        self.log("✅ Application initialized successfully!")
        self.log(f"📁 Detected browsers: {', '.join(self.browsers.keys()) if self.browsers else 'None'}")
        if not self.browsers:
            self.log("⚠️ No browsers detected! Please install Chrome, Edge, Opera, or Brave.")
    
    def show_info(self):
        info_window = ctk.CTkToplevel(self)
        info_window.title("ℹ️ Information")
        info_window.geometry("700x800")
        info_window.resizable(False, False)
        info_window.lift()
        info_window.focus_force()
        info_window.attributes('-topmost', True)
        
        title = ctk.CTkLabel(
            info_window,
            text="ℹ️ AniWorld Watchlist Manager V2",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(pady=20)
        
        credit_label = ctk.CTkLabel(
            info_window,
            text="Made by TheHolyOneZ",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#667eea"
        )
        credit_label.pack(pady=5)
        
        def open_github():
            webbrowser.open("https://github.com/TheHolyOneZ")
        
        github_btn = ctk.CTkButton(
            info_window,
            text="🔗 Visit GitHub",
            command=open_github,
            width=200,
            height=35,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        github_btn.pack(pady=10)
        
        scrollable = ctk.CTkScrollableFrame(info_window, width=650, height=550)
        scrollable.pack(pady=20, padx=20, fill="both", expand=True)
        
        info_sections = [
            ("📧 Email & Password", "Enter your AniWorld account credentials. These are saved locally and used for automatic login."),
            ("🌐 Ngrok Token", "Optional. Required for PUBLIC internet sharing via QR code. Without it, sharing only works on your local WiFi network. Get a free token at: https://dashboard.ngrok.com/get-started/your-authtoken"),
            ("🌐 Browser Selection", "Choose which browser to use. Chrome is the default and most reliable option. The tool will use the browser's profile for faster login."),
            ("🎯 Filter Options", "• Series Only: Extract only anime series\n• Movies Only: Extract only anime movies\n• Both: Extract everything (fastest option, no filtering needed)"),
            ("🎯 Anime Limit", "Limit how many anime to process. Leave empty for unlimited. Example: Enter '20' to only process the latest 20 anime from your watchlist. Useful for quick testing or partial exports."),
            ("⚡ Fast Mode", "Uses a temporary browser profile for faster startup (~15-30 seconds). Requires you to manually log in each time. Unchecking this uses your existing browser profile (slower startup but automatic login if previously logged in)."),
            ("🚀 Extract Watchlist", "Starts the extraction process. The tool will:\n1. Open the browser\n2. Log in to AniWorld\n3. Extract your watchlist\n4. Generate multiple file formats (TXT, JSON, Markdown, HTML)\n5. Save everything to the script folder"),
            ("👁️ Preview HTML", "Opens the generated HTML preview in your default browser. Shows a beautiful, searchable, and filterable view of your anime collection."),
            ("📱 Share via QR", "Generates a QR code for sharing your watchlist:\n• With Ngrok token: Works from anywhere (internet)\n• Without Ngrok token: Only works on same WiFi network\n\nScan the QR code with your phone to access the watchlist. Keep the QR window open to maintain the sharing server."),
            ("⚠️ Filter Warning", "When selecting 'Series Only' or 'Movies Only', you'll see a warning because filtering requires visiting each anime's detail page (~2 seconds per anime). The 'Both' option is instant because it doesn't need to check individual types."),
            ("📄 Generated Files", "The tool creates multiple file formats:\n• watchlist.txt - Simple text list\n• watchlist.json - Structured data format\n• watchlist.md - Markdown with images\n• watchlist_preview.html - Beautiful web interface\n• watchlist_gallery.html - Gallery view"),
        ]
        
        for title_text, content_text in info_sections:
            section_frame = ctk.CTkFrame(scrollable)
            section_frame.pack(fill="x", pady=10, padx=10)
            
            ctk.CTkLabel(
                section_frame,
                text=title_text,
                font=ctk.CTkFont(size=15, weight="bold"),
                anchor="w"
            ).pack(anchor="w", padx=15, pady=(10, 5))
            
            ctk.CTkLabel(
                section_frame,
                text=content_text,
                font=ctk.CTkFont(size=12),
                wraplength=600,
                justify="left",
                anchor="w"
            ).pack(anchor="w", padx=15, pady=(0, 10))
        
        close_btn = ctk.CTkButton(
            info_window,
            text="Close",
            command=info_window.destroy,
            width=200,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        close_btn.pack(pady=10)
    
    def log(self, message):
        self.log_textbox.configure(state="normal")
        self.log_textbox.insert("end", f"{message}\n")
        self.log_textbox.see("end")
        self.log_textbox.configure(state="disabled")
        self.update()
    
    def update_status(self, message, color="gray"):
        self.status_label.configure(text=message, text_color=color)
        self.update()
    
    def start_extraction(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        ngrok_token = self.ngrok_entry.get().strip()
        preference = self.preference_var.get()
        limit_text = self.limit_entry.get().strip()
        
        anime_limit = None
        if limit_text:
            try:
                anime_limit = int(limit_text)
                if anime_limit <= 0:
                    self.log("❌ Anime limit must be a positive number!")
                    self.update_status("Error: Invalid limit", "red")
                    return
            except ValueError:
                self.log("❌ Anime limit must be a valid number!")
                self.update_status("Error: Invalid limit", "red")
                return
        
        if not email or not password:
            self.log("❌ Please enter email and password!")
            self.update_status("Error: Missing credentials", "red")
            return
        
        if not self.browsers:
            self.log("❌ No browsers detected on your system!")
            self.update_status("Error: No browsers found", "red")
            return
        
        if preference != 'both':
            warning_window = ctk.CTkToplevel(self)
            warning_window.title("⚡ Fast Filtering Mode")
            warning_window.geometry("500x350")
            warning_window.resizable(False, False)
            warning_window.lift()
            warning_window.focus_force()
            warning_window.attributes('-topmost', True)
            
            ctk.CTkLabel(
                warning_window,
                text="⚡ Fast Filtering Mode",
                font=ctk.CTkFont(size=20, weight="bold")
            ).pack(pady=20)
            
            warning_text = (
                "Filtering will navigate through each anime's detail page.\n\n"
                "✅ OPTIMIZED: ~2 seconds per anime\n"
                "⚡ 234 anime = ~8 minutes total\n"
                "🚀 Disabled images for faster loading\n"
                "📊 Shows: Movie Only, Series Only, or Series+Movies\n\n"
                "💡 Still recommend 'Both' for instant results"
            )
            
            ctk.CTkLabel(
                warning_window,
                text=warning_text,
                font=ctk.CTkFont(size=13),
                justify="left"
            ).pack(pady=10, padx=30)
            
            button_frame = ctk.CTkFrame(warning_window, fg_color="transparent")
            button_frame.pack(pady=20)
            
            def use_both():
                self.preference_var.set("both")
                warning_window.destroy()
                self.start_extraction()
            
            def continue_anyway():
                warning_window.destroy()
                self._do_extraction()
            
            ctk.CTkButton(
                button_frame,
                text="⚡ Use 'Both' (Instant)",
                command=use_both,
                fg_color="green",
                width=200,
                height=40,
                font=ctk.CTkFont(size=14, weight="bold")
            ).pack(side="left", padx=10)
            
            ctk.CTkButton(
                button_frame,
                text="✅ Filter (~8 min)",
                command=continue_anyway,
                fg_color="blue",
                width=200,
                height=40,
                font=ctk.CTkFont(size=14, weight="bold")
            ).pack(side="left", padx=10)
            
            return
        
        self._do_extraction()
    
    def _do_extraction(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        ngrok_token = self.ngrok_entry.get().strip()
        limit_text = self.limit_entry.get().strip()
        
        anime_limit = None
        if limit_text:
            try:
                anime_limit = int(limit_text)
            except:
                anime_limit = None
        
        ConfigManager.save_config(email, password, ngrok_token, anime_limit if anime_limit else '')
        self.log("💾 Configuration saved")
        
        self.extract_btn.configure(state="disabled", text="⏳ Extracting...")
        self.preview_btn.configure(state="disabled")
        self.share_btn.configure(state="disabled")
        self.progress_bar.set(0)
        self.update_status("Starting extraction...", "orange")
        
        Thread(target=self.extraction_thread, daemon=True).start()
    
    def extraction_thread(self):
        scraper = None
        try:
            browser_name = self.browser_var.get()
            browser_path = self.browsers[browser_name]
            preference = self.preference_var.get()
            use_temp = self.use_temp_profile.get()
            
            limit_text = self.limit_entry.get().strip()
            anime_limit = None
            if limit_text:
                try:
                    anime_limit = int(limit_text)
                except:
                    anime_limit = None
            
            self.log(f"🌐 Using browser: {browser_name}")
            if use_temp:
                self.log(f"⚡ Using Fast Mode (temporary profile)")
            else:
                self.log(f"📂 Profile: {browser_path[:50]}...")
            
            if anime_limit:
                self.log(f"🎯 Anime limit set to: {anime_limit}")
            
            self.update_status(f"Using {browser_name}", "blue")
            self.progress_bar.set(0.05)
            
            if not use_temp:
                self.log("🔄 Closing browser instances...")
                killed = BrowserDetector.close_browser_processes(browser_name)
                if killed > 0:
                    self.log(f"✅ Closed {killed} processes")
                else:
                    self.log("✅ No running instances")
            
            self.progress_bar.set(0.1)
            self.log("🚀 Initializing driver...")
            self.update_status("Initializing browser...", "blue")
            scraper = AniWorldScraper(browser_name, browser_path, self.log)
            
            try:
                scraper.init_driver(headless=False, use_temp_profile=use_temp)
            except Exception as e:
                if not use_temp:
                    self.log(f"⚠️ Main profile failed, using temp...")
                    scraper.init_driver(headless=False, use_temp_profile=True)
                else:
                    raise
            
            self.progress_bar.set(0.2)
            time.sleep(2)
            
            self.log("🌐 Loading AniWorld...")
            self.update_status("Loading website...", "blue")
            scraper.driver.get("https://aniworld.to")
            self.log("✅ Homepage loaded")
            time.sleep(4)
            
            self.progress_bar.set(0.25)
            
            self.log("🔍 Checking login status...")
            self.update_status("Checking login...", "blue")
            scraper.driver.get("https://aniworld.to/account/watchlist")
            self.log("✅ Watchlist page reached")
            time.sleep(5)
            
            login_needed = not scraper.check_login_status()
            
            if login_needed:
                self.log("🔒 Login required...")
                self.update_status("Logging in...", "blue")
                
                self.log("🔙 Back to homepage...")
                scraper.driver.get("https://aniworld.to")
                time.sleep(3)
                
                if not use_temp:
                    cookie_loaded = CookieManager.load_cookies(scraper.driver)
                    if cookie_loaded:
                        self.log("🍪 Cookies loaded, testing...")
                        scraper.driver.refresh()
                        time.sleep(4)
                        
                        self.log("🔍 Re-checking login...")
                        scraper.driver.get("https://aniworld.to/account/watchlist")
                        time.sleep(5)
                        login_needed = not scraper.check_login_status()
                
                if login_needed:
                    self.log("🔐 Logging in with credentials...")
                    config = ConfigManager.load_config()
                    
                    login_success = scraper.login(config['email'], config['password'])
                    if not login_success:
                        raise Exception("❌ Login failed! Check credentials.")
                    
                    self.log("✅ Logged in! Going to watchlist...")
                    scraper.driver.get("https://aniworld.to/account/watchlist")
                    time.sleep(5)
            else:
                self.log("✅ Already logged in!")
            
            self.progress_bar.set(0.4)
            self.update_status("Extracting...", "green")
            
            anime_list = scraper.get_watchlist_items(preference, anime_limit)
            
            if not anime_list:
                raise Exception("No anime found! Check if you have items in your watchlist.")
            
            self.progress_bar.set(0.8)
            
            self.log(f"💾 Exporting {len(anime_list)} items...")
            self.update_status("Exporting files...", "blue")
            FileExporter.export_all(anime_list)
            
            self.log("🧹 Cleaning up...")
            scraper.close()
            self.progress_bar.set(1.0)
            
            self.log("")
            self.log(f"🎉 SUCCESS! {len(anime_list)} anime extracted!")
            self.log("")
            self.log("📁 Files created:")
            self.log("   • watchlist.txt")
            self.log("   • watchlist.json")
            self.log("   • watchlist.md")
            self.log("   • watchlist_preview.html")
            self.log("   • watchlist_gallery.html")
            self.log("")
            self.update_status(f"✅ Success! {len(anime_list)} items", "green")
            
            self.preview_btn.configure(state="normal", fg_color=["#3B8ED0", "#1F6AA5"])
            self.share_btn.configure(state="normal", fg_color=["#3B8ED0", "#1F6AA5"])
            self.extract_btn.configure(state="normal", text="🚀 Extract Watchlist")
            
        except Exception as e:
            error_msg = str(e)
            self.log("")
            self.log(f"❌ ERROR: {error_msg}")
            self.log("")
            
            if "login" in error_msg.lower() or "credential" in error_msg.lower():
                self.log("💡 Check your email and password")
            elif "timeout" in error_msg.lower():
                self.log("💡 Connection slow, try again")
            elif "not found" in error_msg.lower() or "no anime" in error_msg.lower():
                self.log("💡 Make sure you have anime in your watchlist")
                self.log("💡 Try using Edge browser instead of Chrome")
            
            self.update_status("❌ Error", "red")
            self.extract_btn.configure(state="normal", text="🚀 Extract Watchlist")
            self.progress_bar.set(0)
        finally:
            if scraper:
                try:
                    scraper.close()
                    self.log("✅ Browser closed")
                except:
                    pass
    
    def preview_html(self):
        if os.path.exists('watchlist_preview.html'):
            webbrowser.open('file://' + os.path.abspath('watchlist_preview.html'))
            self.log("🌐 Preview opened!")
            self.update_status("Preview opened", "green")
        else:
            self.log("❌ No preview! Extract first.")
            self.update_status("No preview", "red")
    
    def share_watchlist(self):
        ngrok_token = self.ngrok_entry.get().strip()
        
        if not ngrok_token:
            self.log("⚠️ No Ngrok token - may be limited")
            self.log("ℹ️ Get token: https://dashboard.ngrok.com/get-started/your-authtoken")
        
        if not os.path.exists('watchlist_preview.html'):
            self.log("❌ No watchlist! Extract first.")
            self.update_status("No watchlist", "red")
            return
        
        self.log("🚀 Starting server...")
        self.update_status("Starting server...", "blue")
        self.share_btn.configure(state="disabled", text="⏳ Starting...")
        
        def share_callback(url, qr_path, error=None, local_mode=False):
            if error:
                self.log(f"❌ Sharing failed: {error}")
                self.update_status("Sharing failed", "red")
                self.share_btn.configure(state="normal", text="📱 Share via QR")
                return
            
            if local_mode:
                self.log(f"✅ Local network sharing active!")
                self.log(f"📱 Devices on same WiFi can access it")
            else:
                self.log(f"✅ Internet sharing active!")
            
            self.log(f"🔗 URL: {url}")
            self.log(f"📱 QR: {qr_path}")
            self.update_status("Sharing active", "green")
            
            qr_window = ctk.CTkToplevel(self)
            qr_window.title("QR Code - Share Watchlist")
            qr_window.geometry("550x700")
            qr_window.resizable(False, False)
            qr_window.attributes('-topmost', True)
            
            qr_window.after(100, lambda: qr_window.lift())
            qr_window.after(100, lambda: qr_window.focus_force())
            
            if local_mode:
                title_text = "📱 Scan on Same WiFi"
                info_text = "⚠️ Only works on your local network\n💡 For internet sharing, add Ngrok token"
            else:
                title_text = "📱 Scan from Anywhere"
                info_text = "✅ Works from anywhere with internet"
            
            title = ctk.CTkLabel(
                qr_window,
                text=title_text,
                font=ctk.CTkFont(size=24, weight="bold")
            )
            title.pack(pady=25)
            
            try:
                qr_img = Image.open(qr_path)
                qr_img = qr_img.resize((400, 400), Image.Resampling.LANCZOS)
                photo = ctk.CTkImage(light_image=qr_img, dark_image=qr_img, size=(400, 400))
                
                img_label = ctk.CTkLabel(qr_window, image=photo, text="")
                img_label.image = photo
                img_label.pack(pady=10)
            except:
                ctk.CTkLabel(qr_window, text="⚠️ QR error", text_color="red").pack()
            
            url_frame = ctk.CTkFrame(qr_window)
            url_frame.pack(pady=20, padx=30, fill="x")
            
            ctk.CTkLabel(url_frame, text="🔗 Share Link:", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", pady=(5, 5))
            
            url_entry = ctk.CTkEntry(url_frame, width=450, height=35, font=ctk.CTkFont(size=12))
            url_entry.insert(0, url)
            url_entry.configure(state="readonly")
            url_entry.pack(pady=5)
            
            def copy_url():
                self.clipboard_clear()
                self.clipboard_append(url)
                copy_btn.configure(text="✅ Copied!", fg_color="green")
                self.after(2000, lambda: copy_btn.configure(text="📋 Copy URL", fg_color=["#3B8ED0", "#1F6AA5"]))
            
            copy_btn = ctk.CTkButton(
                url_frame, 
                text="📋 Copy URL", 
                command=copy_url,
                height=35,
                font=ctk.CTkFont(size=13, weight="bold")
            )
            copy_btn.pack(pady=10)
            
            info_label = ctk.CTkLabel(
                qr_window,
                text=info_text,
                font=ctk.CTkFont(size=12),
                text_color="orange" if local_mode else "green",
                justify="center"
            )
            info_label.pack(pady=15)
            
            warning_label = ctk.CTkLabel(
                qr_window,
                text="⚠️ Keep window open to maintain sharing\nClose to stop server",
                font=ctk.CTkFont(size=11),
                text_color="gray",
                justify="center"
            )
            warning_label.pack(pady=5)
            
            def on_close():
                try:
                    from pyngrok import ngrok
                    ngrok.kill()
                except:
                    pass
                qr_window.destroy()
                self.share_btn.configure(state="normal", text="📱 Share via QR")
                self.log("🛑 Sharing stopped")
                self.update_status("Sharing stopped", "gray")
            
            qr_window.protocol("WM_DELETE_WINDOW", on_close)
        
        Thread(target=lambda: ShareManager.generate_qr_and_share(ngrok_token, share_callback), daemon=True).start()

if __name__ == "__main__":
    app = ModernUI()
    app.mainloop()



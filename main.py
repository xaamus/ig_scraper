import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def load_cookies(driver, cookies_file, url):
    """Ładuje ciasteczka z pliku JSON i odświeża stronę"""
    driver.get(url)  # Przejście na stronę, żeby domena się zgadzała
    time.sleep(2)

    with open(cookies_file, "r", encoding="utf-8") as file:
        cookies = json.load(file)

    for cookie in cookies:
        driver.add_cookie(cookie)  # Dodaj ciasteczka

    driver.refresh()  # Odświeżenie strony po dodaniu ciasteczek
    time.sleep(2)

def scroll_and_scrape(driver, url, output_file):
    """Przewija stronę i zapisuje linki zawierające '/p/'"""
    driver.get(url)
    time.sleep(10)

    collected_links = set()  # Unikalne linki
    count = 0  # Licznik zapisanych linków
    last_height = driver.execute_script("return document.body.scrollHeight")  # Początkowa wysokość strony

    with open(output_file, "w", encoding="utf-8") as file:
        while True:
            elements = driver.find_elements(By.TAG_NAME, "a")  # Pobierz wszystkie linki

            for elem in elements:
                link = elem.get_attribute("href")  # Pobranie atrybutu href
                
                # 🔹 Zapisuj tylko linki zawierające "/p/"
                if link and "/p/" in link and link not in collected_links:
                    collected_links.add(link)
                    file.write(link + "\n")
                    count += 1
                    print(f"Zapisano {count} linków: {link}")

            # 🔹 Przewijanie do dołu strony
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(10)  # Czekamy na załadowanie nowych treści

            # 🔹 Sprawdzamy, czy pojawiło się więcej treści
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:  # Jeśli wysokość się nie zmieniła, kończymy
                break
            last_height = new_height  # Aktualizacja wysokości

    print(f"✅ Znaleziono i zapisano {count} unikalnych linków zawierających '/p/'. Wynik w {output_file}")

if __name__ == "__main__":
    options = webdriver.EdgeOptions()
    options.add_argument("--headless")  # Praca w tle (usuń, jeśli chcesz widzieć okno)
    driver = webdriver.Edge(options=options)

    try:
        # 🔹 Import ciasteczek
        cookies_file = r"C:\Users\kacpe\Downloads\cookies.json"  # Plik z ciasteczkami
        site_url = "https://www.instagram.com"  # Adres strony, gdzie trzeba dodać ciasteczka
        load_cookies(driver, cookies_file, site_url)

        # 🔹 Scrapowanie linków
        data_url = "https://www.instagram.com/xaamuss/saved/all-posts/"  # Strona z danymi
        output_file = r"C:\Users\kacpe\Downloads\links.txt"

        scroll_and_scrape(driver, data_url, output_file)

    finally:
        driver.quit()
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
import pandas as pd
import time

def scrape_olx_selenium(url):
    """
    Scrape OLX using Selenium to handle JavaScript rendering

    Args:
        url: The OLX URL to scrape
    """

    # Configure Firefox options
    firefox_options = Options()
    # Uncomment below to run in headless mode (no GUI)
    firefox_options.add_argument("--headless")

    # Setup Firefox driver
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=firefox_options)

    try:
        print(f"Opening URL: {url}")
        driver.get(url)

        # Wait for page to load - adjust wait time if needed
        print("Waiting for page to load...")
        time.sleep(5)  # Wait for JavaScript to render

        # Try multiple selectors for finding ads
        ads = None
        selectors = [
            (By.CLASS_NAME, "olxad-list__item"),
            (By.XPATH, "//div[contains(@class, 'ListingItem')]"),
            (By.XPATH, "//div[@data-testid='listing-item']"),
            (By.CSS_SELECTOR, "[data-testid*='listing']"),
            (By.CLASS_NAME, "sc-1fcmb83-0"),  # Common OLX class
        ]

        for selector_type, selector_value in selectors:
            try:
                ads = driver.find_elements(selector_type, selector_value)
                if ads and len(ads) > 0:
                    print(f"Found {len(ads)} ads using selector: {selector_type} = {selector_value}")
                    break
            except:
                continue

        # Optional: Additional wait for dynamic content
        time.sleep(2)

        # Debug: Save page source to file
        print("Saving page source for debugging...")
        with open("page_debug.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)

        # Get all ads
        print(f"Found {len(ads)} ads")

        # Get all links first
        links = driver.find_elements(By.CSS_SELECTOR, "a.olx-adcard__link")
        print(f"Found {len(links)} property links")

        # Get all h3 elements containing prices
        prices = driver.find_elements(By.CSS_SELECTOR, "h3.typo-body-large")
        print(f"Found {len(prices)} price elements")

        # Get all location elements
        locations = driver.find_elements(By.CSS_SELECTOR, ".typo-caption.olx-adcard__location")
        print(f"Found {len(locations)} location elements")

        # Extract data from each ad
        properties = []
        min_count = min(len(prices), len(locations), len(links))
        print(f"Extracting data from {min_count} ads\n")

        for i in range(min_count):
            try:
                price = prices[i*2].text if i*2 < len(prices) else prices[i].text if i < len(prices) else "Price not found"
                location = locations[i].text if i < len(locations) else "Location not found"
                link = links[i].get_attribute("href") if i < len(links) else "Link not found"

                # Extract title from link text or aria-label
                title = links[i].text.strip() if (i < len(links) and links[i].text) else (links[i].get_attribute("aria-label") if i < len(links) else "Title not found")
                if not title:
                    title = f"Property {i+1}"

                property_info = {
                    'title': title,
                    'price': price,
                    'location': location,
                    'link': link
                }
                properties.append(property_info)

                print(f"{i+1}. {title[:100]}")
                print(f"   Price: {price}")
                print(f"   Location: {location}")
                print(f"   Link: {link[:300] if len(link) > 10 else link}\n")     
            except Exception as e:
                print(f"Error extracting ad {i+1}: {str(e)[:100]}\n")

        return properties

    except Exception as e:
        print(f"Error: {e}")
        return None

    finally:
        print("\nClosing browser...")
        driver.quit()

if __name__ == "__main__":
    # Inicializa lista para armazenar todas as propriedades
    all_properties = []
    
    for i in range(1, 3):  # Scrape first 2 pages as an example
        url = f"https://www.olx.com.br/imoveis/venda/estado-sp/regiao-de-ribeirao-preto/araraquara?o={i}"
        print(f"\nScraping page {i}...\n")

        properties = scrape_olx_selenium(url)
        
        # Adiciona propriedades da página à lista geral
        if properties:
            all_properties.extend(properties)

    # Salva todas as propriedades no CSV após o loop
    if all_properties:
        df_final = pd.DataFrame(all_properties)
        df_final.to_csv('olx_properties.csv', index=False)
        print(f"\n\nTotal properties found: {len(all_properties)}")
        print("Properties saved to 'olx_properties.csv'")
    else:
        print("No properties found.")
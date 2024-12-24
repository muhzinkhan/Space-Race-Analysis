from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
import time
import csv
import re


def init_driver(driver_path):
    """Initialize the Selenium WebDriver"""
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)
    return driver


def save_csv(all_launches):
    """Save data to a CSV file"""
    with open("scraped/mission_launches.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "Organisation",
                "Location",
                "Date",
                "Detail",
                "Rocket_Status",
                "Price",
                "Mission_Status",
            ]
        )
        writer.writerows(all_launches)
    print("Data saved to 'scraped/mission_launches.csv'")


def find_launch_cards(driver: webdriver.Chrome):
    """Finds all the launches displayed on the current page and returns them as a list, 
    else moves on to the next page
    """
    try:
        return driver.find_elements(
            By.CSS_SELECTOR, "a.mdc-button:not([target]):not(.mdc-button--raised)"
        )
    except NoSuchElementException:
        print(f"Could not find any launch cards on this page. Moving on to next page...")
        return None


def find_next_button(driver: webdriver.Chrome):
    try:
        return driver.find_element(By.LINK_TEXT, "NEXT")
    except NoSuchElementException:
        return None


def safe_get_element_text(driver: webdriver.Chrome, selector_type: str, selector_value: str):
    try:
        return driver.find_element(selector_type, selector_value).text
    except NoSuchElementException:
        print(f"Could not find an element; Skipping...")
        return None


def scrape_detail(driver: webdriver.Chrome):

    # Mission status
    mission_status = safe_get_element_text(driver, By.CSS_SELECTOR, "h6.rcorners.status")
    
    # Rocket detail
    _detail1 = safe_get_element_text(driver, By.CSS_SELECTOR, "h4.mdl-card__title-text")
    _detail2 = safe_get_element_text(driver, By.CSS_SELECTOR, "div.mdl-card__title-text")
    detail = _detail2 + " | " + _detail1

    # Date of launch
    date = safe_get_element_text(driver, By.ID, "localized")

    # Location of launch
    location = safe_get_element_text(driver, By.XPATH, "//h3[contains(@class, 'section--center') and contains(text(), 'Location')]/following::h4")
    
    # Rocket's deatil's WebElement
    _rocket_section = driver.find_element(By.XPATH, "//h3[contains(@class, 'section--center mdl-grid title') and contains(text(), 'Rocket')]/following::div[contains(@class, 'mdl-grid a')]")
    
    # Price of project
    _price = safe_get_element_text(_rocket_section, By.XPATH, "//div[contains(text(), 'Price')]")
    price = float("".join(re.findall(r"[\d.]+", _price))) if _price else None

    # Active status of rocket
    _rocket_status = safe_get_element_text(_rocket_section, By.XPATH, "//div[contains(text(), 'Status')]")
    rocket_status = re.sub(r"(: )", "", _rocket_status).strip() if _rocket_status else None

    # Organisation of the mission
    organisation = safe_get_element_text(_rocket_section, By.XPATH, "./*[1]")

    return [organisation, location, date, detail, rocket_status, price, mission_status]


def scrape_missions(url, driver_path):
    driver = init_driver(driver_path)
    driver.get(url)

    all_launches = []
    page = 1

    try:
        while True:
                # Find the launch cards on the page
                print(f"\n------Page: {page}------")
                details_buttons = find_launch_cards(driver)
                print(f"{len(details_buttons)} Launch cards")

                # Get the details of all the launch cards on the page
                for index, launch in enumerate(details_buttons):

                    print(f"\nClicking #{index+1}. Launch card...")
                    launch.click()
                    # time.sleep(2)

                    # Get the details of a single launch card
                    launch_details = scrape_detail(driver)
                    all_launches.append(launch_details)

                    # time.sleep(2)
                    driver.back()
                    # time.sleep(2)


                # Clicking Next Page
                next_button = find_next_button(driver)
                print("\nClicking Next >> Button...")

                if not next_button:
                    print(f"\nCould not navigate to the Next page >> \nStopping the scraper...")
                    break

                next_button.click()
                page += 1
        

        print(f"\n\nSuccesfully scraped all available pages!!")
        driver.quit()
    
    except Exception as e:
        print(f"\nError occured while scraping.\n{e}\n\nStopping the scraper...")
    finally:
        # Save data to a CSV file
        save_csv(all_launches)


URL = r"https://nextspaceflight.com/launches/past/?page=1"
CHROME_DRIVER_PATH = r"C:\Program Files (x86)\Selenium ChromeDriver\chromedriver.exe"

if __name__ == "__main__":
    scrape_missions(URL, CHROME_DRIVER_PATH)

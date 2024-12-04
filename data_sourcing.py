from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import csv

# Initialize the Selenium WebDriver
def init_driver():
    service = Service()  # Update with the path to your chromedriver
    driver = webdriver.Chrome(service=service)
    return driver

# Function to scrape data from a single page
def scrape_page(driver):
    launches = []
    
    # Locate all launch entries on the page
    launch_elements = driver.find_elements(By.CSS_SELECTOR, ".launch")

    for element in launch_elements:
        try:
            date_time = element.find_element(By.CSS_SELECTOR, ".datetimelink").text
            organisation = element.find_element(By.CSS_SELECTOR, ".agency").text
            location = element.find_element(By.CSS_SELECTOR, ".location").text
            rocket_status = element.find_element(By.CSS_SELECTOR, ".status").text
            mission_name = element.find_element(By.CSS_SELECTOR, ".name").text
            mission_details = element.find_element(By.CSS_SELECTOR, ".missiondesc").text
            vehicle_info = element.find_element(By.CSS_SELECTOR, ".vehicle").text
            price = element.find_element(By.CSS_SELECTOR, ".price").text if element.find_elements(By.CSS_SELECTOR, ".price") else "N/A"
            mission_success_status = element.find_element(By.CSS_SELECTOR, ".missionsuccess").text if element.find_elements(By.CSS_SELECTOR, ".missionsuccess") else "N/A"
            
            launches.append([
                date_time,
                organisation,
                location,
                rocket_status,
                mission_name,
                mission_details,
                vehicle_info,
                price,
                mission_success_status
            ])
        except Exception as e:
            print(f"Error while scraping launch: {e}")

    return launches
    

def save_csv(all_launches):
    # Save data to a CSV file
	with open("/scraped/space_missions.csv", "w", newline="", encoding="utf-8") as file:
		writer = csv.writer(file)
		writer.writerow(["Date Time", "Organisation", "Full Location", "Rocket Status", "Mission Name", "Mission Details", "Vehicle Info", "Price", "Mission Success Status"])
		writer.writerows(all_launches)
	print("Data saved to '/scraped/space_missions.csv'")
    

def find_launch_cards(driver):
    return driver.find_elements(By.CSS_SELECTOR, "a.mdc-button:not([target]):not(.mdc-button--raised)")


def find_next_button(driver):
    return driver.find_elements(By.LINK_TEXT, "NEXT")


def scrapre_launch(driver):
    return driver.find_elements(By.CSS_SELECTOR, "h6.rcorners status")


def scrape_missions(url):
    driver = init_driver()
    driver.get(url)

    all_launches = []

    # # launch_cards[0].click()
    # time.sleep(2)  # Wait for the page to load


    next_button = [1]
    step = 5
    while step:
        print(f"\n------step: {step}------")
        details_buttons = find_launch_cards(driver)
        print(len(details_buttons))
        for index, launch in enumerate(details_buttons):
            print(f"{index+1}. {launch.text}, clicking...")
            launch.click()
            launch_details = scrapre_launch(driver)
            
            print(f"\nscraped details len = {len(launch_details)}")
            for i in launch_details:
                print(f"\n{i.text}")
                 
            driver.back()
        print("\n")
        
        # single next button
        next_button = find_next_button(driver)
        next_button[0].click()
        print(next_button.text, "Button clicked!")
        step-=1


    print(f"Could not navigate to the next page, so stopping")
    driver.quit()

    # Save data to a CSV file
    save_csv(all_launches)
    print("Data saved to '/scraped/space_missions.csv'")


URL = r"https://nextspaceflight.com/launches/past/?page=1"

if __name__ == "__main__":
    scrape_missions(URL)

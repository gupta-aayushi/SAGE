from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import json
from datetime import datetime

def setup_browser():
    options = Options()
    #add a piece of code to run this program without opening the browser
    options.add_argument("--headless")  # Adding headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")

    # Fix: Use Service object with ChromeDriverManager
    service = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service, options=options)
    return browser

def close_modal_if_present(browser):
    try:
        #add the class of the button to close the popup inside the find_elements()
        dismiss_buttons = browser.find_elements(
            By.CSS_SELECTOR, 
            "button.artdeco-modal__dismiss, button.artdeco-toast-item__dismiss"
        )
        
        for button in dismiss_buttons:
            if button.is_displayed():
                browser.execute_script("arguments[0].click();", button)
                print("Clicked modal dismiss button")
                time.sleep(1)
    except Exception as e:
        print("No modal found or error handling modal")

def extract_job_description(browser, card):
    try:
        browser.execute_script("arguments[0].click();", card)
        time.sleep(2)
        #add the class of the job description container inside the presence_of_element_located(())
        
        description_container = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.show-more-less-html__markup"))
        )

        js_remove_restrictions = """
        var element = arguments[0];
        element.className = '';
        element.style.maxHeight = 'none';
        element.style.overflow = 'visible';
        return element.innerHTML;
        """

        try:
            #add the class of the show more button inside the find_elements()
           
            show_more_buttons = browser.find_elements(
                By.CSS_SELECTOR, 
                "button.show-more-less-html__button--more, button.show-more-less-html__button"
            )

            
            for button in show_more_buttons:
                if button.is_displayed() and button.get_attribute("aria-expanded") == "false":
                    browser.execute_script("arguments[0].click();", button)
                    print("Clicked 'Show More' button")
                    time.sleep(2)
        except Exception as e:
            print(f"Show More button handling: {e}")

        description = browser.execute_script(js_remove_restrictions, description_container)

        js_get_full_content = """
        var element = arguments[0];
        var parent = element.parentElement;
        parent.style.maxHeight = 'none';
        parent.style.overflow = 'visible';
        element.style.maxHeight = 'none';
        element.style.overflow = 'visible';
        return element.innerText;
        """

        full_text = browser.execute_script(js_get_full_content, description_container)

        if full_text and len(full_text) > len(description):
            description = full_text

        if isinstance(description, str):
            description = re.sub(r'<script[^>]*>.*?</script>', '', description, flags=re.DOTALL)
            description = re.sub(r'<style[^>]*>.*?</style>', '', description, flags=re.DOTALL)
            description = description.replace('<br>', '\n')
            description = description.replace('<li>', '• ')
            description = description.replace('</li>', '\n')
            description = description.replace('<ul>', '\n').replace('</ul>', '\n')
            description = description.replace('<p>', '').replace('</p>', '\n')
            description = re.sub('<[^<]+?>', '', description)
            description = re.sub(r'\n\s*\n', '\n\n', description)
            description = re.sub(r' +', ' ', description)
            description = description.strip()

        return description if description else "No Description Found"

    except Exception as e:
        print(f"Error extracting job description: {e}")
        return "No Description Found"

def detect_job_cards_with_description(keyword, n=5):
    """
    Scrape LinkedIn for job listings based on search parameters.
    
    Args:
        keyword (str): Job keyword or title to search for
        n (int): Number of jobs to scrape (default: 5)
        
    Returns:
        list: List of job listings with details
    """
    base_url = "https://www.linkedin.com/jobs/search"
    formatted_keyword = keyword.replace(" ", "%20")
    url = f"{base_url}?keywords={formatted_keyword}&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0"
    browser = setup_browser()
    job_listings = []

    try:
        browser.get(url)
        print("Page loaded successfully.")
        time.sleep(5)

        close_modal_if_present(browser)

        job_cards = WebDriverWait(browser, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "base-card"))
        )
        print(f"Number of job cards detected: {len(job_cards)}")

        for idx, card in enumerate(job_cards[:n]):
            try:
                print(f"\nProcessing Job Card {idx + 1}...")

                job_data = {
                    "title": card.find_element(By.CLASS_NAME, "base-search-card__title").text.strip(),
                    "company": card.find_element(By.CLASS_NAME, "base-search-card__subtitle").find_element(By.TAG_NAME, "a").text.strip()
                }

                close_modal_if_present(browser)
                job_data["description"] = extract_job_description(browser, card)

                # Extract location if available
                try:
                    job_data["location"] = card.find_element(By.CLASS_NAME, "job-search-card__location").text.strip()
                except:
                    job_data["location"] = "Location not specified"
                
                # Extract date posted if available
                try:
                    job_data["date_posted"] = card.find_element(By.CSS_SELECTOR, "time.job-search-card__listdate").get_attribute("datetime")
                except:
                    job_data["date_posted"] = "Recently posted"

                job_listings.append(job_data)
                print(f"Successfully processed job: {job_data['title']}")

            except Exception as e:
                print(f"Error processing job card {idx + 1}: {e}")

            time.sleep(2)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        browser.quit()

    filename = f"linkedin_jobs.json"

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(job_listings, f, indent=2, ensure_ascii=False)
        print(f"\nJob listings saved to {filename}")
    except Exception as e:
        print(f"Error saving to JSON: {e}")

    return job_listings


if __name__ == "__main__":
    detect_job_cards_with_description('Web Developer')
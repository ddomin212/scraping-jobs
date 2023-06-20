from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
import chromedriver_autoinstaller

n = 1
postings = []
description = []
chromedriver_autoinstaller.install()

# Set up Selenium webdriver
options = Options()
options.add_argument("--ignore-certificate-errors")
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(
    options=options
)  # Replace with the path to your chromedriver executable

# Open the webpage
driver.get(
    "https://www.startupjobs.cz/nabidky?superinput=data&lokalita=ChIJEVE_wDqUEkcRsLEUZg-vAAQ,ChIJi3lwCZyTC0cRkEAWZg-vAAQ&lokalita-vzdalene=1"
)  # Replace with the actual URL

while True:
    try:
        # Find the div element by its ID
        wait = WebDriverWait(driver, 10)  # Maximum wait time of 10 seconds
        div_element = wait.until(
            EC.visibility_of_element_located((By.ID, "offers-list"))
        )

        wait = WebDriverWait(driver, 10)
        article = wait.until(
            EC.visibility_of_element_located((By.TAG_NAME, "article"))
        )
        # Find all the article elements inside the div
        article_elements = div_element.find_elements(By.TAG_NAME, "article")

        article_urls = []
        # Iterate over each article and extract the text
        for article in article_elements:
            atext = article.text
            link_element = article.find_element(By.CSS_SELECTOR, "a")
            article_urls.append(link_element.get_attribute("href"))
            postings.append(atext)

        for url in article_urls:
            driver.get(url)
            wait = WebDriverWait(driver, 10)
            text_element = wait.until(
                EC.visibility_of_element_located((By.CLASS_NAME, "fr-view"))
            )
            text = text_element.text
            description.append(text)

        n += 1

        driver.get(
            f"https://www.startupjobs.cz/nabidky/strana-{str(n)}?superinput=data&lokalita=ChIJEVE_wDqUEkcRsLEUZg-vAAQ,ChIJi3lwCZyTC0cRkEAWZg-vAAQ&lokalita-vzdalene=1"
        )
    except Exception as e:
        break


driver.quit()

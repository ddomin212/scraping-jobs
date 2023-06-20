from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
import time
import re
import chromedriver_autoinstaller


def monke_get_link(text):
    id_pattern = r'id="([^"]*)"'
    id_match = re.search(id_pattern, text)
    if id_match:
        id = id_match.group(1)
        if "mosaic" not in id:
            return id.split("_")[1]


n = 0
postings = []

# Set up Selenium webdriver
chromedriver_autoinstaller.install()
options = Options()
options.add_argument("--ignore-certificate-errors")
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(
    options=options
)  # Replace with the path to your chromedriver executable

# Open the webpage
driver.get(
    "https://cz.indeed.com/jobs?q=data+analyst%2C+data+scientist%2C+machine+learning%2C+buissness+analyst%2C+BI+analyst"
)  # Replace with the actual URL

while True:
    if n == 2:
        break
    try:
        wait = WebDriverWait(driver, 10)
        ul_element = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[@class='jobsearch-ResultsList css-0']")
            )
        )

        article_elements = ul_element.find_elements(By.XPATH, "./li")

        article_urls = []
        # Iterate over each article and extract the text
        for article in article_elements:
            url = monke_get_link(article.get_attribute("innerHTML"))
            if url:
                article_urls.append("https://cz.indeed.com/viewjob?jk=" + url)

        for url in article_urls:
            driver.get(url)
            wait = WebDriverWait(driver, 10)
            job_info = wait.until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "//div[contains(@class, 'jobsearch-JobComponent')]",
                    )
                )
            )
            title = job_info.find_element(
                By.XPATH, "//div[contains(@class, 'jobsearch-JobInfoHeader')]"
            ).text
            comapny_location = job_info.find_element(
                By.XPATH,
                "//div[contains(@class, 'jobsearch-CompanyInfoWithoutHeaderImage')]",
            ).text.split("\n")
            description = job_info.find_element(
                By.XPATH,
                "//div[contains(@class, 'jobsearch-jobDescriptionText')]",
            ).text
            postings.append((title, comapny_location, description))

        n += 1

        driver.get(
            f"https://cz.indeed.com/jobs?q=data+analyst%2C+data+scientist%2C+machine+learning%2C+buissness+analyst%2C+BI+analyst&start={n*10}"
        )
    except Exception as e:
        break


driver.quit()

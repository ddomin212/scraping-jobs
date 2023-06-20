import datetime
import re
import os
from typing import Tuple, Union
import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def engage_selenium(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-image-loading")
    options.add_argument("--blink-settings=imagesEnabled=false")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-browser-side-navigation")
    options.add_argument("--disable-infobars")
    options.add_argument("--incognito")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )
    driver.get(url)
    wait = WebDriverWait(driver, 10)  # Maximum wait time of 10 seconds
    div_element = wait.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "cp-detail__content"))
    )
    text_values = div_element.text
    driver.quit()
    return text_values


class JobsSpider(scrapy.Spider):
    name = "jobs"
    allowed_domains = ["jobs.cz"]
    domain_name = "https://www.jobs.cz"
    start_urls = [
        "https://www.jobs.cz/prace/?q%5B%5D=machine%20learning&q%5B%5D=data%20analytics&q%5B%5D=data%20science&q%5B%5D=MLOps&q%5B%5D=ML&q%5B%5D=strojové%20učení&q%5B%5D=BI%20analytik&q%5B%5D=Buissness%20Analytik&q%5B%5D=bi%20analyst&q%5B%5D=data%20analyst&profession%5B%5D=201100610&profession%5B%5D=201100592&profession%5B%5D=201100418&profession%5B%5D=201100618&profession%5B%5D=201100658"
    ]

    def parse(self, response):
        jobs = response.css("article.SearchResultCard")

        for job in jobs:
            relative_url = job.css("h2 a ::attr(href)").get()
            title = job.css("h2 a ::text").get().strip()
            pay_range = job.css("span[class*=Tag--success]::text").get()
            comapny = response.css(
                "ul.SearchResultCard__footerList li.SearchResultCard__footerItem:first-child span::text"
            ).get()
            location = (
                response.css(
                    "ul.SearchResultCard__footerList li.SearchResultCard__footerItem:nth-child(2)"
                )
                .re(r">([^<]+)<")[3]
                .strip()
            )
            yield response.follow(
                relative_url,
                callback=self.parse_inzerat,
                meta={
                    "title": title,
                    "pay_range": pay_range,
                    "comapny": comapny,
                    "location": location,
                },
            )

        next_page = response.css(
            "ul.Pagination li.Pagination__item:last-child a::attr(href)"
        ).get()
        if next_page:
            next_page_url = self.domain_name + next_page
            yield response.follow(next_page_url, callback=self.parse)

    def parse_inzerat(self, response):
        all_text = "Not Found"
        div_content = (
            response.css("section.cp-detail__content")
            or response.css("div.cp-detail__content")
            or response.css("div.content-rich-text")
            or response.css("div.standalone.jobad__body")
        )
        if div_content:
            # Extract text from <p> tags
            paragraphs = div_content.css("p::text").getall()

            # Extract text from <h2> tags
            headings = div_content.css("h2::text").getall()

            # Extract text from <ul> tags
            list_items = div_content.css("ul li::text").getall()

            # Extract text from <strong> tags
            strong_text = div_content.css("strong::text").getall()

            # Join all the extracted text into a single string
            all_text = " ".join(
                paragraphs + headings + list_items + strong_text
            )
        else:
            # all_text = engage_selenium(response.url)
            pass

        yield {"url": response.url, "text": all_text, **response.meta}

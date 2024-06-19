import requests
from bs4 import BeautifulSoup
import time
import os
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By


def get_html(url):
    headers = {
        "accept-language": "en-GB,en;q=0.9",
        "user-agent": "Mozilla/5.0 (X11; Linux i686; rv:110.0) Gecko/20100101 Firefox/110.0.",
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text


def parse_reviews(html):
    soup = BeautifulSoup(html, 'lxml')
    reviews = []
    for review in soup.select('div.review'):
        title = review.select_one('a.review-title')
        title = title.select_one('span:not([class])') if title else None
        title = title.text.strip() if title else None

        body = review.select_one('span.review-text')
        body = body.text.strip() if body else None

        rating = review.select_one('i.review-rating')
        rating = rating.text.replace('out of 5 stars', '').strip() if rating else None

        image = review.select_one("img.review-image-tile")
        image = image.attrs["src"] if image else None

        reviews.append({
            'rating': rating,
            'title': title,
            'body': body,
            'image_url': image
        })
    return reviews


def get_next_page_url(soup):
    next_page = soup.select_one('div#cm_cr-pagination_bar ul.a-pagination li.a-last a')
    if next_page and 'href' in next_page.attrs:
        return next_page['href']
    return None


def get_all_reviews(url):
    all_reviews = []

    # while url:
    html = get_html(url)
    reviews = parse_reviews(html)
    all_reviews.extend(reviews)

    soup = BeautifulSoup(html, 'lxml')
    url = get_next_page_url(soup)  # Update URL to the next page

    return all_reviews


def get_all_reviews_selenium(url, driver_path):
    install_dir = "/snap/firefox/current/usr/lib/firefox"
    driver_loc = os.path.join(install_dir, "geckodriver")
    binary_loc = os.path.join(install_dir, "firefox")

    service = FirefoxService(driver_loc)
    opts = webdriver.FirefoxOptions()
    opts.binary_location = binary_loc
    driver = webdriver.Firefox(service=service, options=opts)

    driver.get(url)
    time.sleep(2)  # Wait for the page to load

    all_reviews = []

    while True:
        html = driver.page_source
        reviews = parse_reviews(html)
        all_reviews.extend(reviews)

        try:
            next_button = driver.find_element(By.CSS_SELECTOR, 'div#cm_cr-pagination_bar ul.a-pagination li.a-last a')
            if 'a-disabled' in next_button.get_attribute('class'):
                break  # Exit if the "Next" button is disabled
            next_button.click()
            time.sleep(2)  # Wait for the next page to load
        except Exception as e:
            break  # Exit if there's any issue clicking the "Next" button

    driver.quit()
    return all_reviews

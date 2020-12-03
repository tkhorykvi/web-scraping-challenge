from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser
import pandas as pd
import time


def init_browser():
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def mars_scraping():

    browser = init_browser()
    mars_data = {}

    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    element = soup.select_one("ul.item_list li.slide")

    title = element.find("div",class_="content_title").get_text()
    paragraph = element.find("div",class_="article_teaser_body").get_text()


    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)

    # time.sleep(1)

    element_2 = browser.find_by_id("full_image")


    element_2.click()
    next_step = browser.links.find_by_partial_text("more info")


    next_step.click()
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    image = soup.select_one("figure.lede a img").get("src")

    featured_image_url = "https://www.jpl.nasa.gov" + image



    mars_url = "https://space-facts.com/mars/"
    mars_df = pd.read_html(mars_url)


    mars_df_1 = mars_df[0]
    mars_df_1.columns=["Facts","Values"]


    mars_df_html = mars_df_1.to_html(classes="table table-striped")


    hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemisphere_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")


    items = soup.find_all("div", class_="item")


    image_1 = []
    for item in items:
        image = item.find("a")["href"]
        title = item.find("div", class_="description").find("a").find("h3").text
        image_url = "https://astrogeology.usgs.gov" + image 
        browser.visit(image_url)
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        final_image = soup.find("div", class_="downloads").find("ul").find("li").find("a")["href"]
        image_1.append({"title": title, "image_url": final_image})
    image_1

    mars_data = {
        "title": title,
        "paragraph": paragraph,
        "featured_image": featured_image_url,
        "table": mars_df_html,
        "hemisphere": image_1
    }
    return mars_data







import requests
from bs4 import BeautifulSoup

from safeOperator import safe_int

import json
import time
import datetime

class Crawller(object):
    baseUrl = "https://www.taptap.com/app/%s/review?order=default&page=%s"
    starWidth = 14
    def __init__(self, appid, interval=1):
        self.appid = appid
        self._interval = interval

    def get_page_html(self, page):
        url = self.baseUrl%(str(self.appid), str(page))
        response = requests.get(url)
        time.sleep(self._interval)
        return response.text

    def extract_reviews(self, html):
        soup = BeautifulSoup(html)
        reviews = soup.select("li.taptap-review-item")
        return reviews

    def extract_content(self, review):
        reviewItem = review.select("div.review-item-text")
        if reviewItem:
            reviewItem = reviewItem[0]
        else:
            return None

        reviewId = review['id']
        text_ele = reviewItem.select("div.item-text-body")
        start_ele = reviewItem.select("div.item-text-score i.colored")
        text = ""
        if text_ele:
            text = text_ele[0].text.strip("\n")

        stars = -1
        if start_ele:
            style = start_ele[0]['style']
            width = style.replace("width", "").replace(":", "").replace("px", "").strip()
            _stars = safe_int(width) / self.starWidth
            if _stars:
                stars = _stars
        
        return {"text": text, "stars": stars, "reviewId": reviewId}

    def extract(self, page):
        html = self.get_page_html(page)
        reviews = self.extract_reviews(html)
        result = []
        for review in reviews:
            reviewItem = self.extract_content(review)
            if reviewItem:
                result.append(reviewItem)
        return result

    def extract_all(self, page=0):
        page = page
        while True:
            page += 1
            reviewItems = self.extract(page)
            if not reviewItems:
                break
            yield {"page": page, "items": reviewItems}

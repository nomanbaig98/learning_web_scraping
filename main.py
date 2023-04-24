import requests
from bs4 import BeautifulSoup
from tqdm import *

api_url = "http://localhost:8080/api/product/create"
headers = {"Authorization": "Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxIiwiaWF0IjoxNjgwMjk2NjY3LCJleHAiOjE2ODAzODMwNjd9.hwIGwRdCgOMbW6Ghpxve6FU0aKzCX10bKh0JwKFWeIHrRYcZsYb6NQCUnw34VQnvWeJmpHBZlySKxIGylQ2cXw"}


class Scrapper:

    def __init__(self):
        pass

    def get_names_and_prices(self):
        page = 1
        category_links = [
            "https://www.a101.com.tr/market/atistirmalik/",
            "https://www.a101.com.tr/market/ambalaj-malzemeleri/",
            "https://www.a101.com.tr/market/temel-gida/",
            "https://www.a101.com.tr/market/saglikli-yasam-urunleri/",
            "https://www.a101.com.tr/market/icecek/",
            "https://www.a101.com.tr/market/kahvaltilik-sut-urunleri/",
            "https://www.a101.com.tr/market/ev-bakim-temizlik/",
            "https://www.a101.com.tr/market/hazir-yemek/",
            "https://www.a101.com.tr/market/et-tavuk-balik/",
            "https://www.a101.com.tr/market/meyve-sebze/"
        ]

        for link in tqdm(category_links):
            is_next_button = True
            while is_next_button:
                r = requests.get(link + f"?page={page}")
                soup = BeautifulSoup(r.content, "lxml")
                product_list = soup.find_all(
                    "li", {"class": "col-md-4 col-sm-6 col-xs-6 set-product-item"}
                )

                for li in product_list:
                    try:
                        name = li.find("h3", {"class": "name"})
                        stripped_name = name.text.strip()

                        price = li.find("span", {"class": "current"})
                        stripped_price = price.text.strip(
                            "₺").replace(",", ".")

                        response = requests.post(api_url, headers=headers, json=
                        {
                            "vendor" : "A101",
                            "name" : stripped_name,
                            "category": "ET",
                            "weight": 324.3,
                            "price": stripped_price,
                            "logo": "A101 Logo",
                            "market" : {
                                "name" : "A101",
                                "logo" : "A101 Logo",
                            }
                        })

                        print(response.json())
                    except Exception as e:
                        pass

                page += 1
                if soup.find("a", class_="page-link js-pagination-next") == None:
                    page = 1
                    is_next_button = False




if __name__ == "__main__":
    website = Scrapper()
    website.get_names_and_prices()
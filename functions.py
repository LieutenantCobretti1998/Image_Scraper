# %%
import requests as r
from bs4 import BeautifulSoup
import re
import os
import pandas as pd


def unsplash_image_url_title_scraper(resolution: str, name: str) -> dict[list[str]]:
    unsplash_url = f"https://unsplash.com/s/photos/{name}?license=free"
    response = r.get(url=unsplash_url)
    soup = BeautifulSoup(response.content, "html.parser")
    soup.prettify()

    images = soup.find_all(name="figure", attrs={"itemprop": "image"})
    titles = soup.find_all(name="a", class_="rEAWd")
    sources = {}

    for image, title in zip(images, titles):
        img_element = image.find("img", class_="tB6UZ")
        title_element = title.get("title")
        if img_element:
            srcset_value = img_element.get("srcset")
            if srcset_value:
                urls_with_needed_res = re.findall(rf"(https:\/\/[^\s]+)\s{resolution}", srcset_value)

                if urls_with_needed_res:
                    sources[title_element] = urls_with_needed_res[0]
                else:
                    # Handle the case where the resolution was not found
                    sources[title_element] = ("Url with such Resolution is not found, please provide the resolution "
                                              "between 100w- 2000w")
    return sources


def save_images_on_folder(images: list[tuple[str]], directory: str) -> None:
    if not os.path.exists(directory):
        os.makedirs(directory)

    for description, url in images:
        response = r.get(url)
        if response.status_code == 200:
            filename = f"{description}.jpg"
            filepath = os.path.join(directory, filename)

            with open(filepath, "wb") as file:
                file.write(response.content)

            print(f"Downloaded and saved '{description}' as '{filename}'")
    directory_path = os.path.dirname(filepath)
    print(f"all download images are saved at: {directory_path}")


def create_excel_file(images: list[tuple[str]], file_name: str) -> None:
    images_dict = {description: url for description, url in images}
    df = pd.DataFrame(images_dict.items(), columns=["Description", "Image_URl"])
    writer = pd.ExcelWriter(file_name, engine="xlsxwriter")
    df.to_excel(writer, sheet_name="Image Data", index=False)

    writer._save()


def scrape_with_api(images_number: int, name: str) -> None:
    url = (f"https://unsplash.com/napi/search/photos?query={name}&per_page={images_number}&plus=none&xp=plus-freq"
           f"%3Acontrol")

    headers = {
        'authority': 'unsplash.com',
        'accept': '*/*',
        'accept-language': 'en-US',
        'cookie': 'require_cookie_consent=false; xp-premium-pricing-page=experiment; xp-plus-freq=control; '
                  '_ga=GA1.1.404912846.1695102052; azk-ss=true; _sp_ses.0295=*; '
                  '_ga_21SLH4J369=GS1.1.1695109701.2.1.1695109805.0.0.0; '
                  '_sp_id.0295=cffc7e30-d7de-4877-bfe4-c327a33cf7e1.1695102052.2.1695112277.1695103029.058ba3ca-'
                  '762d-44af-afe7-d777d2f4aec3.1be96b81-6811-4d20-a857-5216d71bfc3a.92d5ad1b-eb34-'
                  '4dfb-b91f-1acd2dc29a14.'
                  '1695109673572.51; require_cookie_consent=false',
        'referer': 'https://unsplash.com/s/photos/forest?license=free',
        'sec-ch-ua': '"Microsoft Edge";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.31'
    }

    response = r.get(url, headers=headers)
    json_data = response.json()

    images_url = dict()

    full_urls = [item['urls']['full'] for item in json_data['results']]
    full_descriptions = [item["alt_description"] for item in json_data["results"]]

    for image, description in zip(full_urls, full_descriptions):
        images_url[description] = image

    return images_url

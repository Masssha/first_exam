import requests
from pprint import pprint
import urllib
from urllib.parse import urlencode
from datetime import datetime
import json
import time
from tqdm import tqdm

# mylist = [1,2,3,4,5,6,7,8]




app_id ="51802470"
OAUTH_BASE_URL = 'https://oauth.vk.com/authorize'
params = {
'client_id': app_id,
'redirect_uri': 'https://oauth.vk.com/blank.html',
'display': 'page',
'scope': 'photos',
'response_type': 'token'
}
oauth_url = f'{OAUTH_BASE_URL}?{urlencode(params)}'
# print(oauth_url)
token = "paste your vk token here"

class VKclient:
    base_url = "https://api.vk.com/method/"
    def __init__(self, y_token, user_id, name_folder):
        self.y_token = y_token
        self.user_id = user_id
        self.name_folder = name_folder

    def new_folder(self):
        base_url = "https://cloud-api.yandex.net/"
        url_new_folder = base_url + "v1/disk/resources"
        headers = {
            "Authorization": self.y_token
        }
        params = {
            "path": self.name_folder
        }
        response = requests.put(url_new_folder, headers=headers, params=params)
        for i in tqdm(range(10)):
            time.sleep(0.1)
        # pprint(response.json())


    def photo_to_yandex(self):

        base_url = "https://api.vk.com/method/"
        params = {
            "access_token": token,
            "v": "5.131",
            "owner_id": self.user_id,
            "album_id": "profile",
            "extended": "1",
            "photo_sizes": "1"
        }
        response = requests.get(f'{base_url}photos.get?', params=params)
        # print(response.json())
        with open('result.json', 'w') as fp:
            json.dump(response.json(), fp)

        base_url = "https://cloud-api.yandex.net/"


        like_list = []
        photos_info = []
        for r in response.json()['response']['items']:
            photo_info = {}
            photo_url = r['sizes'][2]['url']
            photo_likes = r['likes']['count']
            photo_name = photo_likes
            if photo_name in like_list:
                photo_name = f"{photo_likes},{datetime.fromtimestamp(int(r['date']))}".split()[0]
            else:
                photo_name = photo_likes
            like_list.append(photo_name)
            photo_info["file_name"] = photo_name
            photo_info["size"] = r['sizes'][2]['type']
            photos_info.append(photo_info)
            # resp = requests.get(photo_url)

            headers = {
                "Authorization": self.y_token
            }
            params = {
                "path": f"{self.name_folder}/{photo_name}.jpg"
            }
            url_load = base_url + "v1/disk/resources/upload"
            response = requests.get(url_load, headers=headers, params=params)
            url_l = response.json().get("href", "")
            ph = requests.get(photo_url)
            response = requests.put(url_l, data=ph)
            for i in tqdm(range(10)):
                time.sleep(0.1)

        with open('photos_info.json', 'w') as fp:
            json.dump(photos_info, fp)




if __name__ == '__main__':
    vk_newer = VKclient("token_from_yandex_p", "22697565", "ar")
    vk_newer.new_folder()
    vk_newer.photo_to_yandex()



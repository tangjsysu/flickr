import os
import flickrapi
import csv
from tqdm import tqdm
import numpy as np
import requests

API_KEY = "YOUR_API_KEY"
API_SECRET = "YOUR_SECRET_KEY"

flickr = flickrapi.FlickrAPI(API_KEY, API_SECRET, cache=True)

tag = "rigi"
path = "../data/rigi/"
if not os.path.exists(path):
    os.makedirs(path)
lati= []
longi = []
ids = []
times = []
save_path = "../data/results.csv"
photo_urls = []
photo_ids = []
def download_image(url, file_path):
    try:
        response = requests.get(url)
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print("photo saved to:", file_path)
    except Exception as e:
        print("error occurred:", e)

for i in tqdm(range(1,21)):
    photos = flickr.photos.search(api_key=API_KEY, tags=tag,per_page=500, page=i)
    photo_elements = photos.findall('photos/photo')
    for photo in photo_elements:
        photo_id = photo.attrib['id']
        photo_user = photo.attrib['owner']
        photo_secret = photo.attrib['secret']
        photo_url = f'https://live.staticflickr.com/65535/{photo_id}_{photo_secret}_c.jpg'
        try:
            coords = flickr.photos.geo.getLocation(api_key=API_KEY, photo_id=photo_id)
            info = flickr.photos.getInfo(api_key=API_KEY, photo_id=photo_id)
            time = info.find('photo/dates').attrib['posted']
            coord = coords.find('photo/location')
            lati.append(coord.attrib['latitude'])
            longi.append(coord.attrib['longitude'])
            times.append(time)
            ids.append(photo_id)
            with open(save_path, mode='a', newline='') as file:
                writer = csv.writer(file, delimiter=',')
                writer.writerow([photo_id, time, coord.attrib['latitude'], coord.attrib['longitude']])
            file_path = os.path.join(path, f'{photo_id}.jpg')
            download_image(photo_url, file_path)
        except Exception as e:
            print(f"An error occurred while getting location for photo {photo_id}: {e}")
print(len(photo_urls))


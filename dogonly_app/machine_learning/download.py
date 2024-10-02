from flickrapi import FlickrAPI
from urllib.request import urlretrieve
from pprint import pprint
import os, time, sys
from django.conf import settings

key = settings.DOWNLOAD_KEY
secret = settings.DOWNLOAD_SECRET_KEY
wait_time = 1

#保存フォルダの指定
classname = sys.argv[1]
savedir = "./photos/another/" + classname

flickr = FlickrAPI(key, secret, format='parsed-json')
result = flickr.photos.search(
    text = classname,
    per_page = 400,
    media = 'photos',
    sort = 'relevance',
    safe_search = 1,
    extras = 'url_q, licence'
)
photos = result['photos']

for i, photo in enumerate(photos['photo']):
    url_q = photo['url_q']
    filepath = savedir + '/' + photo['id'] + '.jpg'
    if os.path.exists(filepath): continue
    urlretrieve(url_q, filepath)
    time.sleep(wait_time)

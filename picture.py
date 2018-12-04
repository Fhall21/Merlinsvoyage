import requests
import urllib.request
from PIL import Image
print ('setup = done')
def picture(url):
	img = Image.open(requests.get(url, stream = True).raw)
	img.save('img2.jpg')
	#urllib.request.urlretrieve(url, 'image3.jpg')

picture('http://www.merlinsvoyage.net/storage/Merlin au loin.jpg?__SQUARESPACE_CACHEVERSION=1538909540383.jpg')
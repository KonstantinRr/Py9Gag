
### REQUIREMENTS FOR THIS SCRIPT
### PyQt5           => pip install PyQt5
### PyQt5WebKit     => pip install PyQtWebKit (not necessary if show = False)
### PyQtWebEngine   => pip install PyQtWebEngine
### lxml            => pip install lxml
### bs4             => pip install bs4

show = False
url = "https://9gag.com"
rurl = 'https://9gag.com/random?ref=9nav'
directory = 'files/'
filename = 'file_{}.jpg'
threads = 2

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
if show:
    from PyQt5.QtWebKit import *
    from PyQt5.QtWebKitWidgets import *
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView

import urllib.request
import urllib.parse

import bs4 as bs
import http.client
from threading import Thread

def unshorten_url(url):
    parsed = urllib.parse.urlparse(url)
    h = http.client.HTTPConnection(parsed.netloc)
    h.request('HEAD', parsed.path)
    response = h.getresponse()
    if response.status // 100 == 3 and response.getheader('Location'):
        return response.getheader('Location')
    else:
        return url

class Render(QWebEngineView):
    def __init__(self, directory):
        self.directory = directory
        self.html = None
        self.imageCount = 0
        QWebEngineView.__init__(self)
        self.loadFinished.connect(self._loadFinished)

    def _loadFinished(self, result):
        # This is an async call, you need to wait for this
        # to be called before closing the app
        self.page().toHtml(self._callable)

    def _callable(self, data):
        self.html = data
        self.parseData()

    def parseData(self):
        soup = bs.BeautifulSoup(self.html, 'lxml')

        # Parses the image data of the post
        image = soup.find('div', {'class' : 'image-post post-view'})
        #video = soup.find('div', {'class' : 'post-view gif-post'})

        if image is not None:
            # Parses the source attribute
            picture = image.findChild()
            imgs = picture.findChildren('img')
            if len(imgs) != 1:
                print('Unknown length')
                sys.exit(-1)
            src = imgs[0].get('src')

            # Download the file
            place = self.directory + filename.format(self.imageCount)
            urllib.request.urlretrieve(src, place)
            self.imageCount += 1

            print(src, 'as', place)
        else:
            print('Video attribute')

        self.load(QUrl(rurl))



def main():

    app = QApplication(sys.argv)

    web = Render(directory)
    web.load(QUrl(rurl))

    if show:
        web.show()

    status = app.exec_()
    if status != 0: sys.exit(status)

if __name__ == '__main__':
    main()
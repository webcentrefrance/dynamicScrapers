#!/usr/bin/python
# coding: utf-8 
import sys
from PyQt4 import QtCore, QtGui, QtWebKit
from lxml import html

# on ouvre notre fichier de sortie
output = open("chemin/vers/un/fichier.txt", "w")

class WebPage(QtWebKit.QWebPage):
	def __init__(self):
		super(WebPage, self).__init__()
		self.mainFrame().loadFinished.connect(self.handleLoadFinished)

	def start(self, urls):
		self._urls = iter(urls)
		self.fetchNext()

	def fetchNext(self):
		try:
			url = next(self._urls)
		except StopIteration:
			return False
		else:
			self.mainFrame().load(QtCore.QUrl(url))
		return True

	def processCurrentPage(self):
		url = self.mainFrame().url().toString()
		result = self.mainFrame().toHtml()
		tree = html.fromstring(str(result.toAscii()))

		# première donnée à scraper
		xpath1 = tree.xpath('//*xpath')
		# on choisit le premier élément de notre liste
		xpath1li = xpath1[0]
		# on encode s'il y a des bizarreries
		xpath1dec = xpath1li.encode("utf-8")

		# deuxième donnée à scraper
		xpath2 = tree.xpath('//*xpath')
		# on choisit le premier élément de notre liste
		xpath2li = xpath2[0]
		# on encode s'il y a des bizarreries
		xpath2dec = xpath2li.encode("utf-8")

		# on vient écrire dans notre fichier, simili csv
		output.write(xpath1dec)
		output.write(',')
		output.write(xpath2dec)
		output.write('\n')

	def handleLoadFinished(self):
		self.processCurrentPage()
		if not self.fetchNext():
			QtGui.qApp.quit()

if __name__ == '__main__':

	# notre liste d'urls à scraper
	urls = open("/chemin/vers/un/fichier-d-urls.txt", "r")

	app = QtGui.QApplication(sys.argv)
	webpage = WebPage()
	webpage.start(urls)
	sys.exit(app.exec_())
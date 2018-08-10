# !/usr/bin/python
# coding: utf-8 
import sys
import unicodecsv as csv
from itertools import izip
from PyQt4 import QtCore, QtGui, QtWebKit
from lxml import html

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

		# les XPath des données qui nous intéressent
		xpath1 = tree.xpath('//*chemin-xpath')
		xpath2 = tree.xpath('//*chemin-xpath')
		xpath3 = tree.xpath('//*chemin-xpath')

		# on crée un fichier csv et on y met les données
		with open('fichier.csv', 'a') as f:
			fieldnames = ['colonne', 'colonne', 'colonne']
			writer = csv.DictWriter(f, fieldnames=fieldnames)
			writer.writeheader()
			writer = csv.writer(f)
			writer.writerows(izip(xpath1, xpath2, xpath3))

	def handleLoadFinished(self):
		self.processCurrentPage()
		if not self.fetchNext():
			QtGui.qApp.quit()


if __name__ == '__main__':

	# urls à scraper
	urls = open('chemin/vers/un/fichier-d-urls.txt', 'r')

	app = QtGui.QApplication(sys.argv)
	webpage = WebPage()
	webpage.start(urls)
	sys.exit(app.exec_())
import urllib2, json
from bs4 import BeautifulSoup

class Search():

	def __init__(self, FirstName, SecondName, Nohits):

		self.FirstName = FirstName
		self.SecondName = SecondName
		self.Nohits = Nohits
		self.PaperList = []

	def performSearch(self):
		if self.Nohits == "":
			nohits = ""
		else:
			nohits = self.Nohits	

		url = "https://inspirehep.net/search?ln=en&p=find+a+" + self.FirstName + "+"+ self.SecondName +"&of=recjson&action_search=Search&rg="+nohits+"&sf=earliestdate&so=d&ot=recid,number_of_citations,authors,title"
		
		try:
			content = urllib2.urlopen(url).read()
			PaperDict = json.loads(content)
		
		# pass the exception to the GUI so it can properly display the error message
		except ValueError:
			pass

		Search.makePapers(PaperDict, self.PaperList)
			
				

	@staticmethod	
	def makePapers(list, storageList):

		for paper in list:
			title_temp = paper['title']['title']
			no_cit = paper['number_of_citations']
			recid_temp = paper['recid']
			
			bib_url = "https://inspirehep.net/record/" + str(recid_temp) + "/export/hx"    #opens the html with the bibtex entry in it
			bib = BeautifulSoup(urllib2.urlopen(bib_url).read()).find('pre').contents[0]

			s = []
			for author in paper['authors']:
				s.append(author['full_name'])

			authors_temp = s

			storageList.append(Paper(title_temp,s,recid_temp,no_cit, bib))

	@staticmethod		  
	def display_papers(PaperList, box):
		for paper in PaperList:
			paper.show(box)


class Paper():

	def __init__(self, title, author, recid, number_of_citations, bibtex):
    
		self.title = title
		self.author = author
		self.recid = recid
		self.number_of_citations = number_of_citations
		self.bibtex = bibtex

	def show(self, box):

		authorstring = ""
		for author in self.author:
			authorstring += author+ "\n"
		

		tempstring = self.title + "\n" + authorstring + str(self.number_of_citations) + "\n" + "\n"

		box.insert(1, tempstring)
	




# Test method for the classes
if __name__ == '__main__':
	new = Search('sam','bartrum')
	new.performSearch()












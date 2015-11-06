import urllib2
from bs4 import BeautifulSoup
from Tkinter import *
import json

INSP = Tk()

font_style = "helvetica 16"

FN = Entry(INSP,highlightbackground= "black")
SN = Entry(INSP,highlightbackground= "black")
NoHits = Entry(INSP,highlightbackground= "black")
FileName = Entry(INSP,highlightbackground= "black")
FN.grid(row=2, column=1, padx = 10), SN.grid(row=3, column=1), NoHits.grid(row=4, column=1), FileName.grid(row=5, column=1)

Label(INSP, text="First Name", font=font_style).grid(row=2, ipadx = 30)
Label(INSP, text="Second Name",font=font_style).grid(row=3)
Label(INSP, text="Number of hits",font=font_style).grid(row=4)
Label(INSP, text="File to write to",font=font_style).grid(row=5)

Label(INSP, text="Search Results",font=font_style).grid(column = 3, row = 1)
Label(INSP, text="BibTex",font=font_style).grid(column = 4, row = 1)


Papers_widget = Listbox(INSP,highlightbackground= "black", width = 40)
Papers_widget.grid(row=2, column=3, rowspan = 10, sticky = W+E+N+S, padx = 10, pady = 10)

Bibtex_widget = Text(INSP, highlightbackground= "black")
Bibtex_widget.grid(row=2, column=4, rowspan = 10, padx = 10, pady =10)



FirstName  =  ""
SecondName =  ""
NoRecords = 0
WriteFile = ""


class Paper():

	def __init__(self, title, author, recid, number_of_citations, bibtex):
    
		self.title = title
		self.author = author
		self.recid = recid
		self.number_of_citations = number_of_citations
		self.bibtex = bibtex

	def show(self):

		authorstring = ""
		for j in range(len(self.author)):
			authorstring = authorstring + self.author[j]+ "\n"
		

		tempstring = self.title + "\n" + authorstring + str(self.number_of_citations) + "\n" + "\n"


		Papers_widget.insert(1, tempstring)
	
	

PaperList=[]

def makepapers(list):
	for i in range(len(list)):
		title_temp = list[i]['title']['title']
		no_cit = list[i]['number_of_citations']
		recid_temp = list[i]['recid']
		
		bib_url = "https://inspirehep.net/record/" + str(recid_temp) + "/export/hx"    #opens the html with the bibtex entry in it
		bib = BeautifulSoup(urllib2.urlopen(bib_url).read()).find('pre').contents[0]

		s = []
		for j in range(len(list[i]['authors'])):
			s.append(list[i]['authors'][j]['full_name'])

		authors_temp = s

		PaperList.append(Paper(title_temp,s,recid_temp,no_cit, bib))


def reset():
	Bibtex_widget.delete('1.0', END)

  
def display_papers(list, nohits):
	for i in range(int(nohits)):
		list[i].show()


def WriteBibtex():
	filename = FileName.get()
	item = Papers_widget.curselection()[0]
	target = open(filename, 'a')
	target.write(PaperList[item].bibtex)
	target.close()



def display_bibtex():

	Bibtex_widget.delete('1.0', END)
	
	item = Papers_widget.curselection()[0]

	Bibtex_widget.insert('insert', PaperList[item].bibtex)
	Bibtex_widget.insert('insert',"\n")
	

def ReadFile():
	Bibtex_widget.delete('1.0', END)

	filename = FileName.get()

	f = open(filename, 'r')
	Bibtex_widget.insert('insert',f.read())
	f.close()


def mainscript():

	Papers_widget.delete(0, END)


	FirstName  =  FN.get()
	SecondName =  SN.get()
	NoRecords = NoHits.get()

	url = "https://inspirehep.net/search?ln=en&p=find+a+" + FirstName + "+"+ SecondName +"&of=recjson&action_search=Search&sf=earliestdate&so=d&ot=recid,number_of_citations,authors,title"

	content = urllib2.urlopen(url).read()
	test = json.loads(content)

	makepapers(test)

	display_papers(PaperList, NoRecords)

def Quit():
	exit()


GoButton= Button(INSP, text="GO",font=font_style, width=10, command= mainscript, justify = CENTER, pady = 10)
GoButton.grid(row=6, column=0)
ResetButton= Button(INSP, text="Reset",font=font_style, width=10, command= reset, justify = CENTER, pady = 10)
ResetButton.grid(row=6, column=1)
bibtexbutton = Button(INSP, text="View bibtex",font=font_style, width=10, command= display_bibtex, justify = CENTER, pady = 10)
bibtexbutton.grid(row=7, column=0)
ExitButton = Button(INSP, text="Exit?",font=font_style, width = 10, command = Quit, justify = CENTER, pady = 10)
ExitButton.grid(row=7, column=1)


Write = Button(INSP, text="Write?",font=font_style, width = 10, command = WriteBibtex, justify = CENTER, pady = 10)
Write.grid(row=8, column=0)

Read = Button(INSP, text="Read file?",font=font_style, width = 10, command = ReadFile, justify = CENTER, pady = 10)
Read.grid(row=8, column=1)


mainloop()





from __future__ import unicode_literals
from Tkinter import *
from paper import Paper, Search
import tkMessageBox

class PSDisplay():

	font_style = "helvetica 16"

	def __init__(self, frame):

		frame.title("PaperScraper")
		self.populateWidget(frame)

		# Stores the current search, allowing for it to be passed between methods
		self.currentSearch = 0

	def populateWidget(self,frame):	

		self.FN = Entry(frame,highlightbackground= "black")
		self.SN = Entry(frame,highlightbackground= "black")
		self.NoHits = Entry(frame,highlightbackground= "black")
		self.FileName = Entry(frame,highlightbackground= "black")
		self.FN.grid(row=2, column=1), self.SN.grid(row=3, column=1), self.NoHits.grid(row=4, column=1, padx =20), self.FileName.grid(row=5, column=1)

		Label(frame, text="First Name", font=PSDisplay.font_style).grid(row=2)
		Label(frame, text="Second Name",font=PSDisplay.font_style).grid(row=3)
		Label(frame, text="Number of hits",font=PSDisplay.font_style, padx =20 ).grid(row=4)
		Label(frame, text="File to write to",font=PSDisplay.font_style).grid(row=5)
		Label(frame, text="Papers",font=PSDisplay.font_style).grid(column = 3, row = 1)
		Label(frame, text="BibTex",font=PSDisplay.font_style).grid(column = 4, row = 1)

		self.Papers_widget = Listbox(frame,highlightbackground= "black", width = 40, borderwidth = 3)
		self.Papers_widget.grid(row=2, column=3, rowspan = 10, sticky = W+E+N+S, padx = 20, pady = 20)
		self.Bibtex_widget = Text(frame, highlightbackground= "black")
		self.Bibtex_widget.grid(row=2, column=4, rowspan = 10, padx = 20, pady =20)

		self.GoButton = Button(frame, text="Search",font=PSDisplay.font_style, width=10, command= self.mainscript, justify = CENTER)
		self.GoButton.grid(row=6, column=0)
		self.ResetButton= Button(frame, text="Reset",font=PSDisplay.font_style, width=10, command= self.reset, justify = CENTER)
		self.ResetButton.grid(row=6, column=1)
		self.bibtexbutton = Button(frame, text="View bibtex",font=PSDisplay.font_style, width=10, command= self.display_bibtex, justify = CENTER)
		self.bibtexbutton.grid(row=7, column=0)

		self.Write = Button(frame, text="Write",font=PSDisplay.font_style, width = 10, command = self.WriteBibtex, justify = CENTER)
		self.Write.grid(row=8, column=0)
		self.Read = Button(frame, text="Read file",font=PSDisplay.font_style, width = 10, command = self.ReadFile, justify = CENTER)
		self.Read.grid(row=8, column=1)

	# Wipes the bibtex widget
	def reset(self):
		self.Bibtex_widget.delete('1.0', END)


	def mainscript(self):

		self.Papers_widget.delete(0, END)

		self.FirstName  =  self.FN.get()
		self.SecondName =  self.SN.get()
		self.NoRecords = self.NoHits.get()

		if self.FirstName =="" and self.SecondName =="":
			self.warning("Please enter a name!")

		else:	
			search = Search(self.FirstName, self.SecondName, self.NoRecords)
			self.currentSearch = search

			try:
				search.performSearch()
				Search.display_papers(search.PaperList, self.Papers_widget)

			except:
				self.warning("No papers found")


	def display_bibtex(self):

		# This gets the item which has been selected
		try:
			item = self.Papers_widget.curselection()[0]
			self.Bibtex_widget.delete('1.0', END)
			self.Bibtex_widget.insert('insert', self.currentSearch.PaperList[item].bibtex +"\n")	

		except:
			self.warning("Please select a paper")	

		
	def ReadFile(self):

		#clear the bibtex box first
		self.Bibtex_widget.delete('1.0', END)
		filename = self.FileName.get()

		if filename == "":
			self.warning("Please enter a file name!")

		else:
			try:
				f = open(filename, 'r')
				self.Bibtex_widget.insert('insert',f.read())
				f.close()
			except IOError:
				self.warning("File not found!")	
	
		
	def WriteBibtex(self):	
		filename = self.FileName.get()

		if filename == "":
			self.warning("Please enter a file name")

		elif '.' not in filename:
			self.warning("Please add a file extension")

		else:
			item = self.Papers_widget.curselection()[0]
			target = open(filename, 'a')
			target.write(self.currentSearch.PaperList[item].bibtex)
			target.close()


	def warning(self, message):
		tkMessageBox.showinfo("Hang on!", message)
		return False





if __name__ == '__main__':
	INSP = Tk()
	app = PSDisplay(INSP)
	INSP.mainloop()




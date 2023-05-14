from tkinter import *
from tkinter import ttk
from sys import platform

def updateCanvas(itemframeID):
	itemcanvas["scrollregion"] = itemcanvas.bbox("all")
	itemcanvas.itemconfigure(itemframeID, width=itemcanvas.winfo_width()-3)

def scrollCanvas(*args):
	if itemcanvas.yview() == (0.0, 1.0):
		return
	itemcanvas.yview(*args)

def mousewheelCanvas(event, scroll=None):
	if itemcanvas.yview() == (0.0, 1.0):
		return
	if platform == "linux" or platform == "linux2":
		itemcanvas.yview_scroll(int(scroll), "units")
	if platform == "Windows":
		itemcanvas.yview_scroll(int(-1*(event.delta/120)), "units")
	else:
		itemcanvas.yview_scroll(-1*event.delta, "units")

def bindToCanvas(*args):
	if platform == "linux" or platform == "linux2":
		root.bind_all("<Button-4>", lambda event: mousewheelCanvas(event, -1))
		root.bind_all("<Button-5>", lambda event: mousewheelCanvas(event, 1))
	else:
		root.bind_all("<MouseWheel>", lambda event: mousewheelCanvas(event))
	
def unbindToCanvas(*args):
	if platform == "linux" or platform == "linux2":
		root.unbind_all("<Button-4>")
		root.unbind_all("<Button-5>")
	else:
		root.unbind_all("<MouseWheel>")

root = Tk()
root.geometry('700x700')
root.resizable(False,False)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

mainframe = ttk.Frame(root, padding="3 3 3 3", borderwidth=2, relief="solid")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

itemcanvas = Canvas(mainframe, highlightthickness=0)
itemcanvas.grid(column=0, row=0, sticky=(N, W, E, S), padx=3, pady=3)
itemcanvas.columnconfigure(0, weight=1)
itemcanvas.rowconfigure(0, weight=0)

itemframe = ttk.Frame(itemcanvas)
itemframe.columnconfigure(0, weight=1)
itemframe.rowconfigure(0, weight=0)
itemframeID = itemcanvas.create_window((0, 0), window=itemframe, anchor=NW)

scrollbar = ttk.Scrollbar(mainframe, orient='vertical',
						  command=scrollCanvas)
scrollbar.grid(row=0, column=1, sticky=NS)
itemcanvas['yscrollcommand'] = scrollbar.set
itemcanvas.bind("<Configure>", lambda event: updateCanvas(itemframeID))
itemframe.bind("<Configure>", lambda event: updateCanvas(itemframeID))
itemcanvas.bind("<Enter>", lambda event: bindToCanvas())
itemcanvas.bind("<Leave>", lambda event: unbindToCanvas())

for i in range(100):
	ttk.Label(itemframe, text="test").grid(column=0, row=i)

root.mainloop()

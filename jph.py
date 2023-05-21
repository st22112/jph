from tkinter import *
from tkinter import ttk
from sys import platform

# scrolling

def updateCanvas(itemframeID):
	itemcanvas["scrollregion"] = itemcanvas.bbox("all")
	itemcanvas.itemconfigure(itemframeID, width=itemcanvas.winfo_width())

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

# frame management

def mkframe():
	itemlist.append([])
	frameID = next(i for i, e in enumerate(sorted(itemID) + [ None ], 0) if i != e)
	itemID.append(frameID)
	itemlist[-1].append(ttk.Frame(itemframe, padding="3 3 3 3", borderwidth=2,
							   relief="solid"))
	itemlist[-1][0].grid(column=0, row = len(itemlist)-1, sticky=EW, padx=3, pady=3)
	itemlist[-1][0].bind("<Button-1>", lambda event: rmframe(frameID))

	itemlist[-1].append(ttk.Label(itemlist[-1][0], textvariable=itemdata[-1][0]))

	itemlist[-1][1].grid(column=0, row=0)

	itemlist[-1].append(ttk.Label(itemlist[-1][0], textvariable=itemdata[-1][1]))
	itemlist[-1][2].grid(column=1, row=0)

	itemlist[-1].append(ttk.Label(itemlist[-1][0], textvariable=itemdata[-1][2]))
	itemlist[-1][3].grid(column=2, row=0)

	itemlist[-1].append(ttk.Label(itemlist[-1][0], textvariable=itemdata[-1][3]))
	itemlist[-1][4].grid(column=3, row=0)

	itemlist[-1][0].columnconfigure(0, weight=1, uniform="a")
	itemlist[-1][0].columnconfigure(1, weight=1, uniform="a")
	itemlist[-1][0].columnconfigure(2, weight=1, uniform="a")
	itemlist[-1][0].columnconfigure(3, weight=1, uniform="a")

def rmframe(frameID):
	i = itemID.index(frameID)
	itemlist[i][0].destroy()
	del itemlist[i]
	del itemID[i]
	# del itemdata[i]
	if i < len(itemID):
		for i in range(i, len(itemID)):
			itemlist[i][0].grid(row = i)

def addItem():
	print("TODO")
	itemdata.append([])
	itemdata[-1].append(StringVar())
	itemdata[-1].append(StringVar())
	itemdata[-1].append(StringVar())
	itemdata[-1].append(StringVar())
	itemdata[-1][0].set("name")
	itemdata[-1][1].set("1234")
	itemdata[-1][2].set("test")
	itemdata[-1][3].set("42")
	mkframe()

root = Tk()
root.geometry('700x700')
root.resizable(False,False)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

s = ttk.Style()
s.configure("red.TFrame", background="red")


mainframe = ttk.Frame(root, padding="3 3 3 3")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=0)
mainframe.rowconfigure(1, weight=1)
mainframe.rowconfigure(2, weight=0)

sort = ttk.Frame(mainframe, padding="3 3 3 3", borderwidth=2, relief="solid")
sort.grid(column=0, row=0, sticky=EW, padx=6)
sortName = ttk.Label(sort, text="Name")
sortReceipt = ttk.Label(sort, text="Receipt")
sortItem = ttk.Label(sort, text="Item")
sortItemNum = ttk.Label(sort, text="Number of Items")
sortName.grid(column=0, row=0)
sortItem.grid(column=2, row=0)
sortReceipt.grid(column=1, row=0)
sortItemNum.grid(column=3, row=0)
sort.columnconfigure(0, weight=1, uniform="b")
sort.columnconfigure(1, weight=1, uniform="b")
sort.columnconfigure(2, weight=1, uniform="b")
sort.columnconfigure(3, weight=1, uniform="b")

itemcanvas = Canvas(mainframe, highlightthickness=0)
itemcanvas.grid(column=0, row=1, sticky=(N, W, E, S), padx=3, pady=3)
itemcanvas.columnconfigure(0, weight=1)
itemcanvas.rowconfigure(0, weight=0)

itemframe = ttk.Frame(itemcanvas)
itemframe.columnconfigure(0, weight=1)
itemframe.rowconfigure(0, weight=0)
itemframeID = itemcanvas.create_window((0, 0), window=itemframe, anchor=NW)

scrollbar = ttk.Scrollbar(mainframe, orient='vertical',
						  command=scrollCanvas)
scrollbar.grid(row=0, column=1, sticky=NS, rowspan=2)
itemcanvas['yscrollcommand'] = scrollbar.set
itemcanvas.bind("<Configure>", lambda event: updateCanvas(itemframeID))
itemframe.bind("<Configure>", lambda event: updateCanvas(itemframeID))
itemcanvas.bind("<Enter>", lambda event: bindToCanvas())
itemcanvas.bind("<Leave>", lambda event: unbindToCanvas())

add = ttk.Label(mainframe, text="Add item", borderwidth=2, relief="solid",
				padding="10 10 10 10", anchor="center")
add.grid(row=2, column=0, sticky=EW, columnspan=2, padx=3, pady=3)
add.bind("<Button-1>", lambda event: addItem())

itemlist = []
itemID = []
itemdata = []

root.mainloop()

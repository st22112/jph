from tkinter import *
from tkinter import ttk
from sys import platform


# scrolling
# update itemcanvas scroll region when itemcanvas or itemframe changes size
def updateCanvas(itemFrameID):
	itemCanvas["scrollregion"] = itemCanvas.bbox("all")
	itemCanvas.itemconfigure(itemFrameID, width=itemCanvas.winfo_width())

# scoll itemcanvas only when itemframe is bigger than canvas
def scrollCanvas(*args):
	if itemCanvas.yview() == (0.0, 1.0):
		return
	itemCanvas.yview(*args)

# control scrollwheel scrolling
def mousewheelCanvas(event, scroll=None):
	if itemCanvas.yview() == (0.0, 1.0):
		return
	if platform == "linux" or platform == "linux2":
		itemCanvas.yview_scroll(int(scroll), "units")
	if platform == "Windows":
		itemCanvas.yview_scroll(int(-1*(event.delta/120)), "units")
	else:
		itemCanvas.yview_scroll(-1*event.delta, "units")

# bind scrollwheel to scroll itemcanvas
def bindToCanvas(*args):
	if platform == "linux" or platform == "linux2":
		root.bind_all("<Button-4>", lambda event: mousewheelCanvas(event, -1))
		root.bind_all("<Button-5>", lambda event: mousewheelCanvas(event, 1))
	else:
		root.bind_all("<MouseWheel>", lambda event: mousewheelCanvas(event))
	
# unbind scrollwheel to scroll itemcanvas
def unbindToCanvas(*args):
	if platform == "linux" or platform == "linux2":
		root.unbind_all("<Button-4>")
		root.unbind_all("<Button-5>")
	else:
		root.unbind_all("<MouseWheel>")


# frame management
# add frame for item
def mkframe():
	itemList.append([])
	frameID = next(i for i, e in enumerate(sorted(itemID) + [None], 0) if i!=e)
	itemID.append(frameID)
	itemList[-1].append(ttk.Frame(itemFrame, padding="3 3 3 3", borderwidth=2,
							   relief="solid"))
	itemList[-1][0].grid(column=0, row=len(itemList)-1, sticky=EW, padx=3, pady=3)
	itemList[-1][0].bind("<Button-1>", lambda event: rmframe(frameID))

	itemList[-1].append(ttk.Label(itemList[-1][0], textvariable=itemData[-2][0]))
	itemList[-1][1].grid(column=0, row=0)

	itemList[-1].append(ttk.Label(itemList[-1][0], textvariable=itemData[-2][1]))
	itemList[-1][2].grid(column=1, row=0)

	itemList[-1].append(ttk.Label(itemList[-1][0], textvariable=itemData[-2][2]))
	itemList[-1][3].grid(column=2, row=0)

	itemList[-1].append(ttk.Label(itemList[-1][0], textvariable=itemData[-2][3]))
	itemList[-1][4].grid(column=3, row=0)

	itemList[-1][0].columnconfigure((0, 1, 2, 3), weight=1, uniform="item")

# remove frame for item
def rmframe(frameID):
	i = itemID.index(frameID)
	itemList[i][0].destroy()
	del itemList[i]
	del itemID[i]
	del itemData[i]
	if i < len(itemID):
		for i in range(i, len(itemID)):
			itemList[i][0].grid(row = i)

# item entry
# open item entry
def openItemEntry():
	print("TODO")
	addItem.grid_remove()
	cancelItem.grid()
	submitItem.grid()

# close item entry
def closeItemEntry():
	print("TODO")
	addItem.grid()
	cancelItem.grid_remove()
	submitItem.grid_remove()

# create next list for data, close item entry and create frame
def submitItemEntry():
	itemData.append([StringVar(), StringVar(), StringVar(), StringVar()])
	addItem.grid()
	cancelItem.grid_remove()
	submitItem.grid_remove()
	mkframe()


root = Tk()
root.geometry('700x700')
root.resizable(False,False)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)


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
sort.columnconfigure((0, 1, 2, 3), weight=1, uniform="sort")


itemCanvas = Canvas(mainframe, highlightthickness=0)
itemCanvas.grid(column=0, row=1, sticky=(N, W, E, S), padx=3, pady=3)
itemCanvas.columnconfigure(0, weight=1)
itemCanvas.rowconfigure(0, weight=0)

itemFrame = ttk.Frame(itemCanvas)
itemFrame.columnconfigure(0, weight=1)
itemFrame.rowconfigure(0, weight=0)
itemFrameID = itemCanvas.create_window((0, 0), window=itemFrame, anchor=NW)

scrollbar = ttk.Scrollbar(mainframe, orient='vertical',
						  command=scrollCanvas)
scrollbar.grid(row=0, column=1, sticky=NS, rowspan=2)
itemCanvas['yscrollcommand'] = scrollbar.set
itemCanvas.bind("<Configure>", lambda event: updateCanvas(itemFrameID))
itemFrame.bind("<Configure>", lambda event: updateCanvas(itemFrameID))
itemCanvas.bind("<Enter>", lambda event: bindToCanvas())
itemCanvas.bind("<Leave>", lambda event: unbindToCanvas())


itemEntryFrame = ttk.Frame(mainframe)
itemEntryFrame.grid(column=0, row=2, sticky=EW, columnspan=2)
itemEntryFrame.columnconfigure(0, weight=1, uniform="entry")
itemEntryFrame.columnconfigure(1, weight=1, uniform="entry")
addItem = ttk.Label(itemEntryFrame, text="Add item", borderwidth=2,
				relief="solid", padding="10 10 10 10", anchor="center")
addItem.grid(column=0, row=0, sticky=EW, columnspan=2, padx=3, pady=3)
addItem.bind("<Button-1>", lambda event: openItemEntry())

cancelItem = ttk.Label(itemEntryFrame, text="Cancel", borderwidth=2,
				relief="solid", padding="10 10 10 10", anchor="center")
cancelItem.grid(column=0, row=0, sticky=EW, padx=3, pady=3)
cancelItem.bind("<Button-1>", lambda event: closeItemEntry())
cancelItem.grid_remove()

submitItem = ttk.Label(itemEntryFrame, text="Submit", borderwidth=2,
				relief="solid", padding="10 10 10 10", anchor="center")
submitItem.grid(column=1, row=0, sticky=EW, padx=3, pady=3)
submitItem.bind("<Button-1>", lambda event: submitItemEntry())
submitItem.grid_remove()


itemList = []
itemID = []
itemData = [[StringVar(), StringVar(), StringVar(), StringVar()]]

root.mainloop()

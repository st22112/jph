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
		itemCanvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
	else:
		itemCanvas.yview_scroll(-1 * event.delta, "units")


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
def mkFrame():
	itemList.append([])
	frameID = next(
		i for i, e in enumerate(sorted(itemID) + [None], 0) if i != e
	)
	itemID.append(frameID)
	itemList[-1].append(
		ttk.Frame(itemFrame, padding="3 3 3 3", borderwidth=2, relief="solid")
	)
	itemList[-1][0].grid(
		column=0, row=len(itemList) - 1, sticky=EW, padx=3, pady=3
	)


	itemList[-1].append(
		ttk.Label(itemList[-1][0], textvariable=itemData[-2][0])
	)
	itemList[-1][1].grid(column=0, row=0)

	itemList[-1].append(
		ttk.Label(itemList[-1][0], textvariable=itemData[-2][1])
	)
	itemList[-1][2].grid(column=1, row=0)

	itemList[-1].append(
		ttk.Label(itemList[-1][0], textvariable=itemData[-2][2])
	)
	itemList[-1][3].grid(column=2, row=0)

	itemList[-1].append(
		ttk.Label(itemList[-1][0], textvariable=itemData[-2][3])
	)
	itemList[-1][4].grid(column=3, row=0)

	itemList[-1][0].columnconfigure((0, 1, 2, 3), weight=1, uniform="item")

	itemList[-1].append(ttk.Button(itemList[-1][0], text="edit", width=4, command=lambda: openEdit(frameID)))
	itemList[-1][5].grid(column=4, row=0, padx=6)

	itemList[-1].append(ttk.Button(itemList[-1][0], text="\U0001f5d9", width=3, style="delete.TButton", command=lambda: rmFrame(frameID)))
	itemList[-1][6].grid(column=5, row=0)


	itemList[-1].append(
		ttk.Entry(itemList[-1][0], validate="key")
	)
	itemList[-1][7].grid(column=0, row=0)
	itemList[-1][7].grid_remove()
	itemList[-1][7]["validatecommand"] = (inputName.register(validateName), "%d", "%P")

	itemList[-1].append(
		ttk.Entry(itemList[-1][0], validate="key")
	)
	itemList[-1][8].grid(column=1, row=0)
	itemList[-1][8].grid_remove()
	itemList[-1][8]["validatecommand"] = (inputName.register(validateReceipt), "%d", "%P")

	itemList[-1].append(
		ttk.Entry(itemList[-1][0], validate="key")
	)
	itemList[-1][9].grid(column=2, row=0)
	itemList[-1][9].grid_remove()
	itemList[-1][9]["validatecommand"] = (inputName.register(validateName), "%d", "%P")

	itemList[-1].append(
		ttk.Entry(itemList[-1][0], validate="key")
	)
	itemList[-1][10].grid(column=3, row=0)
	itemList[-1][10].grid_remove()
	itemList[-1][10]["validatecommand"] = (inputName.register(validateItemNum), "%d", "%P")

	itemList[-1].append(ttk.Button(itemList[-1][0], text="\U0001f5d9", width=3, command=lambda: cancelEdit(frameID)))
	itemList[-1][11].grid(column=4, row=0, padx=6)
	itemList[-1][11].grid_remove()

	itemList[-1].append(ttk.Button(itemList[-1][0], text="\u2713", width=3, command=lambda: submitEdit(frameID)))
	itemList[-1][12].grid(column=5, row=0)
	itemList[-1][12].grid_remove()



# remove frame for item
def rmFrame(frameID):
	i = itemID.index(frameID)
	itemList[i][0].destroy()
	del itemList[i]
	del itemID[i]
	del itemData[i]
	if i < len(itemID):
		for i in range(i, len(itemID)):
			itemList[i][0].grid(row=i)

def openEdit(frameID):
	i = itemID.index(frameID)
	for j in range(4):
		itemData[i].append(StringVar())
		itemData[i][j+4].set(itemData[i][j].get())

	for j in range(4):
		itemList[i][j+7]["textvariable"] = itemData[i][j+4]

	for j in range(4):
		itemList[i][j+1].grid_remove()
		itemList[i][j+7].grid()
	itemList[i][5].grid_remove()
	itemList[i][6].grid_remove()
	itemList[i][11].grid()
	itemList[i][12].grid()

def cancelEdit(frameID):
	i = itemID.index(frameID)
	del itemData[i][-4:]
	for j in range(4):
		itemList[i][j+1].grid()
		itemList[i][j+7].grid_remove()
	itemList[i][5].grid()
	itemList[i][6].grid()
	itemList[i][11].grid_remove()
	itemList[i][12].grid_remove()

def submitEdit(frameID):
	i = itemID.index(frameID)
	valid = validateData(i, 1)
	if valid == 0:
		for j in range(4):
			itemData[i][j].set(itemData[i][j+4].get())
		del itemData[i][-4:]
		for j in range(4):
			itemList[i][j+1].grid()
			itemList[i][j+7].grid_remove()
		itemList[i][5].grid()
		itemList[i][6].grid()
		itemList[i][11].grid_remove()
		itemList[i][12].grid_remove()
	else:
		print("TODO")


# item entry
# open item entry
def openItemEntry():
	for i in range(4):
		itemData[-1][i].set("")
	addItem.grid_remove()
	listItem.grid()
	cancelItem.grid()
	submitItem.grid()
	inputError.grid_remove()
	root.bind("<Return>", lambda event: submitItemEntry())


# close item entry
def closeItemEntry():
	addItem.grid()
	listItem.grid_remove()
	cancelItem.grid_remove()
	submitItem.grid_remove()
	inputError.grid_remove()


# create next list for data, close item entry and create frame
def submitItemEntry():
	valid = validateData(-1, 0)
	if valid == 0:
		itemData.append([StringVar(), StringVar(), StringVar(), StringVar()])
		inputName["textvariable"] = itemData[-1][0]
		inputReceipt["textvariable"] = itemData[-1][1]
		inputItemName["textvariable"] = itemData[-1][2]
		inputItemNum["textvariable"] = itemData[-1][3]
		addItem.grid()
		listItem.grid_remove()
		cancelItem.grid_remove()
		submitItem.grid_remove()
		inputError.grid_remove()
		mkFrame()
		root.bind("<Return>", lambda event: openItemEntry())
	else:
		addItemError(valid)


# jump
def validateName(inputAction, inputStr):
	if inputAction == "1" and len(inputStr) > 20:
		return False
	return True

def validateReceipt(inputAction, inputStr):
	if inputAction == "1" and (len(inputStr) > 20 or not inputStr.isdigit()):
		return False
	return True

def validateItemNum(inputAction, inputStr):
	if inputAction == "1" and (len(inputStr) > 3 or not inputStr.isdigit() or int(inputStr) > 500):
		return False
	return True

def validateData(index, mode):
	if mode == 0:
		itemData[index][0].set(itemData[index][0].get().strip())
		itemData[index][1].set(itemData[index][1].get().lstrip("0"))
		itemData[index][2].set(itemData[index][2].get().strip())
		itemData[index][3].set(itemData[index][3].get().lstrip("0"))
		for i in range(4):
			if itemData[index][i].get() == "":
				return (i+1)
		if itemData[index][1].get() in [receipt[1].get() for receipt in itemData[:-1]]:
			return 5
		return 0;
	if mode == 1:
		itemData[index][4].set(itemData[index][4].get().strip())
		itemData[index][5].set(itemData[index][5].get().lstrip("0"))
		itemData[index][6].set(itemData[index][6].get().strip())
		itemData[index][7].set(itemData[index][7].get().lstrip("0"))
		for i in range(4):
			if itemData[index][i+4].get() == "":
				return (i+1)
		if itemData[index][5].get() in [receipt[1].get() for receipt in itemData[0:index]]:
			return 5
		if itemData[index][5].get() in [receipt[1].get() for receipt in itemData[index+1:]]:
			return 5
		return 0;

def addItemError(error):
	if error == 1:
		inputError["text"] = "Customer name must not be empty"
	if error == 2:
		inputError["text"] = "Receipt number must not be empty"
	if error == 3:
		inputError["text"] = "Item name must not be empty"
	if error == 4:
		inputError["text"] = "Number of items must not be empty"
	if error == 5:
		inputError["text"] = "Receipt number must be unique"
	inputError.grid()


root = Tk()
root.geometry("700x700")
#root.resizable(False, False)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)


itemList = []
itemID = []
itemData = [[StringVar(), StringVar(), StringVar(), StringVar()]]

s = ttk.Style()
s.theme_use("clam")
s.configure("error.TLabel", foreground="red")
s.configure(
	"delete.TButton",
	background="red",
	bordercolor="red",
	lightcolor="red",
	darkcolor="red",
	focuscolor="none"
)
s.map(
	"delete.TButton",
	background=[("pressed", "red"), ("active", "red")],
	borderwidth=[("active", 0)],
)


mainframe = ttk.Frame(root, padding="3 3 3 3")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=0)
mainframe.rowconfigure(1, weight=1)
mainframe.rowconfigure(2, weight=0)


sort = ttk.Frame(mainframe, padding="3 3 94 3", borderwidth=2, relief="solid")
# 3 + itemList[-1][5].winfo_width() + 2*6 + itemList[-1][6].winfo_width()
sort.grid(column=0, row=0, sticky=EW, padx=6)
sortName = ttk.Label(sort, text="Customer name")
sortReceipt = ttk.Label(sort, text="Receipt number")
sortItem = ttk.Label(sort, text="Item name")
sortItemNum = ttk.Label(sort, text="Number of Items")
sortName.grid(column=0, row=0)
sortReceipt.grid(column=1, row=0)
sortItem.grid(column=2, row=0)
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

scrollbar = ttk.Scrollbar(mainframe, orient="vertical", command=scrollCanvas)
scrollbar.grid(row=0, column=1, sticky=NS, rowspan=2)
itemCanvas["yscrollcommand"] = scrollbar.set
itemCanvas.bind("<Configure>", lambda event: updateCanvas(itemFrameID))
itemFrame.bind("<Configure>", lambda event: updateCanvas(itemFrameID))
itemCanvas.bind("<Enter>", lambda event: bindToCanvas())
itemCanvas.bind("<Leave>", lambda event: unbindToCanvas())


itemEntryFrame = ttk.Frame(mainframe)
itemEntryFrame.grid(column=0, row=2, sticky=EW, columnspan=2)
itemEntryFrame.columnconfigure(0, weight=1, uniform="entry")
itemEntryFrame.columnconfigure(1, weight=1, uniform="entry")

#addItem = ttk.Label(
#	itemEntryFrame,
#	text="Add item",
#	borderwidth=2,
#	relief="solid",
#	padding="10 10 10 10",
#	anchor="center"
#)
addItem = ttk.Button(
	itemEntryFrame,
	text="Add item",
	padding="10 10 10 10",
	command=openItemEntry
)
addItem.grid(column=0, row=0, sticky=EW, columnspan=2, padx=3, pady=3)
#addItem.bind("<Button-1>", lambda event: openItemEntry())

listItem = ttk.Frame(
	itemEntryFrame, padding="3 3 3 3", borderwidth=2, relief="solid"
)
listItem.grid(column=0, row=0, sticky=EW, columnspan=2, padx=3, pady=3)
ttk.Label(listItem, text="Customer name").grid(column=0, row=0)
ttk.Label(listItem, text="Receipt number").grid(column=1, row=0)
ttk.Label(listItem, text="Item name").grid(column=2, row=0)
ttk.Label(listItem, text="Number of Items").grid(column=3, row=0)
inputName = ttk.Entry(listItem, textvariable=itemData[-1][0], validate="key")
inputReceipt = ttk.Entry(listItem, textvariable=itemData[-1][1], validate="key")
inputItemName = ttk.Entry(listItem, textvariable=itemData[-1][2], validate="key")
inputItemNum = ttk.Entry(listItem, textvariable=itemData[-1][3], validate="key")
inputName["validatecommand"] = (inputName.register(validateName), "%d", "%P")
inputReceipt["validatecommand"] = (inputName.register(validateReceipt), "%d", "%P")
inputItemName["validatecommand"] = (inputName.register(validateName), "%d", "%P")
inputItemNum["validatecommand"] = (inputName.register(validateItemNum), "%d", "%P")
inputName.grid(column=0, row=1)
inputReceipt.grid(column=1, row=1)
inputItemName.grid(column=2, row=1)
inputItemNum.grid(column=3, row=1)
inputError = ttk.Label(listItem, style="error.TLabel")
inputError.grid(column=0, row=2, columnspan=4, padx=3, pady=3)
inputError.grid_remove()
listItem.columnconfigure((0, 1, 2, 3), weight=1, uniform="listItem")
listItem.grid_remove()

#cancelItem = ttk.Label(
#	itemEntryFrame,
#	text="Cancel",
#	borderwidth=2,
#	relief="solid",
#	padding="10 10 10 10",
#	anchor="center"
#)
cancelItem = ttk.Button(
	itemEntryFrame,
	text="Cancel",
	padding="10 10 10 10",
	command=closeItemEntry
)
cancelItem.grid(column=0, row=1, sticky=EW, padx=3, pady=3)
#cancelItem.bind("<Button-1>", lambda event: closeItemEntry())
cancelItem.grid_remove()

#submitItem = ttk.Label(
#	itemEntryFrame,
#	text="Submit",
#	borderwidth=2,
#	relief="solid",
#	padding="10 10 10 10",
#	anchor="center"
#)
submitItem = ttk.Button(
	itemEntryFrame,
	text="Submit",
	padding="10 10 10 10",
	command=submitItemEntry
)
submitItem.grid(column=1, row=1, sticky=EW, padx=3, pady=3)
#submitItem.bind("<Button-1>", lambda event: submitItemEntry())
submitItem.grid_remove()

root.bind("<Return>", lambda event: openItemEntry())


root.mainloop()

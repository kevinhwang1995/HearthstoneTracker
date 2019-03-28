from tkinter import *
import sqlite3 as sq

#Initializes the window.
window = Tk()
window.title("Hearthstone Tracker")
window.geometry("700x500")
window.configure(background = "grey")
#Creating SQL tables
con = sq.connect('hearthstone.db')
c = con.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS deck (
	name varchar(20),
    deck_class varchar(20), wins int(11), losses int(11),
    winrate int(11))"""
)

c.execute("""CREATE TABLE IF NOT EXISTS game (
    deck_id int(11),
    opponent_class varchar(20),
    result BOOLEAN,
    FOREIGN KEY(deck_id) REFERENCES deck(id))"""
)
con.commit()

def get():
	print("You have submitted a deck.")
	c.execute('INSERT INTO deck (name, deck_class, wins, losses, winrate) VALUES (?, ?, 0, 0, NULL)', (deck_name.get(), deck_class.get()))
	con.commit()
	
def clear():
	deck_class.set('----')
	deck_name.set('')
	
#Adds the logo at the top of the window.
logo = PhotoImage(file = "legend.gif")
header = Label(window, image = logo, bg = "grey")
header.place(relx = 0.5, y = 20,anchor = CENTER)

#Input fields for adding a deck.
L1 = Label(window, text = "Add a deck.", font = ("arial", 14), bg = "grey").place(x = 10, y = 50)
L2 = Label(window, text = "Class:", font = ("arial", 12), bg = "grey").place(x = 10, y = 90)
L3 = Label(window, text = "Deck Name:", font = ("arial", 12), bg = "grey").place(x = 120 , y = 90)

deck_class = StringVar(window)
deck_name = StringVar(window)

deck_class_dict = {'Druid', 'Hunter', 'Mage', 'Paladin', 'Priest', 'Rogue', 'Shaman', 'Warlock', 'Warrior'}

deck_class_d = OptionMenu(window, deck_class, *deck_class_dict)
deck_class_d.place(x = 70, y = 90)

deck_name_input = Entry(window, textvariable = deck_name)
deck_name_input.place(x = 210, y = 92)

addButton = Button(window, text = "Submit Deck", command = get)
addButton.place(x = 10, y = 130)

clearButton = Button(window, text = "Clear Entries", command = clear)
clearButton.place(x = 90, y = 130)

#Creates the decklists UI.
decksTitle = Message(window, width = 100, text = "Decklists", bg = "grey").place(x = 60, y = 170)
decksBox = Frame(window, width = 200, height = 300)
decksBox.place(x = 0, y = 190)

#Pulls deck information from database and displays in decklists UI.
c.execute("SELECT * FROM deck")
data = c.fetchall()



window.mainloop()
con.close()
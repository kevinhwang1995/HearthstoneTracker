from tkinter import *
import sqlite3 as sq

#Initializes the window.
window = Tk()
window.title("Hearthstone Tracker")
window.geometry("700x500")
window.update()
window.configure(background = "black")
window.maxsize(window.winfo_width(), window.winfo_height())

#Creating SQL tables
con = sq.connect('hearthstone.db')
c = con.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS deck (
	id integer PRIMARY KEY, name varchar(20), deck_class varchar(20), 
	wins int(11), losses int(11), winrate float)"""
)

c.execute("""CREATE TABLE IF NOT EXISTS game (
    deck_id int(11),
    opponent_class varchar(20),
    result BOOLEAN,
    FOREIGN KEY(deck_id) REFERENCES deck(id))"""
)
con.commit()

#Method used to submit a deck to the database.
def get():
	print("You have submitted a deck.")
	c.execute('INSERT INTO deck (name, deck_class, wins, losses, winrate) VALUES (?, ?, 0, 0, 0)', (deck_name.get(), deck_class.get()))
	con.commit()
	update_decks()
	clear()
	
#Method used to clear the input fields.
def clear():
	deck_class.set('----')
	deck_name.set('')
	
#Switch method used to choose class color for decklists UI.
def get_class_color(class_name):
	switcher = {
		"Druid": "tan4",
		"Hunter": "green",
		"Mage": "deep sky blue",
		"Paladin": "yellow",
		"Priest": "snow",
		"Rogue": "grey",
		"Shaman": "blue",
		"Warlock": "purple",
		"Warrior": "red"
	}
	return switcher.get(class_name)
	
#Switch method used to choose class portrait for statistics UI.
def get_class_portrait(class_name):
	switcher = {
		"Druid": "druid.gif",
		"Hunter": "hunter.gif",
		"Mage": "mage.gif",
		"Paladin": "paladin.gif",
		"Priest": "priest.gif",
		"Rogue": "rogue.gif",
		"Shaman": "shaman.gif",
		"Warlock": "warlock.gif",
		"Warrior": "warrior.gif"
	}
	return switcher.get(class_name)
	
def update_decks():
	for widget in decks_box.winfo_children():
		widget.destroy()
	c.execute("SELECT * FROM deck")
	data = c.fetchall()
	print(data)
	for row in data:
		deck_button = Button(decks_box, text = row[1], width = 25, bg = get_class_color(row[2]), relief = RAISED, command = lambda row = row: update_stats(row[1], row[2]))
		deck_button.pack()
	
def update_stats(deck_name, deck_class):
	for widget in stats_frame.winfo_children():
		widget.destroy()
	for widget in portrait_frame.winfo_children():
		widget.destroy()
	c.execute("SELECT * FROM deck WHERE name = ? AND deck_class = ?", (deck_name, deck_class))
	data = c.fetchall()
	for row in data:
		portrait = PhotoImage(file = get_class_portrait(row[2]))
		class_portrait = Label(portrait_frame, image = portrait, bg = "black")
		class_portrait.image = portrait
		class_portrait.pack(anchor = NE)
		deck_name_label = Label(stats_frame, text = row[1], font = ("arial", 20), bg = "black", fg = get_class_color(row[2])).grid(row = 0, column = 0, sticky = W)
		wins_label = Label(stats_frame, text = "Wins: " + str(row[3]), font = ("arial", 14), bg = "black", fg = get_class_color(row[2])).grid(row = 2, column = 0, sticky = W, pady = 15)
		losses_label = Label(stats_frame, text = "Losses: " + str(row[4]), font = ("arial", 14), bg = "black", fg = get_class_color(row[2])).grid(row = 3, column = 0, sticky = W, pady = 15)
		winrate = (str(row[5])[:2])
		winrate_label = Label(stats_frame, text = "Winrate: " + winrate + "%", font = ("arial", 14), bg = "black", fg = get_class_color(row[2])).grid(row = 4, column = 0, sticky = W, pady = 15)	
		delete_button = Button(stats_frame, text = "Delete Deck", command = lambda: delete_deck(row[1], row[2])).grid(row = 5, column = 0, pady = 15, sticky = W)
		add_game = Label(stats_frame, text = "Add a Game:", font = ("arial", 18), bg = "black", fg = "white").grid(row = 3, column = 1, sticky = E)
		game_opponent = Label(stats_frame, text = "Opponent's Class:", font = ("arial", 14), bg = "black", fg = "white").grid(row = 4, column = 1, sticky = E)
		game_win = Button(stats_frame, text = "Add Win", command = lambda: add_win(row[1], row[2])).grid(row = 5, column = 1, sticky = E)
		game_loss = Button(stats_frame, text = "Add Loss", command = lambda: add_loss(row[1], row[2])).grid(row = 5, column = 2, sticky = E)
		
def delete_deck(deck_name, deck_class):
	c.execute('DELETE FROM deck WHERE name = ? AND deck_class = ?', (deck_name, deck_class))
	con.commit()
	update_decks()
	update_stats(deck_name, deck_class)

def add_win(deck_name, deck_class):
	c.execute('UPDATE deck SET wins = wins + 1 WHERE name = ? AND deck_class = ?', (deck_name, deck_class))
	con.commit()
	c.execute('UPDATE deck SET winrate = (100 * Cast(wins AS float)) / (Cast(wins AS float) + Cast(losses AS float)) WHERE name = ? AND deck_class = ?', (deck_name, deck_class))
	con.commit()
	update_stats(deck_name, deck_class)
	
def add_loss(deck_name, deck_class):
	c.execute('UPDATE deck SET losses = losses + 1 WHERE name = ? AND deck_class = ?', (deck_name, deck_class))
	con.commit()
	c.execute('UPDATE deck SET winrate = (100 * Cast(wins AS float)) / (Cast(wins AS float) + Cast(losses AS float)) WHERE name = ? AND deck_class = ?', (deck_name, deck_class))
	con.commit()
	update_stats(deck_name, deck_class)
	
#Adds the logo at the top of the window.
logo = PhotoImage(file = "legend.gif")
header = Label(window, image = logo, bg = "black")
header.place(relx = 0.5, y = 20,anchor = CENTER)

#Input fields for adding a deck.
L1 = Label(window, text = "Add a deck.", font = ("arial", 14), bg = "black", fg = "white").place(x = 10, y = 50)
L2 = Label(window, text = "Class:", font = ("arial", 12), bg = "black", fg = "white").place(x = 10, y = 90)
L3 = Label(window, text = "Deck Name:", font = ("arial", 12), bg = "black", fg = "white").place(x = 150 , y = 90)

deck_class = StringVar(window)
deck_name = StringVar(window)

deck_class_dict = {'Druid', 'Hunter', 'Mage', 'Paladin', 'Priest', 'Rogue', 'Shaman', 'Warlock', 'Warrior'}

deck_class_d = OptionMenu(window, deck_class, *deck_class_dict)
deck_class_d.place(x = 70, y = 90)

deck_name_input = Entry(window, textvariable = deck_name)
deck_name_input.place(x = 240, y = 92)

add_button = Button(window, text = "Submit Deck", command = get)
add_button.place(x = 10, y = 130)

clear_button = Button(window, text = "Clear Entries", command = clear)
clear_button.place(x = 90, y = 130)

#Creates the decklists UI.
decks_title = Message(window, width = 100, text = "Decklists", borderwidth = 0, bg = "black", fg = "white").place(x = 60, y = 170)
decks_box = Frame(window, width = 200, height = 300, bg = "black")
decks_box.place(x = 0, y = 190)

#Creates the statistics UI.
stats_frame = Frame(window, width = 500, height = 310, bg = "black", borderwidth = 5, relief = SUNKEN)
stats_frame.place(x = 200, y = 190)
stats_frame.grid_propagate(0)

#Creates the portrait UI.
portrait_frame = Frame(window, bg = "black")
portrait_frame.place(x = 500, y = -5)

update_decks()

#End the program.
window.mainloop()
con.close()
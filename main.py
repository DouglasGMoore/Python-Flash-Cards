from tkinter import *
import pandas
from pandas import DataFrame
import random

BACKGROUND_COLOR = "#B1DDC6"


# --------------------------  Functionality -------------------------- #
try:
    words_to_learn = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    word_df = pandas.read_csv("data/french_words.csv")
    to_learn = word_df.to_dict(orient="records")
else:
    to_learn = words_to_learn.to_dict(orient="records")
finally:
    current_card = {}


def known():
    global current_card
    to_learn.remove(current_card)
    df = DataFrame(to_learn, columns=['French', 'English'])
    df.to_csv("data/words_to_learn.csv", index=False)
    next_word()


def flip_card():
    global current_card
    canvas.itemconfig(card_title, fill="white", text="English")
    canvas.itemconfig(card_word, fill="white", text=current_card["English"])
    canvas.itemconfig(card_background, image=card_back)


def next_word():
    global current_card, timer
    window.after_cancel(timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_word, fill="black", text=current_card["French"])
    canvas.itemconfig(card_title, fill="black", text="French")
    canvas.itemconfig(card_background, image=card_front)
    timer = window.after(3000, flip_card)


# -------------------------------- UI -------------------------------- #
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

timer = window.after(3000, flip_card)

# Card
canvas = Canvas(width=800, height=526)
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=2)

# Card text
card_title = canvas.create_text(400, 150, font=("Arial", 40, "italic"), text="")
card_word = canvas.create_text(400, 263, font=("Arial", 60, "bold"), text="")

# Buttons
# Right
check = PhotoImage(file="images/right.png")
knew_button = Button(image=check, highlightthickness=0, command=known)
knew_button.grid(column=1, row=1)

# Wrong
unknown = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=unknown, highlightthickness=0, command=next_word)
unknown_button.grid(column=0, row=1)

next_word()


window.mainloop()

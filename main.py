from tkinter import *
from tkinter import messagebox
import random


# Constants
BG_COLOR = "#0C0C0C"
FG_COLOR = "#F2613F"
time_running = False
score = 0
test = None


# Create random 200 words for the test
def create_test():
    with open("words.csv", "r") as file:
        words = file.readlines()[1:]
        random.shuffle(words)
        typing_test = [word.strip() for word in words][:200]
        return typing_test


# Load new test into text_zone and start timer
def start_timer():
    global time_running, test
    test = create_test()
    text_zone.configure(text=test)
    typing_zone.configure(state="normal")
    typing_zone.focus()
    time_running = True
    count_down(60)


# Count down mechanism
def count_down(sec):
    global time_running, test
    if sec > 0 and time_running:
        window.after(1000, count_down, sec-1)
        timer_canvas.itemconfig(timer, text=sec)
    elif sec == 0:
        get_results()
        messagebox.showinfo(title="Congratulations!",
                            message=f"Your result is {score} words per second.")
        time_running = False


# Calculate score after timer ends
def get_results():
    global score
    result = typing_zone.get("1.0", "end-1c").split()

    for word1, word2 in zip(result, test):
        if word1 == word2:
            score += 1


# Reset timer and score
def reset():
    global time_running, score
    window.after_cancel(count_down)
    timer_canvas.itemconfig(timer, text="60")
    time_running = False
    text_zone.configure(text="")
    score = 0
    typing_zone.delete("1.0", "end-1c")
    typing_zone.configure(state="disabled")


# UI
window = Tk()
window.title("Fingers On Fire")
window.config(background=BG_COLOR, padx=30, pady=30)

canvas = Canvas(width=256, height=256, background=BG_COLOR, highlightthickness=0)
logo = PhotoImage(file="logo.png")
canvas.create_image(128, 128, image=logo)
canvas.grid(column=0, row=0)

timer_canvas = Canvas(width=128, height=128, background=BG_COLOR, highlightthickness=0)
timer_canvas.create_oval(10, 10, 124, 124, outline=FG_COLOR, width=4)
timer = timer_canvas.create_text(64, 64, text="60", font=("Bebas Neue", 60, "bold"), fill=FG_COLOR)
timer_canvas.grid(column=0, row=2)

text_zone = Label(text="", font=("Roboto", 18),
                  width=70, height=20, wraplength=700,
                  background=BG_COLOR, highlightthickness=5)
text_zone.grid(column=1, row=0, columnspan=2, rowspan=2, padx=10, pady=10)

typing_zone = Text(width=70, height=10, font=("Roboto", 18),
                   background="white",  foreground=BG_COLOR,
                   highlightthickness=0, state="disabled")
typing_zone.grid(column=1, row=2, columnspan=2, padx=10, pady=10)

start_button = Button(text="START", font=("Bebas Neue", 30, "bold"),
                      highlightthickness=0, command=start_timer)
start_button.grid(column=1, row=3, padx=20, pady=20)

reset_button = Button(text="RESET", font=("Bebas Neue", 30, "bold"),
                      highlightthickness=0, command=reset)
reset_button.grid(column=2, row=3, padx=20, pady=20)

window.mainloop()

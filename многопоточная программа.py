import pyautogui
from multiprocessing import Process
from tkinter import *
from tkinter import messagebox


root = Tk()
root.title("Piano Tiles")
root.configure(bg="#adb5bd")
root.geometry("500x500")
root.resizable(0, 0)


processes = []
points_positions = []
status = "off"
stop = False


def clear_points_positions():
    global points_positions
    points_positions = []
    p1_text.delete(0, END)
    p2_text.delete(0, END)
    p3_text.delete(0, END)
    p4_text.delete(0, END)


def add_points_position():
    global points_positions
    if len(points_positions) < 4:
        command = f"p{len(points_positions)+1}_text.insert(0, pyautogui.position())"
        eval(command)
        points_positions.append(pyautogui.position())



def main_function(position, key):
    state = False
    while True:
        color = pyautogui.pixel(x=position[0], y=position[1])
        if color[0] != 0:
            if state:
                pyautogui.keyUp(key)
                state = False
            continue
        if not state:
            if color[1] <= 150:
                pyautogui.keyDown(key)
                state = True


def start_button_function():
    global status
    global processes
    if status == "off":
        global points_positions

        if len(points_positions) != 4:
            messagebox.showerror(title='Проблема с позициями', message='Какие-то проблемы с позициями. Надо бы исправить')      
        else:
            keys = ['a', 's', 'd', 'f']
            for i in range(4):
                processes.append(
                        Process(target=main_function, args=(points_positions[i], keys[i]))
                    )

            for process in processes:
                process.start()

            status = "on"
            status_label["text"] = "Включен"
            status_label["fg"] = "#66cd00"
            start_button["text"] = "Выключить"

    elif status == "on":
        for process in processes:
            process.terminate()

        status = "off"
        status_label["text"] = "Выключен"
        status_label["fg"] = "#c92a2a"
        start_button["text"] = "Включить"
        processes = []


def main():
    root.bind("<Control-q>", lambda event: add_points_position())

    root.mainloop()


start_button = Button(root, width=8, height=2, text="Включить", font="Arial 14 bold", command=start_button_function, relief=FLAT)

status_label = Label(root, text="Выключен", font="Arial 14 bold", bg="#adb5bd", fg="#c92a2a")

p1_text = Entry(root, width=10, font="Arial 15 bold", relief=RIDGE, justify="center")
p2_text = Entry(root, width=10, font="Arial 15 bold", relief=RIDGE, justify="center")
p3_text = Entry(root, width=10, font="Arial 15 bold", relief=RIDGE, justify="center")
p4_text = Entry(root, width=10, font="Arial 15 bold", relief=RIDGE, justify="center")

set_points_button = Button(root, width=13, height=1, text="Очистить список", font="Arial 10 bold", command=clear_points_positions, relief=FLAT)

start_button.place(x=200, y=200)
Label(root, text="Статус:", font="Arial 15 bold", bg="#adb5bd").place(x=150, y=449)
status_label.place(x=230, y=450)
p1_text.place(x=10, y=10)
p2_text.place(x=10, y=40)
p3_text.place(x=10, y=70)
p4_text.place(x=10, y=100)
set_points_button.place(x=10, y=130)

if __name__ == "__main__":
    main()

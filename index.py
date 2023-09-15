from tkinter.ttk import Label, Button, Combobox, Style
from ttkthemes import ThemedTk
from PIL import Image, ImageTk
from tkinter import messagebox
import keyboard
import pyautogui
from window import hidden_client
import json
import threading
import pynput
import time


HOTKEYS = ['Desligado', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12']

root = ThemedTk(theme="arc", themebg=True)
root.title("LmBot")
#root.geometry("200x200+100+100")
root.resizable(False, False)
style = Style()
style.configure('TButton', font=("Roboto", 12))
style.configure('Ativado.TButton', foreground="green")
style.configure('Desativado.TButton', foreground="red")

def generate_widget(widget, row , column, sticky="NSEW", columnspan=None,**kwargs):
    my_widget = widget(**kwargs)
    my_widget.grid(row=row, column=column, padx=2, pady=2, sticky=sticky, columnspan=columnspan)
    return my_widget

def load_trash():
    load_image = Image.open('lixo.png')
    resized_image = load_image.resize((16,16))
    return ImageTk.PhotoImage(resized_image)


rgb = ''
mana_position = ''

def get_mana_position():
    global rgb
    global mana_position
    messagebox.showinfo(title="Mana Position", message="Posicione o mouse em cima da barra de mana e pressione a tecla insert")
    keyboard.wait('insert')
    x, y = pyautogui.position()
    rgb = pyautogui.screenshot().getpixel((x,y))
    messagebox.showinfo(title="Mana Result", message=f"X: {x} Y:{y} - RGB: {rgb}")
    lbl_mana_position.configure(text=f"({x}, {y})")
    mana_position = [x, y]

def clear():
    lbl_mana_position.config(text="Empty")

def opacity():
    result = hidden_client()
    if result == 1:
        btn_opacity.configure(style='Ativado.TButton')
        return
    else:
        btn_opacity.configure(style='Desativado.TButton')
        print("Não aplicado")

def save():
    my_data = {
        "food": {
            "value": cbx_food.get(),
            "position": cbx_food.current()
        },
        "spell": {
            "value": cbx_cast.get(),
            "position": cbx_cast.current()
        },
        "mana_pos":{
            "position": mana_position,
            "rgb": rgb
        }

    }
    with open('infos.json', 'w') as file:
        file.write(json.dumps(my_data))  


def load():
    with open('infos.json', "r") as file:
        data = json.loads(file.read())
    cbx_food.current(data['food']['position'])
    cbx_cast.current(data['spell']['position'])
    lbl_mana_position.configure(text=data['mana_pos']['position'])
    return data

def run():
    wait_to_eat_food = 60
    time_food = time.time()
    while not myEvent.is_set():
        if data['mana_pos']['position'] is not None:
            x = data['mana_pos']['position'][0]
            y = data['mana_pos']['position'][1]
            if(pyautogui.pixelMatchesColor(x,y, tuple(data['mana_pos']['rgb']))):
                if(data['spell']['value'] != 'Desligado'):
                    pyautogui.press(data['spell']['value'])
            if(data['food']['value'] != 'Desligado'):
                if int(time.time() - time_food) >= wait_to_eat_food:
                    pyautogui.press(['food']['value'])
                    time_food = time.time()

def key_code(key):
    if (key == pynput.keyboard.Key.esc):
        myEvent.set()
        root.deiconify()
        return False
    
def listener_keyboard():
    with pynput.keyboard.Listener(on_press=key_code) as listener:
        listener.join()

def start():
    root.iconify()
    save()
    global data
    global myEvent
    global start_th
    data = load()
    myEvent = threading.Event()
    start_th = threading.Thread(target=run)
    start_th.start()
    keyboard_th = threading.Thread(target=listener_keyboard)
    keyboard_th.start()
    
    
#btn_alarms = generate_widget(Button, row=2, column=1 , text="Alarms")
#btn_tools = generate_widget(Button, row=2, column=2 , text="Tools")
#btn_healer = generate_widget(Button, row=2, column=3 , text="Healer")
#btn_cavebot = generate_widget(Button, row=2, column=4 , text="Cavebot")
#btn_targeting = generate_widget(Button, row=2, column=5 , text="Targeting")


lbl_food = generate_widget(Label, row=0, column=0, text='Hotkey Eat Food', sticky="W")
cbx_food = generate_widget(Combobox, row=0, column=1, values=HOTKEYS, state="readonly", width=12)
cbx_food.current(0)

lbl_cast = generate_widget(Label, row=1, column=0 , text='Hoytkey Cast', sticky="W")
cbx_cast = generate_widget(Combobox, row=1, column=1, values=HOTKEYS, state="readonly", width=12)
cbx_cast.current(0)


btn_mana_position = generate_widget(Button, row=2, column=0, text="Mana Position", command=get_mana_position)
lbl_mana_position = generate_widget(Label, row=2,column=1, text="Empty")

trash = load_trash()
btn_mana_position_trash = generate_widget(Button, row=2, column=2, image=trash, command=clear)


btn_opacity = generate_widget(Button, row=4, column=0, text='Aplicar opacidade', columnspan=3, command=opacity)

btn_load = generate_widget(Button, row=5, column=0, text='Load', command=load)

btn_start = generate_widget(Button, row=5, column=1, text='Start', command=start)

root.mainloop()
import customtkinter as ctk
import time
import can
import threading
from cxxheaderparser.simple import parse_file  # Import cxxheaderparser
import os
import re
import glob  # Import glob to handle multiple files

ctk.set_appearance_mode("dark")  # ou "dark"
ctk.set_default_color_theme("blue")  # Testa diferentes temas: "blue", "green", "dark-blue"

# Função para exibir cores sólidas (RGBW) por ciclos rápidos
def solid_color_test():
    solid_colors = ["red", "green", "blue", "white"]
    solid_test_app = ctk.CTk()
    solid_test_app.geometry("800x480")
    solid_test_app.title("Solid Colors Test")

    # Frame para mostrar cores sólidas
    solid_frame = ctk.CTkFrame(solid_test_app, width=800, height=480)
    solid_frame.pack()

    for _ in range(2):  # 2 ciclos rápidos
        for color in solid_colors:
            solid_frame.configure(fg_color=color)
            solid_test_app.update()
            time.sleep(0.3)  # Muda a cor a cada 0.5 segundos

    solid_test_app.destroy()  # Fecha a janela de teste de cor
#solid_color_test()



# Start Main Window and Window Attributes
app = ctk.CTk()
app.geometry("800x480")
app.title("Dashboard")
app.attributes("-fullscreen", True)  # Commented out for debugging
# R2D WARNING
R2D_label = ctk.CTkLabel(app, text="R2D PLACEHOLDER", font=("Noto Sans Bold", 30, "bold"), text_color="red")
R2D_label.place(relx=0.5, rely=0.04, anchor="center")

# Main Frame
frame = ctk.CTkFrame(app, width=600, height=400)
frame.place(relx=0.5, rely=0.5, anchor="center")

# Variables
rect_width = 160
rect_height = 80
speed = 36  # Initial speed value DEBUGGING

soc_lv_level= 0.6
soc_hv_level = 0.78

data_1 = float(16.3)
data_2 = float(27.8)
data_3 = float(30)
data_4 = 40
data_5 = 50
data_6 = 60

# Retângulo 1 - DATA XXXXXX
rect_1 = ctk.CTkFrame(frame, width=rect_width, height=rect_height, corner_radius=15) # Cria um retângulo
rect_1.place(x=10, y=10) # Posição do retângulo
title_1 = ctk.CTkLabel(rect_1, text="Temp 1 ", font=("Noto Sans Bold ", 18)) # Cria uma Label
title_1.place(relx=0.5, rely=0.25, anchor='center') # Posição da Label
data_label_1=ctk.CTkLabel(rect_1, text=data_1, font=("Noto Sans Bold ", 30, "bold"))
data_label_1.place(relx=0.5, rely=0.65, anchor='center')

# Retângulo 2 - DATA XXXXX
rect_2 = ctk.CTkFrame(frame, width=rect_width, height=rect_height, corner_radius=15)
rect_2.place(x=220, y=10)
title_2 = ctk.CTkLabel(rect_2, text="Temp COLD", font=("Noto Sans Bold ", 18)) # Cria uma Label
title_2.place(relx=0.5, rely=0.25, anchor='center')
data_label_2=ctk.CTkLabel(rect_2, text=data_2, font=('Noto Sans Bold ', 30, 'bold'))
data_label_2.place(relx=0.5, rely=0.65, anchor='center')

# Retângulo 3 - DATA XXXXXX
rect_3 = ctk.CTkFrame(frame, width=rect_width, height=rect_height, corner_radius=15)
rect_3.place(x=430, y=10)
title_3 = ctk.CTkLabel(rect_3, text="Temp 3", font=("Noto Sans Bold ", 18)) # Cria uma Label
title_3.place(relx=0.5, rely=0.25, anchor='center')
data_label_3=ctk.CTkLabel(rect_3, text=data_3, font=("Noto Sans Bold ", 30, "bold"))
data_label_3.place(relx=0.5, rely=0.65, anchor='center')

# Retângulo 4 - Kw Inst.
rect_4 = ctk.CTkFrame(frame, width=285, height=rect_height, corner_radius=5)
rect_4.place(x=10, rely=0.75)
title_4 = ctk.CTkLabel(rect_4, text="Kw Inst:", font=("Noto Sans Bold ", 24))
title_4.place(relx=0.3, rely=0.5, anchor='center')
data_label_4 =ctk.CTkLabel(rect_4, text=data_4, font=("Noto Sans Bold ", 45, "bold"))
data_label_4.place(relx=0.7, rely=0.5, anchor='center')

# Retângulo 5 - Kw Limit
rect_5 = ctk.CTkFrame(frame, width=285, height=rect_height, corner_radius=5)
rect_5.place(x=305, rely=0.75)
title_5 = ctk.CTkLabel(rect_5, text="Kw Limit:", font=("Noto Sans Bold ", 24))
title_5.place(relx=0.3, rely=0.5, anchor='center')
data_label_5 =ctk.CTkLabel(rect_5, text=data_5, font=("Noto Sans Bold ", 45, "bold"))
data_label_5.place(relx=0.7, rely=0.5, anchor='center')

#####Barras SoC#####

# Progress Bar SoC LV - Left
soc_HV_bar_label = ctk.CTkLabel(app, text="SoC\nLV", font=("Noto Sans Bold ", 20))
soc_HV_bar_label.place(x=33, y=20)
soc_HV_bar = ctk.CTkProgressBar(app, orientation="vertical", width=60, height=320, corner_radius=4)
soc_HV_bar.place(x=20, y=80)
soc_HV_bar.set(soc_lv_level)
soc_HV_per = ctk.CTkLabel(app, text = str(int(soc_lv_level * 100)) + '%', font=("Noto Sans Bold ", 32, "bold"))
soc_HV_per.place(x=50, y=430, anchor='center')

# Progress Bar SoC HV - Right
soc_LV_bar_label = ctk.CTkLabel(app, text="SoC\nHV", font=("Noto Sans Bold ", 20)) # Criar label de topo da barra
soc_LV_bar_label.place(x=733, y=20) # Posicionar a label do topo da barra
soc_LV_bar = ctk.CTkProgressBar(app, orientation="vertical", width=60, height=320, corner_radius=4) # Criar a barra
soc_LV_bar.place(x=720, y=80) # Posicionar a barra
soc_LV_bar.set(soc_hv_level) # Nível da Barra de Acordo com o Valor do SoC
soc_LV_per = ctk.CTkLabel(app, text = str(int(soc_hv_level * 100)) + '%', font=("Noto Sans Bold ", 32, "bold")) # Criar Label no Interior da Barra
soc_LV_per.place(x=750, y=430, anchor='center') # Posicionar a label no interior da barra

# Speed and Units
speed_label = ctk.CTkLabel(frame, text=str(speed), font=("Noto Sans Bold ", 130, "bold"))
speed_label.place(relx=0.5, rely=0.5, anchor='center')
speed_unit = ctk.CTkLabel(frame, text="Km/h", font=("Noto Sans Bold ", 30, "bold"))
speed_unit.place(relx=0.75, rely=0.60, anchor='center')

def check_speed(): # Update speed unit position on triple digits
    if speed > 100:
        speed_unit.place(relx=0.77, rely=0.6, anchor='center')
    else:
        speed_unit.place(relx=0.7, rely=0.6, anchor='center')
    frame.after(50, check_speed)  # Schedule the function to be called again after 50 ms

check_speed()

def update_data():
    global speed
    global data_1
    global data_2
    global data_3
    global data_4
    global data_5
    global data_6
    global soc_lv_level
    global soc_hv_level

    speed_label.configure(text=str(speed))
    data_label_1.configure(text=str(data_1))
    data_label_2.configure(text=str(data_2))
    data_label_3.configure(text=str(data_3))
    data_label_4.configure(text=str(data_4))
    data_label_5.configure(text=str(data_5))
    soc_HV_bar.set(soc_lv_level)
    soc_HV_per.configure(text=str(int(soc_lv_level * 100)) + '%')
    soc_LV_bar.set(soc_hv_level)
    soc_LV_per.configure(text=str(int(soc_hv_level * 100)) + '%')

    frame.after(5, update_data)  # Schedule the function to be called again after 1 s
update_data()

######################################################################################################## Debug Window
def open_debug_window():
    debug_window = ctk.CTkToplevel(app)
    debug_window.geometry("800x480")
    debug_window.title("DEBUG")
    close_button = ctk.CTkButton(debug_window, text="Close", command=debug_window.destroy) # Close Button
    close_button.place(y=450)

    # Create the header
    line = ctk.CTkFrame(debug_window, width=850, height=7, fg_color="black")
    line.place(x=-5, y=50)
    # Create the title label
    title_label = ctk.CTkLabel(debug_window, text="DEBUG", font=("Noto Sans Bold", 32, "bold"), bg_color="transparent")
    title_label.place(relx=0.5, y=23, anchor='center')

    # Display the current time on the far left of the header
    def update_time():
        current_time = time.strftime("%H:%M")
        time_label.configure(text=current_time)
        debug_window.after(1000, update_time)  # Update the time every second

    time_label = ctk.CTkLabel(debug_window, text="", font=("Noto Sans Bold", 27, "bold"))
    time_label.place(x=20, y=8)
    update_time()
    # Placeholder data for debugging
    categories = {
        "Cells": ["Cell Voltage", "Cell Temperature", "Cell Resistance"],
        "Drivetrain": ["Motor RPM", "Motor Temperature", "Torque"],
        "Test": ["Test Voltage", "Test Current", "Test Power"]
    }

    y_position = 80  # Initial y position for the first category

    for category, items in categories.items():
        # Create a frame for the category
        category_frame = ctk.CTkFrame(debug_window, width=350, height=len(items) * 30 + 50, corner_radius=10)
        category_frame.place(x=20 if category != "Test" else 420, y=y_position)

        # Create a label for the category
        category_label = ctk.CTkLabel(category_frame, text=category, font=("Noto Sans Bold", 20))
        category_label.place(relx=0.5, rely=0.1, anchor='center')

        # Create labels for each item in the category
        for i, item in enumerate(items):
            item_label = ctk.CTkLabel(category_frame, text=item, font=("Noto Sans", 16))
            item_label.place(x=10, y=40 + i * 30)

        y_position += len(items) * 30 + 70  # Update y position for the next category

def open_calibration_window():
    calibration_window = ctk.CTkToplevel(app)
    calibration_window.geometry("800x480")
    calibration_window.title("CALIBRATION")
    # Removed the line setting the entire window background to black

    # Create the header frame
    header_frame = ctk.CTkFrame(calibration_window, width=800, height=60, fg_color="black")
    header_frame.place(x=0, y=0)

    # Create the title label
    title_label = ctk.CTkLabel(calibration_window, text="CALIBRATION", font=("Noto Sans Bold", 32, "bold"), bg_color="black")
    title_label.place(relx=0.5, y=23, anchor='center')

    # Function to flash the title label
    def flash_title():
        current_color = title_label.cget("text_color")
        new_color = "yellow" if current_color == "red" else "red"
        title_label.configure(text_color=new_color)
        calibration_window.after(300, flash_title)  # Flash every 300 ms

    flash_title()

    # Display the current time on the far left of the header
    def update_time():
        current_time = time.strftime("%H:%M")
        time_label.configure(text=current_time)
        calibration_window.after(1000, update_time)  # Update the time every second

    time_label = ctk.CTkLabel(calibration_window, text="", font=("Noto Sans Bold", 27, "bold"), text_color="white", bg_color="black")
    time_label.place(x=20, y=8)
    update_time()

    # Placeholder data for calibration
    categories = {
        "Cells": ["Cell Voltage", "Cell Temperature", "Cell Resistance"],
        "Drivetrain": ["Motor RPM", "Motor Temperature", "Torque"],
        "Test": ["Test Voltage", "Test Current", "Test Power"]
    }

    y_position = 80  # Initial y position for the first category

    for category, items in categories.items():
        # Create a frame for the category
        category_frame = ctk.CTkFrame(calibration_window, width=350, height=len(items) * 30 + 50, corner_radius=10)
        category_frame.place(x=20 if category != "Test" else 420, y=y_position)

        # Create a label for the category
        category_label = ctk.CTkLabel(category_frame, text=category, font=("Noto Sans Bold", 20))
        category_label.place(relx=0.5, rely=0.1, anchor='center')

        # Create labels for each item in the category
        for i, item in enumerate(items):
            item_label = ctk.CTkLabel(category_frame, text=item, font=("Noto Sans", 16))
            item_label.place(x=10, y=40 + i * 30)

        y_position += len(items) * 30 + 70  # Update y position for the next category

##### PLACEHOLDER BUTTON TO OPEN DEBUG WINDOW #####
# Button to open the new window
open_window_button = ctk.CTkButton(app, text="DEBUG", command=open_debug_window)
open_window_button.place(relx=0.4, rely=0.95, anchor='center')
open_window_button = ctk.CTkButton(app, text="CALIBRATION", command=open_calibration_window)
open_window_button.place(relx=0.7, rely=0.95, anchor='center')
###################################################

bus = can.Bus(interface="socketcan", channel="can0", bitrate=1000000)

def poll_can():
    msg = bus.recv(timeout=0.0)
    # Flush stale messages
    while True:
        new_msg = bus.recv(timeout=0.0)
        if not new_msg:
            break
        msg = new_msg
    if msg:
        update_gui(msg)
    app.after(50, poll_can)

def parse_can_header(folder_path):  # Modify to accept a folder path
    macros_by_id = {}
    decode_macros = {}
    for header_path in glob.glob(os.path.join(folder_path, "*.h")):  # Iterate over all .h files
        current_can_id = None
        with open(header_path, 'r') as file:
            for line in file:
                # Match CAN ID definitions
                can_match = re.match(r'#define CAN_(\w+)\s+(\w+)', line)
                if can_match:
                    current_can_id = int(can_match.group(2), 16)
                    if current_can_id not in macros_by_id:
                        macros_by_id[current_can_id] = []
                    continue
                # Match MAP_DECODE macros and associate them with the current CAN ID
                decode_match = re.match(r'#define (MAP_DECODE_\w+)\s*\(x\)\s*(.+)', line)
                if decode_match and current_can_id is not None:
                    macro_name = decode_match.group(1)
                    decode_expr = decode_match.group(2).strip()
                    if decode_expr.startswith('(x)'):
                        decode_expr = decode_expr[3:].strip()
                    decode_expr = decode_expr.replace('(x)(', '(').replace('(x) ', ' ').replace('(x)', '')
                    while re.search(r'MAP_DECODE_\w+', decode_expr):
                        nested_macro = re.search(r'(MAP_DECODE_\w+)', decode_expr).group(1)
                        if nested_macro in decode_macros:
                            decode_expr = decode_expr.replace(nested_macro, f"({decode_macros[nested_macro]})")
                        else:
                            break
                    decode_macros[macro_name] = decode_expr
                    macros_by_id[current_can_id].append(macro_name)

    return macros_by_id, decode_macros

# Parse macros on startup
HEADER_FOLDER = "Can-Header-Map"  # Change from single file to folder
macros_by_id, decode_macros = parse_can_header(HEADER_FOLDER)

def decode_data(data_bytes, macro_expr):
    x = list(data_bytes)  # Define 'x' as a list of data bytes
    data_str = ''.join(f'{byte:02x}' for byte in data_bytes)  # Define 'data_str'
    macro_expr_python = re.sub(
        r'\bdata\[(\d+)\]',
        lambda m: f'int("0x{data_str[int(m.group(1))*2:int(m.group(1))*2+2]}", 16)',
        macro_expr
    )
    return eval(macro_expr_python, {}, {'x': x})  # Pass 'x' to eval

def update_gui(msg):
    global data_1, data_2, data_3, data_4, data_5, data_6
    if msg.arbitration_id in macros_by_id:
        #print(f"[DEBUG] Recognized ID={hex(msg.arbitration_id)}; Macros={macros_by_id[msg.arbitration_id]}")
        for macro_name in macros_by_id[msg.arbitration_id]:
            if macro_name not in decode_macros:
                #print(f"[DEBUG] Skipping non-decode macro='{macro_name}'")
                continue
            expr = decode_macros[macro_name]
            result = decode_data(msg.data, expr)
            #print(f"[DEBUG] Macro='{macro_name}' DecodedValue={result}")
            match macro_name:
                case "MAP_DECODE_MOTOR_TEMPERATURE":
                    data_1 = result
                    data_label_1.configure(text=str(result))
                case "MAP_DECODE_INVERTER_TEMPERATURE":
                    data_2 = result
                    data_label_2.configure(text=str(result))
                case "MAP_DECODE_CONSUMED_POWER":
                    data_3 = result
                    data_label_3.configure(text=str(result))
                    print(f"DecodedValue={result}")
                case "MAP_DECODE_TARGET_POWER":
                    data_4 = result
                    data_label_4.configure(text=str(result))
                case "MAP_DECODE_BRAKE_PRESSURE":
                    data_5 = result
                    data_label_5.configure(text=str(result))
                # case "MAP_DECODE_TOQUE_VECTORING":  # Example
                #     data_label_3.configure(text=str(result))
                case _:
                    pass

poll_can()
app.mainloop()

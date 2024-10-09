import customtkinter as ctk
import time
import threading

ctk.set_appearance_mode("light")  # ou "dark"
ctk.set_default_color_theme("blue")  # Testa diferentes temas: "blue", "green", "dark-blue"

# Função para exibir barras de cores como no padrão de calibração de telas
def color_bars_test():
    test_app = ctk.CTk()
    test_app.geometry("800x480")
    test_app.title("Color Bars Calibration Test")

    # Criar o frame principal que irá conter as barras de cores
    bar_frame = ctk.CTkFrame(test_app, width=800, height=480)
    bar_frame.pack()

    # Cores usadas nas barras
    colors = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#00FFFF", "#FF00FF", "#FFFFFF"]

    # Tamanho de cada barra (dividindo a largura total pela quantidade de barras)
    bar_width = int(800 / len(colors))

    # Criar as barras de cores no estilo de calibração
    for i, color in enumerate(colors):
        bar = ctk.CTkFrame(bar_frame, width=bar_width, height=480, fg_color=color)
        bar.place(x=i * bar_width, y=0)

    test_app.update()
    time.sleep(1)  # Mostrar as barras de calibração por 1s

    # Fechar a janela de teste de barras
    test_app.destroy()

    # Iniciar o teste de cores sólidas
    solid_color_test()

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

# Executar o teste de barras de cores antes do dashboard
#color_bars_test()

#################Separação dos Testes#########################

# Start Main Window
app = ctk.CTk()
app.geometry("800x480")
app.title("Dashboard")

# R2D WARNING
R2D_label = ctk.CTkLabel(app, text="R2D PLACEHOLDER", font=("Noto Sans Bold", 35, "bold"), text_color="red")
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

data_1 = 147
data_2 = 20
data_3 = 30
data_4 = 40
data_5 = 50
data_6 = 60

# Retângulo 1 - DATA XXXXXX
rect_1 = ctk.CTkFrame(frame, width=rect_width, height=rect_height, corner_radius=15) # Cria um retângulo
rect_1.place(x=10, y=10) # Posição do retângulo
title_1 = ctk.CTkLabel(rect_1, text="Temp 1 ", font=("Noto Sans Bold ", 18)) # Cria uma Label
title_1.place(relx=0.5, rely=0.3, anchor='center') # Posição da Label
data_label_1=ctk.CTkLabel(rect_1, text=data_1, font=("Noto Sans Bold ", 24, "bold"))
data_label_1.place(relx=0.5, rely=0.65, anchor='center')

# Retângulo 2 - DATA XXXXXX
rect_2 = ctk.CTkFrame(frame, width=rect_width, height=rect_height, corner_radius=15)
rect_2.place(x=220, y=10)
title_2 = ctk.CTkLabel(rect_2, text="Temp COLD", font=("Noto Sans Bold ", 18)) # Cria uma Label
title_2.place(relx=0.5, rely=0.3, anchor='center')
data_label_2=ctk.CTkLabel(rect_2, text=data_2, font=('Noto Sans Bold ', 24, 'bold'))
data_label_2.place(relx=0.5, rely=0.65, anchor='center')

# Retângulo 3 - Temp Bateria
rect_3 = ctk.CTkFrame(frame, width=rect_width, height=rect_height, corner_radius=15)
rect_3.place(x=430, y=10)
title_3 = ctk.CTkLabel(rect_3, text="Temp 3", font=("Noto Sans Bold ", 18)) # Cria uma Label
title_3.place(relx=0.5, rely=0.3, anchor='center')
data_label_3=ctk.CTkLabel(rect_3, text=data_3, font=("Noto Sans Bold ", 24, "bold"))
data_label_3.place(relx=0.5, rely=0.65, anchor='center')

# Retângulo 4 - Kw Instantenous
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
soc_HV_per = ctk.CTkLabel(app, text = str(int(soc_lv_level * 100)) + '%', font=("Noto Sans Bold ", 27, "bold"))
soc_HV_per.place(x=50, y=430, anchor='center')

# Progress Bar SoC HV - Right
soc_LV_bar_label = ctk.CTkLabel(app, text="SoC\nHV", font=("Noto Sans Bold ", 20)) # Criar label de topo da barra
soc_LV_bar_label.place(x=733, y=20) # Posicionar a label do topo da barra
soc_LV_bar = ctk.CTkProgressBar(app, orientation="vertical", width=60, height=320, corner_radius=4) # Criar a barra
soc_LV_bar.place(x=720, y=80) # Posicionar a barra
soc_LV_bar.set(soc_hv_level) # Nível da Barra de Acordo com o Valor do SoC
soc_LV_per = ctk.CTkLabel(app, text = str(int(soc_hv_level * 100)) + '%', font=("Noto Sans Bold ", 27, "bold")) # Criar Label no Interior da Barra
soc_LV_per.place(x=750, y=430, anchor='center') # Posicionar a label no interior da barra

#Speed and Units
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
    speed += 1  # Increment speed for demonstration purposes

    data_label_1.configure(text=str(data_1))
    data_label_2.configure(text=str(data_2))
    data_label_3.configure(text=str(data_3))
    data_label_4.configure(text=str(data_4))
    data_label_5.configure(text=str(data_5))

    soc_HV_bar.set(soc_lv_level)
    soc_HV_per.configure(text=str(int(soc_lv_level * 100)) + '%')
    soc_LV_bar.set(soc_hv_level)
    soc_LV_per.configure(text=str(int(soc_hv_level * 100)) + '%')

    data_1 += 1

    frame.after(1000, update_data)  # Schedule the function to be called again after 1 s
update_data()

#RUN APP
app.mainloop()

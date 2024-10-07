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

# Title
title_label = ctk.CTkLabel(app, text="Dashboard", font=("TkDefaultFont", 20))
title_label.pack(pady=10)

# Main Frame
frame = ctk.CTkFrame(app, width=600, height=400)
frame.place(x=100, y=50)

# Variables
rect_width = 160
rect_height = 80
soc_level = 0.60
speed = 88  # Initial speed value


# Retângulo 1 - Temp ENGINE
rect_1 = ctk.CTkFrame(frame, width=rect_width, height=rect_height, corner_radius=15) # Cria um retângulo
rect_1.place(x=10, y=10) # Posição do retângulo
data_1 = ctk.CTkLabel(rect_1, text="Temp 1: \n65°C", font=("Arial", 18)) # Cria uma Label
data_1 = ctk.CTkLabel(rect_1, text="Temp 1: \n65°C", font=("Arial", 18)) # Cria uma Label
data_1.place(relx=0.5, rely=0.5, anchor='center') # Posição da Label

# Retângulo 2 - Temp COLD
rect_2 = ctk.CTkFrame(frame, width=rect_width, height=rect_height, corner_radius=15)
rect_2.place(x=220, y=10)
data_2 = ctk.CTkLabel(rect_2, text="Temp COLD: \n40°C", font=("Arial", 18)) # Cria uma Label
data_2.place(relx=0.5, rely=0.5, anchor='center')

# Retângulo 3 - Temp Bateria
rect_3 = ctk.CTkFrame(frame, width=rect_width, height=rect_height, corner_radius=15)
rect_3.place(x=430, y=10)
data_3 = ctk.CTkLabel(rect_3, text="Temp 3:\n 32.6°C", font=("Arial", 18)) # Cria uma Label
data_3.place(relx=0.5, rely=0.5, anchor='center')

# Retângulo 4 - Kw Instantenous
rect_4 = ctk.CTkFrame(frame, width=285, height=rect_height, corner_radius=5)
rect_4.place(x=10, rely=0.75)
title_4 = ctk.CTkLabel(rect_4, text="Kw Inst.", font=("Arial", 20))
title_4.place(relx=0.5, rely=0.35, anchor='center')
data_label_4 =ctk.CTkLabel(rect_4, text="70 kW", font=("Arial", 24, "bold"))
data_label_4.place(relx=0.5, rely=0.65, anchor='center')

# Retângulo 5 - Kw Limit
rect_5 = ctk.CTkFrame(frame, width=285, height=rect_height, corner_radius=5)
rect_5.place(x=305, rely=0.75)
title_5 = ctk.CTkLabel(rect_5, text="Kw Limit:", font=("Arial", 20))
title_5.place(relx=0.5, rely=0.35, anchor='center')
data_label_5 =ctk.CTkLabel(rect_5, text="50 kW", font=("Arial", 24, "bold"))
data_label_5.place(relx=0.5, rely=0.65, anchor='center')

#####Barras SoC#####

# Barra lateral esquerda (SOC)
soc_HV_bar_label = ctk.CTkLabel(app, text="SOC", font=("Arial", 18))
soc_HV_bar_label.place(x=30, y=50)
soc_HV_bar = ctk.CTkProgressBar(app, orientation="vertical", width=60, height=320, corner_radius=4)
soc_HV_bar.place(x=20, y=80)
soc_HV_bar.set(soc_level)
soc_HV_int_text = ctk.CTkLabel(soc_HV_bar, text=(soc_level*100), font=("Arial", 20, "bold"))
soc_HV_int_text.place(relx=0.5, rely=0.5, anchor='center')

# Barra lateral direita (SOC-LV)
soc_lv_bar_label = ctk.CTkLabel(app, text="SOC-LV", font=("Arial", 18)) # Criar label de topo da barra
soc_lv_bar_label.place(x=720, y=50) # Posicionar a label do topo da barra
soc_lv_bar = ctk.CTkProgressBar(app, orientation="vertical", width=60, height=320, corner_radius=4) # Criar a barra
soc_lv_bar.place(x=720, y=80) # Posicionar a barra
soc_lv_bar.set(soc_level) # Nível da Barra de Acordo com o Valor do SoC
soc_right_text = ctk.CTkLabel(soc_lv_bar, text=(soc_level*100), font=("Arial", 20, "bold")) # Criar Label no Interior da Barra
soc_right_text.place(relx=0.5, rely=0.5, anchor='center') # Posicionar a label no interior da barra

#########
#####Speed#####

# Display speed in the center of the main rectangle
speed_label = ctk.CTkLabel(frame, text=str(speed), font=("Arial", 150, "bold"))



######Incrementar Velocidade Para Testes#####
def update_speed():
    global speed
    speed_label.configure(text=str(speed))
    speed += 1  # Increment speed for demonstration purposes
    frame.after(1000, update_speed)  # Schedule the function to be called again after 100 ms

update_speed()
##############################################

speed_label.place(relx=0.5, rely=0.5, anchor='center')
unit_label = ctk.CTkLabel(frame, text="Km/h", font=("Arial", 30, "bold"))
unit_label.place(relx=0.7, rely=0.60, anchor='center')
############
def check_speed():
    if speed > 100:
        unit_label.place(relx=0.8, rely=0.63, anchor='center')
    else:
        unit_label.place(relx=0.7, rely=0.63, anchor='center')
    frame.after(50, check_speed)  # Schedule the function to be called again after 100 ms

check_speed()
#RUN
app.mainloop()

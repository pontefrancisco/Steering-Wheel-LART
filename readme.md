# Steering-Wheel-LART

## Login Armbian
```
User: root
Password: root
```
## Iniciar sistema

Caso o sistema se encontre bem configurado, para arrancar com a interface gráfica do volante, apenas será necessário correr o comando:
```bash
startx
```
---


## Configuração Inicial do Sistema

### Configuração Física

Interface de CAN física a funcionar num Raspberry Pi/BananaPI

Fazer as conexões físicas:

O pinout para ligar MCP2515 a um Raspberry Pi Zero:

![Raspberry Pi Image](https://forums.raspberrypi.com/download/file.php?id=13939&sid=9352ccfb77f2a6f527bc6fe32d9c964e)

### Configurações no sistema

1. Atualizar o sistema:
   ```bash
   sudo apt update -y && sudo apt upgrade -y
   ```

2. Instalar dependências necessárias para o ambiente Python:
   ```bash
   sudo apt install xserver-xorg xinit openbox python3 python3-pip python3-tk customtkinter
   ```

3. Desativar serviços não essenciais (Reativar caso seja necessário fazer debug a problemas de sistema):
   ```bash
   sudo systemctl disable armbian-zram-config.service  # Desativa a configuração de zram do Armbian
   sudo systemctl disable systemd-random-seed.service  # Desativa a semente aleatória do systemd
   sudo systemctl disable rsyslog.service  # Desativa o logging do sistema
   sudo systemctl disable e2scrub_reap.service  # Desativa a limpeza do e2scrub
   sudo systemctl mask armbian-zram-config.service  # Mascara a configuração de zram do Armbian
   sudo systemctl mask systemd-random-seed.service  # Mascara a semente aleatória do systemd
   sudo systemctl mask armbian-ramlog.service  # Mascara o logging em RAM do Armbian
   sudo systemctl disable systemd-timesyncd.service
   ```

4. Desligar Servidor DNS e Configurar Estáticos (Resolução de Nomes):

   ```bash
   sudo systemctl disable systemd-resolved.service  # Desativa a resolução de nomes do systemd
   sudo nano /etc/resolv.conf
   ```
   - Adicionar ao ficheiro as seguintes linhas:
     ```ini
     nameserver 8.8.8.8
     nameserver 1.1.1.1
     ```

5. Atrasar arranque do serviço `systemd-logind`:
   ```bash
   sudo systemctl edit systemd-logind.service
   ```
   - Adicionar o seguinte texto no espaço aberto entre comentários:
     ```ini
     [Service]
     ExecStartPre=/bin/sleep 1
     ```

6. Configurar o arranque automático do user root:
   ```bash
   sudo mkdir -p /etc/systemd/system/getty@tty1.service.d/
   sudo nano /etc/systemd/system/getty@tty1.service.d/override.conf
   ```
   - Adicionar ao ficheiro as seguintes linhas:
     ```ini
     [Service]
     ExecStart=
     ExecStart=-/sbin/agetty --autologin root --noclear %I $TERM
     ```
   - Executar os seguintes comandos:
     ```bash
     sudo systemctl daemon-reexec
     sudo systemctl restart getty@tty1.service
     sudo reboot
     ```
   - Verificar que está tudo ok após o reboot.

7. Instalar o pacote `can-utils`:
   ```bash
   sudo apt install can-utils
   ```

8. Configurar a interface CAN:
   ```bash
   sudo ip link set can0 up type can bitrate 1000000
   ```

9. Verificar se a interface se encontra a funcionar. Deve ter o nome algo similar a `can0` ou `slcan0`:
   ```bash
   ip a

   # Testar a interface:
    
   # Enviar uma mensagem de teste:
   cansend can0 MENSAGEM

   # Fazer dump da interface:
   candump can0
   ```

10. Clonar o repositório da interface:
   ```bash
   sudo git clone https://github.com/pontefrancisco/Steering-Wheel-LART /root/Steering-Wheel-LART
   ```

11. Navegar até ao repositório:
   ```bash
   cd ~/Steering-Wheel-LART
   ```

12. Criar um ambiente virtual Python:
   ```bash
   python3 -m venv venv
   ```

13. Ativar o ambiente virtual:
   ```bash
   source venv/bin/activate
   ```

14. Instalar as dependências do projeto:
   ```bash
   pip3 install -r requirements.txt
   ```

15. Configurar a abertura da interface gráfica ao arrancar o X11:
   ```bash
   sudo nano ~/.xinitrc
   ```
   - Adicionar ao ficheiro as seguintes linhas:
     ```bash
      #!/bin/bash -i
      openbox &
      cd /root/Steering-Wheel-LART/
      . /root/Steering-Wheel-LART/venv/bin/activate
      export DISPLAY=:0
      echo $DISPLAY
      python3 /root/Steering-Wheel-LART/interface.py
     ```
16. Configurar o arranque automático da interface após o auto login:
    ```bash
    sudo nano ~/.bashrc
    ```
      Inserir no **FINAL** ficheiro:

    ```bash
    # Iniciar automaticamente a interface gráfica ao fazer login
    if [ -z "$DISPLAY" ] && [ "$(tty)" == "/dev/tty1" ]; then
        startx
    fi
    ```

17.  Reiniciar o sistema:
   ```bash
   sudo reboot
   ```

---

## Setup Após a Primeira Vez

Caso o sistema já tenha sido configurado previamente e seja necessário fazer alterações, basta seguir os passos abaixo para iniciar o ambiente:

1. Ativar o ambiente virtual Python:
   ```bash
   source ~/Steering-Wheel-LART/venv/bin/activate
   ```

2. Navegar para o diretório do projeto:
   ```bash
   cd ~/Steering-Wheel-LART
   ```

3. Iniciar a interface gráfica:
   ```bash
   startx
   ```

## Alguns comandos necessários (Debug)
1. Terminar a interface gráfica (Que abriu automaticamente com o arranque):
   ```bash
   ps aux | grep Xorg
   sudo kill -9 PROCESSO
   ```
2. Arrancar novamente o X com a interface:
   ```bash
   startx
   ```
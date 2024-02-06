####################

#   00  On
#   01  Off

#   04  Config SSID
#   05  Config Passwd

####################

import socket, subprocess, json, time, os

host = "192.168.1.8"
port = 4444

def get_status():
    result = subprocess.run("termux-battery-status", shell=True, capture_output=True, text=True)
    status = json.loads(result.stdout)
    print("=== === === ===")
    print('Health: '+status["health"])
    print('Battery:'+str(status["percentage"])+'%')
    print('Plug: '+status["plugged"])
#    print('Temprature: '+status["temperature"])
#    print('Current: '+status["current"])
    print("=== === === ===")

def send_udp_data(data, host, port):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.sendto(data, (host, port))
    udp_socket.close()

while True:
    os.system('clear')
    get_status()
    match input(' >'):
        case 'on':
            send_udp_data(b'\x00', host, port)
            #t_on()
            #   0x00    TurnOn
        case 'off':
            send_udp_data(b'\x01', host, port)
            #t_off()
            #   0x01    TurnOff
        case 'q':
            exit()

        case _:
            print('unknown')

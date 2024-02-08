####################

#   00  On
#   01  Off

####################

from operator import truediv
import socket, subprocess, json, time, os, threading

host = "192.168.1.8"
port = 4444

statList = ["Manual", "Auto", "Keep"]
statInd = 0
status = {
    "percentage": -1,
    "health": "N/A",
    "plugged": "N/A"
}
charge_on = False

Max_bat = 80
Min_bat = 20

def get_battery():
    global status
    result = subprocess.run("termux-battery-status", shell=True, capture_output=True, text=True)
    status = json.loads(result.stdout)

def fake_percentage():
    bool down = false
    while True:
        if status['percentage'] >= 90:
            down = true
        if status['percentage'] <= 10:
            down = false

        if down:
            status['percentage'] -= 10
        else:
            status['percentage'] += 10
        time.sleep(0.5)

def draw():
    print("=== === === === === === === ===")
    print(
        f"\n"
        f"IP: {host}\n"
        f"Battery: {str(status['percentage'])+'%'} Mode: {statList[statInd]}\n"
        f"Health: {status['health']}\n"
        f"Plug: {status['plugged']}\n"
        f"Charging: {charge_on}\n"
        f"Range: {Min_bat}% - {Max_bat}%\n"
    )
    print("=== === === === === === === ===")
    

def send_udp_data(data, host, port):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.sendto(data, (host, port))
    udp_socket.close()

def clamp_charge():
    while True:
        if charge_on:
            if status["percentage"] >= Max_bat:
                charge_on = False
                send_udp_data(b'\x01', host, port)
        else:
            if status["percentage"] <= Min_bat:
                charge_on = True
                send_udp_data(b'\x00', host, port)
        time.sleep(5)

#get_battery()
send_udp_data(b'\x00', host, port)
threading.Thread(target=clamp_charge).start()
threading.Thread(target=fake_percentage).start()

while True:
    #get_battery()
    os.system('clear')
    draw()
    inp = input(' >')
    match inp:
        case 'on':
            Max_bat = 80
            Min_bat = 20
            send_udp_data(b'\x00', host, port)
            statInd = 0     # To Manual
            charge_on = True
            #   0x00    TurnOn
        case 'off':
            Max_bat = 80
            Min_bat = 20
            send_udp_data(b'\x01', host, port)
            statInd = 0     # To Manual
            charge_on = False
            #   0x01    TurnOff
        case 'auto':
            Max_bat = 80
            Min_bat = 20
            statInd = 1     # To Auto
        case 'keep':
            Max_bat = 90
            Min_bat = 85
            statInd = 2     # To Keep
        case 'q' | 'exit':
            exit()

        case _:
            print('unknown')

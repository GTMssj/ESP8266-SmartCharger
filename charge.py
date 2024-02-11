import socket, subprocess, json, time, os, sys, threading


class ChargStatus:

    status = {}
    Max_bat = 80
    Min_bat = 20

    host = "192.168.1.8"
    port = 4444

    def __init__(self):
        self.getStat()

    def getStat(self):
        result = json.loads(subprocess.run("termux-battery-status", shell=True, capture_output=True, text=True).stdout)
        self.status = result

    def send_cmd(self, data):
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.sendto(data, (self.host, self.port))
        udp_socket.close()
        
    def draw(self):
        os.system("clear")
        print("=== === === === === === === ===")
        print(
            f"\n"
            f"IP: {self.host} on Port: {self.port}\n"
            f"Battery: {self.status['percentage']}%\n"
            f"Status: {self.status['status']}\n"
            f"Range: {self.Min_bat}% - {self.Max_bat}%\n"
            f"\n"
            f"  (Ctrl-C to close)\n"
        )
        print("=== === === === === === === ===")
    
    def set_limit(self, range):
        self.Min_bat, self.Max_bat = range.split("-")
        if self.Max_bat <= self.Min_bat:
            tmp = self.Max_bat
            self.Max_bat = self.Min_bat
            self.Min_bat = tmp
    
    def set_host(self, host: str):
        self.host, self.port = host.split(":")
        


#   =================== #

charge = ChargStatus()
def loop():
    while True:
        if charge.status['percentage'] < charge.Min_bat and charge.status['status'] == 'DISCHARGING':
            charge.send_cmd(b"\x01")
        if charge.status['percentage'] > charge.Max_bat and charge.status['status'] == 'CHARGING':
            charge.send_cmd(b"\x00")
        charge.draw()
        time.sleep(10)

args = sys.argv[1:]
i = 0
while i < len(args):
    cmd = args[i]
    if cmd[0] == '-':
        match cmd:
            case '-h' | '-help':
                print(f"\nUsage: {sys.argv[0]} [-h] [-mode auto|hold] [-host IP:Port]\n [-manual low-high]")
                exit()
            case '-mode':
                match args[i+1]:
                    case 'auto':
                        charge.set_limit("20-80")
                    case 'hold':
                        charge.set_limit("90-95")
            case '-host':
                charge.set_host(args[i+1])
            case '-manual':
                charge.set_limit(args[i+1])
    i += 1
    
loopThread = threading.Thread(target=loop)
loopThread.setDaemon
loopThread.start()
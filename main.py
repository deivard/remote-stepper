from machine import Pin, reset, WDT
import usocket as socket
import uselect as select
import time
from socketutils import *
from steppermotor import StepperMotor
import network
import time
from config import SSID, KEY, PINS


def connect_to_wifi(ssid, key):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        start_time = time.time()
        wlan.connect(ssid, key)
        while not wlan.isconnected():
            if time.time() - start_time > 10:
                print(f"Could not connect to network {ssid}, timed out.")
                return
        print('network config:', wlan.ifconfig())
        sync_clock()
        print(f"Updated RTC via NTP: Current time is {time.localtime(time.time() + 3600)}")
    
def sync_clock():
    import ntptime
    ntptime.settime()

def is_connected():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    return wlan.isconnected()


def setup_server_socket(ip, port):
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((ip, port))
        server_socket.listen(5)
    except:
        print("Socket is already bound, resetting...")
        reset()
    return server_socket
    

def main():
    stepper = StepperMotor(PINS, 24)
    
    server_socket = setup_server_socket("0.0.0.0", 80)
    sockets_list = [server_socket]
    
    poll = select.poll()
    poll.register(server_socket, select.POLLIN)
    # wdt = WDT(timeout=100*1000)
    while True:
        # wdt.feed()
        poll_results = poll.poll()
        for poll_result in poll_results:
            polled_socket, event = poll_result
            if event & select.POLLHUP:
                print(polled_socket, event)
            elif event & select.POLLERR == select.POLLERR:
                print("Socket error")
            elif event & select.POLLIN == select.POLLIN:
                if polled_socket == server_socket:
                    cl, addr = server_socket.accept()
                    print('client connected from', addr)
                    sockets_list.append(cl)
                    poll.register(cl)
                else:
                    data = receive_data(polled_socket)
                    print(f"Received data: {data}")
                    if data == b'':
                        print(f"Closed socket: {polled_socket}")
                        polled_socket.close()
                        sockets_list.remove(polled_socket)
                        poll.unregister(polled_socket)
                    decoded = data.decode("utf8")
                    try:
                        stepper.step(int(decoded))
                    except:
                        print(f"Could not get number of steps, invalid format for data: {decoded}")

if __name__ == "__main__":
    connect_to_wifi(SSID, KEY)
    main()

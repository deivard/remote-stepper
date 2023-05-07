import socket
import time
from socketutils import *
import keyboard
from functools import partial

IP = "192.168.50.140"
PORT = 80

def keyboard_event_callback(sock, step):
    send_data(sock, str(step))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.connect((IP, PORT))

keyboard.add_hotkey("left", callback=partial(keyboard_event_callback, s, "-3"))
keyboard.add_hotkey("right", callback=partial(keyboard_event_callback, s, "3"))
keyboard.add_hotkey("shift+left", callback=partial(keyboard_event_callback, s, "-1"))
keyboard.add_hotkey("shift+right", callback=partial(keyboard_event_callback, s, "1"))
keyboard.wait()

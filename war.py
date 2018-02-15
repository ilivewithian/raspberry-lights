import sys
from sys import stdin
import logging
logging.basicConfig()
from thread import start_new_thread
status = "pending"

import websocket

try:
	import thread
except ImportError:
	import _thread as thread
import time

def on_message(ws, message):
	global status
	if message.startswith('42["status"'):
		status = message.split('"')[3]

def on_error(ws, error):
	print(error)

def on_close(ws):
	print("## closed ##")

def on_open(ws):
	print("open")

def war_loop():
	while True:
		print status
		time.sleep(1.5)

start_new_thread(war_loop, ())

if __name__ == "__main__":
	ws = websocket.WebSocketApp("ws://e1349c1d.ngrok.io/socket.io/?transport=websocket",
		on_message = on_message,
		on_error = on_error,
		on_close = on_close)
	ws.on_open = on_open
	ws.run_forever()
	stdin.readline()
	ws.close()

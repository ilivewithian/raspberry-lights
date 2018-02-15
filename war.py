import sys
from sys import stdin
import logging
logging.basicConfig()
from thread import start_new_thread
status = "pending"

RED_PIN = 17
GREEN_PIN = 22
BLUE_PIN = 24

import websocket
import os
import sys
import termios
import tty
import pigpio
import time

try:
	import thread
except ImportError:
	import _thread as thread
import time

brightChanged = False
pi = pigpio.pi()

currentR = 0
currentG = 0
currentB = 0

def setLights(r,g,b,brightness):
	global currentR
	global currentG
	global currentB

	if r > 255:
		r = 255
	if r < 0:
		r = 0
	if g > 255:
		g = 255
	if g < 0:
		g = 0
	if b > 255:
		b = 255
	if b < 0:
		b = 0

	if r != currentR:
		pi.set_PWM_dutycycle(RED_PIN, r)
		currentR = r
	if g != currentG:
		pi.set_PWM_dutycycle(GREEN_PIN, g)
		currentG = g
	if b != currentB:
		pi.set_PWM_dutycycle(BLUE_PIN, b)
		currentB = b


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

		if status == "none":
			setLights(0, 0, 0, 255)
			time.sleep(0.5)
		elif status == "voting":
			setLights(255, 0, 0, 255)
			time.sleep(0.5)
		elif status == "war impending":
			setLights(0, 255, 255, 255)
			time.sleep(0.5)
		elif status == "war active":
			setLights(0, 0, 255, 255)
			time.sleep(0.5)
		elif status == "war stopping":
			setLights(255, 255, 0, 255)
			time.sleep(0.5)
		else:
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

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(26, GPIO.OUT, initial=GPIO.LOW)

while True:
  GPIO.output(26, GPIO.HIGH)
  time.sleep(1)
  GPIO.output(26, GPIO.LOW)
  time.sleep(1)
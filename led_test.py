import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(26, GPIO.OUT, initial=GPIO.LOW)

try:
  while True:
    GPIO.output(26, GPIO.HIGH)
    time.sleep(10)
    GPIO.output(26, GPIO.LOW)
    time.sleep(10)
except KeyboardInterrupt:
  GPIO.clenup()
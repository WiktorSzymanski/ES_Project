import RPi.GPIO as GPIO

GPIO.sermode(GPIO.BOARD)
GPIO.setup(26, GPIO.OUT, initial=GPIO.LOW)

while True:
  GPIO.output(26, GPIO.HIGH)
  sleep(1)
  GPIO.output(26, GPIO.LOW)
  sleep(1)
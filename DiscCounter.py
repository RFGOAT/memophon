import RPi.GPIO as GPIO

BUTTON_GPIO = 16
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)


while True:
    GPIO.wait_for_edge(BUTTON_GPIO, GPIO.FALLING)
    print("Button pressed!")

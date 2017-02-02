'''IMPORTEREN VAN ALLE LIBRARY'S'''

import RPi.GPIO as GPIO

import time

import random

#---------------------------------------------------------



'''PINMODES AANGEVEN'''

GPIO.setmode(GPIO.BCM)

GPIO.setwarnings(False)

#---------------------------------------------------------



'''OP WELKE PINS ZITTEN DE MOTOREN'''

pinLinksVooruit = 10

pinLinksAchteruit = 9

pinRechtsVooruit = 8

pinRechtsAchteruit = 7

#---------------------------------------------------------



'''OP WELKE PINS ZITTEN DE 'OGEN' '''

pinStuurSignaal = 17

pinOntvangSignaal = 18

#---------------------------------------------------------



'''OP WELKE PINS ZITTEN DE LICHTSENSOREN'''

pinLichtSensor = 25

#---------------------------------------------------------



'''OP WELKE PINS ZITTEN DE LEDJES'''

pinLED1 = 22

pinLED2 = 23

#----------------------------------------------------------



'''FREQUENTIE VAN DE WIELEN, HOEVAAK AAN/UIT PER SECONDE'''

frequentie = 16

#---------------------------------------------------------



'''PROCENTEN DAT DE WIELEN AAN MOETEN STAAN'''

rondjesLinks = 30

rondjesRechts = 30

#---------------------------------------------------------



'''VARIABELE VOOR HET STOPPEN VAN DE AUTO'''

stop = 0

#---------------------------------------------------------



'''ZIJN DE PINNEN IN/OUT-PUT'''

GPIO.setup(pinLinksVooruit, GPIO.OUT)

GPIO.setup(pinLinksAchteruit, GPIO.OUT)

GPIO.setup(pinRechtsVooruit, GPIO.OUT)

GPIO.setup(pinRechtsAchteruit, GPIO.OUT)



GPIO.setup(pinStuurSignaal, GPIO.OUT)

GPIO.setup(pinOntvangSignaal, GPIO.IN)



GPIO.setup(pinLichtSensor, GPIO.IN)



GPIO.setup(pinLED1, GPIO.OUT)

GPIO.setup(pinLED2, GPIO.OUT)

#---------------------------------------------------------



'''VARIABELEN VOOR AFSTANDSMETING'''

hoeDichtBij = 15.0

draaiTijd = 0.75

#---------------------------------------------------------



'''ZET PWM OP 'FREQUENTIE' '''

pwmMotorLinksVooruit = GPIO.PWM(pinLinksVooruit, frequentie)

pwmMotorLinksAchteruit = GPIO.PWM(pinLinksAchteruit, frequentie)

pwmMotorRechtsVooruit = GPIO.PWM(pinRechtsVooruit, frequentie)

pwmMotorRechtsAchteruit = GPIO.PWM(pinRechtsAchteruit, frequentie)

#---------------------------------------------------------



'''ZET ALLES UIT'''

pwmMotorLinksVooruit.start(stop)

pwmMotorLinksAchteruit.start(stop)

pwmMotorRechtsVooruit.start(stop)

pwmMotorRechtsAchteruit.start(stop)

#---------------------------------------------------------



'''FUNCTIE VOOR ALLE MOTORS UIT'''

def motorsUit():

    pwmMotorLinksVooruit.ChangeDutyCycle(stop)

    pwmMotorLinksAchteruit.ChangeDutyCycle(stop)

    pwmMotorRechtsVooruit.ChangeDutyCycle(stop)

    pwmMotorRechtsAchteruit.ChangeDutyCycle(stop)

#---------------------------------------------------------



'''FUNCTIE VOOR VOORUIT'''

def rijVooruit():

    pwmMotorLinksVooruit.ChangeDutyCycle(rondjesLinks)

    pwmMotorLinksAchteruit.ChangeDutyCycle(stop)

    pwmMotorRechtsVooruit.ChangeDutyCycle(rondjesRechts)

    pwmMotorRechtsAchteruit.ChangeDutyCycle(stop)

#---------------------------------------------------------



'''FUNCTIE VOOR ACHTERUIT'''

def rijAchteruit():

    pwmMotorLinksVooruit.ChangeDutyCycle(stop)

    pwmMotorLinksAchteruit.ChangeDutyCycle(rondjesLinks)

    pwmMotorRechtsVooruit.ChangeDutyCycle(stop)

    pwmMotorRechtsAchteruit.ChangeDutyCycle(rondjesRechts)



'''FUNCTIE VOOR LINKS'''

def Links():

    pwmMotorLinksVooruit.ChangeDutyCycle(stop)

    pwmMotorLinksAchteruit.ChangeDutyCycle(rondjesLinks)

    pwmMotorRechtsVooruit.ChangeDutyCycle(rondjesRechts)

    pwmMotorRechtsAchteruit.ChangeDutyCycle(stop)

#---------------------------------------------------------



'''FUNCTIE VOOR RECHTS'''

def Rechts():

    pwmMotorLinksVooruit.ChangeDutyCycle(rondjesLinks)

    pwmMotorLinksAchteruit.ChangeDutyCycle(stop)

    pwmMotorRechtsVooruit.ChangeDutyCycle(stop)

    pwmMotorRechtsAchteruit.ChangeDutyCycle(rondjesRechts)

#---------------------------------------------------------



'''FUNCITE VOOR AFSTAND METEN'''

def meetAfstand():

    GPIO.output(pinStuurSignaal, True)

    time.sleep(0.00001)

    GPIO.output(pinStuurSignaal, False)

    StartTime = time.time()

    StopTime = StartTime

    while GPIO.input(pinOntvangSignaal) == 0:

        StartTime = time.time()

        StopTime = StartTime

    while GPIO.input(pinOntvangSignaal) == 1:

        StopTime = time.time()

        if StopTime-StartTime >= 0.04:

            StopTime = StartTime

            print 'YOU ARE TOO FAR AWAY :('

    return ((StopTime-StartTime)*34326)/2
	
#---------------------------------------------------------


'''DETECTEREN VAN OBSTAKEL'''

def isObstakel(lokaleHoeDichtBij):

    return meetAfstand() < lokaleHoeDichtBij

#---------------------------------------------------------

try: 
	while isObstakel(lokaleHoeDichtBij) < 11: 
		print "kleiner dan 11 naar voren"
		rijVooruit()

	while isObstakel(lokaleHoeDichtBij) <= 4:
		print "kleiner dan 4. motor uit."
		motorsUit()
		
	while isObstakel(lokaleHoeDichtBij) >= 11:
		print "groter dan 11. Nu snel naar links."
		Links()
		time.sleep(0.2)
		
except KeyboardInterrupt:
	GPIO.cleanup()

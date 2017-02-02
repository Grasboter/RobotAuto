import RPi.GPIO as GPIO # Import de GPIO Library
import time     # Import de Time library

# Zet de GPIO modes
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Zet de variabellen voor de GPIO motor pinnen
pinLinksVooruit = 10
pinLinksAchteruit = 9
pinRechtsVooruit = 8
pinRechtsAchteruit = 7

# Defineer de GPIO pinnen voor de sonar
pinTrigger = 17
pinEcho = 18

# Defineer de GPIO pinnen voor de LEDs
pinLedA = 24
pinLedB = 23

# Hoeveel keer per seconden de pinnen aan en uit doen
Frequency = 35
# Hoelang de pin aan blijft staan per cycle, als precentage
CycleAperc = 30
CycleBperc = 30
# Als de cycle op 0 staat, stoppen de motoren met draaien
Stop = 0

# Pin mode naar Output
GPIO.setup(pinLinksVooruit, GPIO.OUT)
GPIO.setup(pinLinksAchteruit, GPIO.OUT)
GPIO.setup(pinRechtsVooruit, GPIO.OUT)
GPIO.setup(pinRechtsAchteruit, GPIO.OUT)

# pinnen als output en input
GPIO.setup(pinTrigger, GPIO.OUT)
GPIO.setup(pinEcho, GPIO.IN)      

# LEDs pinnen
GPIO.setup(pinLedA, GPIO.OUT) 
GPIO.setup(pinLedB, GPIO.OUT)  

# Set Frequency
pwmLinksVooruit = GPIO.PWM(pinLinksVooruit, Frequency)
pwmLinksAchteruit = GPIO.PWM(pinLinksAchteruit, Frequency)
pwmRechtsVooruit = GPIO.PWM(pinRechtsVooruit, Frequency)
pwmRechtsAchteruit = GPIO.PWM(pinRechtsAchteruit, Frequency)

# Start PWM met een cycle 0
pwmLinksVooruit.start(Stop)
pwmLinksAchteruit.start(Stop)
pwmRechtsVooruit.start(Stop)
pwmRechtsAchteruit.start(Stop)

# naar voren
def Forwards(AdditionalSpeed):
    pwmLinksVooruit.ChangeDutyCycle(CycleAperc + AdditionalSpeed)
    pwmLinksAchteruit.ChangeDutyCycle(Stop)
    pwmRechtsVooruit.ChangeDutyCycle(CycleBperc + AdditionalSpeed)
    pwmRechtsAchteruit.ChangeDutyCycle(Stop)

# naar achter
def Backwards(AdditionalSpeed):
    pwmLinksVooruit.ChangeDutyCycle(Stop)
    pwmLinksAchteruit.ChangeDutyCycle(CycleAperc + AdditionalSpeed)
    pwmRechtsVooruit.ChangeDutyCycle(Stop)
    pwmRechtsAchteruit.ChangeDutyCycle(CycleBperc + AdditionalSpeed)

# naar links
def Left(AdditionalSpeed):
    pwmLinksVooruit.ChangeDutyCycle(Stop)
    pwmLinksAchteruit.ChangeDutyCycle(CycleAperc + AdditionalSpeed)
    pwmRechtsVooruit.ChangeDutyCycle(CycleBperc + AdditionalSpeed)
    pwmRechtsAchteruit.ChangeDutyCycle(Stop)

# naar rechts
def Right(AdditionalSpeed):
    pwmLinksVooruit.ChangeDutyCycle(CycleAperc + AdditionalSpeed)
    pwmLinksAchteruit.ChangeDutyCycle(Stop)
    pwmRechtsVooruit.ChangeDutyCycle(Stop)
    pwmRechtsAchteruit.ChangeDutyCycle(CycleBperc + AdditionalSpeed)

# motoren uit
def StopMotors():
    pwmLinksVooruit.ChangeDutyCycle(Stop)
    pwmLinksAchteruit.ChangeDutyCycle(Stop)
    pwmRechtsVooruit.ChangeDutyCycle(Stop)
    pwmRechtsAchteruit.ChangeDutyCycle(Stop)

# meet de afstand
def Measure():
    GPIO.output(pinTrigger, True)
    time.sleep(0.00001)
    GPIO.output(pinTrigger, False)
    StartTime = time.time()
    StopTime = StartTime

    while GPIO.input(pinEcho)==0:
        StartTime = time.time()
        StopTime = StartTime

    while GPIO.input(pinEcho)==1:
        StopTime = time.time()
      
        
        if StopTime-StartTime >= 0.04:
            print("Hold on there!  You're too close for me to see.")
            StopTime = StartTime
            break

    ElapsedTime = StopTime - StartTime
    Distance = (ElapsedTime * 34300)/2

    return Distance

# de code
try:
     # Zet de trigger op False
    GPIO.output(pinTrigger, False)

    # ff stil
    time.sleep(0.1)

    #herhallen voor forever!!
    while True:
        print("Seeking the car")
        GPIO.output(pinLedA, True)
        GPIO.output(pinLedB, False)

        SeekSize = 0.15 # Draai 0.25s
        SeekCount = 1 # aantal keer zoeken
        MaxSeekCount = 8 # max antal keer zoeken

        # hoe lang zijn we aan het zoeken?
        while SeekCount <= MaxSeekCount:
            DistanceToObject = Measure()
            print(DistanceToObject)
            # auto binnen bereik?
            if DistanceToObject <= 65:
                print('Within 50cm')
                GPIO.output(pinLedB, True)
                GPIO.output(pinLedA, False)
                # langzamer gaan rijden als dichtbij
                if DistanceToObject <= 25:
                    Forwards(-10)
                    time.sleep(1)
                    StopMotors()
                    continue
                # harder gaan rijden als verweg
                if DistanceToObject >= 35:
                    Forwards(10)
                    time.sleep(1)
                    StopMotors()
                    continue
                # standaard snelheid
                Forwards(0)
                time.sleep(1)
                StopMotors()
                continue

            Left(0)
            time.sleep(SeekSize)
            StopMotors()
            # Zoek teller met 1
            SeekCount += 1

# cleanup en stop
except KeyboardInterrupt:
    GPIO.cleanup()

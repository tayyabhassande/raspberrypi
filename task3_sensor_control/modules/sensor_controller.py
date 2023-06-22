import time
import numpy
import statistics
USE_FAKE_GPIO = False # Chage to FALSE if testing in the Raspberry Pi

if USE_FAKE_GPIO:
    from .fake_gpio import GPIO  # For running app
else:
    import RPi.GPIO as GPIO  # For testing in Raspberry Pi



# import ...

class SensorController:

    def __init__(self):
        self.PIN_TRIGGER = 18  # do not change
        self.PIN_ECHO = 24  # do not change
        self.distance = None
        self.color_from_distance = [False, False, False]
        print('Sensor controller initiated')

    def track_rod(self):
        # ...
        measurements=[]
        for x in range(10):
            start_time = time.time()
            end_time = time.time()

            GPIO.setmode(GPIO.BCM)

            GPIO.setup(self.PIN_TRIGGER, GPIO.OUT)
            GPIO.setup(self.PIN_ECHO, GPIO.IN)

            GPIO.output(self.PIN_TRIGGER, GPIO.LOW)

            time.sleep(0.1)
            GPIO.output(self.PIN_TRIGGER, GPIO.HIGH)

            time.sleep(0.01)
            GPIO.output(self.PIN_TRIGGER, GPIO.LOW)

            while GPIO.input(self.PIN_ECHO) == 0:
                start_time = time.time()
            while GPIO.input(self.PIN_ECHO) == 1:
                end_time = time.time()

            pulse_duration = end_time - start_time
            self.distance = round(pulse_duration * 17.150, 2)
            measurements.append(self.distance)

        #self.distance = None
        #measurements.sort()
        print(measurements)
        #self.distance = statistics.median(measurements)
            #print('end time',end_time)
            #print('start time',start_time)
            #pulse_duration = end_time - start_time
            #print('pulse',pulse_duration)
            #self.distance = round(pulse_duration* 17150,2)
            #measurements.append(self.distance)
            #print(measurements)
        measurements.sort()
        #print(measurements)
        self.distance = statistics.median(measurements)
        #print(self.distance)
        #self.distance = 0

        if self.distance >15 and self.distance<=21:
            self.color_from_distance = [True, False, False]
        if self.distance >9 and self.distance<=15:
            self.color_from_distance = [False, True, False]
        if self.distance >4 and self.distance<=9:
            self.color_from_distance = [False, False, True]
            
        print('Monitoring')
        print(self.color_from_distance)

            
       
    def get_distance(self):
        self.track_rod()
        return self.distance

    def get_shape_from_distance(self):
        return self.color_from_distance
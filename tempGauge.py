import time
import board
import adafruit_ahtx0#adafruit_dht 
from gpiozero import AngularServo, Buzzer 

servo = AngularServo(12, min_angle=-90, max_angle=90,
                     min_pulse_width=0.0005, max_pulse_width=0.0025)

i2c = board.I2C()
dht_device = adafruit_ahtx0.AHTx0(i2c)#adafruit_dht.DHT11(board.D4)
#bz = Buzzer(21)

while True:
    try:
        temp_c = dht_device.temperature
        temp_f = temp_c * (9 / 5) + 32
        humidity = dht_device.relative_humidity#humidity
        
        for x in range(9):
            temp_f += dht_device.temperature * (9 / 5) + 32
            humidity += dht_device.relative_humidity#humidity
            time.sleep(1.0)
        
        temp_f = temp_f / 10
        print(f'Temp: {temp_f:.2f} Humidity: {humidity:.2f}')
        
        if temp_f > 75:
            temp_f = 75
        if temp_f < 70:
            temp_f = 70
        angle = (((temp_f - 70) * 180) / 5 - 90) * -1
        if angle > 90:
            angle = 90
        if angle < -90:
            angle = -90
        print(f'Angle: {angle:.2f}')
        servo.angle = angle
	#bz.on()
	#sleep(0.5)
	#bz.off()
    except RuntimeError as error:
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        dht_device.exit()
        raise error
    time.sleep(2.0)


# Webots_LineFollower

To repozytorium zawiera projekt inteligentego robota typu **Line-follower** posiadającego system  regulacji  prędkości jazdy.
Robot  ma adaptować  się  do  pokonywanej  trasy  zmieniając  swoją  prędkość, w zależności od jej kształtu, za pomocą czujników IR oraz analizy pobieranego obrazu z kamery. Całosć wykonana jest w symulatorze **Webots**,  wykorzystując kontroler sterujący robotem napisany w języku **Python.**

## Zaimportowanie bibliotek oraz kontrolerów
Na samym początku kodu znajdują się wszystkie zaimportowane w kontrolerze biblioteki oraz wykorzystywane urzadzenia programu Webots. 

	from controller import Robot
	from controller import Camera
	from controller import DistanceSensor, Motor
	import time
	import cv2
	import numpy as np
	import sys
	from controller import Display

## funkcja CountSpeed
Funkcja CountSpeed  jest funkcją ustalającą prędkość, z jaką porusza się robot. Przyjmuje dwie watości `CountL` i ` CountR` adące liczbą czarnych pikseli po prawej i lewej stronie wyświetlacza. W zależnosci od ich liczby, funkcja zwraca wartość będącą maksymalną prędkoscią robota.

	def CountSpeed(CountL, CountR):
	    #licz różnice pikseli
	    if( CountL + CountR < 2000):
	        speed = 3
	    elif( CountL + CountR < 10100):
	        speed = 7
	    else:
	        speed = 20
	    return speed
    


## Funkcja run_robot
Funkcja run_robot jest główną funkcjązawierającą sterowanie robotem. Na jej początku definkiujemy wartości zmiennych `time_step`, `max_speed` oraz `step `

	def run_robot(robot):
	    time_step = 32
	    max_speed = 0
	    step = -1
	    
## Aktywowanie kamery
	    
	    #camera
	    camera = Camera('camera')
	    camera.enable(time_step)
	    
## Aktywowanie silników dla prawego i lewego koła

	    #motors
	    left_motor = robot.getDevice('left wheel motor')
	    right_motor = robot.getDevice('right wheel motor')
	    left_motor.setPosition(float('inf'))
	    right_motor.setPosition(float('inf'))
	    left_motor.setVelocity(0.0)
	    right_motor.setVelocity(0.0)
	    
## Aktywowanie czujników IR
	    #irsensors
	    left_ir = robot.getDevice('IRL')
	    left_ir.enable(time_step)
	    
	    right_ir = robot.getDevice('IRR')
	    right_ir.enable(time_step)

	        
## Pobieranie danych z symulacji 

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
W tym miejscu, program dla każdego wykonanego kroku pobiera wartość z obu czujników IR, oraz zapisuje obraz z kamery jako  **cam.png** 

	    # Step simulation
	    while robot.step(time_step) != -1:
	    
	        left_ir_value = left_ir.getValue()
	        right_ir_value = right_ir.getValue()
	        
	        camera.saveImage("cam.png", 20)
	        
## Analiza i obróbka obrazu przy pomocy biblioteki OpenCV

Zapisany wcześniej obraz, wczytujemy do zmiennej **icv** przy pomocy funkcji `icv = cv2.imread("cam.png")` a następnie przycinamy, ograniczając jedynie do interesującego nas obszaru. Stworzone zostały dwie kopie, jedna imCropp i druga  bw-która ma zostać wykorzystana do stworzenia czarno białej wersji.


	    #opencv
	         # Read image
	        icv = cv2.imread("cam.png")
	        
	    
	    # Display cropped image

	        imCrop = icv[ 400:640, 150:450]
	        bw = icv[ 400:640, 150:450]
	        
Przez środek obrazu **bw** rysujemy pionową, zieloną linie, która ma za zadaniejedynie umożliwić użytkownikowi podgląd na żywo.

	        width, height = 300, 140
	        x1, y1 = 150, 0
	        x2, y2 = 150, 240
	        line_thickness = 2
	        cv2.line(bw, (x1, y1), (x2, y2), (0, 255, 0), thickness=line_thickness)
	        
Nadpisujemy cam.png jego wersją skadrowaną

	        cv2.imwrite( 'cam.png', imCrop) 
	    
W tym momencie, obraz **bw.png** jest przedtawiany w binarnych wartościach,  gdzie cały jasny obszar zastępowany jest białymi pikselami, a ciemny jako czarne.

	        # plot the binary image
	        (thresh, blackAndWhiteImage) = cv2.threshold(bw, 127, 255, cv2.THRESH_BINARY)
	        cv2.imwrite( 'bw.png', blackAndWhiteImage) 
	        
Następnie program liczy liczbę czarnych pikseli na całym obrazie i wypisuje ją na ekranie, po czym tworzy dwa dodatkowe pliki .png będące prawą i lewą częścią wyświetlanego obrazu, i wykonuje dla nich tą samą czynność liczenia pikseli.	        
	        
	        bwcount = cv2.imread("bw.png", 0)
	        zeros = 72000 - cv2.countNonZero(bwcount)
	        print ("liczba czarnych pikseli: ", zeros)

	        # Cut the image in half
	        
	        left1 = bwcount[:, 0:150]
	        right1 = bwcount[:, 150:300]
	        
	        One_left = 36000 - cv2.countNonZero(left1)
	        One_right = 36000 - cv2.countNonZero(right1)
	        print ("liczba czarnych pikseli po lewej: ", One_left, " po prawej: ", One_right)

W dalszej części kodu, aktywowany zostaje wyświetlacz, pokazujący podgląd obrazu **bw.png**

	        #display
	        display = Display('display')
	        display = robot.getDevice('display')
	        img = display.imageLoad('bw.png')
	        coords = [0, 0, 0, 0]
	        frame_xy = [[x1, y1] for x1 in coords
	                                  for y1 in coords]
	        frames = len(frame_xy)
	        frame = step % frames
	        pos = frame_xy[frame]
	    
	        display.imagePaste(img, pos[0], pos[1], False)
		
## Poruszanie się robota i śledzenie ścieżki

Dalsza część kodu odpowiada za poruszanie się robota po trasie. Wartość `max_speed` będąca prędkością robota zostaje w tym miejscu określona przez wcześniej opisaną fukcję  `CountSpeed(One_left, One_right) `. i zostaje ona przypisana do prędkosci osiąganej przez prawe i lewe koło. 

		left_speed = max_speed * 0.25
	    right_speed = max_speed * 0.25
	        

W konsoli wypisana zostaje wartość pobrana wcześniej przez czujniki IR, i w zalezności od ich warosci robot skręca. Jesli ` (left_ir_value > right_ir_value)` oraz  ` (6 < left_ir_value < 14) `, robot musi skręcić w prawo, w tym celu prędkość na prawym kole zostaje zamieniona na wartość przeciwną. Analogicznie w przypadku prawej strony.

	        max_speed = CountSpeed(One_left, One_right)
    
	        print("left: {}  right: {} ".format( left_ir_value, right_ir_value))
	        
	        left_speed = max_speed * 0.25
	        right_speed = max_speed * 0.25
	        
	        if (left_ir_value > right_ir_value) and (6 < left_ir_value < 14):
	            print("Go left")
	            left_speed = -max_speed * 0.25
	        elif (right_ir_value > left_ir_value) and (4 < right_ir_value < 14):
	            print("Go right")
	            right_speed = -max_speed * 0.25
	        
Prędkosć prawego i lewego silnika zostaje określona jako wartosci zmienych odpowiednio   `left_speed ` i  `right_speed `

	        left_motor.setVelocity(left_speed)
	        right_motor.setVelocity(right_speed)
	    

Na końcu znajduje się funkcja główna main,   zawirająca stworzenie nowego obiektu robota i wywołanie dla niego funkcji głównej `run_robot()`
  
if __name__ == "__main__":
    
    my_robot = Robot()
    run_robot(my_robot)

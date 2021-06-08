# from controller import Camera
from controller import Robot
from controller import Camera
from controller import  DistanceSensor, Motor


def run_robot(robot):


    time_step = 32
    max_speed = 3
    
    camera = Camera('camera')
    camera.enable(time_step)
    
    #motors
    left_motor = robot.getDevice('left wheel motor')
    right_motor = robot.getDevice('right wheel motor')
    left_motor.setPosition(float('inf'))
    right_motor.setPosition(float('inf'))
    left_motor.setVelocity(0.0)
    right_motor.setVelocity(0.0)
    
    #irsensors
    left_ir = robot.getDevice('IRL')
    left_ir.enable(time_step)
    
    right_ir = robot.getDevice('IRR')
    right_ir.enable(time_step)
       
       
    # Step simulation
    while robot.step(time_step) != -1:
    
        left_ir_value = left_ir.getValue()
        right_ir_value = right_ir.getValue()
        
        print("kontrolny: left: {}  right: {} ".format( left_ir_value, right_ir_value))
        
        left_speed = max_speed * 0.25
        right_speed = max_speed * 0.25
        
        if (left_ir_value > right_ir_value) and (6 < left_ir_value < 14):
            print("kontrolny: Go left")
            left_speed = -max_speed * 0.25
        elif (right_ir_value > left_ir_value) and (4 < right_ir_value < 14):
            print("kontrolny: Go right")
            right_speed = -max_speed * 0.25
        
        left_motor.setVelocity(left_speed)
        right_motor.setVelocity(right_speed)
    
    
if __name__ == "__main__":
    my_robot = Robot()
    run_robot(my_robot)
    



    
    
    



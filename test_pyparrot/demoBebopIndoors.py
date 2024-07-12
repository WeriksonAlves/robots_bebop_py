"""
Demo the Bebop indoors (sets small speeds and then flies just a small amount)
Note, the bebop will hurt your furniture if it hits it.  Even though this is a very small
amount of flying, be sure you are doing this in an open area and are prepared to catch!

Author: Amy McGovern
"""

from pyparrot.Bebop import Bebop

bebop = Bebop(drone_type="Bebop2")

print("connecting")
success = bebop.connect(100)
print(success)

if (success):
    print("turning on the video")
    bebop.start_video_stream()

    print("sleeping")
    bebop.smart_sleep(2)

    bebop.ask_for_state_update()

    bebop.takeoff()

    # set safe indoor parameters
    bebop.set_max_tilt(5)
    bebop.set_max_vertical_speed(1)

    # trying out the new hull protector parameters - set to 1 for a hull protection and 0 without protection
    bebop.set_hull_protection(1)

    print("Flying direct: Slow move for indoors")
    #bebop.fly_direct(roll=0, pitch=40, yaw=0, vertical_movement=0, duration=2)
    
    # bebop.ask_for_state_update()
    # print("Start:\n", bebop.sensors.sensors_dict)
    
    #............................................................
    # bebop.move_relative(2,-1,0,0)
    
    # bebop.smart_sleep(5)
    # bebop.land()
    # bebop.smart_sleep(1)
    # bebop.ask_for_state_update()
    # bebop.takeoff()
    
    # bebop.move_relative(-2,1,0,0)
    
    # bebop.smart_sleep(5)
    # bebop.land()
    # bebop.smart_sleep(2)

    # bebop.ask_for_state_update()

    # bebop.takeoff()

    # bebop.move_relative(-3,-1,0,0)
    #............................................................
    
    # bebop.ask_for_state_update()
    # print("Middle:\n", bebop.sensors.sensors_dict)
    
    # bebop.move_relative(0,lado,0,0)
    # bebop.move_relative(-lado,0,0,0)
    # bebop.move_relative(0,-lado,0,0)
    
    bebop.smart_sleep(5)
    
    print("End:\n", bebop.sensors.sensors_dict)
    
    bebop.land()

    print("DONE - disconnecting")
    bebop.stop_video_stream()
    bebop.smart_sleep(5)
    print(bebop.sensors.battery)
    bebop.disconnect()
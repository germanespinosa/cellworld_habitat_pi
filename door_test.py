import doors
from time import sleep

door_inst = doors.Doors()
door_inst.test_door(1, 3)
sleep(1)
door_inst.test_door(2, 3)
sleep(1)

door_inst.close_door(2)
door_inst.close_door(1)
door_inst.close_door(3)
door_inst.close_door(0)
print(door_inst.status())
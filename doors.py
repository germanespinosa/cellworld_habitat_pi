from time import sleep
from os import path
from gpiozero import Button
from pi_messages import *
import RPi.GPIO as GPIO

class Doors:
    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        self.neutral_values = []
        self.open_sensor_pin = []
        self.close_sensor_pin = []
        self.open_pwm_pin = []
        self.close_pwm_pin = []

        self.sensor_open = []
        self.sensor_close = []
        self.motor_open = []
        self.motor_close = []

        self.door_open = []
        self.detected = []

        self.load_calibration()

        for dn in range(4):
            self.door_open.append(False)
            if not self.detected[dn]:
                self.sensor_open.append('')
                self.sensor_close.append('')
                self.motor_open.append('')
                self.motor_close.append('')
            else:
                GPIO.setup(self.open_pwm_pin[dn], GPIO.OUT)
                GPIO.setup(self.close_pwm_pin[dn], GPIO.OUT)
                self.motor_open.append(GPIO.PWM(self.open_pwm_pin[dn], 1000))  # create PWM instance with frequency
                self.motor_close.append(GPIO.PWM(self.close_pwm_pin[dn], 1000))  # create PWM instance with frequency
                self.sensor_open.append(Button(self.open_sensor_pin[dn], None, False))
                self.sensor_close.append(Button(self.close_sensor_pin[dn], None, False))

                self.motor_open[dn].start(0)  # start PWM of required Duty Cycle
                self.motor_close[dn].start(0)

    def open_door(self,door):
        if self.detected[door]:
            self.motor_open[door].ChangeDutyCycle(75)
            self.sensor_open[door].wait_for_press(3)
            if self.sensor_open[door].is_pressed:
                self.brake(door)
                self.door_open[door] = True
            else:
                self.brake(door)
            sleep(0.5)
            self.loose_stop(door)

    def close_door(self, door):
        if self.detected[door]:
            self.motor_close[door].ChangeDutyCycle(75)
            self.sensor_close[door].wait_for_press(3)
            if self.sensor_close[door].is_pressed:
                self.brake(door)
                self.door_open[door] = False
            else:
                self.brake(door)
            sleep(0.5)
            self.loose_stop(door)

    def test_door(self, door, repetitions):
        if self.detected[door]:
            for i in range(repetitions):
                self.open_door(door)
                sleep(0.2)
                self.close_door(door)
                sleep(0.2)

    def brake(self, door):
        if self.detected[door]:
            self.motor_open[door].ChangeDutyCycle(100)
            self.motor_close[door].ChangeDutyCycle(100)

    def loose_stop(self, door):
        if self.detected[door]:
            self.motor_open[door].ChangeDutyCycle(self.neutral_values[door])
            self.motor_close[door].ChangeDutyCycle(self.neutral_values[door])

    def save_calibration(self):
        for dn in range(len(self.door_open)):
            if self.detected[dn]:
                f = open("door%d.cal" % dn, "w")
                f.write(str(self.neutral_values[dn]))
                f.write("\n")
                f.write(str(self.open_sensor_pin[dn]))
                f.write("\n")
                f.write(str(self.close_sensor_pin[dn]))
                f.write("\n")
                f.write(str(self.open_pwm_pin[dn]))
                f.write("\n")
                f.write(str(self.close_pwm_pin[dn]))
                f.write("\n")
                f.close()

    def status(self):
        status = DoorInfoList()
        for dn in range(4):
            if self.detected[dn]:
                # if self.sensor_close[dn].is_pressed:
                #     door_state = 'closed'
                # elif self.sensor_open[dn].is_pressed:
                #     door_state = 'closed'
                # else:
                #     door_state = 'unknown'
                door_status = DoorInfo(num=dn, state='opened' if self.door_open[dn] else 'closed')
                status.append(door_status)
        return status

    def load_calibration(self):
        for dn in range(4):
            cal_file_name = "./door%d.cal" % dn
            if path.exists(cal_file_name):
                lines = open(cal_file_name, "r").readlines()
                self.neutral_values.append(float(lines[0].replace("\n", "")))
                self.open_sensor_pin.append(int(lines[1].replace("\n", "")))
                self.close_sensor_pin.append(int(lines[2].replace("\n", "")))
                self.open_pwm_pin.append(int(lines[3].replace("\n", "")))
                self.close_pwm_pin.append(int(lines[4].replace("\n", "")))
                self.detected.append(True)
            else:
                self.neutral_values.append(0)
                self.open_sensor_pin.append('')
                self.close_sensor_pin.append('')
                self.open_pwm_pin.append('')
                self.close_pwm_pin.append('')
                self.detected.append(False)

    # def calibrate(self, door_number, direction, opening_time, closing_time):
    #     increment = -.005
    #     close_b = self.neutral_values[door]
    #     open_b = self.neutral_values[door]
    #     if door < 4 and self.detected[door]:
    #         # Lower limit
    #         print("calibrating lower limit")
    #         # print("opening door")
    #         self.kit.continuous_servo[door].throttle = -0.5 * self.directions[door] + self.neutral_values[door]
    #         self.sensor_open[door].wait_for_press(3)
    #         if not self.sensor_open[door].is_pressed:
    #             self.kit.continuous_servo[door].throttle = self.neutral_values[door]
    #             print("door not opening")
    #             return
    #         else:
    #             # print('starting calibration')
    #             self.kit.continuous_servo[door].throttle = self.neutral_values[door]
    #             sleep(5)
    #             if self.sensor_open[door].is_pressed:
    #                 stationary = True
    #                 while stationary:
    #                     close_b = close_b - increment * self.directions[door]
    #                     print(stationary)
    #                     print(close_b)
    #                     self.kit.continuous_servo[door].throttle = close_b
    #                     sleep(2)
    #                     if self.sensor_open[door].is_pressed:
    #                         # print('sensor_pressed')
    #                         continue
    #                     else:
    #                         # print('sensor not pressed, opening door')
    #                         self.kit.continuous_servo[door].throttle = -0.5 * self.directions[door] + \
    #                                                                    self.neutral_values[door]
    #                         self.sensor_open[door].wait_for_press()
    #                         self.kit.continuous_servo[door].throttle = self.neutral_values[door]
    #                         sleep(.1)
    #                         stationary = False
    #             else:
    #                 increment = -.01
    #                 stationary = False
    #                 while not stationary:
    #                     print(stationary)
    #                     print(close_b)
    #                     close_b = close_b + increment * self.directions[door]
    #                     # print('opening door')
    #                     self.kit.continuous_servo[door].throttle = -0.5 * self.directions[door] + self.neutral_values[
    #                         door]
    #                     self.sensor_open[door].wait_for_press()
    #                     self.kit.continuous_servo[door].throttle = close_b
    #                     sleep(1)
    #                     if self.sensor_open[door].is_pressed:
    #                         # print('sensor pressed')
    #                         stationary = True
    #                     else:
    #                         # print('sensor not pressed')
    #                         continue
    #
    #         sleep(3)
    #         print("Calibrating upper limit")
    #         # print("closing door")
    #         self.kit.continuous_servo[door].throttle = 0.5 * self.directions[door] + self.neutral_values[door]
    #         self.sensor_close[door].wait_for_press(3)
    #         if not self.sensor_close[door].is_pressed:
    #             self.kit.continuous_servo[door].throttle = self.neutral_values[door]
    #             print("door not closing")
    #             return
    #         else:
    #             # print('starting calibration')
    #             self.kit.continuous_servo[door].throttle = self.neutral_values[door]
    #             sleep(5)
    #             if self.sensor_close[door].is_pressed:
    #                 stationary = True
    #                 while stationary:
    #                     open_b = open_b + increment * self.directions[door]
    #                     print(stationary)
    #                     print(open_b)
    #                     self.kit.continuous_servo[door].throttle = open_b
    #                     sleep(2)
    #                     if self.sensor_close[door].is_pressed:
    #                         # print('sensor_pressed')
    #                         continue
    #                     else:
    #                         # print('sensor not pressed, closing door')
    #                         self.kit.continuous_servo[door].throttle = 0.5 * self.directions[door] + \
    #                                                                    self.neutral_values[door]
    #                         self.sensor_close[door].wait_for_press()
    #                         self.kit.continuous_servo[door].throttle = self.neutral_values[door]
    #                         sleep(.1)
    #                         stationary = False
    #             else:
    #                 increment = -.01
    #                 stationary = False
    #                 while not stationary:
    #                     print(stationary)
    #                     print(open_b)
    #                     open_b = open_b - increment * self.directions[door]
    #                     # print('closing door')
    #                     self.kit.continuous_servo[door].throttle = 0.5 * self.directions[door] + self.neutral_values[
    #                         door]
    #                     self.sensor_close[door].wait_for_press()
    #                     self.kit.continuous_servo[door].throttle = open_b
    #                     sleep(1)
    #                     if self.sensor_close[door].is_pressed:
    #                         # print('sensor pressed')
    #                         stationary = True
    #                     else:
    #                         # print('sensor not pressed')
    #                         continue
    #
    #                         # self.opening_time[door_number] = opening_time
    #         # self.closing_time[door_number] = closing_time
    #         # self.directions[door_number] = direction
    #         # print('final values')
    #         # print(f'closing bound: {close_b}, opening bound: {open_b}')
    #         average = (close_b + open_b) / 2
    #         # print(f'average = {average}')
    #         self.neutral_values[door] = average
    #         self.kit.continuous_servo[door].throttle = self.neutral_values[door]
    #     return

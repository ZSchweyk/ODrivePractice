import odrive
from time import sleep
from threading import Thread
from RPi_ODrive.ODrive_Ease_Lib import *
from pidev.Joystick import Joystick

def startup(od):
    assert od.config.enable_brake_resistor is True, "Check for faulty brake resistor."
    ax = ODrive_Axis(od.axis0, 30, 10)
    ax.set_gains()
    if not ax.is_calibrated():
        print("Calibrating...")
        # ax.calibrate()
        ax.calibrate_with_current_lim(30)

    ax.axis.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

    print("Velocity Limit:", ax.get_vel_limit())

    joystick = Joystick(0, False)

    od_j_events = ODrive_Joystick_Events(joystick, ax)

    Thread(target=od_j_events.test_joystick_method).start()

    Thread(target=od_j_events.main).start()


class ODrive_Joystick_Events:
    def __init__(self, joystick: Joystick, ax: ODrive_Axis):
        self.joystick = joystick
        self.ax = ax

    def set_relative_od_position(self):
        if self.joystick.get_button_state(3):
            self.ax.set_relative_pos(1)
        elif self.joystick.get_button_state(4):
            self.ax.set_relative_pos(-1)


    def set_od_velocity(self):
        joy_reading = round(self.joystick.get_axis("x"), 2)
        scaled_joy_reading = self.scale(joy_reading, -1, 1, -10, 10)
        self.ax.set_vel(scaled_joy_reading * -1)


    def test_joystick_method(self):
        while True:
            if self.joystick.click_n_times_check(2, 3, 2, .15, False):
                print("YYYYYYYYYYYYYYYYYYYYYYYY")
            else:
                print("NNNNNNNNNNNNNNNNNNNNNNNN")
            sleep(.2)

    def main(self):
        while True:
            self.set_relative_od_position()
            print("set_relative_od_position")
            sleep(.1)
            self.set_od_velocity()
            print("set_od_velocity")
            sleep(.15)


    @staticmethod
    def scale(value, v_min, v_max, r_min, r_max):
        percentage = (value - v_min) / (v_max - v_min)
        return round(r_min + percentage * (r_max - r_min), 2)

    # @staticmethod
    # def execute_and_print_all(*methods):
    #     for method in methods:
    #         method()
    #         print(method().__name__)
    #
    # @staticmethod
    # def execute_and_print(method):
    #     method()
    #     print(method().__name__)


od = find_odrive()
startup(od)

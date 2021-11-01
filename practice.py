"""
Example usage of the ODrive python library to monitor and control ODrive devices
"""
import odrive
from time import sleep
from RPi_ODrive.ODrive_Ease_Lib import *


def startup(od):
    assert od.config.enable_brake_resistor is True, "Check for faulty brake resistor."
    dump_errors(od)

    # Selecting an axis to talk to, axis0 and axis1 correspond to M0 and M1 on the ODrive
    ax = ODrive_Axis(od.axis0)
    # Basic motor tuning, for more precise tuning follow this guide: https://docs.odriverobotics.com/control.html#tuning
    ax.set_gains()

    if not ax.is_calibrated():
        print("calibrating...")
        # ax.calibrate()
        ax.calibrate_with_current_lim(20)

    print("Current Limit: ", ax.get_current_limit())
    print("Velocity Limit: ", ax.get_vel_limit())

    print("Velocity Tolerance: ", ax.axis.controller.config.vel_limit_tolerance)
    print("Using Velocity Tolerance: ", ax.axis.controller.config.enable_overspeed_error)

    # print("homing")
    # ax.home_with_endstop(1, .5, 2)  # Home with velocity 1 to endstop on GPIO Pin 2, then offset .5 rotations
    # ax.home_without_endstop(1, .5)  # Home with velocity 1 until wall is hit, then offset .5 rotations
    # print("Current Position in Turns = ", round(ax.get_pos(), 2))  # should be at 0.0
    # sleep(1)


    # SETTING POSITION
    ax.set_vel_limit(5)
    ax.set_pos(5)
    while ax.is_busy():
        sleep(.01)
    print("Current Position in Turns = ", round(ax.get_pos(), 2))
    ax.set_relative_pos(-5)
    while ax.is_busy():
        sleep(.01)

    # SETTING VELOCITY
    print("Current Position in Turns = ", round(ax.get_pos(), 2))
    ax.set_vel_limit(5)  # Sets the velocity limit to be X turns/s
    ax.set_vel(3)  # Starts turning the motor X turns/s
    sleep(5)
    print("Encoder Measured Velocity = ", round(ax.get_vel(), 2))
    ax.set_vel(0)  # Stops motor
    sleep(1)
    print("Current Position in Turns = ", round(ax.get_pos(), 2))
    ax.set_pos(0)
    while ax.is_busy():
        sleep(.01)
    print("Current Position in Turns = ", round(ax.get_pos(), 2))

    # SETTING RAMPED VELOCITY
    ax.set_vel_limit(5)  # Sets the velocity limit to be X turns/s
    print("speeding up")
    ax.set_ramped_vel(5, 1)  # Starts accelerating motor to X turns/s
    sleep(10)
    print("slowing down")
    ax.set_ramped_vel(0, 1)  # Stops motor
    while ax.is_busy():
        sleep(.01)
    print("Current Position in Turns = ", round(ax.get_pos(), 2))

    # USING TRAJECTORY CONTROL
    ax.set_vel_limit(12)
    ax.set_pos_traj(0, 1, 10, 1)  # Moves motor to absolute position 0 with accel 1, max vel. 10, and decel. 1
    while ax.is_busy():
        sleep(.01)
    print("Current Position in Turns = ", round(ax.get_pos(), 2))

    ax.idle()  # Removes motor from CLOSED_LOOP_CONTROL, essentially 'frees' the motor


if __name__ == "__main__":
    od = find_odrive()
    startup(od)
    dump_errors(od)
# region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain = Brain()

# Robot configuration code
BL_Wheel = Motor(Ports.PORT19, GearSetting.RATIO_18_1, True)
TL_Wheel = Motor(Ports.PORT16, GearSetting.RATIO_18_1, False)
BR_Wheel = Motor(Ports.PORT18, GearSetting.RATIO_18_1, False)
TR_Wheel = Motor(Ports.PORT17, GearSetting.RATIO_18_1, True)
controller_1 = Controller(PRIMARY)
IntakeRollerMotor = Motor(Ports.PORT15, GearSetting.RATIO_18_1, False)
CatapultMotor = Motor(Ports.PORT10, GearSetting.RATIO_18_1, False)

# wait for rotation sensor to fully initialize
wait(30, MSEC)

# define variables used for controlling motors based on controller inputs
controller_1_up_down_buttons_control_motors_stopped = True


# define a task that will handle monitoring inputs from controller_1
def rc_auto_loop_function_controller_1():
    global controller_1_up_down_buttons_control_motors_stopped, remote_control_code_enabled
    # process the controller input every 20 milliseconds
    # update the motors based on the input values
    while True:
        if remote_control_code_enabled:
            # check the buttonUp/buttonDown status
            # to control BL_Wheel
            if controller_1.buttonUp.pressing():
                BL_Wheel.spin(FORWARD)
                controller_1_up_down_buttons_control_motors_stopped = False
            elif controller_1.buttonDown.pressing():
                BL_Wheel.spin(REVERSE)
                controller_1_up_down_buttons_control_motors_stopped = False
            elif not controller_1_up_down_buttons_control_motors_stopped:
                BL_Wheel.stop()
                # set the toggle so that we don't constantly tell the motor to stop when
                # the buttons are released
                controller_1_up_down_buttons_control_motors_stopped = True
        # wait before repeating the process
        wait(20, MSEC)


# define variable for remote controller enable/disable
remote_control_code_enabled = True

rc_auto_loop_thread_controller_1 = Thread(rc_auto_loop_function_controller_1)
# endregion VEXcode Generated Robot Configuration

# ------------------------------------------
#
# 	Project:      Epimetheus _RCV3.0
#	Author:       Bryan B-R
#	Created:      May 8th, 2023
#	Description:  Middle School Competition Robot Years:2022-2023, Spin Up!
#
# ------------------------------------------

# Library imports
from vex import *

# Begin project code
CodeVersion = 3.0

# !! // pre_autonomous code // !!
# actions to do when the program starts (pre-functions needed to be outside of other functions as they will be used globally in the code.)
brain.screen.clear_screen()
brain.screen.print("pre auton code")
wait(1, SECONDS)


# Turning("R", False) -- Turns the robot Right Forward
# Turning("R", True) -- Turns the robot Right in Reverse

# PRE AUTONAMOUS CODE END !!

def autonomous():
    brain.screen.clear_screen()
    brain.screen.print("autonomous code")
    # place automonous code here


def user_control():
    brain.screen.clear_screen()

    # place driver control in this while loop

    def ForwardMovement(direction):
        if direction == "F":
            BR_Wheel.spin(FORWARD, 7, VOLT)
            TR_Wheel.spin(FORWARD, 7, VOLT)
            BL_Wheel.spin(FORWARD, 7, VOLT)
            TL_Wheel.spin(FORWARD, 7, VOLT)
        elif direction == "B":
            BR_Wheel.spin(REVERSE, 7, VOLT)
            TR_Wheel.spin(REVERSE, 7, VOLT)
            BL_Wheel.spin(REVERSE, 7, VOLT)
            TL_Wheel.spin(REVERSE, 7, VOLT)
        elif direction == "C":
            BR_Wheel.stop()
            TR_Wheel.stop()
            BL_Wheel.stop()
            TL_Wheel.stop()

    # // Controller --> Robot Handlers
    R2_Pressed = False
    L2_Pressed = False

    IntakeRollerToggled = False

    def R2_ButtonPressed():
        global R2_Pressed
        R2_Pressed = True
        ForwardMovement("F")

    def R2_ButtonReleased():
        global R2_Pressed
        R2_Pressed = False
        ForwardMovement("C")

    def L2_ButtonPressed():
        global L2_Pressed
        L2_Pressed = True
        ForwardMovement("B")

    def L2_ButtonReleased():
        global L2_Pressed
        L2_Pressed = False
        ForwardMovement("C")

    def ButtonA_Function():
        global IntakeRollerToggled
        if IntakeRollerToggled:
            IntakeRollerToggled = False
            IntakeRollerMotor.spin(FORWARD, 12, VOLT)
        else:
            IntakeRollerToggled = True
            IntakeRollerMotor.stop()

    def LeftJoystickCode():
        if controller_1.axis4.position() == 0:
            if R2_Pressed and L2_Pressed:
                ForwardMovement("C")
            elif R2_Pressed:
                ForwardMovement("F")
            elif L2_Pressed:
                ForwardMovement("B")
            else:
                ForwardMovement("C")
        elif controller_1.axis4.position() > 0:
            if controller_1.axis3.position() > 0:  # If Joystick is Up, Right
                BL_Wheel.spin(FORWARD, 7, VOLT)
            elif controller_1.axis3.position() < 0:  # If Joystick is Down, Right
                TL_Wheel.spin(REVERSE, 7, VOLT)
            elif controller_1.axis3.position() == 0:  # If Joystick is centered, Right
                BL_Wheel.spin(FORWARD, 7, VOLT)
        elif controller_1.axis4.position() < 0:
            if controller_1.axis3.position() > 0:  # If Joystick is Up, Left
                BR_Wheel.spin(FORWARD, 7, VOLT)
            elif controller_1.axis3.position() < 0:  # If Joystick is Down, Left
                TR_Wheel.spin(REVERSE, 7, VOLT)
            elif controller_1.axis3.position() == 0:  # If Joystick is centered, Left
                BR_Wheel.spin(FORWARD, 7, VOLT)

    # // Event Handlers //
    controller_1.axis4.changed(LeftJoystickCode)

    controller_1.buttonR2.pressed(R2_ButtonPressed)
    controller_1.buttonR2.released(R2_ButtonReleased)

    controller_1.buttonL2.pressed(L2_ButtonPressed)
    controller_1.buttonL2.released(L2_ButtonReleased)

    controller_1.buttonA.pressed(ButtonA_Function)


# create competition instance
comp = Competition(user_control, autonomous)
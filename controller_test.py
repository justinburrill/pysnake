from inputs import get_gamepad
import math
import threading
import time


class XboxController(object):
    MAX_JOY_VAL = math.pow(2, 15)

    def __init__(self):
        self.LeftJoystickY = 0
        self.LeftJoystickX = 0

        self._monitor_thread = threading.Thread(
            target=self._monitor_controller, args=())
        self._monitor_thread.daemon = True
        self._monitor_thread.start()

    def read(self):  # return the buttons/triggers that you care about in this methode
        x = self.LeftJoystickX
        y = self.LeftJoystickY
        return [x, y]

    def _monitor_controller(self):
        while True:
            events = get_gamepad()
            for event in events:
                if event.code == 'ABS_Y':
                    self.LeftJoystickY = event.state / \
                        XboxController.MAX_JOY_VAL  # normalize between -1 and 1
                elif event.code == 'ABS_X':
                    self.LeftJoystickX = event.state / \
                        XboxController.MAX_JOY_VAL  # normalize between -1 and 1


class ControllerController:
    def check(self):
        if __name__ == '__main__':
            joy = XboxController()
            deadzone = 0.4
            while True:
                info = joy.read()
                if info[0] > deadzone or info[1] > deadzone or info[0] < -deadzone or info[1] < -deadzone:
                    print(info)

    def __init__(self):
        t = threading.Thread(target=self.check)
        t.start()


ControllerController()

x = 0
while True:
    time.sleep(1)
    print(x)
    x = x+1

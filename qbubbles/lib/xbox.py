try:
    from inputs import get_gamepad, UnpluggedError

    GAMEPAD_SUPPORT = True
except AttributeError as e:
    if e.args[0] == "'NoneType' object has no attribute 'XInputGetState'":
        GAMEPAD_SUPPORT = False

import math


class XboxController(object):
    MAX_TRIG_VAL = math.pow(2, 8)
    MAX_JOY_VAL = math.pow(2, 15)

    def __init__(self):

        self.LeftJoystickY = 0
        self.LeftJoystickX = 0
        self.RightJoystickY = 0
        self.RightJoystickX = 0
        self.LeftTrigger = 0
        self.RightTrigger = 0
        self.LeftBumper = 0
        self.RightBumper = 0
        self.A = 0
        self.X = 0
        self.Y = 0
        self.B = 0
        self.LeftThumb = 0
        self.RightThumb = 0
        self.Back = 0
        self.Start = 0
        self.LeftDPad = 0
        self.RightDPad = 0
        self.UpDPad = 0
        self.DownDPad = 0

        # self._monitor_thread = threading.Thread(target=self.update, args=())
        # self._monitor_thread.daemon = True
        # self._monitor_thread.start()

    def read(self):
        if not GAMEPAD_SUPPORT:
            return
        x = self.LeftJoystickX
        y = self.LeftJoystickY
        a = self.A
        b = self.X  # b=1, x=2
        rb = self.RightBumper
        return [x, y, a, b, rb]

    def update(self):
        if not GAMEPAD_SUPPORT:
            return
        try:
            events = get_gamepad()
        except UnpluggedError:
            return
        for event in events:
            if event.code == 'ABS_Y':
                self.LeftJoystickY = event.state / XboxController.MAX_JOY_VAL  # normalize between -1 and 1
            elif event.code == 'ABS_X':
                self.LeftJoystickX = event.state / XboxController.MAX_JOY_VAL  # normalize between -1 and 1
            elif event.code == 'ABS_RY':
                self.RightJoystickY = event.state / XboxController.MAX_JOY_VAL  # normalize between -1 and 1
            elif event.code == 'ABS_RX':
                self.RightJoystickX = event.state / XboxController.MAX_JOY_VAL  # normalize between -1 and 1
            elif event.code == 'ABS_Z':
                self.LeftTrigger = event.state / XboxController.MAX_TRIG_VAL  # normalize between 0 and 1
            elif event.code == 'ABS_RZ':
                self.RightTrigger = event.state / XboxController.MAX_TRIG_VAL  # normalize between 0 and 1
            elif event.code == 'BTN_TL':
                self.LeftBumper = event.state
            elif event.code == 'BTN_TR':
                self.RightBumper = event.state
            elif event.code == 'BTN_SOUTH':
                self.A = event.state
            elif event.code == 'BTN_NORTH':
                self.X = event.state
            elif event.code == 'BTN_WEST':
                self.Y = event.state
            elif event.code == 'BTN_EAST':
                self.B = event.state
            elif event.code == 'BTN_THUMBL':
                self.LeftThumb = event.state
            elif event.code == 'BTN_THUMBR':
                self.RightThumb = event.state
            elif event.code == 'BTN_SELECT':
                self.Back = event.state
            elif event.code == 'BTN_START':
                self.Start = event.state
            elif event.code == 'BTN_TRIGGER_HAPPY1':
                self.LeftDPad = event.state
            elif event.code == 'BTN_TRIGGER_HAPPY2':
                self.RightDPad = event.state
            elif event.code == 'BTN_TRIGGER_HAPPY3':
                self.UpDPad = event.state
            elif event.code == 'BTN_TRIGGER_HAPPY4':
                self.DownDPad = event.state
            elif event.code == "ABS_HAT0X":
                if event.state == -1:
                    self.LeftDPad = 1
                elif event.state == 0:
                    self.LeftDPad = 0
                    self.RightDPad = 0
                elif event.state == 1:
                    self.RightDPad = 1
            elif event.code == "ABS_HAT0Y":
                if event.state == -1:
                    self.UpDPad = 1
                elif event.state == 0:
                    self.UpDPad = 0
                    self.DownDPad = 0
                elif event.state == 1:
                    self.DownDPad = 1
            elif event.code == "SYN_REPORT":
                pass
            else:
                from sys import stderr
                print("[XboxContoller]: Invalid input: %s" % event.code, file=stderr)
            # print(event.__dict__)

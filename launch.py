import math
import time
import ntcore
import launchpad_py as launchpad
from launchpad_py import LaunchpadMiniMk3
from ntcore import NetworkTableInstance
from pygame import time
from pyvjoystick import vjoy
from pyvjoystick.vjoy import VJoyDevice


class LaunchpadMini3Controller:
    lp: LaunchpadMiniMk3 = None
    hid0: VJoyDevice = None
    hid1: VJoyDevice = None
    teamnumber: int = None
    networkTables: NetworkTableInstance = None
    launchpadTable: ntcore._ntcore.NetworkTable = None
    buttons = None # type: dict[int, dict[int, ntcore._ntcore.IntegerArraySubscriber]]
    buttonStates: list[list[bool]] = [([False] for i in range(8)) for k in range(8)]
    stop: bool = False

    def __init__(self, ntTable: str):
        self.printWarning()

        if launchpad.LaunchpadMiniMk3().Check(1):
            self.lp = launchpad.LaunchpadMiniMk3()
            if self.lp.Open(1, "minimk3"):
                self.startupLeds()

                while True:
                    try:
                        self.teamnumber = int(input("Please enter your team number: "))
                        break
                    except:
                        print("Not a valid teamnumber, please input again\n")

                hid0 = vjoy.VJoyDevice(1)
                hid1 = vjoy.VJoyDevice(2)

                print("Launchpad Mini Mk3")

                self.setupNetworkTableClient(ntTable)
        else:
            raise Exception("Launchpad Attached is not an Mk3 or is not connected.")


    def setupNetworkTableClient(self, launchpadNTKey: str):
        self.networkTables = ntcore.NetworkTableInstance.getDefault()
        self.networkTables.startClient4("launchpad")
        self.networkTables.setServerTeam(self.teamnumber)
        # self.networkTables.setServer("localhost") # Sim only
        self.networkTables.startDSClient()
        self.launchpadTable = self.networkTables.getTable(launchpadNTKey)
        self.buttons = {row: {column: self.launchpadTable.getSubTable(str(row))
                              .getIntegerArrayTopic(str(column))
                              .subscribe([0, 0, 0]) for column in range(0,8)} for row in range(0,8)}


    def updateLeds(self):
        if self.networkTables.isConnected():
            for i, v in self.buttons.items():
                for j, l in v.items():
                    for k in l.readQueue():
                        self.setLed(i, j, k.value[0], k.value[1], k.value[2])


    def updateButtonStates(self):
        XYState = self.lp.ButtonStateXY()
        while XYState != []:
            if XYState[2] > 0:
                print(f"({XYState[0]},{XYState[1]-1}) is {"pressed" if [XYState[2]] != 0 else "not pressed"}.")
                self.buttonStates[XYState[0]][XYState[1]-1] = (XYState[2] != 0)
                XYState = self.lp.ButtonStateXY()
            elif XYState[1] == 7 and XYState[2] == 0:
                self.stop = True


    def updateHidStates(self):
        for row in range(self.buttonStates):
            for col in range(row):
                if row < 4:
                    self.hid0.set_button((1+col+row*7), self.buttonStates[row][col])
                else:
                    self.hid1.set_button((1+col+(row-4)*7), self.buttonStates[row][col])


    def startupLeds(self):
        self.lp.LedAllOn(5)
        self.lp.LedCtrlString(f"{self.teamnumber}", 0, 0, 63, -1, waitms=0)
        self.lp.LedAllOn(0)


    def setLed(self, x, y, red, green, blue):
        self.lp.LedCtrlXY(x, y+1, red, green, blue)


    def printWarning(self):
        print("\nCurrently this program only works with the Novation Launchpad Mk3 Mini")
        print(
            "0,0 is defined as the top left of the launchpad whitespace(ONLY THE WHITESPACE IS USED), +y is down and +x is to the right from the top left white space")
        print(
            "If you want any LED pattern set by default do it with the associated Java library")
        print("Stop button will be the on the top-most button row, and to the right, should be just left of the corner")
        print("PLEASE MAKE SURE YOUR VJOY CONFIG IS CORRECT")
        print("It needs to be 2 vJoy devices, with no enabled Axes, no Force Feedback, 0 POVs, and 32 buttons")
        print("Please confirm that vJoy device 1 is on driverstation usb order 1, and same with 2")
        print("Make sure this is run on the same computer as the driver station for NT and HID reasons")
        print("PLEASE USE THE ASSOCIATED JAVA CLASS FOR INTERACTION\n")


    def stopCheck(self):
        return self.stop


    def close(self):
        self.lp.LedCtrlString("BYE!", 22, 0, 63, -1, waitms=0)

        self.lp.Reset()  # turn all LEDs off
        self.lp.Close()  # close the Launchpad (will quit with an error due to a PyGame bug)
        self.hid0.reset()
        self.hid1.reset()



def main():
    launchPad = LaunchpadMini3Controller("launchpad")

    # General Loop for buttons and colors
    while True:
        time.wait(1)
        launchPad.updateButtonStates()
        launchPad.updateHidStates()
        launchPad.updateLeds()
        if launchPad.stopCheck():
            break

    launchPad.close()

if __name__ == '__main__':
    main()
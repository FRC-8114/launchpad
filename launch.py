import time
import ntcore
import launchpad_py as launchpad
from pygame import time
from pyvjoystick import vjoy

looping = True
mode = None

#max is 63
#[63,0,0] - Red || [0,63,0] - Green || [0,0,63] - Blue  || [63,63,63] - White || [0,0,0] - Blank/Black

blankleds = [
    [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],
    [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],
    [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],
    [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],
    [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],
    [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],
    [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],
    [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],
    [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
]

compLEDS = [
	[[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],
    [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],
    [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],
    [[0,0,0],[0,0,0],[0,63,63],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],
    [[0,0,0],[0,0,0],[12,0,13],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],
    [[0,0,0],[0,31,0],[31,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],
    [[13,24,0],[63,0,30],[0,63,0],[63,0,63],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],
    [[0,24,13],[0,0,0],[63,63,0],[0,0,0],[0,0,0],[0,0,0],[0,63,0],[0,0,0],[0,0,0]],
    [[63,63,63],[0,0,0],[63,0,0],[30,0,0],[0,0,0],[0,0,0],[63,0,0],[0,0,0],[0,0,0]]
]

buttonMatrix = (
    (81, 82, 83, 84, 85, 86, 87, 88, 71, 72, 73, 74, 75, 76, 77, 78,
    61, 62, 63, 64, 65, 66, 67, 68, 51, 52, 53, 54, 55, 56, 57, 58),
    (41, 42, 43, 44, 45, 46, 47, 48, 31, 32, 33, 34, 35, 36, 37, 38,
    21, 22, 23, 24, 25, 26, 27, 28, 11, 12, 13, 14, 15, 16, 17, 18)
)


def main():
	# Start of Program
	print("\nCurrently this program only works with the Novation Launchpad Mk3 Mini")
	print("0,0 is defined as the top left of the launchpad whitespace(ONLY THE WHITESPACE IS USED), down is +y and right is +x")
	print("If you want any LED pattern set by default use the compLEDS array to set the colors, otherwise do it with the associated Java library")
	print("Stop button will be the on the top-most button row, and to the right, should be just left of the corner")
	print("PLEASE MAKE SURE YOUR VJOY CONFIG IS CORRECT")
	print("It needs to be 2 vJoy devices, with no enabled Axes, no Force Feedback, 0 POVs, and 32 buttons")
	print("Please confirm that vJoy device 1 is on driverstation usb order 1, and same with 2")
	print("If you do not want to use our associated java class, (0,0) through (3,7) are device 1, and the rest are device 2")
	print()
	while True:
		try:
			teamnumber = int(input("Please enter your team number: "))
			break
		except:
			print("Not a valid teamnumber, please input again\n")
	launchpadType = "mk3"

	print()

	#Launch the launchpad and connect to vJoy
	if launchpadType == "mk3":
		if launchpad.LaunchpadMiniMk3().Check( 1 ):
			lp = launchpad.LaunchpadMiniMk3()
			if lp.Open( 1, "minimk3" ):
				print("Launchpad Mini Mk3")
				mode = "launched"
		else:
			print("Did not find any Launchpads, meh...")
			input()
			return
	print("")
	j1 = vjoy.VJoyDevice(1)
	j2 = vjoy.VJoyDevice(2)
 
	#Beginning LEDs
	lp.LedAllOn(5)

	lp.LedCtrlString( f"FRC-{teamnumber}", 63, 0, 63, -1, waitms = 0 )

	lp.LedAllOn(0)

	setwithaset(compLEDS,lp)

	#NT setup
	inst = ntcore.NetworkTableInstance.getDefault()
	inst.startClient4("launchpad")
	inst.setServerTeam(teamnumber)
	inst.startDSClient()

	#General Loop for buttons and colors
	while looping:
		time.wait(1)
		inputs = []
		got = lp.ButtonStateXY()
		
		if got == []:
			continue

		while got != []:
			inputs.append(got)
			got = lp.ButtonStateXY()

		for button in inputs:
			if button == [7,0,127]:
				break
			elif button[0] <= 7 and button[1] > 0:
				if button[1] < 5:
					j1.set_button((1+button[0]+(button[1]-1)*7), button[2] != 0)
				else:
					j2.set_button((1+button[0]+(button[1]-5)*7), button[2] != 0)

	# now quit...
	print("Quitting !\n\n")

	lp.LedCtrlString( "BYE!", 22, 0, 63, -1, waitms = 0 )

	lp.Reset() # turn all LEDs off
	lp.Close() # close the Launchpad (will quit with an error due to a PyGame bug)
	j1.reset()
	j2.reset()

	time.delay(200)

def setled(row,col,red,green,blue,lp):
	lp.LedCtrlXY(row,col,red,green,blue)

def setwithaset(sets,lp):
	for r in range(8):
		for c in range(8):
			if sets[r][c] != [0,0,0]:
				setled(c, r, sets[r][c][0], sets[r][c][1], sets[r][c][2],lp)

if __name__ == '__main__':
	main()
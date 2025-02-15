import time
import ntcore
import launchpad_py as launchpad
from pygame import time
from pyvjoystick import vjoy

def main():
	# Start of Program
	print("\nCurrently this program only works with the Novation Launchpad Mk3 Mini")
	print("0,0 is defined as the top left of the launchpad whitespace(ONLY THE WHITESPACE IS USED), down is +y and right is +x")
	print("If you want any LED pattern set by default use the compLEDS array to set the colors, otherwise do it with the associated Java library")
	print("Stop button will be the on the top-most button row, and to the right, should be just left of the corner")
	print("PLEASE MAKE SURE YOUR VJOY CONFIG IS CORRECT")
	print("It needs to be 2 vJoy devices, with no enabled Axes, no Force Feedback, 0 POVs, and 32 buttons")
	print("Please confirm that vJoy device 1 is on driverstation usb order 1, and same with 2\n")
	while True:
		try:
			teamnumber = int(input("Please enter your team number: "))
			break
		except:
			print("Not a valid teamnumber, please input again\n")

	launchpadType = "mk3"
	print()
	mode = None

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

	#NT setup
	inst = ntcore.NetworkTableInstance.getDefault()
	buttons = []
	for i in range(8):
		buttons.append([])
		for j in range(8):
			buttons[i].append(inst.getTable("launchpad").getSubTable(str(i)).getIntegerArrayTopic(str(j)).subscribe([0,0,0]))
	inst.startClient4("launchpad")
	inst.setServerTeam(8114)
	inst.startDSClient()

	#General Loop for buttons and colors
	while True:
		time.wait(1)

		if inst.isConnected():
			for i in buttons:
				for j in i:
					for k in j.readQueue():
						setled(j, i+1, k[0], k[1], k[2], lp)

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

def setled(x,y,red,green,blue,lp1):
	lp1.LedCtrlXY(x,y,red,green,blue)

if __name__ == '__main__':
	main()
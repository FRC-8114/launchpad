import sys
import subprocess
import os

try:
	import launchpad_py as launchpad
except ImportError:
	try:
		import launchpad
	except ImportError:
		sys.exit("error loading launchpad.py")

import random
from pygame import time

looping = True
mode = None

#max is 63
#[63,0,0] - Red || [0,63,0] - Green || [0,0,63] - Blue  || [63,63,63] - White || [0,0,0] - Blank/Black
ballleds = [
    [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],
    [[0,0,0],[0,0,0],[0,0,0],[0,0,63],[0,0,63],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],
    [[0,0,0],[0,0,0],[0,0,63],[0,0,0],[0,0,0],[0,0,63],[0,0,0],[0,0,0],[0,0,0]],
    [[0,0,0],[0,0,0],[0,0,63],[0,0,0],[0,0,0],[0,0,63],[0,0,0],[0,0,0],[0,0,0]],
    [[0,0,0],[0,0,0],[0,0,63],[0,0,0],[0,0,0],[0,0,63],[0,0,0],[0,0,0],[0,0,0]],
    [[0,0,0],[0,0,0],[0,0,63],[0,0,0],[0,0,0],[0,0,63],[0,0,0],[0,0,0],[0,0,0]],
    [[0,0,0],[0,0,63],[0,0,63],[0,0,63],[0,0,63],[0,0,63],[0,0,63],[0,0,0],[0,0,0]],
    [[0,0,0],[0,0,63],[0,0,0],[0,0,63],[0,0,63],[0,0,0],[0,0,63],[0,0,0],[0,0,0]],
    [[0,0,0],[0,0,63],[0,0,63],[0,0,63],[0,0,63],[0,0,63],[0,0,63],[0,0,0],[0,0,0]]
]

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

amongusleds = [
    [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],
    [[0,0,0],[0,0,0],[63,0,0],[63,0,0],[63,0,0],[63,0,0],[63,0,0],[0,0,0],[0,0,0]],
    [[0,0,0],[63,0,0],[63,0,0],[63,0,0],[63,0,0],[63,0,0],[63,0,0],[0,0,0],[0,0,0]],
    [[0,0,0],[0,0,63],[0,0,63],[0,0,63],[63,0,0],[63,0,0],[63,0,0],[63,0,0],[0,0,0]],
    [[0,0,0],[0,0,63],[0,0,63],[0,0,63],[63,0,0],[63,0,0],[63,0,0],[63,0,0],[0,0,0]],
    [[0,0,0],[63,0,0],[63,0,0],[63,0,0],[63,0,0],[63,0,0],[63,0,0],[63,0,0],[0,0,0]],
    [[0,0,0],[63,0,0],[63,0,0],[63,0,0],[63,0,0],[63,0,0],[63,0,0],[0,0,0],[0,0,0]],
    [[0,0,0],[63,0,0],[63,0,0],[0,0,0],[0,0,0],[63,0,0],[63,0,0],[0,0,0],[0,0,0]],
    [[0,0,0],[63,0,0],[63,0,0],[0,0,0],[0,0,0],[63,0,0],[63,0,0],[0,0,0],[0,0,0]]
]

# experimental MK3 implementation
# The MK3 has two MIDI instances per device; we need the 2nd one.
# If you have two MK3s attached, its "1" for the first and "3" for the 2nd device
if launchpad.LaunchpadMiniMk3().Check( 1 ):
	lp = launchpad.LaunchpadMiniMk3()
	if lp.Open( 1, "minimk3" ):
		print("Launchpad Mini Mk3")
		mode = "Pro"

def main():
	if mode is None:
		print("Did not find any Launchpads, meh...")
		return

	count = 1



	lp.LedAllOn(5)

	lp.LedCtrlString( "BFM INC.", 63, 0, 63, -1, waitms = 0 )

	lp.LedAllOn(52)

	setwithaset(amongusleds)

	while looping:
		loopin()

	# now quit...
	print("Quitting !\n\n")

	lp.LedCtrlString( "BYE!", 22, 0, 63, -1, waitms = 0 )

	lp.Reset() # turn all LEDs off
	lp.Close() # close the Launchpad (will quit with an error due to a PyGame bug)

	time.delay(200)

def setled(row,col,red,green,blue):
	lp.LedCtrlXY(row,col,red,green,blue)

def setwithaset(sets):
	for r in range(9):
		for c in range(9):
			if sets[r][c] != [0,0,0]:
				setled(c, r, sets[r][c][0], sets[r][c][1], sets[r][c][2])

count = 0

def loopin():
	buta = lp.ButtonStateRaw()
	global looping
	global count

	if buta != []:
		print(buta," ",count)
		count += 1

	if buta == [11,127]:
		os.system("E:\\SteamLibrary\\steamapps\\common\\Soundpad\\Soundpad -rc DoPlaySound(10)")

	if buta == [12,127]:
		os.system("E:\\SteamLibrary\\steamapps\\common\\Soundpad\\Soundpad -rc DoPlaySound(124)")

	if buta == [98,0]:
		os.system("E:\\SteamLibrary\\steamapps\\common\\Soundpad\\Soundpad -rc DoStopSound()")
		looping = False

	if buta == [19,0]:
		os.system("E:\\SteamLibrary\\steamapps\\common\\Soundpad\\Soundpad -rc DoStopSound()")


if __name__ == '__main__':
	main()
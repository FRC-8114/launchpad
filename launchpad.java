package frc.robot;

import edu.wpi.first.networktables.NetworkTable;
import edu.wpi.first.networktables.NetworkTableInstance;
import edu.wpi.first.networktables.NetworkTableValue;
import edu.wpi.first.wpilibj.util.Color8Bit;
import edu.wpi.first.wpilibj2.command.Commands;
import edu.wpi.first.wpilibj2.command.button.CommandGenericHID;
import edu.wpi.first.wpilibj2.command.button.Trigger;

public class launchpad {

    //numbers must be within 0-63
    //[63,0,0] - Red || [0,63,0] - Green || [0,0,63] - Blue  || [63,63,63] - White || [0,0,0] - Blank/Black
    //This will update the LEDs once the python attaches to NT
    //This table is visually accurate to the launchpad each of these rbg sets will change it's respective button
    public long[][][] rgbTable = {
        {{0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}},
        {{0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}},
        {{0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}},
        {{0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}},
        {{0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}},
        {{0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}},
        {{0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}},
        {{0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}}
    };
    private Trigger[][] buttons = new Trigger[8][8];
    private Color8Bit pressedColor;

    private NetworkTableInstance table;
    private NetworkTable launch;

    public launchpad(int vjoy1, int vjoy2, Color8Bit pressedColor) {
        table = NetworkTableInstance.getDefault();
        launch = table.getTable("launchpad");
        int[] vjoyPorts = new int[]{vjoy1, vjoy2};
        this.pressedColor = pressedColor;
        defaultLEDs();
        for (int i=0; i < 2; i++) {
            CommandGenericHID hidController = new CommandGenericHID(vjoyPorts[i]);
            for (int j=0; j < 4; j++) {
                for (int k=0; k < 7; k++) {
                    int finalJ = j, finalI = i, finalK = k;
                    buttons[j+i*4][k] = hidController.button((k+1)+(j*8));
                    buttons[j+i*4][k].whileTrue(Commands.runOnce(() -> changeLED(finalJ + finalI * 4, finalK, this.pressedColor)));
                    buttons[j+i*4][k].onFalse(Commands.runOnce(() -> changeLED(finalJ + finalI * 4, finalK, this.rgbTable[finalJ + finalI * 4][finalK])));
                }
            }
        }
    }

    /**
     * Gets the trigger connected to a button
     *
     * @param x x Position of the launchpad, where +x is to the right, starting at the top left (0-7)
     * @param y x Position of the launchpad, where +y is down, starting at the top left (0-7)
     * @return The trigger class connected to the button
     * @throws IllegalArgumentException if x or y is not within 0-7
     */
    public Trigger getButton(int x, int y) {
        if (x > 7 || y > 7 || x < 0 || y < 0) {
            throw new IllegalArgumentException("Coords must be less than 7");
        }
        return buttons[y][x];
    }

    /**
     * Changes the color of a button's LED
     *
     * @param x x Position of the launchpad, where +x is to the right, starting at the top left (0-7)
     * @param y y Position of the launchpad, where +y is down, starting at the top left (0-7)
     * @param rgb the long[3] array that describes the color of the button, each position of the array must be (0-63)
     * @throws IllegalArgumentException if x or y is not within 0-7, or if array is invalid.
     */
    public void changeLED(int x, int y, long[] rgb) {
        if (x > 7 || y > 7 || x < 0 || y < 0) {
            throw new IllegalArgumentException("Coords must be within 0-7");
        }
        if (rgb.length != 3) {
            throw new IllegalArgumentException("Array length must be 3");
        }
        for (long i : rgb) {
            if (i > 63 || i < 0) {
                throw new IllegalArgumentException(i + " is an invalid rgb input, must be within 0-63");
            }
        }
        launch.getSubTable(Integer.toString(y)).putValue(Integer.toString(x), NetworkTableValue.makeIntegerArray(rgb));
    }

    /**
     * Changes the color of a button's LED
     *
     * @param x x Position of the launchpad, where +x is to the right, starting at the top left (0-7)
     * @param y y Position of the launchpad, where +y is down, starting at the top left (0-7)
     * @param rgb the Color8Bit object that describes the color of the button
     * @throws IllegalArgumentException if x or y is not within 0-7
     */
    public void changeLED(int x, int y, Color8Bit color8Bit) {
        if (x > 7 || y > 7 || x < 0 || y < 0) {
            throw new IllegalArgumentException("Coords must be within 0-7");
        }
        launch.getSubTable(Integer.toString(y)).putValue(Integer.toString(x), NetworkTableValue.makeIntegerArray(convertColor8Bit(color8Bit)));
    }

    /** 
     * Converts Color8Bit to proper long[3] array
     * 
     * @param color Color8Bit to convert
     * @return long[3] for the rgb value
     */
    public long[] convertColor8Bit(Color8Bit color) {
        return new long[]{(color.red/4), (color.green/4), (color.blue/4)};
    }

    /**
     * Changes the color of the whole LED board based on the 8x8 rgbTable array in the class
     * @throws IllegalArgumentException if anything in the rgbTable array is invalid
     */
    public void defaultLEDs() {
        if (rgbTable.length != 8) {
            throw new IllegalArgumentException(rgbTable.length + " is an invalid rgbTable length");
        }
        for (int i=0; i < rgbTable.length; i++) {
            if (rgbTable[i].length != 8) {
                throw new IllegalArgumentException(rgbTable[i].length + " is an invalid rgbTable length");
            }
            for (int j=0; j < rgbTable[i].length; j++) {
                for (long l : rgbTable[i][j]) {
                    if (l > 63 || l < 0) {
                        throw new IllegalArgumentException(i + " is an invalid rgb input, must be within 0-63");
                    }
                }
                launch.getSubTable(Integer.toString(i)).putValue(Integer.toString(j), NetworkTableValue.makeIntegerArray(rgbTable[i][j]));
            }
        }
    }

}
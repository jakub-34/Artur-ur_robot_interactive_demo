#!/usr/bin/env python3

import sys
from robot_control import put_pose, start
from poses import red_setup_pose, green_setup_pose, blue_setup_pose, standby_pose



def main():
    # Start the robot if needed
    if len(sys.argv) > 1 and sys.argv[1] == "-s":
        start()

    print("Setting up cubes")
    put_pose(standby_pose)
    
    # Red cube
    # put_pose...
    print("Place RED cube here")
    put_pose(red_setup_pose)
    input("Press Enter to continue...")

    # Green cube
    # put_pose...
    print("Place GREEN cube here")
    put_pose(green_setup_pose)
    input("Press Enter to continue...")

    # Blue cube
    # put_pose...
    print("Place BLUE cube here")
    put_pose(blue_setup_pose)
    input("Press Enter to continue...")

    put_pose(standby_pose)


if __name__ == "__main__":
    main()
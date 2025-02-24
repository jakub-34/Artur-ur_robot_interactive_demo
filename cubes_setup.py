#!/usr/bin/env python3

import sys
from robot_control import put_pose, start
from poses import red_setup_pose, green_setup_pose, blue_setup_pose, standby_pose


# Print help message
def print_help():
    print("Usage: ./cubes_setup.py -a <IP:PORT> [-s] [-h]")
    print("  -a <IP:PORT>  Specify the server IP address and port (required)")
    print("  -s            Start the robot (optional)")
    print("  -h            Show this help message and exit")
    sys.exit(0)


def main():
    # Parse arguments
    if "-h" in sys.argv:
        print_help()
    
    if "-a" not in sys.argv:
        print("Error: Missing required argument -a")
        print_help()
    
    try:
        a_index = sys.argv.index("-a")
        server_ip = sys.argv[a_index + 1]
    except (ValueError, IndexError):
        print("Error: Missing value for -a")
        print_help()
    
    # Check if -s is provided
    if "-s" in sys.argv:
        start(server_ip)

    print("Setting up cubes")
    put_pose(server_ip, standby_pose)
    
    # Red cube
    # put_pose...
    print("Place RED cube here")
    put_pose(server_ip, red_setup_pose)
    input("Press Enter to continue...")

    # Green cube
    # put_pose...
    print("Place GREEN cube here")
    put_pose(server_ip, green_setup_pose)
    input("Press Enter to continue...")

    # Blue cube
    # put_pose...
    print("Place BLUE cube here")
    put_pose(server_ip, blue_setup_pose)
    input("Press Enter to continue...")

    put_pose(server_ip, standby_pose)


if __name__ == "__main__":
    main()
#!/usr/bin/env python3

import sys
from robot_control import put_pose, start
import poses

# Print help message
def print_help() -> None:
    print("Usage: ./cubes_setup.py -a <IP:PORT> [-s] [-h]")
    print("  -a <IP:PORT>  Specify the server IP address and port (required)")
    print("  -t <table_height_cm>  Specify the table height in centimeters (required)")
    print("  -s            Start the robot (optional)")
    print("  -h            Show this help message and exit")
    sys.exit(0)


def main() -> None:
    # Parse arguments
    if "-h" in sys.argv:
        print_help()
    
    if "-a" not in sys.argv:
        print("Error: Missing required argument -a (server IP and port)")
        print_help()
    
    try:
        a_index = sys.argv.index("-a")
        server_ip = sys.argv[a_index + 1]
    except (ValueError, IndexError):
        print("Error: Missing value for -a")
        print_help()

    if "-t" not in sys.argv:
        print("Error: Missing required argument -t (table height in cm)")
        print_help()

    try:
        t_index = sys.argv.index("-t")
        table_height_cm = float(sys.argv[t_index + 1])
    except (ValueError, IndexError):
        print("Error: Invalid or missing value for -t (should be a number in cm)")
        print_help()
    
    # Check if -s is provided
    if "-s" in sys.argv:
        start(server_ip)


    poses.initialize_poses(table_height_cm)

    print("Setting up cubes")
    put_pose(server_ip, poses.standby_pose)
    
    # Red cube
    # put_pose...
    print("Place RED cube here")
    put_pose(server_ip, poses.red_setup_pose)
    input("Press Enter to continue...")

    # Green cube
    # put_pose...
    print("Place GREEN cube here")
    put_pose(server_ip, poses.green_setup_pose)
    input("Press Enter to continue...")

    # Blue cube
    # put_pose...
    print("Place BLUE cube here")
    put_pose(server_ip, poses.blue_setup_pose)
    input("Press Enter to continue...")

    put_pose(server_ip, poses.standby_pose)


if __name__ == "__main__":
    main()
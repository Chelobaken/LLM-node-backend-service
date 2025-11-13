import os

class RootSafety:
    def __init__(self):
        if os.geteuid() != 0:
            exit("You need to have root privileges to run this script.\nPlease try again, this time using 'sudo'. Exiting.")
    def check_valid_path(self):
        pass
rootsafety=RootSafety()
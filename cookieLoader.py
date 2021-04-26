import os
import sys
from colors import b_colors


def get_cookie():
    """
    Return cookie from file 'cookie.txt'.
    If file or cookie not exists - terminate program.
    """

    try:
        with open(sys.path[0] + "/cookie.txt") as f:
            if os.stat(sys.path[0] + "/cookie.txt").st_size == 0:
                print(
                    b_colors.WARNING + "File cookie.txt is empty! Please set you cookie in this file and try again." + b_colors.ENDC)
                sys.exit(os.EX_OSERR)
            else:
                cookie = f.read()
            return cookie
    except IOError:
        print(b_colors.FAIL + "File cookie.txt not exist! Creating..." + b_colors.ENDC)
        open(sys.path[0] + "/cookie.txt", "x")
        sys.exit(os.EX_OSERR)

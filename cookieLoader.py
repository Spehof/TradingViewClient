import os
import sys
from colors import b_colors


def get_cookie():
    try:
        with open("cookie.txt") as f:
            if os.stat("cookie.txt").st_size == 0:
                print(b_colors.WARNING + "File cookie.txt is empty! Please set you cookie in this file and try again." + b_colors.ENDC)
                sys.exit(os.EX_OSERR)
            else:
                cookie = f.read()
            return cookie
    except IOError:
        print(b_colors.FAIL + "File cookie.txt not exist! Creating..." + b_colors.ENDC)
        open("cookie.txt", "x")
        sys.exit(os.EX_OSERR)



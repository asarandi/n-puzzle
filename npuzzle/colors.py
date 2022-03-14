enabled = False


def color(c, s):
    tab = {
        "black2": "\033[1;30m",
        "red2": "\033[1;31m",
        "green2": "\033[1;32m",
        "yellow2": "\033[1;33m",
        "blue2": "\033[1;34m",
        "magenta2": "\033[1;35m",
        "cyan2": "\033[1;36m",
        "white2": "\033[1;37m",
        "eoc": "\033[0;00m",
        "black": "\033[0;30m",
        "red": "\033[0;31m",
        "green": "\033[0;32m",
        "yellow": "\033[0;33m",
        "blue": "\033[0;34m",
        "magenta": "\033[0;35m",
        "cyan": "\033[0;36m",
        "white": "\033[0;37m",
    }
    return f"{tab[c]}{s}{tab['eoc']}" if enabled else s

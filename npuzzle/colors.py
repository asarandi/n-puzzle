# straight outta ft_printf_colors.c

enabled = False

color_names = ['black2','red2','green2','yellow2','blue2','magenta2','cyan2','white2','eoc','black','red','green','yellow','blue','magenta','cyan','white']
color_codes = ['\033[1;30m','\033[1;31m','\033[1;32m','\033[1;33m','\033[1;34m','\033[1;35m','\033[1;36m','\033[1;37m','\033[0;00m','\033[0;30m','\033[0;31m','\033[0;32m','\033[0;33m','\033[0;34m','\033[0;35m','\033[0;36m','\033[0;37m']

def color(c, msg):
    if enabled and c in color_names:
        ci = color_names.index(c)
        eoci = color_names.index('eoc')
        return color_codes[ci] + msg + color_codes[eoci]
    else:
        return msg


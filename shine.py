import sys
import math
import re
def num(oper):
    try:
        x = float(oper)
    except TypeError:
        return False
    except ValueError:
        return False
    else:
    	return True
def panta(x0,y0,r,n):
    list1 = [x0 + r,y0,"moveto"]
    deg = 2 * pi / n
    g = 1
    while g < n:
        x1 = x0 + r * math.cos( deg * g)
        y1 = y0 + r * math.sin( deg * g)
        list1 += [x1,y1,"lineto"]
        g += 1
    list1 += [x0 + r,y0,"lineto"]
    return list1


def do(putin,zan):
    i = 0
    while i < len(putin):
        if putin[i] == "line":
            i += 2
            x0 = float(putin[i])
            i += 1
	    y0 = float(putin[i])
            i += 1
            x1 = float(putin[i])
            i += 1
            y1 = float(putin[i])
            i += 1
            zan += [x0,y0,"moveto"]
            zan += [x1,y1,"lineto"]
            zan += ["stroke"]
        elif putin[i] == "rect" or putin[i] == "filledrect":
            i += 2
            x0 = float(putin[i])
            i += 1
	    y0 = float(putin[i])
            i += 1
       	    w = float(putin[i])
            i += 1
            h = float(putin[i])
            i += 1
	    x1 = x0 + w
            y1 = y0
	    x2 = x0 + w
            y2 = y0 + h
	    x3 = x0
            y3 = y0 + h
            zan += [x0,y0,"moveto"]
            zan += [x1,y1,"lineto"]
            zan += [x2,y2,"lineto"]
            zan += [x3,y3,"lineto"]
            zan += [x0,y0,"lineto"]
            if putin[i - 6] == "filledrect":
                zan += ["fill"]
            else: zan += ["stroke"]
        elif putin[i] == "tri" or putin[i] == "filledtri":
            i += 2
            x0 = float(putin[i])
            i += 1
	    y0 = float(putin[i])
            i += 1
            r = float(putin[i])
            i += 1
            n = 3
	    list1 = panta(x0,y0,r,n)
            zan += list1
            if putin[i - 5] == "filledtri":
                zan += ["fill"]
            else: zan += ["stroke"]
        elif putin[i] == "square" or putin[i] == "filledsquare":
            i += 2
            x0 = float(putin[i])
            i += 1
	    y0 = float(putin[i])
            i += 1
            r = float(putin[i])
            i += 1
            n = 4
	    list1 = panta(x0,y0,r,n)
            zan += list1
            if putin[i - 5] == "filledsquare":
                zan += ["fill"]
            else: zan += ["stroke"]
        elif putin[i] == "penta" or putin[i] == "filledpenta":
            i += 2
            x0 = float(putin[i])
            i += 1
	    y0 = float(putin[i])
            i += 1
            r = float(putin[i])
            i += 1
            n = 5
	    list1 = panta(x0,y0,r,n)
            zan += list1
            if putin[i - 5] == "filledpenta":
                zan += ["fill"]
            else: zan += ["stroke"]
        elif putin[i] == "hexa" or putin[i] == "filledhexa":
            i += 2
            x0 = float(putin[i])
            i += 1
	    y0 = float(putin[i])
            i += 1
            r = float(putin[i])
            i += 1
            n = 6
	    list1 = panta(x0,y0,r,n)
            zan += list1
            if putin[i - 5] == "filledhexa":
                zan += ["fill"]
            else: zan += ["stroke"]
        elif putin[i] == "ngon" or putin[i] == "filledngon":
            i += 2
            x0 = float(putin[i])
            i += 1
	    y0 = float(putin[i])
            i += 1
            r = float(putin[i])
            i += 1
            n = float(putin[i])
            i += 1
	    list1 = panta(x0,y0,r,n)
            zan += list1
            if putin[i - 6] == "filledngon":
                zan += ["fill"]
            else: zan += ["stroke"]
        elif putin[i] == "sector" or putin[i] == "filledsector":
            i += 2
            x0 = float(putin[i])
            i += 1
            y0 = float(putin[i])
            i += 1
            r = float(putin[i])
            i += 1
            b = float(putin[i])
            i += 1
            e = float(putin[i])
            i += 1
            while b < 0:
                b += 360
            while e < 0:
                e += 360
            while b >= 360:
                b -= 360
            while e >= 360:
                e -= 360
            zan += [x0,y0,"moveto"]
            zan += [x1,y1,"lineto"]
            zan += [x0,y0,r,b,e,"arc"]
            zan += [x0,y0,"lineto"]
            if putin[i - 7] == "filledsector":
                zan += ["fill"]
            else: zan += ["stroke"]
	elif putin[i] == ")":
	    i += 1


global zan
zan = []
global dict
dict = {}
global pi
pi = 3.1415926
putin1 = sys.stdin.read()
putin1 = putin1.replace(',',' ')
putin1 = putin1.replace('(',' ( ')
putin1 = putin1.replace(')',' ) ')
putin2 = ' '.join(putin1.split())
putin3 = re.split(" |\t|\n|\r|",putin2)
putin = []
for i in putin3:
    if i != " " and i != "" and i != None:
        putin.append(i)
do(putin,zan)
sys.stdout.write("%!PS-Adobe-3.0 EPSF-3.0\r")
sys.stdout.write("%%BoundingBox: 0 0 1239 1752\r")
for sb in zan:
	if (num(sb)):
		sys.stdout.write( str(sb) + " ")
	else:
		sys.stdout.write( str(sb) + "\n")

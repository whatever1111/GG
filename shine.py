import sys
import math
import re

def profix(i,putin):
    	judg = 0
	res = 0
	sb = putin[i]
	if (sb == "("):
		dou = value(i,putin)
		sb = float(dou[0])
		i = dou[1]
		judg = 1
	if (sb == "cos"):
		i += 1
		dou = value(i,putin)
		a = float(dou[0])
		i = dou[1]
		res = float(math.cos(a*pi / 180))
		judg = 2
	elif (sb == "sin"):
		i += 1
		dou = value(i,putin)
		a = float(dou[0])
		i = dou[1]
		res = float(math.sin(a*pi / 180))
		judg = 2
	if judg == 1:
		a = sb
	else:
		dou = value(i,putin)
		a = float(dou[0])
		i = dou[1]
	if judg == 2:
		oper = "wocao"
	else:
		i += 1
		oper = putin[i]
		i += 1
	if (oper == "+"): 
		dou = value(i,putin)
		b = float(dou[0])
		i = dou[1]
		res = a + b		
	elif (oper == "-"):
		dou = value(i,putin)
		b = float(dou[0])
		i = dou[1]
		res = a - b
	elif (oper == "*"):
		dou = value(i,putin)
		b = float(dou[0])
		i = dou[1]
		res = a * b
	elif (oper == "/"):
		dou = value(i,putin)
		b = float(dou[0])
		i = dou[1]
		res = a / b
	elif ( num(oper) ):

		res = float(oper)
	judg = 0
	i += 1
	dou = [res,i]
	return dou


def num(oper):
    try:
        x = float(oper)
    except TypeError:
        return False
    except ValueError:
        return False
    else:
    	return True
def value(i,putin):
    oper = putin[i]
    res = 0
    if (oper == "("):
        i += 1
        dou = profix(i,putin)
	res = dou[0]
	i = dou[1]
	dou = [res,i]
	return dou
    elif (num(oper)):  
        res = float(oper)
    elif dict.has_key(oper):
        res = dict[oper]
    dou = [res,i]
    return dou

def panta(x0,y0,r,n,xp,yp,degp,sp):
    done = deal (x0,y0,xp,yp,degp,sp)
    x0 = float(done[0])
    y0 = float(done[1])
    r = r * sp
    list1 = [x0 + r,y0,"moveto"]
    deg = 2 * pi / n
    g = 1
    while g < n:
        x1 = x0 + r * math.cos( deg * g + degp)
        y1 = y0 + r * math.sin( deg * g + degp)
        list1 += [x1,y1,"lineto"]
        g += 1
    list1 += [x0 + r,y0,"lineto"]
    return list1

def deal(x,y,xp,yp,degp,sp):
    x = (x + xp) * sp
    y = (y + yp) * sp
    len1 = math.sqrt(x ** 2 + y ** 2)
    if len1 == 0:
	   done = [0 , 0]
	   return done
    else: deg = math.acos(y / len1 )
    if degp == 0:
	   done = [x , y]
	   return done
    else:
    	x = len1 * math.cos(deg + degp)*sp
   	y = len1 * math.sin(deg + degp)*sp
        done = [x , y]  
    	return done

def do(i,xp,yp,degp,sp,putin,zan):
    while i < len(putin):
        if putin[i] == "(":
	    i += 1
            i = do(i,xp,yp,degp,sp,putin,zan)
        if putin[i] == "line":
            i += 2
            dou = value(i,putin)
            x0 = float(dou[0])
            i = dou[1]
            i += 1
            dou = value(i,putin)
            y0 = float(dou[0])
            i = dou[1]
            i += 1
            dou = value(i,putin)
            x1 = float(dou[0])
            i = dou[1]
            i += 1
            dou = value(i,putin)
            y1 = float(dou[0])
            i = dou[1]
            i += 1
            done = deal (x0,y0,xp,yp,degp,sp)
            x0 = float(done[0])
            y0 = float(done[1])
            done = deal (x1,y1,xp,yp,degp,sp)
            x1 = float(done[0])
            y1 = float(done[1])
            zan += [x0,y0,"moveto"]
            zan += [x1,y1,"lineto"]
            zan += ["stroke"]
        elif putin[i] == "rect" or putin[i] == "filledrect":
            i += 2
            dou = value(i,putin)
            x0 = float(dou[0])
            i = dou[1]
            i += 1
            dou = value(i,putin)
            y0 = float(dou[0])
            i = dou[1]
            i += 1
            dou = value(i,putin)
            w = float(dou[0])
            i = dou[1]
            i += 1
            dou = value(i,putin)
            h = float(dou[0])
            i = dou[1]
            i += 1
            x1 = x0 + w
            y1 = y0
            x2 = x0 + w
            y2 = y0 + h
            x3 = x0
            y3 = y0 + h
            done = deal (x0,y0,xp,yp,degp,sp)
            x0 = float(done[0])
            y0 = float(done[1])
            done = deal (x1,y1,xp,yp,degp,sp)
            x1 = float(done[0])
            y1 = float(done[1])
            done = deal (x2,y2,xp,yp,degp,sp)
            x2 = float(done[0])
            y2 = float(done[1])
            done = deal (x3,y3,xp,yp,degp,sp)
            x3 = float(done[0])
            y3 = float(done[1])
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
            dou = value(i,putin)
            x0 = float(dou[0])
            i = dou[1]
            i += 1
            dou = value(i,putin)
            y0 = float(dou[0])
            i = dou[1]
            i += 1
            dou = value(i,putin)
            r = float(dou[0])
            i = dou[1]
            i += 1
            n = 3
            list1 = panta(x0,y0,r,n,xp,yp,degp,sp)
            zan += list1
            if putin[i - 5] == "filledtri":
                zan += ["fill"]
            else: zan += ["stroke"]
        elif putin[i] == "square" or putin[i] == "filledsquare":
            i += 2
            dou = value(i,putin)
            x0 = float(dou[0])
            i = dou[1]
            i += 1
            dou = value(i,putin)
            y0 = float(dou[0])
            i = dou[1]
            i += 1
            dou = value(i,putin)
            r = float(dou[0])
            i = dou[1]
            i += 1
            n = 4
            list1 = panta(x0,y0,r,n,xp,yp,degp,sp)
            zan += list1
            if putin[i - 5] == "filledsquare":
                zan += ["fill"]
            else: zan += ["stroke"]
        elif putin[i] == "penta" or putin[i] == "filledpenta":
            i += 2
            dou = value(i,putin)
            x0 = float(dou[0])
            i = dou[1]
            i += 1
            dou = value(i,putin)
            y0 = float(dou[0])
            i = dou[1]
            i += 1
            dou = value(i,putin)
            r = float(dou[0]) 
            i = dou[1]
            i += 1
            n = 5
            list1 = panta(x0,y0,r,n,xp,yp,degp,sp)
            zan += list1
            if putin[i - 5] == "filledpenta":
                zan += ["fill"]
            else: zan += ["stroke"]
        elif putin[i] == "hexa" or putin[i] == "filledhexa":
            i += 2
            dou = value(i,putin)
            x0 = float(dou[0])
            i = dou[1]
            i += 1
            dou = value(i,putin)
            y0 = float(dou[0])
            i = dou[1]
            i += 1
            dou = value(i,putin)
            r = float(dou[0])
            i = dou[1]
            i += 1
            n = 6
            list1 = panta(x0,y0,r,n,xp,yp,degp,sp)
            zan += list1
            if putin[i - 5] == "filledhexa":
                zan += ["fill"]
            else: zan += ["stroke"]
        elif putin[i] == "ngon" or putin[i] == "filledngon":
            i += 2
            dou = value(i,putin)
            x0 = float(dou[0])
            i = dou[1]
            i += 1
            dou = value(i,putin)
            y0 = float(dou[0])
            i = dou[1]
            i += 1
            dou = value(i,putin)
            r = float(dou[0])
            i = dou[1]
            i += 1
            dou = value(i,putin)
            n = float(dou[0])
            i = dou[1]
            i += 1
            list1 = panta(x0,y0,r,n,xp,yp,degp,sp)
            zan += list1
            if putin[i - 6] == "filledngon":
                zan += ["fill"]
            else: zan += ["stroke"]
        elif putin[i] == "sector" or putin[i] == "filledsector":
            i += 2
            dou = value(i,putin)
            x0 = float(dou[0])
            i = dou[1]
            i += 1
            dou = value(i,putin)
            y0 = float(dou[0])

            i = dou[1]
            i += 1
            dou = value(i,putin)
            r = float(dou[0])
            i = dou[1]
            i += 1
            dou = value(i,putin)
            b = float(dou[0])
            i = dou[1]
            i += 1
            dou = value(i,putin)
            e = float(dou[0])
            i = dou[1]
            i += 1
            while b < 0:
                b += 360
            while e < 0:
                e += 360
            while b >= 360:
                b -= 360
            while e >= 360:
                e -= 360
            degb = 2 * pi * b /360
            dege = 2 * pi * e /360
            x1 = x0 + r * math.cos(degb)
            y1 = y0 + r * math.sin(degb)
            x2 = x0 + r * math.cos(dege)
            y2 = y0 + r * math.sin(dege)
            done = deal (x0,y0,xp,yp,degp,sp)
            x0 = float(done[0])
            y0 = float(done[1])
            done = deal (x1,y1,xp,yp,degp,sp)
            x1 = float(done[0])
            y1 = float(done[1])
            done = deal (x2,y2,xp,yp,degp,sp)
            x2 = float(done[0])
            y2 = float(done[1])  
            zan += [x0,y0,"moveto"]
            zan += [x1,y1,"lineto"]
            zan += [x0,y0,float(r * sp),float(b + degp),float(e + degp),"arc"]
            zan += [x0,y0,"lineto"]
            if putin[i - 7] == "filledsector":
                zan += ["fill"]
            else: zan += ["stroke"]
        elif putin[i] == "translate":
            i += 2
            xp = value(i + 1)
            yp = value(i + 2)
            i = do(i,xp,yp,degp,sp,putin,zan)
        elif putin[i] == "rotate":
            i += 2
            degp = value(i + 1)
            degp = 2 * pi * degp /360
            i = do(i,xp,yp,degp,sp,putin,zan)
        elif putin[i] == "translate":
            i += 2
            sp = value(i + 1)
            i = do(i,xp,yp,degp,sp,putin,zan)


        elif putin[i] == "color":
            i += 2
            r = value(i,putin)
            i += 1
            g = value(i,putin)
            i += 1
            b = value(i,putin)
            i += 1
            zan += [r,g,b,"setrgbcolor"]
        elif putin[i] == "linewith":
            i += 1
            w = value(i,putin)
            i += 1
            zan += [w,"setlinewidth"]
        elif putin[i] == ")":
            i += 1
            return i

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
n = len(putin)
i = 0
while i < n:

    i = do(i,0,0,0,1,putin,zan)
sys.stdout.write("%!PS-Adobe-3.0 EPSF-3.0\r")
sys.stdout.write("%%BoundingBox: 0 0 1239 1752\r")
for sb in zan:
   	if (num(sb)):
        	sys.stdout.write( str(sb) + " ")
	else:
		sys.stdout.write( str(sb) + "\n")

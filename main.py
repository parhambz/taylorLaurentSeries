import numpy.lib.polynomial as P
from sympy import *
import math


def getQ():
    # this function gets the numberator Coefficients
    res = []
    n = int(input("numberator degree +1 :"))
    for i in range(0, n):
        re = int(input("enter real part for z**" + str(n - i - 1) + ":"))
        im = int(input("enter imaginary part for z**" + str(n - i - 1) + ":"))
        res = res + [complex(re, im)]
    resault = P.poly1d(res)
    return resault


def polyFromRoot(xs):
    # this function creates the polynomial from roots
    res = P.poly1d([complex(1, 0)])
    for i in xs:
        res = res * P.poly1d([1, -i])
    return res


def getD():
    # this function gets the Denominator roots
    res = []
    n = int(input("number of roots in Denominator :"))
    for i in range(0, n):
        re = int(input("enter real part for root " + str(i + 1) + " :"))
        im = int(input("enter imaginary part for root " + str(i + 1) + " :"))
        res = res + [complex(re, im)]
    return res


def simplize(numberator, denominator, roots):
    # simplizes the numberator and Denominator
    counter = 0
    for i in roots:
        if P.polyval(numberator, i) == 0:
            numberator = P.polydiv(numberator, polyFromRoot([i]))
            numberator = numberator[0]
            denominator = P.polydiv(denominator, polyFromRoot([i]))
            denominator = denominator[0]
            roots = roots[:counter] + roots[counter + 1:]
        counter += 1
    return [numberator, denominator, roots]


def removeZero(denominator, roots):
    # deletes (z-0) from Denominator and counts them
    global zeroCount
    counter = 0
    for i in roots:
        if i == complex(0, 0):
            denominator = P.polydiv(denominator, P.poly1d([complex(1, 0), 0]))
            denominator = denominator[0]
            roots = roots[:counter] + roots[counter + 1:]
            zeroCount += 1
        counter += 1
    return [denominator, roots]


def seprate(numberator, roots):
    # seprates a fraction
    tempRes = []
    for i in roots:
        temp = P.poly1d([complex(1, 0)])
        for j in roots:
            if not i == j:
                temp = temp * P.poly1d([complex(1, 0), -j])
        tempRes += [P.polyval(numberator, i) / P.polyval(temp, i)]
    res = []
    for i in range(0, len(tempRes)):
        s = tempRes[i]
        m = P.poly1d([complex(1, 0), -roots[i]])
        k = [s, roots[i]]
        res += [k]
    return res


def taylor(a, root, n):
    # taylor series for a/(z-root)
    res = [[0, 1] for i in range(n)]
    for i in range(0, len(res)):
        for j in range(0, i):
            res[i][0] += 1
            res[i][1] = res[i][1] / root
    for i in range(0, len(res)):
        res[i][1] = res[i][1] * a / root * (-1)
    return res


def laurent(a, root, n):
    # laurent series for a/(z-root)
    res = [[0, 1] for i in range(n)]
    for i in range(0, len(res)):
        for j in range(0, i):
            res[i][0] += -1
            res[i][1] *= root
        res[i][0] += -1
        res[i][1] *= a
    return res


def sum(xs, ys):
    # sums 2 series xs=[[power,Coefficient],[p2,c2]]
    if len(xs) < len(ys):
        xs, ys = ys, xs
    for i in range(0, len(xs)):
        for j in range(0, len(ys)):
            if xs[i][0] == ys[j][0]:
                xs[i][1] += ys[j][1]
                ys[j][1] = 0
    for j in range(0, len(ys)):
        if not ys[j][1] == 0:
            xs += [ys[j]]
    return xs


def mul(xs, ys):
    # multiplys 2 series xs=[[power,Coefficient],[p2,c2]]
    for i in range(0, len(xs)):
        xs[i][0] += ys[0]
        xs[i][1] *= ys[1]
    return xs


def poly1dToArr(p):
    # creates xs=[[power,Coefficient],[p2,c2]] from polynomial
    ks = p.c
    res = []
    for i in range(0, len(ks)):
        power = len(ks) - i - 1
        res += [[power, ks[i]]]
    return res


def giveR(i):
    # gets a complex number and return r
    r = i.real * i.real + i.imag * i.imag
    r = r ** (1 / 2)
    return r


def write(root, seprated, zeroCount, quotient, n):
    # write sum of taylor/laurent series for r<giveR(root)
    r = giveR(root)
    res = []
    for i in seprated:
        if giveR(i[1]) < r:
            res = sum(res, laurent(i[0], i[1], n))
        else:
            res = sum(res, taylor(i[0], i[1], n))
    res = sum(res, poly1dToArr(quotient))
    res = mul(res, [-zeroCount, 1])
    return res


def seriesToStr(xs):
    # creates readable series from arr
    z = symbols("Z")
    res = 0
    for i in xs:
        res += z ** i[0] * i[1]
    return res


def seriesSortHelp(val):
    return val[0]


def deffR(seprated, zeroCount, quotient, roots, n):
    # for defferent r writes defferent series
    for i in range(0, len(roots)):
        roots[i] = abs(roots[i])
    roots.sort()
    roots = roots + [math.inf]
    for i in range(0, len(roots)):
        series = write(roots[i], seprated, zeroCount, quotient, n)
        series.sort(key=seriesSortHelp, reverse=False)
        print("\nfor r<", roots[i], ":\n", seriesToStr(series))


n = int(input("enter number of taylor poly :"))

zeroCount = 0
numberator = getQ()
roots = getD()
denominator = polyFromRoot(roots)

simpleRes = simplize(numberator, denominator, roots)
numberator = simpleRes[0]
denominator = simpleRes[1]
roots = simpleRes[2]

simpleRes = removeZero(denominator, roots)
denominator = simpleRes[0]
roots = simpleRes[1]

divRes = P.polydiv(numberator, denominator)
quotient = divRes[0]
numberator = divRes[1]

seprated = seprate(numberator, roots)
deffR(seprated, zeroCount, quotient, roots, n)

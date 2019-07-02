import numpy.lib.polynomial as P
import math
def getQ():
    res=[]
    n=int(input("soorat"))
    for i in range(0,n):
        re=int(input("enter real part"+str(i)))
        im=int(input("enter imaginary part"+str(i)))
        res=res+[complex(re,im)]
    resault=P.poly1d(res)
    return resault
def polyFromRoot(xs):
    res=P.poly1d([complex(1,0)])
    for i in xs:
        res=res*P.poly1d([1,-i])
    return res
def getD():
    res=[]
    n=int(input("makhraj"))
    for i in range(0,n):
        re=int(input("enter real part"+str(i)))
        im=int(input("enter imaginary part"+str(i)))
        res=res+[complex(re,im)]
    return res
def simplize(soorat,makhraj,roots):
    counter=0
    for i in roots:
        if P.polyval(soorat,i)==0:
            soorat=P.polydiv(soorat,polyFromRoot([i]))
            soorat=soorat[0]
            makhraj = P.polydiv(makhraj, polyFromRoot([i]))
            makhraj=makhraj[0]
            roots=roots[:counter]+roots[counter+1:]
        counter+=1
    return [soorat,makhraj,roots]
def removeZero(makhraj,roots):
    global zeroCount
    counter = 0
    for i in roots:
        if i==complex(0,0):
            makhraj = P.polydiv(makhraj, P.poly1d([complex(1, 0), 0]))
            makhraj=makhraj[0]
            roots = roots[:counter] + roots[counter + 1:]
            zeroCount+=1
        counter+=1
    return [makhraj,roots]
def seprate(soorat,roots):
    tempRes=[]
    for i in roots:
        temp=P.poly1d([complex(1,0)])
        for j in roots:
            if not i==j:
                temp=temp*P.poly1d([complex(1,0),-j])
        tempRes+=[P.polyval(soorat,i)/P.polyval(temp,i)]
    res=[]
    for i in range(0,len(tempRes)):
        s=tempRes[i]
        m=P.poly1d([complex(1,0),-roots[i]])
        k=[s,roots[i]]
        res+=[k]
    return res
def taylor(a,root,n):
    res=[[0,1] for i in range (n)]
    for i in range(0,len(res)):
        for j in range(0,i):
            res[i][0]+=1
            res[i][1]=res[i][1]/root
    for i in range(0,len(res)):
        res[i][1]=res[i][1]*a/root*(-1)
    return res
def laurent(a,root,n):
    res = [[0,1] for i in range(n)]
    for i in range(0, len(res)):
        for j in range(0, i):
            res[i][0]+=-1
            res[i][1]*=root
        res[i][0]+=-1
        res[i][1]*=a
    return res
def sum(xs,ys):
    if len(xs)<len(ys):
        xs,ys=ys,xs
    for i in range(0,len(xs)):
        for j in range(0,len(ys)):
            if xs[i][0]==ys[j][0]:
                xs[i][1]+=ys[j][1]
                ys[j][1]=0
    for j in range(0, len(ys)):
        if not ys[j][1] == 0:
            xs+=[ys[j]]
    return xs
def mul(xs,ys):
    for i in range(0,len(xs)):
        xs[i][0]+=ys[0]
        xs[i][1]*=ys[1]
    return xs
def poly1dToArr(p):
    ks=p.c
    res=[]
    for i in range(0,len(ks)):
        power=len(ks)-i-1
        res+=[[power,ks[i]]]
    return res
def giveR(i):
    r = i.real * i.real + i.imag * i.imag
    r = r ** (1 / 2)
    return r
def write(root,seprated,zeroCount,kharejghesmat,n):
    r=giveR(root)
    res=[]
    for i in seprated:
        if giveR(i[1])<r:
            res = sum(res, laurent(i[0], i[1], n))
        else:
            res = sum(res,taylor (i[0], i[1], n))
    res=sum(res,poly1dToArr(kharejghesmat))
    res=mul(res,[-zeroCount,1])
    return res
def deffR(seprated,zeroCount,kharejghesmat,roots,n):
    for i in range(0,len(roots)):
        roots[i]=abs(roots[i])
    roots.sort()
    roots=roots+[math.inf]
    for i in range(0,len(roots)):
        series=write(roots[i],seprated,zeroCount,kharejghesmat,n)
        print("for r<",roots[i],":\n",series)
n=5

zeroCount=0
soorat=getQ()
roots=getD()
makhraj=polyFromRoot(roots)

simpleRes=simplize(soorat,makhraj,roots)
soorat=simpleRes[0]
makhraj=simpleRes[1]
roots=simpleRes[2]


simpleRes=removeZero(makhraj,roots)
makhraj=simpleRes[0]
roots=simpleRes[1]


divRes=P.polydiv(soorat,makhraj)
kharejghesmat=divRes[0]
soorat=divRes[1]


seprated=seprate(soorat,roots)
deffR(seprated,zeroCount,kharejghesmat,roots,n)

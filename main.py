import numpy.lib.polynomial as P
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
            zeroCount+=-1
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
        s=P.poly1d([tempRes[i]])
        m=P.poly1d([complex(1,0),-roots[i]])
        k=s/m
        res+=[k]
    return res
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

print("soorat : \n",soorat)
print("makhraj :\n",makhraj)
print("kharej ghesmat :\n",kharejghesmat)
print("roots :\n",roots)
seprated=seprate(soorat,roots)
for i in seprated:
    print(i)


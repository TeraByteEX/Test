from PIL import Image
import os
import math
import numpy as np
import cv2
#0:left,1:up,2:right,3:down

size = 58
num = 240
rn = range(0,num)

pos = [[0]]

keys = []
images = []
datas = []

print("欢迎使用拼图游戏，该程序用于以游戏的形式进行拼图。虽然效率不高，但起码能用\n规则：")
print("1.使用左键点击一块拼图，可以在该块拼图周围的空白处拼上拼图")
print("2.使用右键点击一块拼图，可以将该块拼图取下")
print("3.按esc退出")
print("每次操作后，都会保存一次（保存在pos.txt中），在程序运行时则会自动读取存档")
print("接下来，请输入拼图所在的路径，或者编辑源码设定path：")
#path = "flag\\"
path = input()

for i in os.listdir(path):
    keys.append(i);
    images.append(Image.open(path + i))
    datas.append(images[-1].load())

def cut(arr,dct) :
    res = []
    for i in range(size):
        if dct==0 :
            res.append(arr[0,i-1])
        if dct==1 :
            res.append(arr[i-1,0])
        if dct==2 :
            res.append(arr[size-1,i-1])
        if dct==3 :
            res.append(arr[i-1,size-1])
    return res

def same(e1,e2) :
    res = 0
    for i,j in zip(e1,e2) :
        res += math.sqrt(math.pow(i[2]-j[2],2))
    return res

def find(i,d) :
    e1 = cut(datas[i],d)
    ms = 1e9
    mj = -1
        
    surplus = [i for i in rn]
        
    for x in range(0,len(pos)) :
        for y in range(0,len(pos[x])) :
            if pos[x][y]!=-1 :
                surplus.remove(pos[x][y])
    for j in surplus :
        e2 = cut(datas[j],(d+2)%4)
        sv = same(e1,e2)
        if sv < ms :
            mj = j
            ms = sv
    return mj

def change(npos) :
    pos.clear()
    for i in npos :
        pos.append(i)


def save() :
    total().save('total.png')
    print(pos,file=open("pos.txt","w"))

def load() :
    try :
        npos = eval(open("pos.txt").read())
        change(npos)
    except :
        print("no saved data")
        save()

def reshape() :
    x1=10000
    y1=10000
    x2=-1
    y2=-1
    for x in range(0,len(pos)) :
        for y in range(0,len(pos[x])) :
            if pos[x][y]!=-1 :
                if x<x1 :
                    x1 = x
                if x>x2 :
                    x2 = x
                if y<y1 :
                    y1 = y
                if y>y2 :
                    y2 = y
    #print(x1,x2,y1,y2)
    npos = [[-1 for i in range(y1-1,y2+2)] for j in range(x1-1,x2+2)]
    #print(len(npos),len(npos[0]),len(pos),len(pos[0]))
    for i in  range(x1,x2+1):
        for j in range(y1,y2+1) :
            npos[i+1-x1][j+1-y1] = pos[i][j]
    change(npos)

def total() :
    reshape()
    total = Image.new("RGBA",(size*len(pos),size*len(pos[0])))
    for x in range(0,len(pos)) :
        for y in range(0,len(pos[x])) :
            if pos[x][y]!=-1 :
                total.paste(images[pos[x][y]],(x*size,y*size))
    #total.show()
    return total
    

def com(x,y,d,re = False) :
    nx=x
    ny=y
    if d==0 :
        nx-=1
    if d==1 :
        ny-=1
    if d==2 :
        nx+=1
    if d==3 :
        ny+=1
    if pos[nx][ny]!=-1 and not re :
        return
    pos[nx][ny] = find(pos[x][y],d)
    #print(f"find({nx},{ny}):",pos[nx][ny])

def combine(x,y,re = False) :
    com(x,y,0,re)
    com(x,y,1,re)
    com(x,y,2,re)
    com(x,y,3,re)
    reshape()
###################################################



#鼠标回调函数
def down(event,x,y,flags,param):
    x=int(x/size)
    y=int(y/size)
    if event==cv2.EVENT_LBUTTONDOWN :
        combine(x,y)
        save()

    elif event==cv2.EVENT_RBUTTONDOWN :
        pos[x][y]=-1
        save()

cv2.namedWindow('image')
cv2.setMouseCallback('image',down)

load()

while(1):
    cv2.imshow('image',cv2.imread("total.png"))
    if cv2.waitKey(20)&0xFF==27:
        break

cv2.destroyAllWindows()
save()



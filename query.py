import requests
import random
from urllib.request import urlretrieve
import os
from bs4 import BeautifulSoup
from PIL import Image as PI
import pyocr
import pyocr.builders
import pytesseract
import time

tools = pyocr.get_available_tools()
tool=tools[0]

def two_value(name):    
     # 打开文件夹中的图片  
    image=PI.open('png/'+name)  
    # 灰度图  
    lim=image.convert('L')  
    # 灰度阈值设为165，低于这个值的点全部填白色
    dataFormal=lim.load()
    sum=0
    count=0
    for i in range(0,180):
        for j in range(0,100):
            sum+=dataFormal[i,j]
            count+=1
    threshold=sum/count-40
    table=[] 
    for j in range(256):  
        if j<threshold:  
            table.append(0)  
        else:  
            table.append(1) 
    bim=lim.point(table,'1')
    data=bim.load()
    times=3
    for time in range(0,times):
        tochange=[]
        for i in range(1,179):
            for j in range(1,99):
                if data[i,j]==1:
                    if data[i-1,j]==0:
                        tochange.append((i-1,j))
                    if data[i+1,j]==0:
                        tochange.append((i+1,j))
                    if data[i,j-1]==0:
                        tochange.append((i,j-1))
                    if data[i,j+1]==0:
                        tochange.append((i,j+1))
        for (i,j) in tochange:
            data[i,j]=1
    times=3
    for time in range(0,times):
        tochange=[]
        for i in range(1,179):
            for j in range(1,99):
                if data[i,j]==0:
                    if data[i-1,j]==1:
                        tochange.append((i-1,j))
                    if data[i+1,j]==1:
                        tochange.append((i+1,j))
                    if data[i,j-1]==1:
                        tochange.append((i,j-1))
                    if data[i,j+1]==1:
                        tochange.append((i,j+1))
        for (i,j) in tochange:
            data[i,j]=0
    bim.save('jpg/'+name.replace('.png','.jpg'))
    image=PI.open('jpg/'+name.replace('.png','.jpg'),'r')
    txt = tool.image_to_string(
        image,
        lang='eng',
        builder=pyocr.builders.TextBuilder()
    )
    txt=txt.replace(' ','').replace('S','5').replace('O','0')
    return txt

headers={
    'host': 'cache.neea.edu.cn',
    'connection': 'keep-alive',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    'accept': '*/*',
    'referer': 'http://cet.neea.edu.cn/cet',
    'accept-encoding': 'gzip, deflate',
    'accept-language': 'zh-CN,zh;q=0.9'
}

#这一部分修改成个人信息即可,upper，lower为座位号上下限，roomId为初始考场号，seatId为初始座位号，username为姓名，areaId为考区号
lower=1
upper=30
roomId=33
seatId=5
username='XXX'
areaId='4304211811'
if len(str(roomId))<3:
    roomId_str='0'+str(roomId)
else:
    roomId_str=str(roomId)
'''tstring=''
for i in range(16):
    tstring+=str(random.randint(0,9))'''
if not os.path.exists('png'):
    os.mkdir('png')
if not os.path.exists('jpg'):
    os.mkdir('jpg')
if not os.path.exists('record.txt'):
    file=open('record.txt','w',encoding='utf-8')
    file.close()
while True:
    try:
        chars='0123456789abcdefghijklmnopqrstuvwxyz'
        if len(str(roomId))==2:
            roomId_str='0'+str(roomId)
        elif len(str(roomId))==1:
            roomId_str='00'+str(roomId)
        else:
            roomId_str=str(roomId)
        tstring=''
        for i in range(16):
            tstring+=str(random.randint(0,9))
        print('当前考场号为'+roomId_str+'  当前座位号为'+str(seatId))
        if seatId<10:
            ik=areaId+roomId_str+'0'+str(seatId)
        else:
            ik=areaId+roomId_str+str(seatId)
        while True:
            tsting=str(random.random())
            url='http://cache.neea.edu.cn/Imgs.do?c=CET&ik='+ik+'&t=0.'+tstring
            r=requests.get(url,headers=headers)
            source_url=r.text.replace('result.imgs("','').replace('");','')
            name=source_url.split('/')[-1]
            urlretrieve(source_url,'png/'+name)
            v=two_value(name)
            if len(v)==4 and v[0] in chars and v[1] in chars and v[2] in chars and v[3] in chars:
                print(url)
                break
        query_url='http://cache.neea.edu.cn/cet/query'
        payload={
            'data':'CET'+str(int(areaId[-1])*2+2)+'_'+areaId[6:9]+'_DANGCI,'+ik+','+username,
            'v':str(v)
            }
        count=0
        while True:
            r2=requests.post(query_url,headers=headers,data=payload)
            bsObj=BeautifulSoup(r2.text,'html.parser')
            script=bsObj.findAll('script')[1].get_text().replace('parent.result.callback(','').replace(');','')
            if script=='''"{'error':'您查询的结果为空！'}"''':
                print('您查询的结果为空！')
                if seatId<upper:
                    seatId+=1
                else:
                    seatId=lower
                    roomId+=1
                break
            elif script=='''"{error:'抱歉，验证码错误！'}"''':
                count+=1
                #print('抱歉，验证码错误！请再次尝试！')
            else:
                print('似乎你的成绩查到了！')
                print(script)
                file=open('record.txt','a',encoding='utf-8')
                file.write(script+'\t'+str(roomId)+'\t'+str(seatId))
                file.close()
                break
            if count>=100:
                print('抱歉，验证码错误！请再次尝试！')
                break
    except Exception as e:
        print(e)
        print('出错了，稍等重试！')
        time.sleep(3)

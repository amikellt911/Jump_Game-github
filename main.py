#导入库
from machine import SPI,Pin,ADC,I2C
import utime
import st7789
import urandom
import math
import ds1307

#关键颜色
MapColor = st7789.BLACK
PieceColor = st7789.BLUE
PlatformColor = st7789.YELLOW

#记录与分数
score=0
record=0
count=0

#时钟的初始化
i2c = I2C(1, sda=Pin(0), scl=Pin(1), freq=400000)#构建I2C0，时钟频率100000（时钟屏幕根据具体传感器而定，一般使用100000或400000）
ds = ds1307.DS1307(i2c)
ds.set_time([2023,7,25,0,10,34,0])


#界面初始化
spi = SPI(0, baudrate=40000000, polarity=1, phase=0, bits=8, endia=0, sck=Pin(6), mosi=Pin(8))
display = st7789.ST7789(spi, 240, 240, reset=Pin(11,func=Pin.GPIO, dir=Pin.OUT), dc=Pin(7,func=Pin.GPIO, dir=Pin.OUT))
display.init()

#游戏初始界面
display.fill(st7789.color565(255,0,0))
utime.sleep_ms(90)
display.fill_rect(120, 120, 10, 10, st7789.YELLOW)
utime.sleep_ms(90)
display.fill(st7789.BLACK)
utime.sleep_ms(90)
display.draw_string(80,110,"JUMP",color=st7789.RED, bg=st7789.YELLOW, size=4)
utime.sleep_ms(90)
display.fill(st7789.BLACK)
display.draw_string(0,20,"Developer:",color=st7789.RED, bg=st7789.YELLOW, size=3)
display.draw_string(0,45,"amikellt911",color=st7789.RED, bg=st7789.YELLOW, size=3)
display.draw_string(0,110,"Mail:",color=st7789.RED, bg=st7789.YELLOW, size=4)
display.draw_string(0,140,"amikellt911",color=st7789.RED, bg=st7789.YELLOW, size=3)
display.draw_string(0,165,"@gmail.com",color=st7789.RED, bg=st7789.YELLOW, size=3)

utime.sleep(1)
display.fill(MapColor)

#关键函数
def DrawPlatform(pos,length):
    display.fill_rect((pos)*10,220,10,20,PlatformColor)
    display.fill_rect((pos-(length//2))*10-3,210,length*10,10,PlatformColor)
def DrawPiece(begin):
    display.fill_rect(begin*5-2,210,10,30,PlatformColor)
    display.fill_rect(begin*5-2,190,10,20,PieceColor)
def DrawNextPiece(nextpos):
    display.fill_rect(nextpos-2,190,10,20,PieceColor)
def DrawScore():
    display.draw_string(110,10,"Score = "+str(score),color=st7789.RED, bg=st7789.YELLOW, size=2)
    display.draw_string(100,30,"Record = "+str(record),color=st7789.RED, bg=st7789.YELLOW, size=2)

#游戏主体循环
while True:
    #最后press to continue消去
    display.fill(st7789.BLACK)

    #关键物的初始化随机
    beginpos=urandom.randint(2,12)#棋子位置
    PlatformPos=urandom.randint(3+beginpos//2,22)#平台底座位置
    if PlatformPos>15:#平台长度与棋子初始位置有关，不然会板子与棋子位置重合。
        PlatformLength=urandom.randint(3,2*(24-PlatformPos))
    else :
        PlatformLength=urandom.randint(3,2*(PlatformPos-beginpos//2))
    #游戏界面初始化
    while (PlatformPos-PlatformLength//2)*10-3<=beginpos*5-2:
        PlatformPos+=1
    while ((PlatformPos-PlatformLength//2)*10-3+PlatformLength*10)>=239:
        PlatformLength-=1
    DrawPiece(beginpos)
    DrawPlatform(PlatformPos,PlatformLength)
    DrawScore()#不止有score,还有record

    
    #距离初始化
    #后面变为函数传达压力转变距离

    utime.sleep_ms(90)
    display.fill(st7789.BLACK)
    display.draw_string(0,80,"Hold and",color=st7789.RED, bg=st7789.YELLOW, size=3)
    display.draw_string(0,110,"Observe the Bar",color=st7789.RED, bg=st7789.YELLOW, size=3)
    utime.sleep(1)
    display.fill(st7789.BLACK)
    display.draw_string(0,120,"Release to Jump",color=st7789.RED, bg=st7789.YELLOW, size=3)
    utime.sleep_ms(99)
    display.fill(st7789.BLACK)
    display.rect(beginpos*5-2,120,240-beginpos*5,20,st7789.RED)
    DrawPiece(beginpos)
    DrawPlatform(PlatformPos,PlatformLength)
    press=0
    f=1
    x1=0
    

    
    while True:
        if f==1:
            display.draw_string(0,0,str(ds.get_time()),color=st7789.WHITE, bg=st7789.BLACK, size=1)
        elif f==2:
            display.draw_string(0,0,str(ds.get_time()),color=st7789.WHITE, bg=st7789.BLACK, size=1)
        elif f==3:
            display.draw_string(0,0,str(ds.get_time()),color=st7789.GREEN, bg=st7789.BLACK, size=1)
        elif f==4:
            display.draw_string(0,0,str(ds.get_time()),color=st7789.GREEN, bg=st7789.BLACK, size=1)
        elif f==5:
            display.draw_string(0,0,str(ds.get_time()),color=st7789.BLUE, bg=st7789.BLACK, size=1)
        elif f==6:
            display.draw_string(0,0,str(ds.get_time()),color=st7789.BLUE, bg=st7789.BLACK, size=1)
        elif f==7:
            display.draw_string(0,0,str(ds.get_time()),color=st7789.YELLOW, bg=st7789.BLACK, size=1)
        elif f==8:
            display.draw_string(0,0,str(ds.get_time()),color=st7789.YELLOW, bg=st7789.BLACK, size=1)
        elif f==9:
            display.draw_string(0,0,str(ds.get_time()),color=st7789.RED, bg=st7789.BLACK, size=1)
        elif f==10:
            display.draw_string(0,0,str(ds.get_time()),color=st7789.RED, bg=st7789.BLACK, size=1)
            break
        adc=ADC(Pin(13))
        adc.equ(ADC.EQU_MODEL_8)
        x=adc.read()
        utime.sleep(1)
        if x>1870:
            if f==1:
                continue       
        else:
            f+=1
            display.fill(st7789.BLACK)
            display.rect(beginpos*5-2,120,240-beginpos*5+2,20,st7789.RED)
            DrawPiece(beginpos)
            DrawPlatform(PlatformPos,PlatformLength)
            x//=50
            x1=36-x
            display.fill_rect(beginpos*5-2,120,x1*7,20,st7789.RED)

    utime.sleep_ms(90)
    #important
    press=x1//2
    print(press)
    display.fill(st7789.BLACK)
    #游戏界面初始化
    DrawPiece(beginpos)
    DrawPlatform(PlatformPos,PlatformLength)
    DrawScore()#不止有score,还有record

    #初始化棋子消失
    display.fill_rect(beginpos*5-2,190,10,10,st7789.BLACK)
    utime.sleep_ms(90)
    display.fill_rect(beginpos*5-2,200,10,10,st7789.BLACK)
    utime.sleep_ms(90)

    #跳跃数据
    r = press*7 # 半径
    x = beginpos*5+r-2 # 圆心x坐标
    y = 200 # 圆心y坐标  

    #跳跃过程动画化
    angles = math.radians(0)
    x0 = x - int(r * math.cos(angles))
    y0 = y - int(r * math.sin(angles))
    f2=False
    for angle in range(1,180):
        rangle = math.radians(angle)
        angles = math.radians(angle-1)
        x1 = x - int(r * math.cos(rangle))
        y1 = y - int(r * math.sin(rangle))
        x0 = x - int(r * math.cos(angles))
        y0 = y - int(r * math.sin(angles))
        if x1>229:
            f2=True
            break
        display.fill_rect(x1,y1,10,10,st7789.BLUE)
        utime.sleep_ms(10)
        display.fill_rect(x0,y0,10,10,st7789.BLACK)
    utime.sleep_ms(90)
    if f2:
        display.fill_rect(x1,y1,10,10,st7789.RED)    
    else:
        display.fill_rect(x1,y1,10,10,st7789.BLACK)    

        #跳跃到下一个位置的棋子初始化
        utime.sleep(1)
        DrawNextPiece(press*14+beginpos*5)
        utime.sleep_ms(90)

    x=(press*14+(beginpos)*5-2+press*14+(beginpos)*5-2+10)//2
    y=((PlatformPos)*10+10+(PlatformPos)*10-3)//2


    #如果跳跃成功，有什么情况
    if press*14+(beginpos)*5-2 >= (PlatformPos-int(PlatformLength/2))*10-6 and press*14+(beginpos)*5-2+10 <= PlatformLength*10+(PlatformPos-int(PlatformLength/2))*10+6:
        print("YES!")
        display.draw_string(0,80,"Congratulations",color=st7789.YELLOW, bg=st7789.RED, size=3)
        display.draw_string(40,125,"Next level",color=st7789.YELLOW, bg=st7789.RED, size=3)
        utime.sleep(1)
        utime.sleep_ms(90)
        display.fill(st7789.BLACK)
        fl=True
        if x>=y-3 and x<=y+3:
            count+=1
            score+=3
            fl=False
        else :
            count=0
            score+=1
        if count==5:
            score+=10
            count=0
        if fl:
            display.draw_string(45,115,"Score + 1",color=st7789.YELLOW, bg=st7789.RED, size=3)
        else:
            display.draw_string(45,115,"Score + 3",color=st7789.YELLOW, bg=st7789.RED, size=3)
        utime.sleep_ms(90)
        display.fill(st7789.BLACK)
        display.draw_string(55,115,"come on!",color=st7789.YELLOW, bg=st7789.RED, size=3)
        utime.sleep(1)
        display.fill(st7789.BLACK)
        

    #如果跳跃不成功，有什么情况
    else:
        print("NO!")
        display.draw_string(15,115,"Unfortunately",color=st7789.RED, bg=st7789.WHITE, size=3)
        utime.sleep(1)
        display.fill(st7789.BLACK)
        if record<score:
            record=score
            display.draw_string(35,100,"New Record",color=st7789.YELLOW, bg=st7789.RED, size=3)
            display.draw_string(35,125,str(record)+" !",color=st7789.YELLOW, bg=st7789.RED, size=3)
            utime.sleep(1)
        else:
            display.draw_string(25,100,"History",color=st7789.RED, bg=st7789.WHITE, size=3)
            display.draw_string(25,140,"Record="+str(record),color=st7789.RED, bg=st7789.WHITE, size=3)
            utime.sleep(1)
            display.fill(st7789.BLACK)
            display.draw_string(15,115,"Your Score="+str(score),color=st7789.RED, bg=st7789.WHITE, size=3)
            utime.sleep(1)
            utime.sleep_ms(90)
        utime.sleep(1)
        display.fill(st7789.BLACK)
        display.draw_string(45,120,"Try Again",color=st7789.RED, bg=st7789.CYAN, size=3)

        utime.sleep(1)
        display.fill(st7789.BLACK)
        display.draw_string(45,90,"Press to",color=st7789.RED, bg=st7789.CYAN, size=3)
        display.draw_string(55,125,"continue",color=st7789.RED, bg=st7789.CYAN, size=3)
        score=0
        while True:
            adc=ADC(Pin(13))
            adc.equ(ADC.EQU_MODEL_8)
            x=adc.read()
            if (x<1800):
                break
        


---
tags: ros
---
# op2 使用紀錄

## 連線

直接ssh，用網路線連接op2跟筆電，然後用putty，連線```192.168.123.1```，那個port號22別動，直接暗確定

![](https://i.imgur.com/MctNhSm.png)

## 框架

可以在```/robotis/Framework```之下去修改框架

![](https://i.imgur.com/mXAwZ59.png)
![](https://i.imgur.com/xAERqd5.png)

## 程式碼

在```/robotis/Linux/project```聽說裡面有程式碼


- customizing 訂製:
    - 動作創建/操作（通過roboplus或動作編輯器）調整（帶步行tunet的步行參數，帶偏移調諧器的機器人姿勢偏移）

- diagnosis 診斷：
    - dxl監視器（執行器和子控制器監視）
    - firmware installerb（子控制器和執行器firaware安裝程序）

## ros

注意：千萬不要安裝升級後的內核。升級內核可能會導致圖形驅動程序問題。

### 安裝
有關如何安裝ROS（Indigo Igloo）的信息，請參閱以下鏈接。
為了在Linux Mint上正確安裝ROS，sources.list必須如下修改設置。
```cmake
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu trusty main" > /etc/apt/sources.list.d/ros-latest.list'
```
如果不行在看[wiki](
http://wiki.ros.org/indigo/Installation/Ubuntu)

### ROSO包適用於ROBOTIS-OP2

正確安裝ROS後，應安裝相關軟件包以運行ROBOTIS-OP2。ROBOTIS-OP3的一些ROS軟件包可以按原樣使用，而其他軟件包則需要進行一些修改。
為ROBOTIS-OP2修改的軟件包已上載到不同的存儲庫中。
按照以下說明下載軟件包：

```cmake
$ cd ~/catkin_ws/src
$ git clone https://github.com/ROBOTIS-GIT/DynamixelSDK
$ git clone https://github.com/ROBOTIS-GIT/ROBOTIS-Framework
$ git clone https://github.com/ROBOTIS-GIT/ROBOTIS-Framework-msgs
$ git clone https://github.com/ROBOTIS-GIT/ROBOTIS-Math
$ git clone https://github.com/ROBOTIS-GIT/ROBOTIS-OP2
$ git clone https://github.com/ROBOTIS-GIT/ROBOTIS-OP2-Common
$ git clone https://github.com/ROBOTIS-GIT/ROBOTIS-OP3
$ git clone https://github.com/ROBOTIS-GIT/ROBOTIS-OP3-msgs
$ git clone https://github.com/ROBOTIS-GIT/ROBOTIS-OP3-Tools
```

### ROBOTIS-OP2存儲庫

1.cm_740_module：從ROBOTIS-OP3存儲庫移出。

2.op2_gui_demo：某些配置文件和啟動文件已被修改為在ROBOTIS-OP2上運行op3_gui_demo。

3.op2_kinematics_dynamics：根據ROBOTIS-OP2僅修改了一些值，例如op2_walking_module中使用的關節方向。

4.op2_manager：對運動模塊和ROBOTIS-OP2的配置文件進行了一些修改。與ROBOTIS-OP3中的OpenCR不同，ROBOTIS-OP2中的CM-740具有默認設置的Dynamixel Power OFF。因此，修改源代碼來處理這種差異。

5.op2_walking_module：ROBOTIS-OP2的修改代碼（聯合方向，平衡增益等）

### ROBOTIS-OP2-通用存儲庫

1.robotis_op2_description：ROBOTIS-OP2 URDF模型

2.robotis_op2_gazebo：ROBOTIS-OP2涼亭模擬

### 如何運行GUI程序

構建源代碼

```cmake
cd ~/catkin_ws
catkin_make
```
執行op2_manager

```cmake
 roslaunch op2_manager op2_manager.launch
```

當op2_manager啟動時，所有關節都是扭矩並首先進行站立運動，然後是遊戲坐姿運動。

將VNC查看器或監視器連接到ROBOTIS-OP2並執行GUI演示程序。

```cmake
roslaunch op2_gui_demo op2_demo.launch

```

### 如何使用GUI程序

基本操作測試與ROBOTIS-OP3相同，後者在OP3教程頁面中進行了描述：
[參考：](http://emanual.robotis.com/docs/en/platform/op3/tutorials/#description-2)

>Mode Control，Walking，Head Control，Motion標籤是可用的。
Demo，Online Walking標籤不可用。


## op2動作列表
### 模組

 |000.              |022.              |044.talk2         |066.            
 |--|--|--|-
 |001.init   起立蹲下      |023.d1    生右手        |045.talk2   廢話等級4       |067.             
 |002.ok    點頭        |024.d2  揮手          |046.talk2    廢話等級1      |068.             
 |003.no       搖頭     |025.d2 揮手            |047.talk2      廢話等級1    |069.             
 |004.hi    手頭起來點頭        |026.              |048.              |070.rPASS        
 |005.??     往右上看了一眼       |027.d3    揮手        |049.              |071.lPASS        
 |006.talk1   膜你說話姿勢      |028.              |050.              |072.             
 |007.              |029.talk2         |051.              |073.             
 |008.              |030.talk2         |052.              |074.             
 |009.walkready  蹲下準備走路   |031.d4     空幹王       |053.              |075.             
 |010.f up   向前爬起       |032.              |054.int    拍拍手好棒棒       |076.             
 |011.b up     向後爬起     |033.              |055.int    激烈拍拍手       |077.             
 |012.rk  右踢          |034.              |056.int    超級激烈拍拍手       |078.             
 |013.lk   左踢         |035.              |057.int   短+超快激烈拍拍手        |079.             
 |014.              |036.              |058.int           |080.             
 |015.sit down      |037.              |059.              |081.             
 |016.stand up      |038.d2            |060.              |082.             
 |017.mul1  倒立        |039.d2            |061.              |083.             
 |018.mul2   自摔...       |040.              |062.              |084.             
 |019.mul3    自摔...       |041.talk2   廢話等級1      |063.              |085.             
 |020.raise_hand  蹲下..我沒設定好  |042.talk2    廢話等級2      |064.              |086.             
 |021.              |043.talk2    廢話等級3      |065.              |087.             
 |088.              |110.              |132.              |154.             
 |089.              |111.              |133.              |155.             
 |090.lie down      |112.              |134.              |156.             
 |091.lie up        |113.              |135.              |157.             
 |092.              |114.              |136.              |158.             
 |093.              |115.              |137.              |159.             
 |094.              |116.              |138.              |160.             
 |095.              |117.              |139.              |161.             
 |096.              |118.              |140.              |162.             
 |097.              |119.              |141.              |163.             
 |098.              |120.              |142.              |164.             
 |099.              |121.              |143.              |165.             
 |100.              |122.              |144.              |166.             
 |101.              |123.              |145.              |167.             
 |102.              |124.              |146.              |168.             
 |103.              |125.              |147.              |169.             
 |104.              |126.              |148.              |170.             
 |105.              |127.              |149.              |171.             
 |106.              |128.              |150.              |172.             
 |107.              |129.              |151.              |173.             
 |108.              |130.              |152.              |174.             
 |109.              |131.              |153.              |175.   
 |176.              |198.              |220.              |242.             
 |177.              |199.              |221.              |243.             
 |178.              |200.              |222.              |244.             
 |179.              |201.              |223.              |245.             
 |180.              |202.              |224.              |246.             
 |181.              |203.              |225.              |247.             
 |182.              |204.              |226.              |248.             
 |183.              |205.              |227.              |249.             
 |184.              |206.              |228.              |250.             
 |185.              |207.              |229.              |251.             
 |186.              |208.              |230.              |252.             
 |187.              |209.              |231.              |253.             
 |188.              |210.              |232.              |254.             
 |189.              |211.              |233.              |255.             
 |190.              |212.              |234.              |                
 |191.              |213.              |235.              |                
 |192.              |214.              |236.              |                
 |193.              |215.              |237.sit down      |                
 |194.              |216.              |238.              |                
 |195.              |217.              |239.sit down      |                
 |196.              |218.              |240.sit down      |                
 |197.              |219.              |241.sit down      |          
 
 ### 馬達
 ID: 1(R_SHO_PITCH)[1480] 1498 1480|---- ---- ---- ---- ---- 55 init            
|--|--
ID: 2(L_SHO_PITCH)[2610] 2518 2610|---- ---- ---- ---- ---- 55 Page Number:0001
ID: 3(R_SHO_ROLL) [1747] 1845 1747|---- ---- ---- ---- ---- 55  Address:0x00200
ID: 4(L_SHO_ROLL) [2343] 2248 2343|---- ---- ---- ---- ---- 55   Play Count:001
ID: 5(R_ELBOW)    [2147] 2381 2147|---- ---- ---- ---- ---- 55    Page Step:002
ID: 6(L_ELBOW)    [1944] 1712 1944|---- ---- ---- ---- ---- 55   Page Speed:032
ID: 7(R_HIP_YAW)  [2047] 2048 2047|---- ---- ---- ---- ---- 55   Accel Time:032
ID: 8(L_HIP_YAW)  [2047] 2048 2047|---- ---- ---- ---- ---- 55 Link to Next:000
ID: 9(R_HIP_ROLL) [2047] 2052 2047|---- ---- ---- ---- ---- 55 Link to Exit:000
ID:10(L_HIP_ROLL) [2047] 2044 2047|---- ---- ---- ---- ---- 55                 
ID:11(R_HIP_PITCH)[2013] 1637 2013|---- ---- ---- ---- ---- 55                 
ID:12(L_HIP_PITCH)[2080] 2459 2080|---- ---- ---- ---- ---- 55                 
ID:13(R_KNEE)     [2047] 2653 2047|---- ---- ---- ---- ---- 55                 
ID:14(L_KNEE)     [2047] 1443 2047|---- ---- ---- ---- ---- 55                 
ID:15(R_ANK_PITCH)[2063] 2369 2063|---- ---- ---- ---- ---- 55                 
ID:16(L_ANK_PITCH)[2030] 1727 2030|---- ---- ---- ---- ---- 55                 
ID:17(R_ANK_ROLL) [2047] 2057 2047|---- ---- ---- ---- ---- 55                 
ID:18(L_ANK_ROLL) [2047] 2039 2047|---- ---- ---- ---- ---- 55                 
ID:19(HEAD_PAN)   [2047] 2048 2047|---- ---- ---- ---- ---- 55                 
ID:20(HEAD_TILT)  [2170] 2161 2170|---- ---- ---- ---- ---- 55                 
   PauseTime      [ 000]  000  000| 000  000  000  000  000                    
   Time(x 8msec)  [ 000]  125  125| 000  000  000  000  000                    
                   STP7  STP0 STP1 STP2 STP3 STP4 STP5 STP6                    
]                                                                              

## 動作編輯器

1.首先先切換資料夾
```cmake
cd /robotis/Linux/project/action_editor
```
2.用make去編譯cpp
```cmake
make
```
3.去執行編譯的檔案
```cmake
./action_editor
```
4.任意鑑enter
![](https://i.imgur.com/yPITJh6.png)

5.會出現這個畫面
![](https://i.imgur.com/hKMI7oG.png)

6.開始使用：
指令如下
指令名稱|功能
--|--
page 頁數|切換到哪一個指令集
play|執行
list|回歸表單
copy 頁數|拷貝那一頁的動作
off id |把id幾號的馬達關掉
name|命名
save|儲存

### 範例創建一個動作
首先去找一個空的頁數，假設20頁是空的，接下來開始動作
1. ```page 20```進入到該頁數
2. ```copy 1```複製你要的動作近來
![](https://i.imgur.com/csYwxeI.png)
3. 根據要求要抬起右手臂，根據嚴密計算過後，我知道要把1 3 5這三個馬達關掉，你就會看到他們的位置出現???
```cmake
off 1 3 5
```
![](https://i.imgur.com/5JDoJf8.png)
4. 接著直接把他的手抬起來，輸入```on```
5. 這時候你就會看到她的位置變成新的位置
![](https://i.imgur.com/l3Z6Pgq.png)
6. 把剛剛的動作加到最後的初始動作，輸入```i2```，的訊息就會被被拷貝到STP2中

## 程式碼
### 向後走

- 檔案位置：```robotisop2/Linux/project/tutorial/walk_back```
- 使用方法：
	- 先創建一個新資料夾在```robotisop2/Linux/project/tutorial```
	- 再把檔案下載到裡面，分別是```main.cpp```和```Makefile```
	- 用指令```make```進行編譯
	- 再去執行
	>記得在su模式下進行，否則無法開啟電機


```main.cpp```
```cpp=
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <libgen.h>
#include "LinuxDARwIn.h"
 
#define INI_FILE_PATH       "../../../../Data/config.ini"
#define U2D_DEV_NAME        "/dev/ttyUSB0"
 
using namespace Robot;
 
 
void change_current_dir()
{
    char exepath[1024] = {0};
    if(readlink("/proc/self/exe", exepath, sizeof(exepath)) != -1)
        chdir(dirname(exepath));
}
 
int main(void)
{
    //printf( "\n===== Walk Backward Tutorial for DARwIn =====\n\n");
 
    change_current_dir();
 
    minIni* ini = new minIni(INI_FILE_PATH);
 
	//////////////////// Framework Initialize ////////////////////////////
	LinuxCM730 linux_cm730(U2D_DEV_NAME);
	CM730 cm730(&linux_cm730);
	if(MotionManager::GetInstance()->Initialize(&cm730) == false)
	{
		//printf("Fail to initialize Motion Manager!\n");
			return 0;
	}
        //Port initialization and opening, dynamixel power on
 
        MotionManager::GetInstance()->LoadINISettings(ini);
        Walking::GetInstance()->LoadINISettings(ini);
        //Load default settings for MotionManager and Walking module
 
	MotionManager::GetInstance()->AddModule((MotionModule*)Head::GetInstance());
	MotionManager::GetInstance()->AddModule((MotionModule*)Walking::GetInstance());
        LinuxMotionTimer *motion_timer = new LinuxMotionTimer(MotionManager::GetInstance());
        motion_timer->Start();
        //Create MotionManager object and registers head and walking modules, then timers are initialized.
	/////////////////////////////////////////////////////////////////////
 
        /////////////////////////Capture Motor Position//////////////////////
	int n = 0;
	int param[JointData::NUMBER_OF_JOINTS * 5];
	int wGoalPosition, wStartPosition, wDistance;
 
	for(int id=JointData::ID_R_SHOULDER_PITCH; id<JointData::NUMBER_OF_JOINTS; id++)
	{
		wStartPosition = MotionStatus::m_CurrentJoints.GetValue(id);
		wGoalPosition = Walking::GetInstance()->m_Joint.GetValue(id);
		if( wStartPosition > wGoalPosition )
			wDistance = wStartPosition - wGoalPosition;
		else
			wDistance = wGoalPosition - wStartPosition;
 
		wDistance >>= 2;
		if( wDistance < 8 )
			wDistance = 8;
 
		param[n++] = id;
		param[n++] = CM730::GetLowByte(wGoalPosition);
		param[n++] = CM730::GetHighByte(wGoalPosition);
		param[n++] = CM730::GetLowByte(wDistance);
		param[n++] = CM730::GetHighByte(wDistance);
	}
	cm730.SyncWrite(MX28::P_GOAL_POSITION_L, 5, JointData::NUMBER_OF_JOINTS - 1, param);
        //Capture initial position of Darwin OP 2's motor position
 
	//printf("Press the ENTER key to begin!\n");
	getchar();
 
        Head::GetInstance()->m_Joint.SetEnableHeadOnly(true, true);
        Walking::GetInstance()->m_Joint.SetEnableBodyWithoutHead(true, true);
	MotionManager::GetInstance()->SetEnable(true);
        //Walking and MotionManager enable motors
 
    while(1)
    {
 
	    if(Action::GetInstance()->IsRunning() == 0)
            {
		Head::GetInstance()->m_Joint.SetEnableHeadOnly(true, true);
                Walking::GetInstance()->m_Joint.SetEnableBodyWithoutHead(true, true);
 
                if(Walking::GetInstance()->IsRunning() == false){
                Walking::GetInstance()->X_MOVE_AMPLITUDE = -15.0;
                //X_MOVE_AMPLITUDE is a variable in Walking class that controls Darwin OP 2's walking step length, 
                //each unit corresponds to approximately 1 mm. Set X_MOVE_AMPLITUDE to negative numbers to program 
                //Darwin OP 2 to walk backwards. The Walking class calculates corresponding motor positions 
                //internally
 
                Walking::GetInstance()->A_MOVE_AMPLITUDE = 0.0;
                //A_MOVE_AMPLITUDE is a variable in Walking class that controls Darwin OP 2's yaw movement. Each 
                //unit correspond approximately to 1 degree. Positive degrees for Darwin OP 2 to turn 
                //counterclockwise, negative degree for clockwise. 
 
                Walking::GetInstance()->Start();
                //Start walking algorithm
                }
 
		Walking::GetInstance()->X_MOVE_AMPLITUDE = -15.0;
		Walking::GetInstance()->A_MOVE_AMPLITUDE = 0.0;
 
	     }
 
    }
 
    return 0;
}
```

```Makefile```
```cmake=
TARGET = walk_backward
 
INCLUDE_DIRS = -I../../../include -I../../../../Framework/include
 
CXX = g++
CXXFLAGS += -O2 -DLINUX -Wall $(INCLUDE_DIRS)
#CXXFLAGS += -O2 -DDEBUG -DLINUX -Wall $(INCLUDE_DIRS)
LFLAGS += -lpthread -ljpeg -lrt
 
OBJECTS =   main.o
 
all: $(TARGET)
 
clean:
	rm -f *.a *.o $(TARGET) core *~ *.so *.lo
 
libclean:
	make -C ../../../build clean
 
distclean: clean libclean
 
darwin.a:
	make -C ../../../build
 
$(TARGET): darwin.a $(OBJECTS)
	$(CXX) $(CFLAGS) $(OBJECTS) ../../../lib/darwin.a -o $(TARGET) $(LFLAGS)
	chmod 755 $(TARGET)
 
# useful to make a backup "make tgz"
tgz: clean
	mkdir -p backups
	tar czvf ./backups/ball_following_`date +"%Y_%m_%d_%H.%M.%S"`.tgz --exclude backups *
```

結果：
在測試時需要先進入su模式，接下來開始進行他的動作，他會先站起來在開使走，但是他程式很不穩定，我需要連續開三次才會成功，這個問題在於編譯時的問題

![](https://i.imgur.com/aX8ytz7.png)

錯誤解決方法：
[法1](https://www.cnblogs.com/panfeng412/archive/2011/11/06/segmentation-fault-in-linux.html)

## python物體中心點

```python=
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 14:57:15 2019

@author: dell
"""

import cv2
import numpy as np

cap = cv2.VideoCapture(0)
while(1):
    ret, frame = cap.read()
#    cv2.imshow('image',img)   
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)
    cv2.imshow('image',thresh[1])
    cnts = cv2.findContours(thresh[1].copy(), cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)
    cnts=cnts[1]
    for c in cnts:
# compute the center of the contour
            M = cv2.moments(c)
            cX = int(M['m10'] / M['m00']) if M['m00']!=0 else 0
            cY = int(M['m01'] / M['m00']) if M['m00']!=0 else 0
# 劃出邊緣
#            cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
#劃出中心
            cv2.circle(frame, (cX, cY), 7, (255, 255, 255), -1)
            cv2.putText(frame, 'center', (cX - 20, cY - 20),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv2.imshow('frame',frame) 
    if cv2.waitKey(1)==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
```

## OP2向前模式

### 1. 新增語音到```../../../Data/mp3/Sprint mode.mp3```
### 2. 更改DEMO裡面的```StatusCheck.h```和```StatusCheck.cpp```

```StatusCheck.h```
```cpp=
/*
 * StatusCheck.h
 *
 *  Created on: 2011. 1. 21.
 *      Author: zerom
 */

#ifndef STATUSCHECK_H_
#define STATUSCHECK_H_

#include <sys/time.h>
#include "CM730.h"

namespace Robot
{
   //Line 16
enum {
        INITIAL,
        READY,
        SOCCER,
        MOTION,
        VISION,
        SPRINT, //Add a new mode called "SPRINT" to an enumerated list of modes
        MAX_MODE
    };

    enum {
    	SOCCER_PLAY,
		SOCCER_REST
    };

    enum {
        BTN_MODE = 1,
        BTN_START = 2
    };

    class StatusCheck {
    private:
        static int m_old_btn;
        static int m_chicago_mode_cnt;

    public:
        static int m_cur_mode;
        static int m_is_started;

        static int 	    m_soccer_sub_mode;
        static double   m_soccer_start_time;

        static void Check(CM730 &cm730);
    };
}

#endif /* STATUSCHECK_H_ */
```
```StatusCheck.cpp```
```cpp=
/*
 * StatusCheck.cpp
 *
 *  Created on: 2011. 1. 21.
 *      Author: zerom
 */

#include <stdio.h>
#include <unistd.h>

#include "StatusCheck.h"
#include "Head.h"
#include "Action.h"
#include "Walking.h"
#include "MotionStatus.h"
#include "MotionManager.h"
#include "LinuxActionScript.h"

#define PLAY_TIME 120.0
#define REST_TIME 60.0

#define MAX_CHICAGO_CNT 90

using namespace Robot;

int StatusCheck::m_chicago_mode_cnt = 0;

int StatusCheck::m_cur_mode     = READY;
int StatusCheck::m_old_btn      = 0;
int StatusCheck::m_is_started   = 0;

int StatusCheck::m_soccer_sub_mode = SOCCER_PLAY;
double StatusCheck::m_soccer_start_time = 0.0;

void StatusCheck::Check(CM730 &cm730)
{
    struct timeval _tv;
    gettimeofday(&_tv, NULL);
    double _curr_time = _tv.tv_sec + (_tv.tv_usec/1000000.0);

    if(MotionStatus::FALLEN != STANDUP && m_cur_mode == SOCCER && m_is_started != 0)
    {
        Walking::GetInstance()->Stop();
        while(Walking::GetInstance()->IsRunning() == 1) usleep(8000);

        Action::GetInstance()->m_Joint.SetEnableBody(true, true);

        if(MotionStatus::FALLEN == FORWARD)
            Action::GetInstance()->Start(10);   // FORWARD GETUP
        else if(MotionStatus::FALLEN == BACKWARD)
            Action::GetInstance()->Start(11);   // BACKWARD GETUP

        while(Action::GetInstance()->IsRunning() == 1) usleep(8000);

        Head::GetInstance()->m_Joint.SetEnableHeadOnly(true, true);
        Walking::GetInstance()->m_Joint.SetEnableBodyWithoutHead(true, true);
    }

    if(m_cur_mode == SOCCER && m_is_started == 2)
    {
        if(m_soccer_sub_mode == SOCCER_PLAY && (_curr_time - m_soccer_start_time) > PLAY_TIME)
        {
            Walking::GetInstance()->Stop();
            while(Walking::GetInstance()->IsRunning() == true) usleep(8000);

            Action::GetInstance()->m_Joint.SetEnableBody(true, true);

            while(Action::GetInstance()->Start(15) == false) usleep(8000);
            while(Action::GetInstance()->IsRunning() == true) usleep(8000);

            // TODO: Torque OFF??
            cm730.WriteByte(254, MX28::P_TORQUE_ENABLE, 0, NULL);

            m_soccer_sub_mode = SOCCER_REST;
            gettimeofday(&_tv, NULL);
            m_soccer_start_time = _tv.tv_sec + (_tv.tv_usec/1000000.0);
        }
        else if(m_soccer_sub_mode == SOCCER_REST && (_curr_time - m_soccer_start_time) > REST_TIME)
        {
            MotionManager::GetInstance()->Reinitialize();
            MotionManager::GetInstance()->SetEnable(true);
            LinuxActionScript::PlayMP3("../../../Data/mp3/Start soccer demonstration.mp3");

            Action::GetInstance()->m_Joint.SetEnableBody(true, true);

            while(Action::GetInstance()->Start(15) == false) usleep(8000);
            while(Action::GetInstance()->IsRunning() == true) usleep(8000);

            Action::GetInstance()->Start(9);
            while(Action::GetInstance()->IsRunning() == true) usleep(8000);

            Head::GetInstance()->m_Joint.SetEnableHeadOnly(true, true);
            Walking::GetInstance()->m_Joint.SetEnableBodyWithoutHead(true, true);

            MotionManager::GetInstance()->ResetGyroCalibration();
            while(1)
            {
                if(MotionManager::GetInstance()->GetCalibrationStatus() == 1)
                {
                    LinuxActionScript::PlayMP3("../../../Data/mp3/Sensor calibration complete.mp3");
                    break;
                }
                else if(MotionManager::GetInstance()->GetCalibrationStatus() == -1)
                {
                    LinuxActionScript::PlayMP3Wait("../../../Data/mp3/Sensor calibration fail.mp3");
                    MotionManager::GetInstance()->ResetGyroCalibration();
                }
                usleep(8000);
            }

            m_soccer_sub_mode = SOCCER_PLAY;
            gettimeofday(&_tv, NULL);
            m_soccer_start_time = _tv.tv_sec + (_tv.tv_usec/1000000.0);
        }
    }

    if(m_old_btn == MotionStatus::BUTTON)
    {
        if(m_cur_mode == READY && m_is_started == 0 && m_chicago_mode_cnt > MAX_CHICAGO_CNT)
        {
            fprintf(stderr, "CHICAGO MODE ! \n\n");
      m_cur_mode = SOCCER;
      m_old_btn == BTN_START;
        }
        else if(m_cur_mode == READY && m_is_started == 0 && m_chicago_mode_cnt <= MAX_CHICAGO_CNT)
        {
            m_chicago_mode_cnt++;
      return;
        }
    else
        {
            m_chicago_mode_cnt = 0;
            return;
        }
    }
    else
    {
        m_chicago_mode_cnt = 0;
        m_old_btn = MotionStatus::BUTTON;
    }
    //At the end of if statement Line 141
    if(m_old_btn & BTN_MODE)
        //////////////////////////////
        ///Skipping Unmodified Codes//
        //////////////////////////////
        else if(m_cur_mode == SPRINT) //adding LED and play mp3 for new mode
        {
            cm730.WriteByte(CM730::P_LED_PANNEL, 0x01|0x04, NULL);
            //Signaling Darwin OP 2 which LED to turn on
            LinuxActionScript::PlayMP3("../../../Data/mp3/Sprint mode.mp3");
            //play an mp3 file (you can use any mp3 file but make sure file name matches)
        }
    }
        //////////////////////////////
        ///Skipping Unmodified Codes//
        //////////////////////////////
    if(m_old_btn & BTN_MODE)
    {
        fprintf(stderr, "Mode button pressed.. \n");

        if(m_is_started != 0)
        {
            m_is_started    = 0;
            m_cur_mode      = READY;
            LinuxActionScript::m_stop = 1;

            Walking::GetInstance()->Stop();
            Action::GetInstance()->m_Joint.SetEnableBody(true, true);

            while(Action::GetInstance()->Start(15) == false) usleep(8000);
            while(Action::GetInstance()->IsRunning() == true) usleep(8000);
        }
        else
        {
            m_cur_mode++;
            if(m_cur_mode >= MAX_MODE) m_cur_mode = READY;
        }

        MotionManager::GetInstance()->SetEnable(false);
        usleep(10000);

        if(m_cur_mode == READY)
        {
            cm730.WriteByte(CM730::P_LED_PANNEL, 0x01|0x02|0x04, NULL);
            LinuxActionScript::PlayMP3("../../../Data/mp3/Demonstration ready mode.mp3");
        }
        else if(m_cur_mode == SOCCER)
        {
            cm730.WriteByte(CM730::P_LED_PANNEL, 0x01, NULL);
            LinuxActionScript::PlayMP3("../../../Data/mp3/Autonomous soccer mode.mp3");
        }
        else if(m_cur_mode == MOTION)
        {
            cm730.WriteByte(CM730::P_LED_PANNEL, 0x02, NULL);
            LinuxActionScript::PlayMP3("../../../Data/mp3/Interactive motion mode.mp3");
        }
        else if(m_cur_mode == VISION)
        {
            cm730.WriteByte(CM730::P_LED_PANNEL, 0x04, NULL);
            LinuxActionScript::PlayMP3("../../../Data/mp3/Vision processing mode.mp3");
        }
    }

    if(m_old_btn & BTN_START)
    {
        if(m_is_started == 0)
        {
            fprintf(stderr, "Start button pressed.. & started is false.. \n");

            if(m_cur_mode == SOCCER)
            {
                MotionManager::GetInstance()->Reinitialize();
                MotionManager::GetInstance()->SetEnable(true);
                if(m_chicago_mode_cnt > MAX_CHICAGO_CNT)
                {
            m_chicago_mode_cnt = 0;
                    m_is_started = 2;
                }
        else
                    m_is_started = 1;
                LinuxActionScript::PlayMP3("../../../Data/mp3/Start soccer demonstration.mp3");

                Action::GetInstance()->m_Joint.SetEnableBody(true, true);

                Action::GetInstance()->Start(9);
                while(Action::GetInstance()->IsRunning() == true) usleep(8000);

                Head::GetInstance()->m_Joint.SetEnableHeadOnly(true, true);
                Walking::GetInstance()->m_Joint.SetEnableBodyWithoutHead(true, true);

                MotionManager::GetInstance()->ResetGyroCalibration();
                while(1)
                {
                    if(MotionManager::GetInstance()->GetCalibrationStatus() == 1)
                    {
                        LinuxActionScript::PlayMP3("../../../Data/mp3/Sensor calibration complete.mp3");
                        break;
                    }
                    else if(MotionManager::GetInstance()->GetCalibrationStatus() == -1)
                    {
                        LinuxActionScript::PlayMP3Wait("../../../Data/mp3/Sensor calibration fail.mp3");
                        MotionManager::GetInstance()->ResetGyroCalibration();
                    }
                    usleep(8000);
                }

                m_soccer_sub_mode = SOCCER_PLAY;
                gettimeofday(&_tv, NULL);
                m_soccer_start_time = _tv.tv_sec + (_tv.tv_usec/1000000.0);
            }
            else if(m_cur_mode == MOTION)
            {
                MotionManager::GetInstance()->Reinitialize();
                MotionManager::GetInstance()->SetEnable(true);
                m_is_started = 1;
                LinuxActionScript::PlayMP3("../../../Data/mp3/Start motion demonstration.mp3");

                // Joint Enable..
                Action::GetInstance()->m_Joint.SetEnableBody(true, true);

                Action::GetInstance()->Start(1);
                while(Action::GetInstance()->IsRunning() == true) usleep(8000);
            }
            else if(m_cur_mode == VISION)
            {
                MotionManager::GetInstance()->Reinitialize();
                MotionManager::GetInstance()->SetEnable(true);
                m_is_started = 1;
                LinuxActionScript::PlayMP3("../../../Data/mp3/Start vision processing demonstration.mp3");

                // Joint Enable...
                Action::GetInstance()->m_Joint.SetEnableBody(true, true);

                Action::GetInstance()->Start(1);
                while(Action::GetInstance()->IsRunning() == true) usleep(8000);
            }
        }
        else
        {
            fprintf(stderr, "Start button pressed.. & started is true.. \n");
        }
        else if(m_cur_mode == SPRINT)
  {
      MotionManager::GetInstance()->Reinitialize();
      MotionManager::GetInstance()->SetEnable(true);
      //initialize and enable MotionManager class
      m_is_started = 1;
      LinuxActionScript::PlayMP3("../../../Data/mp3/Start sprint demonstration.mp3");
      //play an mp3 file (you can use any mp3 file but make sure file name matches)
 
      // Joint Enable...
      Action::GetInstance()->m_Joint.SetEnableBody(true, true);
 
      Action::GetInstance()->Start(9);
      while(Action::GetInstance()->IsRunning() == true) usleep(8000);
 
      Head::GetInstance()->m_Joint.SetEnableHeadOnly(true, true);
      Walking::GetInstance()->m_Joint.SetEnableBodyWithoutHead(true, true);
      //Reset Gyro sensor
      MotionManager::GetInstance()->ResetGyroCalibration();
      while(1)
      {
          if(MotionManager::GetInstance()->GetCalibrationStatus() == 1)
          {
              LinuxActionScript::PlayMP3("../../../Data/mp3/Sensor calibration complete.mp3");
              break;
          }
          else if(MotionManager::GetInstance()->GetCalibrationStatus() == -1)
          {
              LinuxActionScript::PlayMP3Wait("../../../Data/mp3/Sensor calibration fail.mp3");
              MotionManager::GetInstance()->ResetGyroCalibration();
          }
          usleep(8000);
      }
  //copied status check condition from soccer mode to new mode
  //These codes initialize Darwin OP 2 for movement and walking
    }
}
```


### 3. ```Framework/src/vision```裡面的```ColorFinder.cpp```

```ColorFinder.cpp```
```cpp=
/*
 * ColorFinder.cpp
 *
 *  Created on: 2011. 1. 10.
 *      Author: zerom
 */

#include <stdlib.h>

#include "ColorFinder.h"
#include "ImgProcess.h"

using namespace Robot;

ColorFinder::ColorFinder() :
        m_center_point(Point2D()),
        m_hue(356),
        m_hue_tolerance(15),
        m_min_saturation(50),
        m_min_value(10),
        m_min_percent(0.07),
        m_max_percent(30.0),
        color_section(""),
        m_result(0)
{ }

ColorFinder::ColorFinder(int hue, int hue_tol, int min_sat, int min_val, double min_per, double max_per) :
        m_hue(hue),
        m_hue_tolerance(hue_tol),
        m_min_saturation(min_sat),
        m_min_value(min_val),
        m_min_percent(min_per),
        m_max_percent(max_per),
        color_section(""),
        m_result(0)
{ }

ColorFinder::~ColorFinder()
{
    // TODO Auto-generated destructor stub
}

void ColorFinder::Filtering(Image *img)
{
    unsigned int h, s, v;
    int h_max, h_min;

    if(m_result == NULL)
        m_result = new Image(img->m_Width, img->m_Height, 1);

    h_max = m_hue + m_hue_tolerance;
    h_min = m_hue - m_hue_tolerance;
    if(h_max > 360)
        h_max -= 360;
    if(h_min < 0)
        h_min += 360;

    for(int i = 0; i < img->m_NumberOfPixels; i++)
    {
        h = (img->m_ImageData[i*img->m_PixelSize + 0] << 8) | img->m_ImageData[i*img->m_PixelSize + 1];
        s =  img->m_ImageData[i*img->m_PixelSize + 2];
        v =  img->m_ImageData[i*img->m_PixelSize + 3];

        if( h > 360 )
            h = h % 360;

        if( ((int)s > m_min_saturation) && ((int)v > m_min_value) )
        {
            if(h_min <= h_max)
            {
                if((h_min < (int)h) && ((int)h < h_max))
                    m_result->m_ImageData[i]= 1;
                else
                    m_result->m_ImageData[i]= 0;
            }
            else
            {
                if((h_min < (int)h) || ((int)h < h_max))
                    m_result->m_ImageData[i]= 1;
                else
                    m_result->m_ImageData[i]= 0;
            }
        }
        else
        {
            m_result->m_ImageData[i]= 0;
        }
    }
}

void ColorFinder::LoadINISettings(minIni* ini)
{
    LoadINISettings(ini, COLOR_SECTION);
}

void ColorFinder::LoadINISettings(minIni* ini, const std::string &section)
{
    int value = -2;
    if((value = ini->geti(section, "hue", INVALID_VALUE)) != INVALID_VALUE)             m_hue = value;
    if((value = ini->geti(section, "hue_tolerance", INVALID_VALUE)) != INVALID_VALUE)   m_hue_tolerance = value;
    if((value = ini->geti(section, "min_saturation", INVALID_VALUE)) != INVALID_VALUE)  m_min_saturation = value;
    if((value = ini->geti(section, "min_value", INVALID_VALUE)) != INVALID_VALUE)       m_min_value = value;

    double dvalue = -2.0;
    if((dvalue = ini->getd(section, "min_percent", INVALID_VALUE)) != INVALID_VALUE)    m_min_percent = dvalue;
    if((dvalue = ini->getd(section, "max_percent", INVALID_VALUE)) != INVALID_VALUE)    m_max_percent = dvalue;

    color_section = section;
}

void ColorFinder::SaveINISettings(minIni* ini)
{
    SaveINISettings(ini, COLOR_SECTION);
}

void ColorFinder::SaveINISettings(minIni* ini, const std::string &section)
{
    ini->put(section,   "hue",              m_hue);
    ini->put(section,   "hue_tolerance",    m_hue_tolerance);
    ini->put(section,   "min_saturation",   m_min_saturation);
    ini->put(section,   "min_value",        m_min_value);
    ini->put(section,   "min_percent",      m_min_percent);
    ini->put(section,   "max_percent",      m_max_percent);

    color_section = section;
}

Point2D& ColorFinder::GetPosition(Image* hsv_img)
{
    int sum_x = 0, sum_y = 0, count = 0;

    Filtering(hsv_img);

    ImgProcess::Erosion(m_result);
    ImgProcess::Dilation(m_result);

    for(int y = 0; y < m_result->m_Height; y++)
    {
        for(int x = 0; x < m_result->m_Width; x++)
        {
            if(m_result->m_ImageData[m_result->m_Width * y + x] > 0)
            {
                sum_x += x;
                sum_y += y;
                count++;
            }
        }
    }

    if(count <= (hsv_img->m_NumberOfPixels * m_min_percent / 100) || count > (hsv_img->m_NumberOfPixels * m_max_percent / 100))
    {
        m_center_point.X = -1.0;
        m_center_point.Y = -1.0;
    }
    else
    {
        m_center_point.X = (int)((double)sum_x / (double)count);
        m_center_point.Y = (int)((double)sum_y / (double)count);
    }

    return m_center_point;
}

//Creted a new function that take image pointer and int reference as parameter and return center coordinates and pixel count
Point2D& ColorFinder::GetPosition(Image* hsv_img, int &count)
{
    int sum_x = 0, sum_y = 0, count = 0;
 
    Filtering(hsv_img);
 
    ImgProcess::Erosion(m_result);
    ImgProcess::Dilation(m_result);
 
    for(int y = 0; y < m_result->m_Height; y++)
    {
        for(int x = 0; x < m_result->m_Width; x++)
        {
            if(m_result->m_ImageData[m_result->m_Width * y + x] > 0)
            {
                sum_x += x;
                sum_y += y;
                count++;
            }
        }
    }
 
    if(count <= (hsv_img->m_NumberOfPixels * m_min_percent / 100) || count > (hsv_img->m_NumberOfPixels * m_max_percent / 100))
    {
        m_center_point.X = -1.0;
        m_center_point.Y = -1.0;
    }
    else
    {
        m_center_point.X = (int)((double)sum_x / (double)count);
        m_center_point.Y = (int)((double)sum_y / (double)count);
    }
 
    return m_center_point;
}
```

### 4. ```Framework/include/ColorFinder.h```裡面的```ColorFinder.h```

```ColorFinder.h```
```cpp=
/*
 * ColorFinder.h
 *
 *  Created on: 2011. 1. 10.
 *      Author: zerom
 */

#ifndef COLORFINDER_H_
#define COLORFINDER_H_

#include <string>

#include "Point.h"
#include "Image.h"
#include "minIni.h"

#define COLOR_SECTION   "Find Color"
#define INVALID_VALUE   -1024.0

namespace Robot
{
    class ColorFinder
    {
    private:
        Point2D m_center_point;

        void Filtering(Image* img);

    public:
        int m_hue;             /* 0 ~ 360 */
        int m_hue_tolerance;   /* 0 ~ 180 */
        int m_min_saturation;  /* 0 ~ 100 */
        int m_min_value;       /* 0 ~ 100 */
        double m_min_percent;  /* 0.0 ~ 100.0 */
        double m_max_percent;  /* 0.0 ~ 100.0 */

        std::string color_section;
        Point2D& GetPosition(Image* hsv_img, int &count);
        Image*  m_result;

        ColorFinder();
        ColorFinder(int hue, int hue_tol, int min_sat, int min_val, double min_per, double max_per);
        virtual ~ColorFinder();

        void LoadINISettings(minIni* ini);
        void LoadINISettings(minIni* ini, const std::string &section);
        void SaveINISettings(minIni* ini);
        void SaveINISettings(minIni* ini, const std::string &section);

        Point2D& GetPosition(Image* hsv_img);
    };
}

#endif /* COLORFINDER_H_ */

```

### 5. ```Linux\project\demo```更改```main.cpp```

```main.cpp```
```cpp=
/*
 * main.cpp
 *
 *  Created on: 2011. 1. 4.
 *      Author: robotis
 */

#include <stdio.h>
#include <unistd.h>
#include <limits.h>
#include <string.h>
#include <libgen.h>
#include <signal.h>

#include "mjpg_streamer.h"
#include "LinuxDARwIn.h"

#include "StatusCheck.h"
#include "VisionMode.h"

#ifdef MX28_1024
#define MOTION_FILE_PATH    "../../../Data/motion_1024.bin"
#else
#define MOTION_FILE_PATH    "../../../Data/motion_4096.bin"
#endif

#define INI_FILE_PATH       "../../../Data/config.ini"
#define SCRIPT_FILE_PATH    "script.asc"

#define U2D_DEV_NAME0       "/dev/ttyUSB0"
#define U2D_DEV_NAME1       "/dev/ttyUSB1"

LinuxCM730 linux_cm730(U2D_DEV_NAME0);
CM730 cm730(&linux_cm730);

void change_current_dir()
{
    char exepath[1024] = {0};
    if(readlink("/proc/self/exe", exepath, sizeof(exepath)) != -1)
    {
        if(chdir(dirname(exepath)))
            fprintf(stderr, "chdir error!! \n");
    }
}

void sighandler(int sig)
{
    exit(0);
}

int main(void)
{
    signal(SIGABRT, &sighandler);
    signal(SIGTERM, &sighandler);
    signal(SIGQUIT, &sighandler);
    signal(SIGINT, &sighandler);

    change_current_dir();

    minIni* ini = new minIni(INI_FILE_PATH);
    Image* rgb_output = new Image(Camera::WIDTH, Camera::HEIGHT, Image::RGB_PIXEL_SIZE);

    LinuxCamera::GetInstance()->Initialize(0);
    LinuxCamera::GetInstance()->SetCameraSettings(CameraSettings());    // set default
    LinuxCamera::GetInstance()->LoadINISettings(ini);                   // load from ini

    mjpg_streamer* streamer = new mjpg_streamer(Camera::WIDTH, Camera::HEIGHT);

    ColorFinder* ball_finder = new ColorFinder();
    ball_finder->LoadINISettings(ini);
    httpd::ball_finder = ball_finder;

    BallTracker tracker = BallTracker();
    BallFollower follower = BallFollower();

    ColorFinder* red_finder = new ColorFinder(0, 15, 45, 0, 0.3, 50.0);
    red_finder->LoadINISettings(ini, "RED");
    httpd::red_finder = red_finder;

    ColorFinder* yellow_finder = new ColorFinder(175, 45, 10, 0, 0.3, 50.0);
    yellow_finder->LoadINISettings(ini, "YELLOW");
    httpd::yellow_finder = yellow_finder;

    ColorFinder* blue_finder = new ColorFinder(225, 15, 45, 0, 135,200);
    blue_finder->LoadINISettings(ini, "BLUE");
    httpd::blue_finder = blue_finder;

    //declare a new object of class ColorFinder
    ColorFinder* finder = new ColorFinder();
     
    //you can initiate the object with 5 input color parameters
    ColorFinder* green_finder = new ColorFinder(115, 15, 45, 0,135,200);
     
    //There are default values of color you can load from ini file. Example
    finder->LoadINISettings(ini, "RED"); 
     
    //To get the position of center of mass of filtered pixels
    Point2D pos;
    pos = finder->GetPosition(LinuxCamera::GetInstance()->fbuffer->m_HSVFrame);
    //first declare an object of class Point2D
    //then set it equal to GetPosition function of ColorFinder object
    httpd::ini = ini;

    //////////////////// Framework Initialize ////////////////////////////
    if(MotionManager::GetInstance()->Initialize(&cm730) == false)
    {
        linux_cm730.SetPortName(U2D_DEV_NAME1);
        if(MotionManager::GetInstance()->Initialize(&cm730) == false)
        {
            printf("Fail to initialize Motion Manager!\n");
            return 0;
        }
    }

    Walking::GetInstance()->LoadINISettings(ini);

    MotionManager::GetInstance()->AddModule((MotionModule*)Action::GetInstance());
    MotionManager::GetInstance()->AddModule((MotionModule*)Head::GetInstance());
    MotionManager::GetInstance()->AddModule((MotionModule*)Walking::GetInstance());

    LinuxMotionTimer *motion_timer = new LinuxMotionTimer(MotionManager::GetInstance());
    motion_timer->Start();
    /////////////////////////////////////////////////////////////////////
    
    MotionManager::GetInstance()->LoadINISettings(ini);

    int firm_ver = 0;
    if(cm730.ReadByte(JointData::ID_HEAD_PAN, MX28::P_VERSION, &firm_ver, 0)  != CM730::SUCCESS)
    {
        fprintf(stderr, "Can't read firmware version from Dynamixel ID %d!! \n\n", JointData::ID_HEAD_PAN);
        exit(0);
    }

    if(0 < firm_ver && firm_ver < 27)
    {
#ifdef MX28_1024
        Action::GetInstance()->LoadFile(MOTION_FILE_PATH);
#else
        fprintf(stderr, "MX-28's firmware is not support 4096 resolution!! \n");
        fprintf(stderr, "Upgrade MX-28's firmware to version 27(0x1B) or higher.\n\n");
        exit(0);
#endif
    }
    else if(27 <= firm_ver)
    {
#ifdef MX28_1024
        fprintf(stderr, "MX-28's firmware is not support 1024 resolution!! \n");
        fprintf(stderr, "Remove '#define MX28_1024' from 'MX28.h' file and rebuild.\n\n");
        exit(0);
#else
        Action::GetInstance()->LoadFile((char*)MOTION_FILE_PATH);
#endif
    }
    else
        exit(0);

    Action::GetInstance()->m_Joint.SetEnableBody(true, true);
    MotionManager::GetInstance()->SetEnable(true);

    cm730.WriteByte(CM730::P_LED_PANNEL, 0x01|0x02|0x04, NULL);

    LinuxActionScript::PlayMP3("../../../Data/mp3/Demonstration ready mode.mp3");
    Action::GetInstance()->Start(15);
    while(Action::GetInstance()->IsRunning()) usleep(8*1000);

    int _ball_found = 0;
    while(1)
    {
        StatusCheck::Check(cm730);

        Point2D ball_pos, red_pos, yellow_pos, blue_pos;

        LinuxCamera::GetInstance()->CaptureFrame();
        memcpy(rgb_output->m_ImageData, LinuxCamera::GetInstance()->fbuffer->m_RGBFrame->m_ImageData, LinuxCamera::GetInstance()->fbuffer->m_RGBFrame->m_ImageSize);

        if(StatusCheck::m_cur_mode == READY || StatusCheck::m_cur_mode == VISION)
        {
            ball_pos = ball_finder->GetPosition(LinuxCamera::GetInstance()->fbuffer->m_HSVFrame);
            red_pos = red_finder->GetPosition(LinuxCamera::GetInstance()->fbuffer->m_HSVFrame);
            yellow_pos = yellow_finder->GetPosition(LinuxCamera::GetInstance()->fbuffer->m_HSVFrame);
            blue_pos = blue_finder->GetPosition(LinuxCamera::GetInstance()->fbuffer->m_HSVFrame);

            unsigned char r, g, b;
            for(int i = 0; i < rgb_output->m_NumberOfPixels; i++)
            {
                r = 0; g = 0; b = 0;
                if(ball_finder->m_result->m_ImageData[i] == 1)
                {
                    r = 255;
                    g = 128;
                    b = 0;
                }
                if(red_finder->m_result->m_ImageData[i] == 1)
                {
                    if(ball_finder->m_result->m_ImageData[i] == 1)
                    {
                        r = 0;
                        g = 255;
                        b = 0;
                    }
                    else
                    {
                        r = 255;
                        g = 0;
                        b = 0;
                    }
                }
                if(yellow_finder->m_result->m_ImageData[i] == 1)
                {
                    if(ball_finder->m_result->m_ImageData[i] == 1)
                    {
                        r = 0;
                        g = 255;
                        b = 0;
                    }
                    else
                    {
                        r = 255;
                        g = 255;
                        b = 0;
                    }
                }
                if(blue_finder->m_result->m_ImageData[i] == 1)
                {
                    if(ball_finder->m_result->m_ImageData[i] == 1)
                    {
                        r = 0;
                        g = 255;
                        b = 0;
                    }
                    else
                    {
                        r = 0;
                        g = 0;
                        b = 255;
                    }
                }

                if(r > 0 || g > 0 || b > 0)
                {
                    rgb_output->m_ImageData[i * rgb_output->m_PixelSize + 0] = r;
                    rgb_output->m_ImageData[i * rgb_output->m_PixelSize + 1] = g;
                    rgb_output->m_ImageData[i * rgb_output->m_PixelSize + 2] = b;
                }
            }
        }
        else if(StatusCheck::m_cur_mode == SPRINT) //under a new mode called Sprint
        {
     
        green = green_finder->GetPosition(LinuxCamera::GetInstance()->fbuffer->m_HSVFrame, greenCount);
        //using the modified GetPosition function that also return filtered pixel counts
        blue = blue_finder->GetPosition(LinuxCamera::GetInstance()->fbuffer->m_HSVFrame, blueCount);
        //store position of green and blue color
     
        if(green.X < 0 || blue.X < 0)
            center.X = -1;
        else
            center.X = (green.X + blue.X)/2;
        if(green.Y < 0 || blue.Y < 0)
        center.Y = -1;
        else 
            center.Y = (green.Y + blue.Y)/2;
        //calculate center of blue and green    
     
        _marker_found = marker_tracker.SearchAndTracking(center);
        //use camera tracking and raise the flag if marker is found
     
        }

        else if(StatusCheck::m_cur_mode == SOCCER)
        {
            //tracker.Process(ball_finder->GetPosition(LinuxCamera::GetInstance()->fbuffer->m_HSVFrame));
            _ball_found = tracker.SearchAndTracking(ball_finder->GetPosition(LinuxCamera::GetInstance()->fbuffer->m_HSVFrame));

            for(int i = 0; i < rgb_output->m_NumberOfPixels; i++)
            {
                if(ball_finder->m_result->m_ImageData[i] == 1)
                {
                    rgb_output->m_ImageData[i*rgb_output->m_PixelSize + 0] = 255;
                    rgb_output->m_ImageData[i*rgb_output->m_PixelSize + 1] = 128;
                    rgb_output->m_ImageData[i*rgb_output->m_PixelSize + 2] = 0;
                }
            }
        }

        streamer->send_image(rgb_output);

        if(StatusCheck::m_is_started == 0)
            continue;

        switch(StatusCheck::m_cur_mode)
        {
        case READY:
            break;
        case SOCCER:
            if(Action::GetInstance()->IsRunning() == 0 &&
                    StatusCheck::m_soccer_sub_mode == SOCCER_PLAY)
            {
                Head::GetInstance()->m_Joint.SetEnableHeadOnly(true, true);
                Walking::GetInstance()->m_Joint.SetEnableBodyWithoutHead(true, true);
                
                if(Walking::GetInstance()->IsRunning() == false && _ball_found != 1){
                    Walking::GetInstance()->X_MOVE_AMPLITUDE = -1.0;
                    Walking::GetInstance()->A_MOVE_AMPLITUDE = 0.0;
                    Walking::GetInstance()->Start();
                }

                if(_ball_found == 1)
                {
                    follower.Process(tracker.ball_position);

                    if(follower.KickBall != 0)
                    {
                        Head::GetInstance()->m_Joint.SetEnableHeadOnly(true, true);
                        Action::GetInstance()->m_Joint.SetEnableBodyWithoutHead(true, true);

                        if(follower.KickBall == -1)
                        {
                            Action::GetInstance()->Start(12);   // RIGHT KICK
                            fprintf(stderr, "RightKick! \n");
                        }
                        else if(follower.KickBall == 1)
                        {
                            Action::GetInstance()->Start(13);   // LEFT KICK
                            fprintf(stderr, "LeftKick! \n");
                        }
                    }
                }
                else if(_ball_found == -1)
                {
                    Walking::GetInstance()->X_MOVE_AMPLITUDE = -1.0;
                    Walking::GetInstance()->A_MOVE_AMPLITUDE = 10.0;
                }
                else
                {
                    Walking::GetInstance()->X_MOVE_AMPLITUDE = -1.0;
                    Walking::GetInstance()->A_MOVE_AMPLITUDE = 0.0;
                }
            }
            break;
        case MOTION:
            if(LinuxActionScript::m_is_running == 0)
                LinuxActionScript::ScriptStart(SCRIPT_FILE_PATH);
            break;
        case VISION:
            int detected_color = 0;
            detected_color |= (red_pos.X == -1)? 0 : VisionMode::RED;
            detected_color |= (yellow_pos.X == -1)? 0 : VisionMode::YELLOW;
            detected_color |= (blue_pos.X == -1)? 0 : VisionMode::BLUE;

            if(Action::GetInstance()->IsRunning() == 0)
                VisionMode::Play(detected_color);
            break;
        case SPRINT:
  //implement new codes here to execute after pressing start button
            if(Action::GetInstance()->IsRunning() == 0)
            {
                Head::GetInstance()->m_Joint.SetEnableHeadOnly(true, true);
                Walking::GetInstance()->m_Joint.SetEnableBodyWithoutHead(true, true);
                //Initialize walking module and head joints
 
                if(Walking::GetInstance()->IsRunning() == false && _ball_found != 1){
                Walking::GetInstance()->X_MOVE_AMPLITUDE = 30.0;
                //Set forward and back step length to 30cm
 
                Walking::GetInstance()->A_MOVE_AMPLITUDE = 0.0;
                //Set yaw step length to 0
 
                Walking::GetInstance()->Start();
                }
 
                if(_marker_found == 1)
                {
                marker_follower.Process(marker_tracker.ball_position);
                //use BallFollower object to start following marker
 
                        if(greenCount >= 10500 || blueCount >= 10500)
                        //pixel count can be used to approximate distance, but in this case, 
                        //this stop condition is sufficient                                 
                        {
                        Walking::GetInstance()->Stop();
            fprintf(stderr, "stop\n");
            while(Walking::GetInstance()->IsRunning() == true) usleep(1000000);
                        }
                 }
                 else
                 {
                 Walking::GetInstance()->X_MOVE_AMPLITUDE = 30.0;
                 Walking::GetInstance()->A_MOVE_AMPLITUDE = 0.0;
                 }       
             }
        }
    }

    return 0;
}

```


## demo模式開啟
使用“killall demo”命令，終止演示進程後，若想再次運行演示程序，請按如下步驟
操作：
- 按OP 的RESET 按鈕。
- 連接UltraVNCViewer，打開終端窗口，輸入“sudo su”命令。
- 輸入“cd /robotis/Linux/project/demo”，進入演示程序目錄下。
- 在demo 目錄下，輸入“./demo&”命令，按Enter 鍵，即可執行演示程序。緊接著在命令之後使用“&”符號，表示在後台（background）執行該進程。
- 如下圖所示，顯示“[1] 1988”信息，其中“[1]”表示只執行一個demo 進程，“1988”表示Ubuntu OS 的進程編號，並且進入準備執行4 種演示動作狀態中。
![](https://i.imgur.com/OFzDLSh.png)


## op2影像紀錄

```python=
import cv2
import numpy as np
frame = cv2.imread('45.png')

drawing = False
ix,iy = -1,-1
def draw_circle(event,x,y,flags,param):
    global ix,iy,drawing
    maxhsv=[0 , 0, 0]
    minhsv=[255 , 255, 255]
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy=x,y
    elif event==cv2.EVENT_MOUSEMOVE and flags==cv2.EVENT_FLAG_LBUTTON:
        if drawing == True:
            cv2.rectangle(img,(ix,iy),(x,y),(0,255,0),-1)
    elif event ==cv2.EVENT_LBUTTONUP:
        drawing == False
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        for i in range (ix,x):
            for j in range (iy,y):
                if hsv[j][i][0]>maxhsv[0]:
                    maxhsv[0]=hsv[j][i][0]
                if hsv[j][i][1]>maxhsv[1]:
                    maxhsv[1]=hsv[j][i][1]
                if hsv[j][i][2]>maxhsv[2]:
                    maxhsv[2]=hsv[j][i][2]
                if hsv[j][i][0]<minhsv[0]:
                    minhsv[0]=hsv[j][i][0]
                if hsv[j][i][1]>minhsv[1]:
                    minhsv[1]=hsv[j][i][1]
                if hsv[j][i][2]>minhsv[2]:
                    minhsv[2]=hsv[j][i][2]
        print('max:',maxhsv)
        print('min:',minhsv)

x=[]
for i in range(480):
    x.append([])
    #x[2].append(0)
    for a in range(640):
        x[i].append([])
        #x[1].append(0)
        for j in range(3):
            x[i][a].append(0)


img = x
cv2.namedWindow('frame')
cv2.setMouseCallback('frame',draw_circle)
while(1):
    #ret, frame = cap.read()
    #frame1=cv2.addWeighted(frame,1,img,1,0)
#    cv2.imshow('image',img)
    cv2.imshow('frame',frame)
    if cv2.waitKey(1)==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
```


## 錯誤

```cmake=
framework/src/vision/ColorFinder.cpp
../../Framework/src/vision/ColorFinder.cpp: In member function
‘Robot::Point2D& Robot::ColorFinder::GetPosition(Robot::Image*,
int&)’:
../../Framework/src/vision/ColorFinder.cpp:130:31: error: declaration
of ‘int count’ shadows a parameter
make: *** [../../Framework/src/vision/ColorFinder.o] Error 1
```

```cmake=
make -C ../../build
make[1]: Entering directory `/robotis/Linux/build'
ar cr ../lib/darwin.a ../../Framework/src/MX28.o
../../Framework/src/CM730.o ../../Framework/src/math/Matrix.o
../../Framework/src/math/Plane.o ../../Framework/src/math/Point.o
../../Framework/src/math/Vector.o
../../Framework/src/motion/JointData.o
../../Framework/src/motion/Kinematics.o
../../Framework/src/motion/MotionManager.o
../../Framework/src/motion/MotionStatus.o
../../Framework/src/motion/modules/Action.o
../../Framework/src/motion/modules/Head.o
../../Framework/src/motion/modules/Walking.o
../../Framework/src/vision/BallFollower.o
../../Framework/src/vision/BallTracker.o
../../Framework/src/vision/ColorFinder.o
../../Framework/src/vision/Image.o
../../Framework/src/vision/ImgProcess.o
../../Framework/src/vision/Camera.o
../../Framework/src/minIni/minIni.o streamer/httpd.o
streamer/jpeg_utils.o streamer/mjpg_streamer.o LinuxActionScript.o
LinuxCamera.o LinuxCM730.o LinuxMotionTimer.o LinuxNetwork.o
make[1]: Leaving directory `/robotis/Linux/build'
g++ -O2 -DLINUX -Wall -I../../include -I../../../Framework/include
-c -o StatusCheck.o StatusCheck.cpp
StatusCheck.cpp: In static member function ‘static void
Robot::StatusCheck::Check(Robot::CM730&)’:
StatusCheck.cpp:123:29: warning: statement has no effect [-Wunused-value]
StatusCheck.cpp:146:9: error: expected primary-expression before ‘else’
StatusCheck.cpp:146:9: error: expected ‘;’ before ‘else’
StatusCheck.cpp: At global scope:
StatusCheck.cpp:157:5: error: expected unqualified-id before ‘if’
make: *** [StatusCheck.o] Error 1

```


```cmake=
make make -C ../../build make[1]: Entering directory 
`/robotis/Linux/build' ar cr ../lib/darwin.a ../../Framework/src/MX28.o 
../../Framework/src/CM730.o ../../Framework/src/math/Matrix.o 
../../Framework/src/math/Plane.o ../../Framework/src/math/Point.o 
../../Framework/src/math/Vector.o ../../Framework/src/motion/JointData.o 
../../Framework/src/motion/Kinematics.o 
../../Framework/src/motion/MotionManager.o 
../../Framework/src/motion/MotionStatus.o 
../../Framework/src/motion/modules/Action.o 
../../Framework/src/motion/modules/Head.o 
../../Framework/src/motion/modules/Walking.o 
../../Framework/src/vision/BallFollower.o 
../../Framework/src/vision/BallTracker.o 
../../Framework/src/vision/ColorFinder.o 
../../Framework/src/vision/Image.o 
../../Framework/src/vision/ImgProcess.o 
../../Framework/src/vision/Camera.o ../../Framework/src/minIni/minIni.o 
streamer/httpd.o streamer/jpeg_utils.o streamer/mjpg_streamer.o 
LinuxActionScript.o LinuxCamera.o LinuxCM730.o LinuxMotionTimer.o 
LinuxNetwork.o make[1]: Leaving directory `/robotis/Linux/build' g++ 
VisionMode.o StatusCheck.o main.o ../../lib/darwin.a -o demo -lpthread -
ljpeg -lrt /usr/lib/gcc/i686-linux-gnu/4.6/../../../i386-linux-
gnu/crt1.o: In function `_start': (.text+0x18): undefined reference to 
`main' collect2: ld returned 1 exit status make: *** [demo] Error 1
```
```cmake=
make -C ../../build
make[1]: Entering directory `/robotis/Linux/build'
g++ -O2 -DLINUX -Wall -shared -I../include -I../../Framework/include
-c -o ../../Framework/src/vision/ColorFinder.o
../../Framework/src/vision/ColorFinder.cpp
../../Framework/src/vision/ColorFinder.cpp: In function
‘Robot::Point2D& GetPosition(Robot::Image*, int&)’:
../../Framework/src/vision/ColorFinder.cpp:131:30: error: declaration
of ‘int count’ shadows a parameter
../../Framework/src/vision/ColorFinder.cpp:133:21: error: ‘Filtering’
was not declared in this scope
../../Framework/src/vision/ColorFinder.cpp:135:24: error: ‘m_result’
was not declared in this scope
../../Framework/src/vision/ColorFinder.cpp:151:45: error:
‘m_min_percent’ was not declared in this scope
../../Framework/src/vision/ColorFinder.cpp:151:106: error:
‘m_max_percent’ was not declared in this scope
../../Framework/src/vision/ColorFinder.cpp:153:8: error:
‘m_center_point’ was not declared in this scope
../../Framework/src/vision/ColorFinder.cpp:158:8: error:
‘m_center_point’ was not declared in this scope
../../Framework/src/vision/ColorFinder.cpp:162:11: error:
‘m_center_point’ was not declared in this scope
../../Framework/src/vision/ColorFinder.cpp:163:1: warning: control
reaches end of non-void function [-Wreturn-type]
make[1]: *** [../../Framework/src/vision/ColorFinder.o] Error 1
make[1]: Leaving directory `/robotis/Linux/build'
make: *** [darwin.a] Error 2
robotis@robotis:/robotis/Linux/project/demo$
```

```cmake=
robotis@robotis:/robotis/Linux/project/demo$ make
make -C ../../build
make[1]: Entering directory `/robotis/Linux/build'
g++ -O2 -DLINUX -Wall -shared -I../include -I../../Framework/include
-c -o ../../Framework/src/vision/ColorFinder.o
../../Framework/src/vision/ColorFinder.cpp
../../Framework/src/vision/ColorFinder.cpp: In member function
‘Robot::Point2D& Robot::ColorFinder::GetPosition(Robot::Image*,
int&)’:
../../Framework/src/vision/ColorFinder.cpp:131:30: error: declaration
of ‘int count’ shadows a parameter
../../Framework/src/vision/ColorFinder.cpp: In member function
‘Robot::Point2D& Robot::ColorFinder::GetPosition(Robot::Image*)’:
../../Framework/src/vision/ColorFinder.cpp:167:2: error: ‘count’ was
not declared in this scope
make[1]: *** [../../Framework/src/vision/ColorFinder.o] Error 1
make[1]: Leaving directory `/robotis/Linux/build'
make: *** [darwin.a] Error 2
robotis@robotis:/robotis/Linux/project/demo$
```


## 模式
### ```StatusCheck.cpp```


```cpp=
/*
 * StatusCheck.cpp
 *
 *  Created on: 2011. 1. 21.
 *      Author: zerom
 */

#include <stdio.h>
#include <unistd.h>

#include "StatusCheck.h"
#include "Head.h"
#include "Action.h"
#include "Walking.h"
#include "MotionStatus.h"
#include "MotionManager.h"
#include "LinuxActionScript.h"

#define PLAY_TIME 120.0
#define REST_TIME 60.0

#define MAX_CHICAGO_CNT 90

using namespace Robot;

int StatusCheck::m_chicago_mode_cnt = 0;

int StatusCheck::m_cur_mode     = READY;
int StatusCheck::m_old_btn      = 0;
int StatusCheck::m_is_started   = 0;

int StatusCheck::m_soccer_sub_mode = SOCCER_PLAY;
double StatusCheck::m_soccer_start_time = 0.0;

void StatusCheck::Check(CM730 &cm730)
{
    struct timeval _tv;
    gettimeofday(&_tv, NULL);
    double _curr_time = _tv.tv_sec + (_tv.tv_usec/1000000.0);

    if(MotionStatus::FALLEN != STANDUP && m_cur_mode == SOCCER && m_is_started != 0)
    {
        Walking::GetInstance()->Stop();
        while(Walking::GetInstance()->IsRunning() == 1) usleep(8000);

        Action::GetInstance()->m_Joint.SetEnableBody(true, true);

        if(MotionStatus::FALLEN == FORWARD)
            Action::GetInstance()->Start(10);   // FORWARD GETUP
        else if(MotionStatus::FALLEN == BACKWARD)
            Action::GetInstance()->Start(11);   // BACKWARD GETUP

        while(Action::GetInstance()->IsRunning() == 1) usleep(8000);

        Head::GetInstance()->m_Joint.SetEnableHeadOnly(true, true);
        Walking::GetInstance()->m_Joint.SetEnableBodyWithoutHead(true, true);
    }

    if(m_cur_mode == SOCCER && m_is_started == 2)
    {
        if(m_soccer_sub_mode == SOCCER_PLAY && (_curr_time - m_soccer_start_time) > PLAY_TIME)
        {
            Walking::GetInstance()->Stop();
            while(Walking::GetInstance()->IsRunning() == true) usleep(8000);

            Action::GetInstance()->m_Joint.SetEnableBody(true, true);

            while(Action::GetInstance()->Start(15) == false) usleep(8000);
            while(Action::GetInstance()->IsRunning() == true) usleep(8000);

            // TODO: Torque OFF??
            cm730.WriteByte(254, MX28::P_TORQUE_ENABLE, 0, NULL);

            m_soccer_sub_mode = SOCCER_REST;
            gettimeofday(&_tv, NULL);
            m_soccer_start_time = _tv.tv_sec + (_tv.tv_usec/1000000.0);
        }
        else if(m_soccer_sub_mode == SOCCER_REST && (_curr_time - m_soccer_start_time) > REST_TIME)
        {
            MotionManager::GetInstance()->Reinitialize();
            MotionManager::GetInstance()->SetEnable(true);
            LinuxActionScript::PlayMP3("../../../Data/mp3/Start soccer demonstration.mp3");

            Action::GetInstance()->m_Joint.SetEnableBody(true, true);

            while(Action::GetInstance()->Start(15) == false) usleep(8000);
            while(Action::GetInstance()->IsRunning() == true) usleep(8000);

            Action::GetInstance()->Start(9);
            while(Action::GetInstance()->IsRunning() == true) usleep(8000);

            Head::GetInstance()->m_Joint.SetEnableHeadOnly(true, true);
            Walking::GetInstance()->m_Joint.SetEnableBodyWithoutHead(true, true);

            MotionManager::GetInstance()->ResetGyroCalibration();
            while(1)
            {
                if(MotionManager::GetInstance()->GetCalibrationStatus() == 1)
                {
                    LinuxActionScript::PlayMP3("../../../Data/mp3/Sensor calibration complete.mp3");
                    break;
                }
                else if(MotionManager::GetInstance()->GetCalibrationStatus() == -1)
                {
                    LinuxActionScript::PlayMP3Wait("../../../Data/mp3/Sensor calibration fail.mp3");
                    MotionManager::GetInstance()->ResetGyroCalibration();
                }
                usleep(8000);
            }

            m_soccer_sub_mode = SOCCER_PLAY;
            gettimeofday(&_tv, NULL);
            m_soccer_start_time = _tv.tv_sec + (_tv.tv_usec/1000000.0);
        }
    }

    if(m_old_btn == MotionStatus::BUTTON)
    {
        if(m_cur_mode == READY && m_is_started == 0 && m_chicago_mode_cnt > MAX_CHICAGO_CNT)
        {
            fprintf(stderr, "CHICAGO MODE ! \n\n");
			m_cur_mode = SOCCER;
			m_old_btn == BTN_START;
        }
        else if(m_cur_mode == READY && m_is_started == 0 && m_chicago_mode_cnt <= MAX_CHICAGO_CNT)
        {
            m_chicago_mode_cnt++;
			return;
        }
		else
        {
            m_chicago_mode_cnt = 0;
            return;
        }
    }
    else
    {
        m_chicago_mode_cnt = 0;
        m_old_btn = MotionStatus::BUTTON;
    }

    if(m_old_btn & BTN_MODE)
    {
        fprintf(stderr, "Mode button pressed.. \n");

        if(m_is_started != 0)
        {
            m_is_started    = 0;
            m_cur_mode      = READY;
            LinuxActionScript::m_stop = 1;

            Walking::GetInstance()->Stop();
            Action::GetInstance()->m_Joint.SetEnableBody(true, true);

            while(Action::GetInstance()->Start(15) == false) usleep(8000);
            while(Action::GetInstance()->IsRunning() == true) usleep(8000);
        }

        else
        {
            m_cur_mode++;
            if(m_cur_mode >= MAX_MODE) m_cur_mode = READY;
        }

        MotionManager::GetInstance()->SetEnable(false);
        usleep(10000);

        if(m_cur_mode == READY)
        {
            cm730.WriteByte(CM730::P_LED_PANNEL, 0x01|0x02|0x04, NULL);
            LinuxActionScript::PlayMP3("../../../Data/mp3/Demonstration ready mode.mp3");
        }
        else if(m_cur_mode == SOCCER)
        {
            cm730.WriteByte(CM730::P_LED_PANNEL, 0x01, NULL);
            LinuxActionScript::PlayMP3("../../../Data/mp3/Autonomous soccer mode.mp3");
        }
        else if(m_cur_mode == MOTION)
        {
            cm730.WriteByte(CM730::P_LED_PANNEL, 0x02, NULL);
            LinuxActionScript::PlayMP3("../../../Data/mp3/Interactive motion mode.mp3");
        }
        else if(m_cur_mode == VISION)
        {
            cm730.WriteByte(CM730::P_LED_PANNEL, 0x04, NULL);
            LinuxActionScript::PlayMP3("../../../Data/mp3/Vision processing mode.mp3");
        }
        else if(m_cur_mode == NEW_MODE) //adding LED and play mp3 for new mode
        {
            cm730.WriteByte(CM730::P_LED_PANNEL, 0x01|0x04, NULL);
            //Signaling Darwin OP 2 which LED to turn on
            LinuxActionScript::PlayMP3("../../../Data/mp3/New_Mode mode.mp3");
            //play an mp3 file (you can use any mp3 file but make sure file name matches)
        }
    }

    if(m_old_btn & BTN_START)
    {
        if(m_is_started == 0)
        {
            fprintf(stderr, "Start button pressed.. & started is false.. \n");

            if(m_cur_mode == SOCCER)
            {
                MotionManager::GetInstance()->Reinitialize();
                MotionManager::GetInstance()->SetEnable(true);
                if(m_chicago_mode_cnt > MAX_CHICAGO_CNT)
                {
				    m_chicago_mode_cnt = 0;
                    m_is_started = 2;
                }
				else
                    m_is_started = 1;
                LinuxActionScript::PlayMP3("../../../Data/mp3/Start soccer demonstration.mp3");

                Action::GetInstance()->m_Joint.SetEnableBody(true, true);

                Action::GetInstance()->Start(9);
                while(Action::GetInstance()->IsRunning() == true) usleep(8000);

                Head::GetInstance()->m_Joint.SetEnableHeadOnly(true, true);
                Walking::GetInstance()->m_Joint.SetEnableBodyWithoutHead(true, true);

                MotionManager::GetInstance()->ResetGyroCalibration();
                while(1)
                {
                    if(MotionManager::GetInstance()->GetCalibrationStatus() == 1)
                    {
                        LinuxActionScript::PlayMP3("../../../Data/mp3/Sensor calibration complete.mp3");
                        break;
                    }
                    else if(MotionManager::GetInstance()->GetCalibrationStatus() == -1)
                    {
                        LinuxActionScript::PlayMP3Wait("../../../Data/mp3/Sensor calibration fail.mp3");
                        MotionManager::GetInstance()->ResetGyroCalibration();
                    }
                    usleep(8000);
                }

                m_soccer_sub_mode = SOCCER_PLAY;
                gettimeofday(&_tv, NULL);
                m_soccer_start_time = _tv.tv_sec + (_tv.tv_usec/1000000.0);
            }
            else if(m_cur_mode == MOTION)
            {
                MotionManager::GetInstance()->Reinitialize();
                MotionManager::GetInstance()->SetEnable(true);
                m_is_started = 1;
                LinuxActionScript::PlayMP3("../../../Data/mp3/Start motion demonstration.mp3");

                // Joint Enable..
                Action::GetInstance()->m_Joint.SetEnableBody(true, true);

                Action::GetInstance()->Start(1);
                while(Action::GetInstance()->IsRunning() == true) usleep(8000);
            }
            else if(m_cur_mode == VISION)
            {
                MotionManager::GetInstance()->Reinitialize();
                MotionManager::GetInstance()->SetEnable(true);
                m_is_started = 1;
                LinuxActionScript::PlayMP3("../../../Data/mp3/Start vision processing demonstration.mp3");

                // Joint Enable...
                Action::GetInstance()->m_Joint.SetEnableBody(true, true);

                Action::GetInstance()->Start(1);
                while(Action::GetInstance()->IsRunning() == true) usleep(8000);
            }
            else if(m_cur_mode == NEW_MODE)
              {
                  MotionManager::GetInstance()->Reinitialize();
                  MotionManager::GetInstance()->SetEnable(true);
                  //initialize and enable MotionManager class
                  m_is_started = 1;
                  LinuxActionScript::PlayMP3("../../../Data/mp3/Start New_Mode demonstration.mp3");
                  //play an mp3 file (you can use any mp3 file but make sure file name matches)

                  // Joint Enable...
                  Action::GetInstance()->m_Joint.SetEnableBody(true, true);

                  Action::GetInstance()->Start(9);
                  while(Action::GetInstance()->IsRunning() == true) usleep(8000);

                  Head::GetInstance()->m_Joint.SetEnableHeadOnly(true, true);
                  Walking::GetInstance()->m_Joint.SetEnableBodyWithoutHead(true, true);
                  //Reset Gyro sensor
                  MotionManager::GetInstance()->ResetGyroCalibration();
                  while(1)
                  {
                      if(MotionManager::GetInstance()->GetCalibrationStatus() == 1)
                      {
                          LinuxActionScript::PlayMP3("../../../Data/mp3/Sensor calibration complete.mp3");
                          break;
                      }
                      else if(MotionManager::GetInstance()->GetCalibrationStatus() == -1)
                      {
                          LinuxActionScript::PlayMP3Wait("../../../Data/mp3/Sensor calibration fail.mp3");
                          MotionManager::GetInstance()->ResetGyroCalibration();
                      }
                      usleep(8000);
                  }
        }
        else
        {
            fprintf(stderr, "Start button pressed.. & started is true.. \n");
        }
    }
}
}
```

### main.cpp

```cpp=
/*
 * main.cpp
 *
 *  Created on: 2011. 1. 4.
 *      Author: robotis
 */

#include <stdio.h>
#include <unistd.h>
#include <limits.h>
#include <string.h>
#include <libgen.h>
#include <signal.h>

#include "mjpg_streamer.h"
#include "LinuxDARwIn.h"

#include "StatusCheck.h"
#include "VisionMode.h"

#ifdef MX28_1024
#define MOTION_FILE_PATH    "../../../Data/motion_1024.bin"
#else
#define MOTION_FILE_PATH    "../../../Data/motion_4096.bin"
#endif

#define INI_FILE_PATH       "../../../Data/config.ini"
#define SCRIPT_FILE_PATH    "script.asc"

#define U2D_DEV_NAME0       "/dev/ttyUSB0"
#define U2D_DEV_NAME1       "/dev/ttyUSB1"

LinuxCM730 linux_cm730(U2D_DEV_NAME0);
CM730 cm730(&linux_cm730);

void change_current_dir()
{
    char exepath[1024] = {0};
    if(readlink("/proc/self/exe", exepath, sizeof(exepath)) != -1)
    {
        if(chdir(dirname(exepath)))
            fprintf(stderr, "chdir error!! \n");
    }
}

void sighandler(int sig)
{
    exit(0);
}

int main(void)
{
    signal(SIGABRT, &sighandler);
    signal(SIGTERM, &sighandler);
    signal(SIGQUIT, &sighandler);
    signal(SIGINT, &sighandler);

    change_current_dir();

    minIni* ini = new minIni(INI_FILE_PATH);
    Image* rgb_output = new Image(Camera::WIDTH, Camera::HEIGHT, Image::RGB_PIXEL_SIZE);

    LinuxCamera::GetInstance()->Initialize(0);
    LinuxCamera::GetInstance()->SetCameraSettings(CameraSettings());    // set default
    LinuxCamera::GetInstance()->LoadINISettings(ini);                   // load from ini

    mjpg_streamer* streamer = new mjpg_streamer(Camera::WIDTH, Camera::HEIGHT);

    ColorFinder* ball_finder = new ColorFinder();
    ball_finder->LoadINISettings(ini);
    httpd::ball_finder = ball_finder;

    BallTracker tracker = BallTracker();
    BallFollower follower = BallFollower();

    ColorFinder* red_finder = new ColorFinder(0, 15, 45, 0, 0.3, 50.0);
    red_finder->LoadINISettings(ini, "RED");
    httpd::red_finder = red_finder;

    ColorFinder* yellow_finder = new ColorFinder(60, 15, 45, 0, 0.3, 50.0);
    yellow_finder->LoadINISettings(ini, "YELLOW");
    httpd::yellow_finder = yellow_finder;

    ColorFinder* blue_finder = new ColorFinder(225, 15, 45, 0, 0.3, 50.0);
    blue_finder->LoadINISettings(ini, "BLUE");
    httpd::blue_finder = blue_finder;

    httpd::ini = ini;

    //////////////////// Framework Initialize ////////////////////////////
    if(MotionManager::GetInstance()->Initialize(&cm730) == false)
    {
        linux_cm730.SetPortName(U2D_DEV_NAME1);
        if(MotionManager::GetInstance()->Initialize(&cm730) == false)
        {
            printf("Fail to initialize Motion Manager!\n");
            return 0;
        }
    }

    Walking::GetInstance()->LoadINISettings(ini);

    MotionManager::GetInstance()->AddModule((MotionModule*)Action::GetInstance());
    MotionManager::GetInstance()->AddModule((MotionModule*)Head::GetInstance());
    MotionManager::GetInstance()->AddModule((MotionModule*)Walking::GetInstance());

    LinuxMotionTimer *motion_timer = new LinuxMotionTimer(MotionManager::GetInstance());
    motion_timer->Start();
    /////////////////////////////////////////////////////////////////////
    
    MotionManager::GetInstance()->LoadINISettings(ini);

    int firm_ver = 0;
    if(cm730.ReadByte(JointData::ID_HEAD_PAN, MX28::P_VERSION, &firm_ver, 0)  != CM730::SUCCESS)
    {
        fprintf(stderr, "Can't read firmware version from Dynamixel ID %d!! \n\n", JointData::ID_HEAD_PAN);
        exit(0);
    }

    if(0 < firm_ver && firm_ver < 27)
    {
#ifdef MX28_1024
        Action::GetInstance()->LoadFile(MOTION_FILE_PATH);
#else
        fprintf(stderr, "MX-28's firmware is not support 4096 resolution!! \n");
        fprintf(stderr, "Upgrade MX-28's firmware to version 27(0x1B) or higher.\n\n");
        exit(0);
#endif
    }
    else if(27 <= firm_ver)
    {
#ifdef MX28_1024
        fprintf(stderr, "MX-28's firmware is not support 1024 resolution!! \n");
        fprintf(stderr, "Remove '#define MX28_1024' from 'MX28.h' file and rebuild.\n\n");
        exit(0);
#else
        Action::GetInstance()->LoadFile((char*)MOTION_FILE_PATH);
#endif
    }
    else
        exit(0);

    Action::GetInstance()->m_Joint.SetEnableBody(true, true);
    MotionManager::GetInstance()->SetEnable(true);

    cm730.WriteByte(CM730::P_LED_PANNEL, 0x01|0x02|0x04, NULL);

    LinuxActionScript::PlayMP3("../../../Data/mp3/Demonstration ready mode.mp3");
    Action::GetInstance()->Start(15);
    while(Action::GetInstance()->IsRunning()) usleep(8*1000);

    int _ball_found = 0;
    while(1)
    {
        StatusCheck::Check(cm730);

        Point2D ball_pos, red_pos, yellow_pos, blue_pos;

        LinuxCamera::GetInstance()->CaptureFrame();
        memcpy(rgb_output->m_ImageData, LinuxCamera::GetInstance()->fbuffer->m_RGBFrame->m_ImageData, LinuxCamera::GetInstance()->fbuffer->m_RGBFrame->m_ImageSize);

        if(StatusCheck::m_cur_mode == READY || StatusCheck::m_cur_mode == VISION)
        {
            ball_pos = ball_finder->GetPosition(LinuxCamera::GetInstance()->fbuffer->m_HSVFrame);
            red_pos = red_finder->GetPosition(LinuxCamera::GetInstance()->fbuffer->m_HSVFrame);
            yellow_pos = yellow_finder->GetPosition(LinuxCamera::GetInstance()->fbuffer->m_HSVFrame);
            blue_pos = blue_finder->GetPosition(LinuxCamera::GetInstance()->fbuffer->m_HSVFrame);

            unsigned char r, g, b;
            for(int i = 0; i < rgb_output->m_NumberOfPixels; i++)
            {
                r = 0; g = 0; b = 0;
                if(ball_finder->m_result->m_ImageData[i] == 1)
                {
                    r = 255;
                    g = 128;
                    b = 0;
                }
                if(red_finder->m_result->m_ImageData[i] == 1)
                {
                    if(ball_finder->m_result->m_ImageData[i] == 1)
                    {
                        r = 0;
                        g = 255;
                        b = 0;
                    }
                    else
                    {
                        r = 255;
                        g = 0;
                        b = 0;
                    }
                }
                if(yellow_finder->m_result->m_ImageData[i] == 1)
                {
                    if(ball_finder->m_result->m_ImageData[i] == 1)
                    {
                        r = 0;
                        g = 255;
                        b = 0;
                    }
                    else
                    {
                        r = 255;
                        g = 255;
                        b = 0;
                    }
                }
                if(blue_finder->m_result->m_ImageData[i] == 1)
                {
                    if(ball_finder->m_result->m_ImageData[i] == 1)
                    {
                        r = 0;
                        g = 255;
                        b = 0;
                    }
                    else
                    {
                        r = 0;
                        g = 0;
                        b = 255;
                    }
                }

                if(r > 0 || g > 0 || b > 0)
                {
                    rgb_output->m_ImageData[i * rgb_output->m_PixelSize + 0] = r;
                    rgb_output->m_ImageData[i * rgb_output->m_PixelSize + 1] = g;
                    rgb_output->m_ImageData[i * rgb_output->m_PixelSize + 2] = b;
                }
            }
        }
        else if(StatusCheck::m_cur_mode == SOCCER)
        {
            //tracker.Process(ball_finder->GetPosition(LinuxCamera::GetInstance()->fbuffer->m_HSVFrame));
            _ball_found = tracker.SearchAndTracking(ball_finder->GetPosition(LinuxCamera::GetInstance()->fbuffer->m_HSVFrame));

            for(int i = 0; i < rgb_output->m_NumberOfPixels; i++)
            {
                if(ball_finder->m_result->m_ImageData[i] == 1)
                {
                    rgb_output->m_ImageData[i*rgb_output->m_PixelSize + 0] = 255;
                    rgb_output->m_ImageData[i*rgb_output->m_PixelSize + 1] = 128;
                    rgb_output->m_ImageData[i*rgb_output->m_PixelSize + 2] = 0;
                }
            }
        }

        streamer->send_image(rgb_output);

        if(StatusCheck::m_is_started == 0)
            continue;

        switch(StatusCheck::m_cur_mode)
        {
        case READY:
            break;
        case SOCCER:
            if(Action::GetInstance()->IsRunning() == 0 &&
                    StatusCheck::m_soccer_sub_mode == SOCCER_PLAY)
            {
                Head::GetInstance()->m_Joint.SetEnableHeadOnly(true, true);
                Walking::GetInstance()->m_Joint.SetEnableBodyWithoutHead(true, true);
                
                if(Walking::GetInstance()->IsRunning() == false && _ball_found != 1){
            		Walking::GetInstance()->X_MOVE_AMPLITUDE = -1.0;
            		Walking::GetInstance()->A_MOVE_AMPLITUDE = 0.0;
            		Walking::GetInstance()->Start();
            	}

                if(_ball_found == 1)
                {
                    follower.Process(tracker.ball_position);

                    if(follower.KickBall != 0)
                    {
                        Head::GetInstance()->m_Joint.SetEnableHeadOnly(true, true);
                        Action::GetInstance()->m_Joint.SetEnableBodyWithoutHead(true, true);

                        if(follower.KickBall == -1)
                        {
                            Action::GetInstance()->Start(12);   // RIGHT KICK
                            fprintf(stderr, "RightKick! \n");
                        }
                        else if(follower.KickBall == 1)
                        {
                            Action::GetInstance()->Start(13);   // LEFT KICK
                            fprintf(stderr, "LeftKick! \n");
                        }
                    }
                }
                else if(_ball_found == -1)
                {
            		Walking::GetInstance()->X_MOVE_AMPLITUDE = -1.0;
            		Walking::GetInstance()->A_MOVE_AMPLITUDE = 10.0;
                }
                else
                {
            		Walking::GetInstance()->X_MOVE_AMPLITUDE = -1.0;
            		Walking::GetInstance()->A_MOVE_AMPLITUDE = 0.0;
                }
            }
            break;
        case MOTION:
            if(LinuxActionScript::m_is_running == 0)
                LinuxActionScript::ScriptStart(SCRIPT_FILE_PATH);
            break;
        case VISION:
            int detected_color = 0;
            detected_color |= (red_pos.X == -1)? 0 : VisionMode::RED;
            detected_color |= (yellow_pos.X == -1)? 0 : VisionMode::YELLOW;
            detected_color |= (blue_pos.X == -1)? 0 : VisionMode::BLUE;

            if(Action::GetInstance()->IsRunning() == 0)
                VisionMode::Play(detected_color);
            break;
        case NEW_MODE:
          //implement new codes here to execute after pressing start button
            break;
        }
    }

    return 0;
}

```

### ```StatusCheck.h```
```cpp=
/*
 * StatusCheck.h
 *
 *  Created on: 2011. 1. 21.
 *      Author: zerom
 */

#ifndef STATUSCHECK_H_
#define STATUSCHECK_H_

#include <sys/time.h>
#include "CM730.h"

namespace Robot
{
    enum {
        INITIAL,
        READY,
        SOCCER,
        MOTION,
        VISION,
        NEW_MODE,
        MAX_MODE
    };

    enum {
    	SOCCER_PLAY,   
		SOCCER_REST
    };

    enum {
        BTN_MODE = 1,
        BTN_START = 2
    };

    class StatusCheck {
    private:
        static int m_old_btn;
        static int m_chicago_mode_cnt;

    public:
        static int m_cur_mode;
        static int m_is_started;

        static int 	    m_soccer_sub_mode;
        static double   m_soccer_start_time;

        static void Check(CM730 &cm730);
    };
}

#endif /* STATUSCHECK_H_ */
```



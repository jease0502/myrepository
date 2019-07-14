---
slideOptions:
transition: slide
tags: ros
---
# 第三份op2紀錄

_marker_found = marker_tracker.SearchAndTracking(center);
streamer->send_image(rgb_output);


## 中文註釋

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

#ifdef MX28_1024 //設定頻率
#define MOTION_FILE_PATH    "../../../Data/motion_1024.bin"
#else
#define MOTION_FILE_PATH    "../../../Data/motion_4096.bin"
#endif

#define INI_FILE_PATH       "../../../Data/config.ini"
#define SCRIPT_FILE_PATH    "script.asc"

#define U2D_DEV_NAME0       "/dev/ttyUSB0"
#define U2D_DEV_NAME1       "/dev/ttyUSB1"


//設定頻率跟宣告一些函式庫

LinuxCM730 linux_cm730(U2D_DEV_NAME0);
CM730 cm730(&linux_cm730);

//呼叫板子跟相機

void change_current_dir()
{
    char exepath[1024] = {0};
    if(readlink("/proc/self/exe", exepath, sizeof(exepath)) != -1)
    {
        if(chdir(dirname(exepath)))
            fprintf(stderr, "chdir error!! \n");
    }
}

//改變當前工作目錄

void sighandler(int sig)
{
    exit(0);
}


//)設置一個函數來處理信號，即信號數量sig的信號處理程序

int main(void)
{
    signal(SIGABRT, &sighandler);  //是中止一个程序
    signal(SIGTERM, &sighandler);  //终止进程 软件终止信号
    signal(SIGQUIT, &sighandler);  //终止进程 软件终止信号
    signal(SIGINT, &sighandler);   //ctrl+c中斷
    //uint count_to_stop=0;        //我設置的段點目前沒用到了

    change_current_dir();

    minIni* ini = new minIni(INI_FILE_PATH);  
    Image* rgb_output = new Image(Camera::WIDTH, Camera::HEIGHT, Image::RGB_PIXEL_SIZE);

    //new 函釋用於動態配置

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

    ColorFinder* green_finder = new ColorFinder(120, 45, 35, 0, 0.3, 40.0);
    ColorFinder* blue_finder = new ColorFinder(225, 15, 45, 0, 0.3, 50.0);
    BallTracker marker_tracker = BallTracker();
    //created a new BallTracker object to use camera tracking
    BallFollower marker_follower = BallFollower();
    //created a new BallFollower object to follow target/marker
    int _marker_found = 0;
    blue_finder->LoadINISettings(ini, "BLUE");
    httpd::blue_finder = blue_finder;

    httpd::ini = ini;
    //上面是在設定顏色
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

    //利用motion manger去控制偵測機器人是否正常

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

    //去偵測是那一顆馬達有問題

    Action::GetInstance()->m_Joint.SetEnableBody(true, true);
    MotionManager::GetInstance()->SetEnable(true);

    cm730.WriteByte(CM730::P_LED_PANNEL, 0x01|0x02|0x04, NULL);

    LinuxActionScript::PlayMP3("../../../Data/mp3/Demonstration ready mode.mp3");
    Action::GetInstance()->Start(15);
    while(Action::GetInstance()->IsRunning()) usleep(8*1000);


    //初始狀態結束

    int _ball_found = 0;

    while(1)
    {
        StatusCheck::Check(cm730);
        int greenCount = 0, blueCount = 0;
        //created 2 int to store filtered pixel counts
        Point2D green, blue, center;
        //created 3 objects of Point2D class
        Point2D ball_pos, red_pos, yellow_pos, blue_pos;

        LinuxCamera::GetInstance()->CaptureFrame(); //去捕捉剛剛線上調整顏色的數值
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

        else if(StatusCheck::m_cur_mode == HONOR) //under a new mode called HONOR
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
                case NEW_MODE:
          //implement new codes here to execute after pressing start button
            break;
        case HONOR:
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
                        Walking::GetInstance()->Stop();
                        if(greenCount >= 10500 || blueCount >= 10500)
                        //pixel count can be used to approximate distance, but in this case,
                        //this stop condition is sufficient
                        {
                            Walking::GetInstance()->Stop();
                            while(Walking::GetInstance()->IsRunning() == true) usleep(1000000);
                        //--------------------------back---------------------------------------
                        
                            if(_ball_found != 1)
                            {
                                while (1)
                                {
                                    Walking::GetInstance()->X_MOVE_AMPLITUDE = -30.0;
                                    //Set forward and back step length to 30cm
                    
                                    Walking::GetInstance()->A_MOVE_AMPLITUDE = 0.0;
                                    //Set yaw step length to 0
                    
                                    Walking::GetInstance()->Start();
                                }
                           
                            }
                            //---------------------------------------------------------------------
                            fprintf(stderr, "stop\n");
                        }
                 else
                 {
                     Walking::GetInstance()->X_MOVE_AMPLITUDE = 30.0;
                     Walking::GetInstance()->A_MOVE_AMPLITUDE = 0.0;
                 }
             }}break;

        case VISION:
            int detected_color = 0;
            detected_color |= (red_pos.X == -1)? 0 : VisionMode::RED;
            detected_color |= (yellow_pos.X == -1)? 0 : VisionMode::YELLOW;
            detected_color |= (blue_pos.X == -1)? 0 : VisionMode::BLUE;

            if(Action::GetInstance()->IsRunning() == 0)
                VisionMode::Play(detected_color);
            break;

    }
    }

    return 0;
}
    
```


## 足球防守

```Action::GetInstance()->Start(12);``` 執行動作編輯器動做

足球防守姿勢
- 左仆倒+右仆倒+躺下+起來+手舉平
- 18、19、90、91、10、11、23、24、25

需要增加的動做
- 1.徹身走路
-  2.低頭


## 新增馬達

1. 先使用USB2B把馬達刷過一次，增加編碼
2. 安裝上去之後，打開```Framework```下```INCLUDE```裡面的```Joindata```
3. 增加馬達名稱跟編號上去
4. 把所有.o黨移除```find -name .o* -delete```
5. 在dxl_moitor裡面更改cmd_proccess.cpp ，增加兩組case
```cpp=
#include <stdio.h>
#include <string.h>
#include "cmd_process.h"

using namespace Robot;

extern int gID;

const char *GetIDString(int id)
{
	switch(id)
	{
	case JointData::ID_R_SHOULDER_PITCH:
		return "R_SHOULDER_PITCH";

	case JointData::ID_L_SHOULDER_PITCH:
		return "L_SHOULDER_PITCH";

	case JointData::ID_R_SHOULDER_ROLL:
		return "R_SHOULDER_ROLL";

	case JointData::ID_L_SHOULDER_ROLL:
		return "L_SHOULDER_ROLL";

	case JointData::ID_R_ELBOW:
		return "R_ELBOW";

	case JointData::ID_L_ELBOW:
		return "L_ELBOW";

	case JointData::ID_R_HIP_YAW:
		return "R_HIP_YAW";

	case JointData::ID_L_HIP_YAW:
		return "L_HIP_YAW";

	case JointData::ID_R_HIP_ROLL:
		return "R_HIP_ROLL";

	case JointData::ID_L_HIP_ROLL:
		return "L_HIP_ROLL";

	case JointData::ID_R_HIP_PITCH:
		return "R_HIP_PITCH";

	case JointData::ID_L_HIP_PITCH:
		return "L_HIP_PITCH";

	case JointData::ID_R_KNEE:
		return "R_KNEE";

	case JointData::ID_L_KNEE:
		return "L_KNEE";

	case JointData::ID_R_ANKLE_PITCH:
		return "R_ANKLE_PITCH";

	case JointData::ID_L_ANKLE_PITCH:
		return "L_ANKLE_PITCH";

	case JointData::ID_R_ANKLE_ROLL:
		return "R_ANKLE_ROLL";

	case JointData::ID_L_ANKLE_ROLL:
		return "L_ANKLE_ROLL";

	case JointData::ID_HEAD_PAN:
		return "HEAD_PAN";

	case JointData::ID_HEAD_TILT:
		return "HEAD_TILT";

	case JointData::ID_HAND_RIGHT:
		return "HAND_RIGHT";

	case JointData::ID_HAND_LEFT:
		return "HAND_LEFT";

	case CM730::ID_CM:
		return "SUB_BOARD";
	}

	return "UNKNOWN";
}

void Prompt(int id)
{
	printf( "\r[ID:%d(%s)] ", id, GetIDString(id) );
}

void Help()
{
	printf( "\n" );
	printf( " exit : Exits the program\n" );
	printf( " scan : Outputs the current status of all Dynamixels\n" );
	printf( " id [ID] : Go to [ID]\n" );
	printf( " d : Dumps the current control table of CM-730 and all Dynamixels\n" );
	printf( " reset : Defaults the value of current Dynamixel\n" );
	printf( " reset all : Defaults the value of all Dynamixels\n" );
	printf( " wr [ADDR] [VALUE] : Writes value [VALUE] to address [ADDR] of current Dynamixel\n" );
	printf( " on/off : Turns torque on/off of current Dynamixel\n" );
	printf( " on/off all : Turns torque on/off of all Dynamixels)\n" );
	printf( "\n       Copyright ROBOTIS CO.,LTD.\n\n" );
}

void Scan(CM730 *cm730)
{
	printf("\n");

	for(int id=1; id<254; id++)
	{
        if(cm730->Ping(id, 0) == CM730::SUCCESS)
        {
            printf("                                  ... OK\r");
            printf(" Check ID:%d(%s)\n", id, GetIDString(id));
        }
        else if(id < JointData::NUMBER_OF_JOINTS || id == CM730::ID_CM)
        {
            printf("                                  ... FAIL\r");
            printf(" Check ID:%d(%s)\n", id, GetIDString(id));
        }
	}

	printf("\n");
}

void Dump(CM730 *cm730, int id)
{
	unsigned char table[128];
	int addr;
	int value;


	if(id == CM730::ID_CM) // Sub board
	{
		if(cm730->ReadTable(id, CM730::P_MODEL_NUMBER_L, CM730::P_RIGHT_MIC_H, &table[CM730::P_MODEL_NUMBER_L], 0) != CM730::SUCCESS)
		{
			printf(" Can not read table!\n");
			return;
		}

		printf( "\n" );
		printf( " [EEPROM AREA]\n" );
		addr = CM730::P_MODEL_NUMBER_L; value = CM730::MakeWord(table[addr], table[addr+1]);
		printf( " MODEL_NUMBER            (R) [%.3d]:%5d (L:0x%.2X H:0x%.2X)\n", addr, value, table[addr], table[addr+1]);
		addr = CM730::P_VERSION; value = table[addr];
		printf( " VERSION                 (R) [%.3d]:%5d\n", addr, value);
		addr = CM730::P_ID; value = table[addr];
		printf( " ID                     (R/W)[%.3d]:%5d\n", addr, value);
		addr = CM730::P_BAUD_RATE; value = table[addr];
		printf( " BAUD_RATE              (R/W)[%.3d]:%5d\n", addr, value);
		addr = CM730::P_RETURN_DELAY_TIME; value = table[addr];
		printf( " RETURN_DELAY_TIME      (R/W)[%.3d]:%5d\n", addr, value);
		addr = CM730::P_RETURN_LEVEL; value = table[addr];
		printf( " RETURN_LEVEL           (R/W)[%.3d]:%5d\n", addr, value);
		printf( "\n" );
		printf( " [RAM AREA]\n" );
		addr = CM730::P_DXL_POWER; value = table[addr];
		printf( " DXL_POWER              (R/W)[%.3d]:%5d\n", addr, value);
		addr = CM730::P_LED_PANNEL; value = table[addr];
		printf( " LED_PANNEL             (R/W)[%.3d]:%5d\n", addr, value);
		addr = CM730::P_LED_HEAD_L; value = CM730::MakeWord(table[addr], table[addr+1]);
		printf( " LED_HEAD               (R/W)[%.3d]:%5d (L:0x%.2X H:0x%.2X)\n", addr, value, table[addr], table[addr+1]);
		addr = CM730::P_LED_EYE_L; value = CM730::MakeWord(table[addr], table[addr+1]);
		printf( " LED_EYE                (R/W)[%.3d]:%5d (L:0x%.2X H:0x%.2X)\n", addr, value, table[addr], table[addr+1]);
		addr = CM730::P_BUTTON; value = table[addr];
		printf( " BUTTON                  (R) [%.3d]:%5d\n", addr, value);
		addr = CM730::P_GYRO_Z_L; value = CM730::MakeWord(table[addr], table[addr+1]);
		printf( " GYRO_Z                  (R) [%.3d]:%5d (L:0x%.2X H:0x%.2X)\n", addr, value, table[addr], table[addr+1]);
		addr = CM730::P_GYRO_Y_L; value = CM730::MakeWord(table[addr], table[addr+1]);
		printf( " GYRO_Y                  (R) [%.3d]:%5d (L:0x%.2X H:0x%.2X)\n", addr, value, table[addr], table[addr+1]);
		addr = CM730::P_GYRO_X_L; value = CM730::MakeWord(table[addr], table[addr+1]);
		printf( " GYRO_X                  (R) [%.3d]:%5d (L:0x%.2X H:0x%.2X)\n", addr, value, table[addr], table[addr+1]);
		addr = CM730::P_ACCEL_X_L; value = CM730::MakeWord(table[addr], table[addr+1]);
		printf( " ACCEL_X                 (R) [%.3d]:%5d (L:0x%.2X H:0x%.2X)\n", addr, value, table[addr], table[addr+1]);
		addr = CM730::P_ACCEL_Y_L; value = CM730::MakeWord(table[addr], table[addr+1]);
		printf( " ACCEL_Y                 (R) [%.3d]:%5d (L:0x%.2X H:0x%.2X)\n", addr, value, table[addr], table[addr+1]);
		addr = CM730::P_ACCEL_Z_L; value = CM730::MakeWord(table[addr], table[addr+1]);
		printf( " ACCEL_Z                 (R) [%.3d]:%5d (L:0x%.2X H:0x%.2X)\n", addr, value, table[addr], table[addr+1]);
        addr = CM730::P_VOLTAGE; value = table[addr];
        printf( " VOLTAGE                 (R) [%.3d]:%5d\n", addr, value);
		addr = CM730::P_LEFT_MIC_L; value = CM730::MakeWord(table[addr], table[addr+1]);
		printf( " LEFT_MIC                (R) [%.3d]:%5d (L:0x%.2X H:0x%.2X)\n", addr, value, table[addr], table[addr+1]);
		addr = CM730::P_RIGHT_MIC_L; value = CM730::MakeWord(table[addr], table[addr+1]);
		printf( " RIGHT_MIC               (R) [%.3d]:%5d (L:0x%.2X H:0x%.2X)\n", addr, value, table[addr], table[addr+1]);

		printf( "\n" );
	}
	else // Actuator
	{		
		if(cm730->ReadTable(id, MX28::P_MODEL_NUMBER_L, MX28::P_PUNCH_H, &table[MX28::P_MODEL_NUMBER_L], 0) != CM730::SUCCESS)
		{
			printf(" Can not read table!\n");
			return;
		}

		printf( "\n" );
		printf( " [EEPROM AREA]\n" );
		addr = MX28::P_MODEL_NUMBER_L; value = CM730::MakeWord(table[addr], table[addr+1]);
		printf( " MODEL_NUMBER            (R) [%.3d]:%5d (L:0x%.2X H:0x%.2X)\n", addr, value, table[addr], table[addr+1]);
		addr = MX28::P_VERSION; value = table[addr];
		printf( " VERSION                 (R) [%.3d]:%5d\n", addr, value);
		addr = MX28::P_ID; value = table[addr];
		printf( " ID                     (R/W)[%.3d]:%5d\n", addr, value);
		addr = MX28::P_BAUD_RATE; value = table[addr];
		printf( " BAUD_RATE              (R/W)[%.3d]:%5d\n", addr, value);
		addr = MX28::P_RETURN_DELAY_TIME; value = table[addr];
		printf( " RETURN_DELAY_TIME      (R/W)[%.3d]:%5d\n", addr, value);
		addr = MX28::P_CW_ANGLE_LIMIT_L; value = CM730::MakeWord(table[addr], table[addr+1]);
		printf( " CW_ANGLE_LIMIT         (R/W)[%.3d]:%5d (L:0x%.2X H:0x%.2X)\n", addr, value, table[addr], table[addr+1]);
		addr = MX28::P_CCW_ANGLE_LIMIT_L; value = CM730::MakeWord(table[addr], table[addr+1]);
		printf( " CCW_ANGLE_LIMIT        (R/W)[%.3d]:%5d (L:0x%.2X H:0x%.2X)\n", addr, value, table[addr], table[addr+1]);
		addr = MX28::P_HIGH_LIMIT_TEMPERATURE; value = table[addr];
		printf( " HIGH_LIMIT_TEMPERATURE (R/W)[%.3d]:%5d\n", addr, value);
		addr = MX28::P_LOW_LIMIT_VOLTAGE; value = table[addr];
		printf( " LOW_LIMIT_VOLTAGE      (R/W)[%.3d]:%5d\n", addr, value);
		addr = MX28::P_HIGH_LIMIT_VOLTAGE; value = table[addr];
		printf( " HIGH_LIMIT_VOLTAGE     (R/W)[%.3d]:%5d\n", addr, value);
		addr = MX28::P_MAX_TORQUE_L; value = CM730::MakeWord(table[addr], table[addr+1]);
		printf( " MAX_TORQUE             (R/W)[%.3d]:%5d (L:0x%.2X H:0x%.2X)\n", addr, value, table[addr], table[addr+1]);
		addr = MX28::P_RETURN_LEVEL; value = table[addr];
		printf( " RETURN_LEVEL           (R/W)[%.3d]:%5d\n", addr, value);
		addr = MX28::P_ALARM_LED; value = table[addr];
		printf( " ALARM_LED              (R/W)[%.3d]:%5d\n", addr, value);
		addr = MX28::P_ALARM_SHUTDOWN; value = table[addr];
		printf( " ALARM_SHUTDOWN         (R/W)[%.3d]:%5d\n", addr, value);
		printf( "\n" );
		printf( " [RAM AREA]\n" );
		addr = MX28::P_TORQUE_ENABLE; value = table[addr];
		printf( " TORQUE_ENABLE          (R/W)[%.3d]:%5d\n", addr, value);
		addr = MX28::P_LED; value = table[addr];
		printf( " LED                    (R/W)[%.3d]:%5d\n", addr, value);
#ifdef MX28_1024
		addr = MX28::P_CW_COMPLIANCE_MARGIN; value = table[addr];
		printf( " CW_COMPLIANCE_MARGIN   (R/W)[%.3d]:%5d\n", addr, value);
		addr = MX28::P_CCW_COMPLIANCE_MARGIN; value = table[addr];
		printf( " CCW_COMPLIANCE_MARGIN  (R/W)[%.3d]:%5d\n", addr, value);
		addr = MX28::P_CW_COMPLIANCE_SLOPE; value = table[addr];
		printf( " CW_COMPLIANCE_SLOPE    (R/W)[%.3d]:%5d\n", addr, value);
		addr = MX28::P_CCW_COMPLIANCE_SLOPE; value = table[addr];
		printf( " CCW_COMPLIANCE_SLOPE   (R/W)[%.3d]:%5d\n", addr, value);
#else
        addr = MX28::P_D_GAIN; value = table[addr];
        printf( " D_GAIN                 (R/W)[%.3d]:%5d\n", addr, value);
        addr = MX28::P_I_GAIN; value = table[addr];
        printf( " I_GAIN                 (R/W)[%.3d]:%5d\n", addr, value);
        addr = MX28::P_P_GAIN; value = table[addr];
        printf( " P_GAIN                 (R/W)[%.3d]:%5d\n", addr, value);
        addr = MX28::P_RESERVED; value = table[addr];
        printf( " RESERVED               (R/W)[%.3d]:%5d\n", addr, value);
#endif
		addr = MX28::P_GOAL_POSITION_L; value = CM730::MakeWord(table[addr], table[addr+1]);
		printf( " GOAL_POSITION          (R/W)[%.3d]:%5d (L:0x%.2X H:0x%.2X)\n", addr, value, table[addr], table[addr+1]);
		addr = MX28::P_MOVING_SPEED_L; value = CM730::MakeWord(table[addr], table[addr+1]);
		printf( " MOVING_SPEED           (R/W)[%.3d]:%5d (L:0x%.2X H:0x%.2X)\n", addr, value, table[addr], table[addr+1]);
		addr = MX28::P_TORQUE_LIMIT_L; value = CM730::MakeWord(table[addr], table[addr+1]);
		printf( " TORQUE_LIMIT           (R/W)[%.3d]:%5d (L:0x%.2X H:0x%.2X)\n", addr, value, table[addr], table[addr+1]);
		addr = MX28::P_PRESENT_POSITION_L; value = CM730::MakeWord(table[addr], table[addr+1]);
		printf( " PRESENT_POSITION       (R/W)[%.3d]:%5d (L:0x%.2X H:0x%.2X)\n", addr, value, table[addr], table[addr+1]);
		addr = MX28::P_PRESENT_SPEED_L; value = CM730::MakeWord(table[addr], table[addr+1]);
		printf( " PRESENT_SPEED          (R/W)[%.3d]:%5d (L:0x%.2X H:0x%.2X)\n", addr, value, table[addr], table[addr+1]);
		addr = MX28::P_PRESENT_LOAD_L; value = CM730::MakeWord(table[addr], table[addr+1]);
		printf( " PRESENT_LOAD           (R/W)[%.3d]:%5d (L:0x%.2X H:0x%.2X)\n", addr, value, table[addr], table[addr+1]);
		addr = MX28::P_PRESENT_VOLTAGE; value = table[addr];
		printf( " PRESENT_VOLTAGE        (R/W)[%.3d]:%5d\n", addr, value);
		addr = MX28::P_PRESENT_TEMPERATURE; value = table[addr];
		printf( " PRESENT_TEMPERATURE    (R/W)[%.3d]:%5d\n", addr, value);
		addr = MX28::P_REGISTERED_INSTRUCTION; value = table[addr];
		printf( " REGISTERED_INSTRUC     (R/W)[%.3d]:%5d\n", addr, value);
		addr = MX28::P_MOVING; value = table[addr];
		printf( " MOVING                 (R/W)[%.3d]:%5d\n", addr, value);
		addr = MX28::P_LOCK; value = table[addr];
		printf( " LOCK                   (R/W)[%.3d]:%5d\n", addr, value);
		addr = MX28::P_PUNCH_L; value = CM730::MakeWord(table[addr], table[addr+1]);
		printf( " PUNCH                  (R/W)[%.3d]:%5d (L:0x%.2X H:0x%.2X)\n", addr, value, table[addr], table[addr+1]);

		printf( "\n" );
	}
}

void Reset(Robot::CM730 *cm730, int id)
{
	int FailCount = 0;
	int FailMaxCount = 10;
	printf(" Reset ID:%d...", id);

	if(cm730->Ping(id, 0) != CM730::SUCCESS)
	{
		printf("Fail\n");
		return;
	}

	FailCount = 0;
	while(1)
	{
		if(cm730->WriteByte(id, MX28::P_RETURN_DELAY_TIME, 0, 0) == CM730::SUCCESS)
			break;

		FailCount++;
		if(FailCount > FailMaxCount)
		{
			printf("Fail\n");
			return;
		}
		usleep(10000);
	}

	FailCount = 0;
	while(1)
	{
		if(cm730->WriteByte(id, MX28::P_RETURN_LEVEL, 2, 0) == CM730::SUCCESS)
			break;

		FailCount++;
		if(FailCount > FailMaxCount)
		{
			printf("Fail\n");
			return;
		}
		usleep(10000);
	}

	if(id != CM730::ID_CM)
	{
		double cwLimit = MX28::MIN_ANGLE;
		double ccwLimit = MX28::MAX_ANGLE;

		switch(id)
		{
		case JointData::ID_R_SHOULDER_ROLL:
			cwLimit = -75.0;
			ccwLimit = 135.0;
			break;

		case JointData::ID_L_SHOULDER_ROLL:
			cwLimit = -135.0;
			ccwLimit = 75.0;
			break;

		case JointData::ID_R_ELBOW:
			cwLimit = -95.0;
			ccwLimit = 70.0;
			break;

		case JointData::ID_L_ELBOW:
			cwLimit = -70.0;
			ccwLimit = 95.0;
			break;

		case JointData::ID_R_HIP_YAW:
            cwLimit = -123.0;
            ccwLimit = 53.0;
            break;

		case JointData::ID_L_HIP_YAW:
			cwLimit = -53.0;
			ccwLimit = 123.0;
			break;

		case JointData::ID_R_HIP_ROLL:
			cwLimit = -45.0;
			ccwLimit = 59.0;
			break;

		case JointData::ID_L_HIP_ROLL:
			cwLimit = -59.0;
			ccwLimit = 45.0;
			break;

		case JointData::ID_R_HIP_PITCH:
			cwLimit = -100.0;
			ccwLimit = 29.0;
			break;

		case JointData::ID_L_HIP_PITCH:
			cwLimit = -29.0;
			ccwLimit = 100.0;
			break;

		case JointData::ID_R_KNEE:
			cwLimit = -6.0;
			ccwLimit = 130.0;
			break;

		case JointData::ID_L_KNEE:
			cwLimit = -130.0;
			ccwLimit = 6.0;
			break;

		case JointData::ID_R_ANKLE_PITCH:
			cwLimit = -72.0;
			ccwLimit = 80.0;
			break;

		case JointData::ID_L_ANKLE_PITCH:
			cwLimit = -80.0;
			ccwLimit = 72.0;
			break;

		case JointData::ID_R_ANKLE_ROLL:
			cwLimit = -44.0;
			ccwLimit = 63.0;
			break;

		case JointData::ID_L_ANKLE_ROLL:
			cwLimit = -63.0;
			ccwLimit = 44.0;
			break;

		case JointData::ID_HEAD_TILT:
			cwLimit = -25.0;
			ccwLimit = 55.0;
			break;
		}
		
		FailCount = 0;
		while(1)
		{
			if(cm730->WriteWord(id, MX28::P_CW_ANGLE_LIMIT_L, MX28::Angle2Value(cwLimit), 0) == CM730::SUCCESS)
				break;

			FailCount++;
			if(FailCount > FailMaxCount)
			{
				printf("Fail\n");
				return;
			}
			usleep(10000);
		}		
		FailCount = 0;
		while(1)
		{
			if(cm730->WriteWord(id, MX28::P_CCW_ANGLE_LIMIT_L, MX28::Angle2Value(ccwLimit), 0) == CM730::SUCCESS)
				break;

			FailCount++;
			if(FailCount > FailMaxCount)
			{
				printf("Fail\n");
				return;
			}
			usleep(10000);
		}		
		FailCount = 0;
		while(1)
		{
			if(cm730->WriteByte(id, MX28::P_HIGH_LIMIT_TEMPERATURE, 80, 0) == CM730::SUCCESS)
				break;

			FailCount++;
			if(FailCount > FailMaxCount)
			{
				printf("Fail\n");
				return;
			}
			usleep(10000);
		}
		FailCount = 0;
		while(1)
		{
			if(cm730->WriteByte(id, MX28::P_LOW_LIMIT_VOLTAGE, 60, 0) == CM730::SUCCESS)
				break;

			FailCount++;
			if(FailCount > FailMaxCount)
			{
				printf("Fail\n");
				return;
			}
			usleep(10000);
		}		
		FailCount = 0;
		while(1)
		{
			if(cm730->WriteByte(id, MX28::P_HIGH_LIMIT_VOLTAGE, 140, 0) == CM730::SUCCESS)
				break;

			FailCount++;
			if(FailCount > FailMaxCount)
			{
				printf("Fail\n");
				return;
			}
			usleep(10000);
		}
		FailCount = 0;
		while(1)
		{
			if(cm730->WriteWord(id, MX28::P_MAX_TORQUE_L, MX28::MAX_VALUE, 0) == CM730::SUCCESS)
				break;

			FailCount++;
			if(FailCount > FailMaxCount)
			{
				printf("Fail\n");
				return;
			}
			usleep(10000);
		}
		FailCount = 0;
		while(1)
		{
			if(cm730->WriteByte(id, MX28::P_ALARM_LED, 36, 0) == CM730::SUCCESS) // Overload, Overheat
				break;

			FailCount++;
			if(FailCount > FailMaxCount)
			{
				printf("Fail\n");
				return;
			}
			usleep(10000);
		}		 
		FailCount = 0;
		while(1)
		{
			if(cm730->WriteByte(id, MX28::P_ALARM_SHUTDOWN, 36, 0) == CM730::SUCCESS) // Overload, Overheat
				break;

			FailCount++;
			if(FailCount > FailMaxCount)
			{
				printf("Fail\n");
				return;
			}
			usleep(10000);
		}		 
	}

	printf("Success\n");
}

void Write(Robot::CM730 *cm730, int id, int addr, int value)
{
	if(addr == MX28::P_RETURN_DELAY_TIME || addr == MX28::P_RETURN_LEVEL)
	{
		printf( " Can not change this address[%d]\n", addr);
		return;
	}

	int error = 0;
	int res;
	if(id == CM730::ID_CM)
	{
		if(addr >= CM730::MAXNUM_ADDRESS)
		{
			printf( " Invalid address\n");
			return;
		}

		if(addr == CM730::P_DXL_POWER
			|| addr == CM730::P_LED_PANNEL)
		{
			res = cm730->WriteByte(addr, value, &error);
		}
		else
		{
			res = cm730->WriteWord(addr, value, &error);
		}
	}
	else
	{
		if(addr >= MX28::MAXNUM_ADDRESS)
		{
			printf( " Invalid address\n");
			return;
		}

		if(addr == MX28::P_ID)
		{
		    if(cm730->Ping(value, 0) == CM730::SUCCESS)
		    {
		        printf( " Can not change the ID. ID[%d] is in use.. \n", value);
		        return;
		    }
		    else
		    {
		        res = cm730->WriteByte(id, addr, value, &error);
		        gID = value;
		    }
		}
		else if(addr == MX28::P_HIGH_LIMIT_TEMPERATURE
            || addr == MX28::P_LOW_LIMIT_VOLTAGE
            || addr == MX28::P_HIGH_LIMIT_VOLTAGE
            || addr == MX28::P_ALARM_LED
            || addr == MX28::P_ALARM_SHUTDOWN
            || addr == MX28::P_TORQUE_ENABLE
            || addr == MX28::P_LED
#ifdef MX28_1024
            || addr == MX28::P_CW_COMPLIANCE_MARGIN
            || addr == MX28::P_CCW_COMPLIANCE_MARGIN
            || addr == MX28::P_CW_COMPLIANCE_SLOPE
            || addr == MX28::P_CCW_COMPLIANCE_SLOPE
#else
			|| addr == MX28::P_P_GAIN
			|| addr == MX28::P_I_GAIN
			|| addr == MX28::P_D_GAIN
			|| addr == MX28::P_RESERVED
#endif
			|| addr == MX28::P_LED
			|| addr == MX28::P_LED)
		{
			res = cm730->WriteByte(id, addr, value, &error);
		}
		else
		{
			res = cm730->WriteWord(id, addr, value, &error);
		}
	}

	if(res != CM730::SUCCESS)
	{
		printf( " Fail to write!\n");
		return;
	}

	if(error != 0)
	{
		printf( " Access or range error!\n");
		return;
	}

	if(id == CM730::ID_CM && addr == MX28::P_BAUD_RATE)
	    cm730->ChangeBaud(value);

	printf(" Writing successful!\n");
}

```
7. 修改main.cpp 找到```i<= JointData::NUMBER_OF_JOINTS```或是``` i<=JointData::某個參數```把參數改成```NUMBER_OF_JOINTS```然後把等於用掉

## 新增馬達ID

<b>================================================
- 步驟1 JointData.h修改ID清單

================================================</b>
OP  路徑:< Darwin/Framework/include/JointData.h > 
OP2路徑:< robotis/Framework/include/JointData.h >

加入新增 ID 清單 例如 :  ID_R_HAND_TEST = 21 
<b>!!重要!! NUMBER_OF_JOINTS 一定要放在最後一行 </b>
![](https://i.imgur.com/Ovr2Wgd.png)
<b>================================================
- 步驟2 修改 Roboplus server code

================================================</b>
OP  路徑:< Darwin/Linux/project/roboplus/main.cpp >
OP2路徑:< robotis/Linux/project/roboplus/main.cpp >

移動至 或 搜尋 365 行指令 
if(id >= JointData::ID_R_SHOULDER_PITCH && id <= JointData::ID_HEAD_TILT) 
 
更改為 
 
if(id >= JointData::ID_R_SHOULDER_PITCH && id < JointData::NUMBER_OF_JOINTS) 
 
條件<=改成< 

JointData::ID_HEAD_TILT 改成 JointData::NUMBER_OF_JOINTS 
<b>================================================
- 步驟3  清除.o 檔 

================================================</b>
OP  路徑:< Darwin > 
OP2路徑:< robotis > 

終端機中輸入指令
find . -name “*.o” -type f -delete 
<b>================================================
   - 步驟4  Remake Roboplus
   
   ================================================</b>

使用終端機進入到 roboplus 底下執行 
 
rm roboplus 
 
之後重新 
 
make 
 
然後 
 
./roboplus 
 
Roboplus Motion Edit All page 新增的馬達 ID 需打勾 
## 籃球

![](https://i.imgur.com/zVLn47U.png)

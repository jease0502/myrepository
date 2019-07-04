---
tags: ros
---
# op2第二份紀錄

## 顏色數值

藍色：(211,25,40,10,255,305)
綠色：(145,30,45,0,255,305)

## 增加顏色

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
        HONOR,
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
		else if (m_cur_mode == HONOR) //adding LED and play mp3 for new mode
		{
			cm730.WriteByte(CM730::P_LED_PANNEL, 0x01 | 0x02, NULL);
			//Signaling Darwin OP 2 which LED to turn on
			LinuxActionScript::PlayMP3("../../../Data/mp3/HONOR mode.mp3");
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
			else if (m_cur_mode == HONOR)
			  {
			  MotionManager::GetInstance()->Reinitialize();
			  MotionManager::GetInstance()->SetEnable(true);
			  //initialize and enable MotionManager class
			  m_is_started = 1;
			  LinuxActionScript::PlayMP3("../../../Data/mp3/Start HONOR demonstration.mp3");
			  //play an mp3 file (you can use any mp3 file but make sure file name matches)

			  // Joint Enable...
			  Action::GetInstance()->m_Joint.SetEnableBody(true, true);

			  Action::GetInstance()->Start(9);
			  while (Action::GetInstance()->IsRunning() == true) usleep(8000);

			  Head::GetInstance()->m_Joint.SetEnableHeadOnly(true, true);
			  Walking::GetInstance()->m_Joint.SetEnableBodyWithoutHead(true, true);
			  //Reset Gyro sensor
			  MotionManager::GetInstance()->ResetGyroCalibration();
			  while (1)
			  {
				  if (MotionManager::GetInstance()->GetCalibrationStatus() == 1)
				  {
					  LinuxActionScript::PlayMP3("../../../Data/mp3/Sensor calibration complete.mp3");
					  break;
				  }
				  else if (MotionManager::GetInstance()->GetCalibrationStatus() == -1)
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

### ```ColorFinder.cpp```


 位置：```Framework/src/vision/ColorFinder.cpp```
 
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


Point2D& ColorFinder::GetPosition(Image* hsv_img, int &count)
{
    int sum_x = 0, sum_y = 0 , count = 0;
 
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

}


 ```
 
  ### ```ColorFinder.h```
 地址：```Framework/include/ColorFinder.h```
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
        
        Image*  m_result;

        ColorFinder();
        ColorFinder(int hue, int hue_tol, int min_sat, int min_val, double min_per, double max_per);
        virtual ~ColorFinder();

        void LoadINISettings(minIni* ini);
        void LoadINISettings(minIni* ini, const std::string &section);
        void SaveINISettings(minIni* ini);
        void SaveINISettings(minIni* ini, const std::string &section);

        Point2D& GetPosition(Image* hsv_img);
	Point2D& GetPosition(Image* hsv_img, int &count);
    };
}

#endif /* COLORFINDER_H_ */
 ```
 
### ```main.cpp```

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

	ColorFinder* green_finder = new ColorFinder(120, 45, 35, 0, 0.3, 40.0);
	green_finder->LoadINISettings(ini, "GREEN");
	httpd::green_finder = green_finder;

    ColorFinder* blue_finder = new ColorFinder(225, 15, 45, 0, 0.3, 50.0);
	BallTracker marker_tracker = BallTracker();
	//created a new BallTracker object to use camera tracking
	BallFollower marker_follower = BallFollower();
	//created a new BallFollower object to follow target/marker
	int _marker_found = 0;
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
		int greenCount = 0, blueCount = 0;
		//created 2 int to store filtered pixel counts
		Point2D green, blue, center;
		//created 3 objects of Point2D class
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
		else if (StatusCheck::m_cur_mode == HONOR) //under a new mode called Sprint
		{

			green = green_finder->GetPosition(LinuxCamera::GetInstance()->fbuffer->m_HSVFrame, greenCount);
			//using the modified GetPosition function that also return filtered pixel counts
			blue = blue_finder->GetPosition(LinuxCamera::GetInstance()->fbuffer->m_HSVFrame, blueCount);
			//store position of green and blue color

			if (green.X < 0 || blue.X < 0)
				center.X = -1;
			else
				center.X = (green.X + blue.X) / 2;
			if (green.Y < 0 || blue.Y < 0)
				center.Y = -1;
			else
				center.Y = (green.Y + blue.Y) / 2;
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
        /*case NEW_MODE:
          //implement new codes here to execute after pressing start button
            break;*/
		case HONOR:
			//implement new codes here to execute after pressing start button
			if (Action::GetInstance()->IsRunning() == 0)
			{
				Head::GetInstance()->m_Joint.SetEnableHeadOnly(true, true);
				Walking::GetInstance()->m_Joint.SetEnableBodyWithoutHead(true, true);
				//Initialize walking module and head joints

				if (Walking::GetInstance()->IsRunning() == false && _ball_found != 1) {
					Walking::GetInstance()->X_MOVE_AMPLITUDE = 30.0;
					//Set forward and back step length to 30cm

					Walking::GetInstance()->A_MOVE_AMPLITUDE = 0.0;
					//Set yaw step length to 0

					Walking::GetInstance()->Start();
				}

				if (_marker_found == 1)
				{
					marker_follower.Process(marker_tracker.ball_position);
					//use BallFollower object to start following marker

					if (greenCount >= 10500 || blueCount >= 10500)
						//pixel count can be used to approximate distance, but in this case, 
						//this stop condition is sufficient                                 
					{
						Walking::GetInstance()->Stop();
						fprintf(stderr, "stop\n");
						while (Walking::GetInstance()->IsRunning() == true) usleep(1000000);
					}
				}
				else
				{
					Walking::GetInstance()->X_MOVE_AMPLITUDE = 30.0;
					Walking::GetInstance()->A_MOVE_AMPLITUDE = 0.0;
				}
			}
			break;
        }
    }

    return 0;
}

```

## 作者的modle

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
        int greenCount = 0, blueCount = 0;
        //created 2 int to store filtered pixel counts
        Point2D green, blue, center;
        //created 3 objects of Point2D class
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
             }break;

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
### colorfinder.cpp
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

Point2D& ColorFinder::GetPosition(Image* hsv_img, int &count)
{
   int sum_x = 0, sum_y = 0 ;
    count = 0;

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


## 增加後退
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
        int greenCount = 0, blueCount = 0;
        //created 2 int to store filtered pixel counts
        Point2D green, blue, center;
        //created 3 objects of Point2D class
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

                        if(greenCount >= 10500 || blueCount >= 10500)
                        //pixel count can be used to approximate distance, but in this case,
                        //this stop condition is sufficient
                        {
                        Walking::GetInstance()->Stop();
                        
                        //--------------------------back---------------------------------------
                        if(Walking::GetInstance()->IsRunning() == false && _ball_found != 1){
                        Walking::GetInstance()->X_MOVE_AMPLITUDE = -30.0;
                        //Set forward and back step length to 30cm
        
                        Walking::GetInstance()->A_MOVE_AMPLITUDE = 0.0;
                        //Set yaw step length to 0
        
                        Walking::GetInstance()->Start();
                        }
                        //---------------------------------------------------------------------
                        
                        
                        
            fprintf(stderr, "stop\n");

            while(Walking::GetInstance()->IsRunning() == true) usleep(1000000);
                        }
                 }
                 else
                 {
                     Walking::GetInstance()->X_MOVE_AMPLITUDE = 30.0;
                     Walking::GetInstance()->A_MOVE_AMPLITUDE = 0.0;
                 }
             }break;

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
import cv2


def gstreamer_pipeline (capture_width=1280, capture_height=720, display_width=1280, display_height=720, framerate=60, flip_method=0) :   
    return ('nvarguscamerasrc ! ' 
    'video/x-raw(memory:NVMM), '
    'width=(int)%d, height=(int)%d, '
    'format=(string)NV12, framerate=(fraction)%d/1 ! '
    'nvvidconv flip-method=%d ! '
    'video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! '
    'videoconvert ! '
    'video/x-raw, format=(string)BGR ! appsink'  % (capture_width,capture_height,framerate,flip_method,display_width,display_height))


cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=2), cv2.CAP_GSTREAMER)

i=0
while True:
	ret,frame=cap.read()
	cv2.imshow("photo",frame)
	if cv2.waitKey(1) & 0xFF == ord('t'):
		cv2.imwrite('./photo/%d.jpg'%i,frame)
		i+=1
	# Hit 'q' on the keyboard to quit!
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()

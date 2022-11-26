import cv2
import progressbar
PwmRange = [1000, 2000]
videoResolationX = 1280
videoResolationY = 720

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
video = cv2.VideoCapture('video.mp4')
videoTotalFrameCount = video.get(cv2.CAP_PROP_FRAME_COUNT)
out = cv2.VideoWriter('test.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 30, (1280, 720))

def face_X_ratio_to_img_X(imageResolationX, faceOnX):
    halfOfX = int(imageResolationX/2)
    ratio = (faceOnX/halfOfX)
    return ratio

def face_Y_ratio_to_img_Y(imageResolationY, faceOnY):
    halfOfY = int(imageResolationY/2)
    ratio = ((imageResolationY-faceOnY)/halfOfY)
    return ratio

def get_X_pwm(pwmRange):
    return int(pwmRange[0] + ((pwmRange[1]-pwmRange[0])/2) * face_X_ratio_to_img_X(videoResolationX, faceCenterX))

def get_Y_pwm(pwmRange): 
    return int(pwmRange[0] + ((pwmRange[1]-pwmRange[0])/2) * face_Y_ratio_to_img_Y(videoResolationY, faceCenterY))

frameNow = 0
widgets = [' [',progressbar.Timer(format= 'elapsed time: %(elapsed)s'),'] ',progressbar.Bar('*'),' (',progressbar.ETA(), ') ',]
bar = progressbar.ProgressBar(max_value=videoTotalFrameCount, widgets=widgets).start()

while(video.isOpened()): 
    ret, frame = video.read()
    bar.update(frameNow)
    if ret == True:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 2)
        try:
            face = faces[0]
            faceCenterX = face[0]+int(face[2]/2)
            faceCenterY = face[1]+int(face[3]/2)
            pwmX = get_X_pwm(PwmRange)
            pwmY = get_Y_pwm(PwmRange)
            cv2.line(frame, (int(videoResolationX/2), int(videoResolationY/2)), (faceCenterX, faceCenterY), (36, 82, 22), 6, 8)
            cv2.putText(frame, ("pwm X: " + str(pwmX)), (0, videoResolationY-150), cv2.FONT_HERSHEY_SIMPLEX, 3, (36, 82, 22), 5, cv2.LINE_AA)
            cv2.putText(frame, ("pwm Y: " + str(pwmY)), (0, videoResolationY-50), cv2.FONT_HERSHEY_SIMPLEX, 3, (36, 82, 22), 5, cv2.LINE_AA)
        except:
            cv2.putText(frame, ("S C A N"), (0, videoResolationY-50), cv2.FONT_HERSHEY_SIMPLEX, 3, (36, 82, 22), 5, cv2.LINE_AA)
        out.write(frame)
        frameNow+= 1
    else: 
        break

import cv2

PwmRange = [1000, 2000]


face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

img = cv2.imread('family.png')
imgResolationX = int(img.shape[1])
imgResolationY = int(img.shape[0])

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, 1.1, 2)
face = faces[0]
faceCenterX = face[0]+int(face[2]/2)
faceCenterY = face[1]+int(face[3]/2)


cv2.line(img, (int(imgResolationX/2), int(imgResolationY/2)), (faceCenterX, faceCenterY), (0, 0, 0), 6, 8)
def face_X_ratio_to_img_X(imageResolationX, faceOnX):
    halfOfX = int(imageResolationX/2)
    ratio = (faceOnX/halfOfX)
    return ratio

def face_Y_ratio_to_img_Y(imageResolationY, faceOnY):
    halfOfY = int(imageResolationY/2)
    ratio = ((imgResolationY-faceOnY)/halfOfY)
    return ratio

def get_X_pwm(pwmRange):
    return int(pwmRange[0] + ((pwmRange[1]-pwmRange[0])/2) * face_X_ratio_to_img_X(imgResolationX, faceCenterX))

def get_Y_pwm(pwmRange): 
    return int(pwmRange[0] + ((pwmRange[1]-pwmRange[0])/2) * face_Y_ratio_to_img_Y(imgResolationY, faceCenterY))

pwmX = get_X_pwm(PwmRange)
pwmY = get_Y_pwm(PwmRange)

cv2.putText(img, ("pwm X: " + str(pwmX)), (0, imgResolationY-150), cv2.FONT_HERSHEY_SIMPLEX, 3, (36, 82, 22), 5, cv2.LINE_AA)
cv2.putText(img, ("pwm Y: " + str(pwmY)), (0, imgResolationY-50), cv2.FONT_HERSHEY_SIMPLEX, 3, (36, 82, 22), 5, cv2.LINE_AA)
cv2.imwrite("test.png", img)

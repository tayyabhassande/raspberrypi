import logging
import threading
import cv2
import numpy as np
USE_FAKE_PI_CAMERA = True # Chage to FALSE if testing in the Raspberry Pi

if USE_FAKE_PI_CAMERA:
    from .camera import Camera  # For running app
else:
    from .pi_camera import Camera  # For running Raspberry Pi

log = logging.getLogger(
    __name__)  # Creates a logger instance, we use it to log things out

class OpenCVController(object):

    def __init__(self):
        self.current_shape = [False, False, False]
        self.camera = Camera()
        print('OpenCV controller initiated')
        self.coord_8 = []
        self.coord_3 = []
        self.coord_1 = []
        self.coord_rod = []

    def process_frame(self):  # generate frame by frame from camera
        while True:
            # Capture frame-by-frame
            frame = self.camera.get_frame() 
              # read the camera frame
            # jpg_to_np = np.frombuffer(frame, np.uint8)
            # imgDecode = cv2.imdecode(jpg_to_np, cv2.COLOR_RGB2BGR)
            hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            ########################## Red Range #############################
            lower_red1 = np.array([0, 120, 70])
            lower_red2 = np.array([10, 255, 255])
            lower_red_mask = cv2.inRange(hsvFrame, lower_red1, lower_red2)

            # range for upper red
            upper_red1 = np.array([170, 120, 70])
            upper_red2 = np.array([180, 255, 255])
            upper_red_mask = cv2.inRange(hsvFrame, upper_red1, upper_red2)

            red_mask = lower_red_mask + upper_red_mask


            ###################################### black range #############

            lower_black = np.array([0,0,0])
            upper_black = np.array([180,80,140])
            black_mask = cv2.inRange(hsvFrame, lower_black, upper_black)


            self.coord_8 = []
            self.coord_3 = []
            self.coord_1 = []
            self.coord_rod = []
            
            # convert the image to grayscale format
            contours, _ = cv2.findContours(black_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2:]

            for contour in contours:
                    area = cv2.contourArea(contour) 

                    if (area > 3000):
                        x, y, w, h = cv2.boundingRect(contour)

                        if w>25 and w < 300:


                            # ############# For Eight #####################

                            #image_copy = hsvFrame.copy()

                            if x in range(230, 320) and y in range(600, 710):
                                coord = [x,y]
                                self.coord_8.append(coord)

                            # # ###################### For THREE ####################

                            elif x in range(600, 670) and y in range(600, 700):
                                coord = [x,y]
                                self.coord_3.append(coord)                        

                            # ##################### For ONE ############################

                            elif x in range(1190, 1350) and y in range(115, 230):
                                coord = [x,y,w,h]
                                self.coord_1.append(coord)


            red_contours, r_hierachy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2:]

            for red_contour in red_contours:
                area = cv2.contourArea(red_contour)
                image_copy = hsvFrame.copy()
                if (area > 1000):
                    r_x, r_y, r_w, r_h = cv2.boundingRect(red_contour)

                    coord = [r_x, r_y, r_w, r_h]
                    self.coord_rod.append(coord)


                    if (r_x + r_w < 550):
                        self.current_shape=[True,False,False]
                    elif (r_x+r_w>550 and r_x<550):
                        self.current_shape = [True, True, False]
                    elif (r_x>550 and r_x+r_w<900):
                        self.current_shape = [False, True, False]
                    elif(r_x< 900 and r_x+r_w>900):
                        self.current_shape = [False, True, True]
                    elif(r_x > 900 ):
                        self.current_shape = [False, False, True]

            image_copy = frame.copy()
            print('8_coord:',self.coord_8)
            print('3_coord:',self.coord_3)
            print('1_coord:',self.coord_1)
            print('rod_cord:',self.coord_rod)

            cv2.rectangle(image_copy, (self.coord_rod[0][0], self.coord_rod[0][1]), (self.coord_rod[0][0] + self.coord_rod[0][2], self.coord_rod[0][1] + self.coord_rod[0][3]), (0, 0, 255), 2)
            cv2.rectangle(image_copy, (self.coord_rod[0][0], self.coord_rod[0][1]), (self.coord_rod[0][0] + 100, self.coord_rod[0][1] - 40), (0, 0, 255), -1)
            cv2.putText(image_copy, "Mark", (self.coord_rod[0][0], self.coord_rod[0][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255),thickness=3)

            cv2.rectangle(image_copy,(self.coord_8[0][0]-50,self.coord_8[0][1]+30),(self.coord_8[0][0]+290 ,self.coord_8[0][1]-440),(0,255,0),2)
            cv2.rectangle(image_copy, (self.coord_8[0][0]-50,self.coord_8[0][1]-440), (self.coord_8[0][0] +50 , self.coord_8[0][1] - 470), (0, 0, 255), -1)
            cv2.putText(image_copy, "EIGHT", (self.coord_8[0][0]-40 ,self.coord_8[0][1]-440), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255),thickness=3)

            cv2.rectangle(image_copy,(self.coord_3[0][0]-10,self.coord_3[0][1]+30),(self.coord_3[0][0]+300 ,self.coord_3[0][1]-440),(0,255,0),2)
            cv2.rectangle(image_copy, (self.coord_3[0][0]-10,self.coord_3[0][1]-440), (self.coord_3[0][0]+90 , self.coord_3[0][1] - 470), (0, 0, 255), -1)
            cv2.putText(image_copy, "THREE", (self.coord_3[0][0]-10 ,self.coord_3[0][1]-440), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255),thickness=3)

            cv2.rectangle(image_copy,(self.coord_1[0][0],self.coord_1[0][1]),(self.coord_1[0][0]+self.coord_1[0][2] ,self.coord_1[0][1]+self.coord_1[0][3]),(0,255,0),2)
            cv2.rectangle(image_copy, (self.coord_1[0][0],self.coord_1[0][1]), (self.coord_1[0][0]+70 , self.coord_1[0][1]-30), (0, 0, 255), -1)
            cv2.putText(image_copy, "ONE", (self.coord_1[0][0] ,self.coord_1[0][1]), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255),thickness=3)

            
            return image_copy
 

    def get_current_shape(self):
        return self.current_shape
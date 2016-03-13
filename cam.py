import sys

import numpy as np
import cv2

import shapes

cap = cv2.VideoCapture(0)
cascPath = sys.argv[1]

def main():
    shapes.init(800, 600)
    
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Our operations on the frame come here
        if ret:
            width, height, _ = frame.shape

            faceCascade = cv2.CascadeClassifier(cascPath)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=3,
                minSize=(220, 220),
                flags=2
            )

            # Draw a rectangle around the faces
            oox = ooy = 0
            if len(faces) != 0:
                x, y, w, h = faces[0]
                ox, oy = ((width/2-x)+209), (height/2-y)-470

                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

                cv2.rectangle(frame, (x-30, y-25), (x+40, y-10), (255, 255, 255), -1)
                cv2.putText(frame, "(%d, %d)" % (ox, oy), (x-30, y-12), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0))

                cv2.rectangle(frame, (x+w//2, y+(w//2-13)), (x+(w//2+55), y+w//2), (255, 255, 255), -1)
                cv2.putText(frame, "%dx%d" % (w, h), (x+w//2, y+h//2), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0))

                shapes.clear()
                c = shapes.Cube()
                
                # if the face has moved, rotate the object accordingly.
                balance = 20
                b = balance
                if abs(ox-oox) > 90:
                    if ox < 0:
                        b = -balance
                    c.rotate_by(0, -(ox-b), 0)
                    
                if abs(oy-ooy) > 90:
                    if oy < 0:
                        b = -balance
                    c.rotate_by(oy-b, 0, 0)
                    
                oox, ooy = ox, oy
                c.display()
                shapes.update()

            cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            shapes.end()
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

main()

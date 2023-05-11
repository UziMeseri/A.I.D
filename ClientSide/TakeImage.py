def TakePicture():
    import cv2

    # Create a VideoCapture object
    cap = cv2.VideoCapture(0)

    # Set the video frame width and height
    cap.set(3, 640)
    cap.set(4, 480)

    # Get a single frame from the camera
    ret, frame = cap.read()

    # Show the frame
    cv2.imshow("frame", frame)

    # Save the frame to an image file
    cv2.imwrite("(Client) capture.jpg", frame)

    # Release the VideoCapture object
    cap.release()

def VideoDisplay():
    # import the opencv library
    import cv2

    # define a video capture object
    vid = cv2.VideoCapture(0)

    while (True):

        # Capture the video frame
        # by frame
        ret, frame = vid.read()

        # Display the resulting frame
        cv2.imshow('frame', frame)

        # the 'q' button is set as the
        # quitting button you may use any
        # desired button of your choice
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # After the loop release the cap object
    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()


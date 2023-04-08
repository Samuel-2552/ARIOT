import cv2
import numpy as np

# Load AR image
ar_img = cv2.imread("C:/Users/Admin/Downloads/Off.png", cv2.IMREAD_UNCHANGED)

# Initiate SIFT detector
sift = cv2.SIFT_create()

# Detect keypoints and compute descriptors for AR image
kp2, des2 = sift.detectAndCompute(ar_img, None)

# Create video capture object for default camera
cap = cv2.VideoCapture(0)

while True:
    # Capture a frame from the video stream
    ret, target_img = cap.read()
    
    # Detect keypoints and compute descriptors for target image
    kp1, des1 = sift.detectAndCompute(target_img, None)
    
    # Match descriptors using FLANN matcher
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)
    
    # Filter matches using Lowe's ratio test
    good_matches = []
    for m,n in matches:
        if m.distance < 0.75*n.distance:
            good_matches.append(m)
    
    # Find the source and destination points from the filtered matches
    src_pts = np.float32([ kp1[m.queryIdx].pt for m in good_matches ]).reshape(-1,1,2)
    dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good_matches ]).reshape(-1,1,2)
    
    # Find the homography matrix using RANSAC
    H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

    
    # Warp the AR image to match the perspective of the target image
    ar_warped = cv2.warpPerspective(ar_img, H, (target_img.shape[1], target_img.shape[0]))
    
    # Overlay the AR image on the target image
    mask = cv2.cvtColor(ar_warped[:, :, 3], cv2.COLOR_GRAY2BGR)
    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    mask[mask > 0] = 255
    mask_inv = cv2.bitwise_not(mask)
    result = cv2.addWeighted(target_img, 1.0, ar_warped[:, :, :3], 1.0, 0.0)
    result = cv2.bitwise_and(result, result, mask=mask)
    target_img = cv2.bitwise_and(target_img, target_img, mask=mask_inv)
    result = cv2.add(target_img, result)
    
    # Display the result
    cv2.imshow('AR', result)
    
    # Exit if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()

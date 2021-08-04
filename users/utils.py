import numpy as np
import cv2 as cv
from tf_bodypix.api import download_model, load_model, BodyPixModelPaths
import cv2
from matplotlib import pyplot as plt
import numpy as np
import cv2
import math 

def main(path):
    """The function which gives the shoulder width in pixels"""

    bodypix_model = load_model(download_model(BodyPixModelPaths.MOBILENET_FLOAT_50_STRIDE_16))
    print(path)
    f = cv2.imread(path)
    result = bodypix_model.predict_single(f)
    mask = result.get_mask(threshold=0.75).numpy().astype(np.uint8)    
    part_mask = result.get_part_mask(mask,part_names=['torso_front','torso_back'])
    #part_mask_not = cv2.bitwise_not(part_mask)
    dimensions = f.shape
    image = np.zeros(dimensions, np.uint8)
    image[:] = (255, 255, 255)

    masked_image = cv2.bitwise_and(image, image, mask=part_mask)
    

    fr = masked_image 
    dimensions = fr.shape
    height = dimensions[0]
    width = dimensions[1]

    frame = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
    font = cv2.FONT_HERSHEY_COMPLEX
    _, threshold = cv2.threshold(frame, 110, 255, cv2.THRESH_BINARY)
    
    # Detecting contours in image.
    contours, _= cv2.findContours(threshold, cv2.RETR_TREE,
                                cv2.CHAIN_APPROX_SIMPLE)
    
    cord=[[],[]]
    # Going through every contours found in the image.
    for cnt in contours :
    
        approx = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt, True), True)
    
        # draws boundary of contours.
        cv2.drawContours(fr, [approx], 0, (0, 0, 255), 5) 
    
        # Used to flatted the array containing
        # the co-ordinates of the vertices.
        n = approx.ravel() 
        i = 0
    
        for j in n :
            if(i % 2 == 0):
                x = n[i]
                y = n[i + 1]

                if(y<(height/2)):
                    cord[0].append(x)
                    cord[1].append(y)

                # String containing the co-ordinates.
                string = str(x) + " " + str(y) 
                
                if(i == 0):
                    # text on topmost co-ordinate.
                    cv2.putText(fr, "Arrow tip", (x, y),
                                    font, 0.5, (255, 0, 0)) 
                else:
                    # text on remaining co-ordinates.
                    cv2.putText(fr, string, (x, y), 
                            font, 0.5, (0, 255, 0)) 
            i = i + 1

    xmin = min(cord[0])
    xmax = max(cord[0])

    x1,y1 = xmin,cord[1][cord[0].index(xmin)]
    x2,y2 = xmax,cord[1][cord[0].index(xmax)]

    sw = ((x2-x1)**2 + abs(y2-y1)**2)**0.5

    if cv2.waitKey(0) & 0xFF == ord('q'): 
        cv2.destroyAllWindows()

    
    return sw



# def get_shoulder_width(image_path, actual_dimensions=1.98, points=8) -> float:
#     """Returns the shoulder width in centimeters in real life"""
#     shoulder_pixels = main(image_path)
#     def most_common(lst) -> int:
#         """Returns most common occurrence"""
#         return max(set(lst), key=lst.count)
#     image = cv.imread(image_path)
#     gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
#     corners = cv.goodFeaturesToTrack(gray, points, 0.01, 8)
#     corners = np.int0(corners)
#     list_x = []
#     list_y = []
#     for i in corners:
#         x, y = i.ravel()

#         list_x.append(x)
#         list_y.append(y)

#         list_x.sort()
#         list_y.sort()

#     diff_x = [t - s for s, t in zip(list_x, list_x[1:])]

#     diff_y = [t - s for s, t in zip(list_y, list_y[1:])]

#     diff_x_limited = [i for i in diff_x if 8 < i < 25]
#     diff_y_limited = [i for i in diff_y if 8 < i < 25]
#     final_set = set(diff_x_limited + diff_y_limited)

#     pixel_candidates_2 = diff_x_limited + diff_y_limited
#     pixel_candidates = list(final_set)
#     pixel_candidates.sort()
#     pixels = pixel_candidates[-1]
#     pixels_2 = sum(pixel_candidates_2) / len(pixel_candidates_2)

#     pixel_avg = sum(pixel_candidates) / len(pixel_candidates)

#     pixels_new = most_common(pixel_candidates_2)

#     shoulder_width = (shoulder_pixels * actual_dimensions) / pixels

#     shoulder_width_avg = (shoulder_pixels * actual_dimensions) / pixel_avg

#     shoulder_width_2 = (shoulder_pixels * actual_dimensions) / pixels_2
#     diff_x_indices = [diff_x.index(i) for i in diff_x if 0 < i < 4]
#     diff_y_indices = [diff_y.index(i) for i in diff_y if 0 < i < 4]
#     final_y_candidates = [diff_y[i] for i in diff_x_indices]
#     final_x_candidates = [diff_x[i] for i in diff_y_indices]

#     final_final = [i for i in final_y_candidates + final_x_candidates if 8 < i < 25]
#     final_final.sort()
#     try:
#         omega_pixels = most_common(final_final)
#     except:
#         omega_pixels = pixel_avg
#     omega_shoulder_width = (shoulder_pixels * actual_dimensions) / omega_pixels
#     shoulder_width_new = (shoulder_pixels * actual_dimensions) / pixels_new
#     global export_size
#     final_size =  (omega_shoulder_width + (2 * shoulder_width_new) + shoulder_width + shoulder_width_2 + shoulder_width_avg) / 6
#     export_size = final_size.round(2)
#     # ik this looks bad , I could use switch but don't want to add another bug in production
    
#     if 0<final_size<=44:
#         return "small"
#     elif 44<final_size <=48:
#         return "medium"
#     elif 48<final_size<52:
#         return "large"
#     elif 52<final_size<=54:
#         return "xlarge"
#     elif 54<final_size<=58:
#         return "xxlarge"
#     else:
#         return final_size.round(3)
    
def get_shoulder_width(image_path, actual_dimensions=1.98, points=12) -> float:
    """Returns the shoulder width in centimeters in real life"""
    shoulder_pixels = main(image_path)
    storing_list = []
    store_list_x=[]
    store_list_y=[]

    term = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_COUNT, 30, 0.1)
    img = cv.imread(image_path)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    corners = cv.goodFeaturesToTrack(gray, 12, 0.01, 8,useHarrisDetector=True)
    refined_corners = cv.cornerSubPix(gray,corners,(11,11),(-1,-1),term)
    new_list_x=[]
    new_list_y=[]
    list_x=[]
    list_y=[]
    for i in refined_corners:
        x,y = i.ravel()
        cv.circle(img,(int(x),int(y)),2,255,-1)
        list_x.append(x)
        list_y.append(y)
    for i in range(len(list_x)):
        for j in  range(len(list_x)):
            new_list_x.append(abs(list_x[j]-list_x[i]))
            new_list_y.append(abs(list_y[j]-list_y[i]))
            store_list_x.append((list_x[j],list_x[i]))
            store_list_y.append((list_y[j],list_y[i]))




    slopes = [(p/q) for p,q in zip(new_list_y,new_list_x)]

# slopes = [(p/q) for p,q in zip(diff_y,diff_x)]

    for i in range(len(slopes)):
        if -0.4<slopes[i]<0.4 or abs(slopes[i])>10:
            if math.isinf(abs(slopes[i])):
            
            #plt.axvline(x=store_list_x[i][0])
                storing_list.append(abs(store_list_y[i][0]-store_list_y[i][1]))

            else:
            
                storing_list.append(abs(new_list_x[i]) if abs(new_list_x[i])> abs(new_list_y[i]) else abs(new_list_y[i]))
                #x = np.linspace(store_list_x[i][0],store_list_x[i][1],100)
                #y = slopes[i]*(x-store_list_x[i][0]) + store_list_y[i][0]
                #plt.plot(x, y, '-g', label=f'y=2x+1')
    refined_storing_list=[x for x in storing_list if 3<x<=30]
    sqaure_side_pixels = min(refined_storing_list)
    shoulder_actual_width = (actual_dimensions*shoulder_pixels)/sqaure_side_pixels
    final_size = shoulder_actual_width



    
  
    global export_size
    export_size = final_size.round(2)
    
    if 0<final_size<=44:
        return "small"
    elif 44<final_size <=48:
        return "medium"
    elif 48<final_size<52:
        return "large"
    elif 52<final_size<=54:
        return "xlarge"
    elif 54<final_size<=58:
        return "xxlarge"
    else:
        return final_size.round(3)
    

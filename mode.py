import numpy as np

def one_two(fing_list):
    # finger_list = [thumb_xavg,thumb_yavg, ind_xavg,ind_yavg,mid_xavg,mid_yavg, ring_xavg,ring_yavg,pinky_xavg,pinky_yavg,wrist_xavg,wrist_yavg,dist]
    print("inone")
    xdist = fing_list[2]-fing_list[4]
    ydist = fing_list[3]-fing_list[5]
    ## Calculate the distance between the index and middle finger tips
    dist_index_middle = np.sqrt(xdist**2+ydist**2)
    print(dist_index_middle)

    # Check if fingers are close to wrist
    wx = fing_list[10]
    wy = fing_list[11]
    # Thumb:
    thumb_dist = np.sqrt((fing_list[0]-wx)**2+(fing_list[1]-wy)**2)
    print("thumb:",thumb_dist)
    # index:
    ind_dist = np.sqrt((fing_list[2]-wx)**2+(fing_list[3]-wy)**2)
    print("index:",ind_dist)
    # Thumb:
    mid_dist = np.sqrt((fing_list[4]-wx)**2+(fing_list[5]-wy)**2)
    print("middle:",mid_dist)
    # Thumb:
    ring_dist = np.sqrt((fing_list[6]-wx)**2+(fing_list[7]-wy)**2)
    print("ring:",ring_dist)
    # Thumb:
    pinky_dist = np.sqrt((fing_list[8]-wx)**2+(fing_list[9]-wy)**2)
    print("pinky:",pinky_dist)

    dist = fing_list[12]
    print("dist index-middle norm:", dist_index_middle*dist/1.5 )
    if dist_index_middle >0.085 and ind_dist > 1.5*thumb_dist and ind_dist > 1.8*ring_dist and ind_dist > 1.8*pinky_dist and ind_dist-mid_dist < 0.05:
        return (2)
    elif dist_index_middle >0.085 and ind_dist > 1.5*thumb_dist and ind_dist > 1.8*ring_dist and ind_dist > 1.8*pinky_dist and ind_dist > 1.8*mid_dist:
        return (1)
    else:
        return(3)
    ## Recognize as peach if the distances are far enough
# def two():

# def mode():

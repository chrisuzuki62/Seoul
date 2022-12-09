
def change_mode(mode, fing_list):
  
            
    if len(fing_list) == 12:
    ## Recognize as peach if the distances are far enough
        if one_two(fing_list) == 1:
            mode = 1
            print(f"mode {mode}")
            # image = cv2.putText(image, 'Peace Sign', (80,80), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 0))
        elif one_two(fing_list) == 2:
            mode = 2
            print(f"mode {mode}")
            print(0)
        else:
            mode = 0 # = "base"
    
    return mode
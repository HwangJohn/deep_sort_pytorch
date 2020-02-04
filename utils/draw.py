import numpy as np
import cv2

palette = (2 ** 11 - 1, 2 ** 15 - 1, 2 ** 20 - 1)


def compute_color_for_labels(label):
    """
    Simple function that adds fixed color depending on the class
    """
    color = [int((p * (label ** 2 - label + 1)) % 255) for p in palette]
    return tuple(color)


def draw_boxes(img, bbox, identities=None, offset=(0,0)):
    for i,box in enumerate(bbox):
        x1,y1,x2,y2 = [int(i) for i in box]
        x1 += offset[0]
        x2 += offset[0]
        y1 += offset[1]
        y2 += offset[1]
        # box text and bar
        id = int(identities[i]) if identities is not None else 0    
        color = compute_color_for_labels(id)
        label = '{}{:d}'.format("", id)
        t_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_PLAIN, 2 , 2)[0]
        cv2.rectangle(img,(x1, y1),(x2,y2),color,3)
        cv2.rectangle(img,(x1, y1),(x1+t_size[0]+3,y1+t_size[1]+4), color,-1)
        cv2.putText(img,label,(x1,y1+t_size[1]+4), cv2.FONT_HERSHEY_PLAIN, 2, [255,255,255], 2)
    return img

def draw_center(img, cur_center_points, prev_center_points, identities=None, prev_identities=None):

    change_amounts = {}
    chk_change_amounts = {} # for debug

    prev_id_center_points = {}
    if len(prev_center_points) > 0:
        for idx, prev_c_p in enumerate(prev_center_points):
            prev_id = int(prev_identities[idx]) if prev_identities is not None else 0
            prev_c_x, prev_c_y = prev_c_p
            prev_id_center_points.update({prev_id:(prev_c_x, prev_c_y)})

        for idx, cur_c_p in enumerate(cur_center_points):
            cur_id = int(identities[idx]) if identities is not None else 0
            if cur_id in prev_id_center_points:
                cur_c_x, cur_c_y = cur_c_p
                prev_c_x, prev_c_y = prev_id_center_points[cur_id]

                # calc chage amount between prev frame and cur frame
                change_x = cur_c_x - prev_c_x
                change_y = cur_c_y - prev_c_y

                change_amounts.update({cur_id:(change_x, change_y)})
                chk_change_amounts.update({cur_id:(cur_c_x, cur_c_y, prev_c_x, prev_c_y)})

    for i,box in enumerate(cur_center_points):
        
        center_x, center_y = box

        cur_id = int(identities[i]) if identities is not None else 0
        change_amount = 0
        if cur_id in change_amounts:
            change_x, change_y = change_amounts[cur_id]
            # draw text
            label = '{:d} {:d}'.format(change_x, change_y)
            cv2.putText(img, label, (center_x, center_y+4), cv2.FONT_HERSHEY_PLAIN, 1, [255, 255, 0], 2)

            # for debug
            cur_c_x, cur_c_y, prev_c_x, prev_c_y = chk_change_amounts[cur_id]
            debug_label = '{:d} {:d} {:d} {:d}'.format(cur_c_x, cur_c_y, prev_c_x, prev_c_y)
            cv2.putText(img, debug_label, (center_x+10, center_y+10), cv2.FONT_HERSHEY_PLAIN, 1, [255, 0, 0], 1)

        # draw point
        cv2.circle(img, (center_x, center_y), 3, [255,0,0])       

        

    return img



if __name__ == '__main__':
    for i in range(82):
        print(compute_color_for_labels(i))

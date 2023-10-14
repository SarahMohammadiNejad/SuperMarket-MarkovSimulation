import cv2
import random
import numpy as np
import imageio
from PIL import Image, ImageDraw, ImageFont


def move_customers_smooth(doodl):
    for cm in doodl.custom: cm.reach_traget = 0
    mult=0
    # jj = 0
    while mult ==0: 
        for cm in doodl.custom:
            if (cm.target_coor_x == cm.current_coor_x) & (cm.target_coor_y == cm.current_coor_y):
                cm.reach_target=1
            else:
                if(cm.loc_old == 'entrance'):

                    if cm.current_coor_y>450: 
                        cm.current_coor_y += doodl.jump*np.sign(450 - cm.current_coor_y) #-1

                    elif cm.current_coor_x != cm.target_coor_x: 
                        cm.current_coor_x += doodl.jump*np.sign(cm.target_coor_x - cm.current_coor_x)

                    elif (cm.current_coor_y<=450)&(cm.current_coor_y>cm.target_coor_y): 
                        cm.current_coor_y += doodl.jump*np.sign(cm.target_coor_y - cm.current_coor_y)
                    elif (cm.target_coor_x == cm.current_coor_x) & (cm.target_coor_y == cm.current_coor_y):
                        cm.reach_target=1
                        

                elif (cm.loc_old in ['fruit', 'drinks','dairy', 'spices']):
                    if cm.loc_new == cm.loc_old:
                        if cm.current_coor_y != cm.target_coor_y: 
                            cm.current_coor_y += doodl.jump*np.sign(cm.target_coor_y - cm.current_coor_y)
                        elif cm.current_coor_x != cm.target_coor_x: 
                            cm.current_coor_x += doodl.jump*np.sign(cm.target_coor_x - cm.current_coor_x)
                        elif (cm.target_coor_x == cm.current_coor_x) & (cm.target_coor_y == cm.current_coor_y):
                            cm.reach_target=1    

                    elif cm.loc_new in ['fruit', 'drinks','dairy', 'spices','checkout']:
                        # print(f'{cm.id}   {cm.current_coor_y}')
                        if (cm.current_coor_y<450)&(cm.target_coor_x != cm.current_coor_x): 
                            cm.current_coor_y += doodl.jump*np.sign(450 - cm.current_coor_y) #-1
                            # if cm.loc_new=='checkout':print(f'here1   {cm.id}    {cm.current_coor_x}   {cm.current_coor_y}')
                        elif (cm.current_coor_y==450)&(cm.target_coor_x != cm.current_coor_x): 
                            cm.current_coor_x += doodl.jump*np.sign(cm.target_coor_x - cm.current_coor_x)
                            # if cm.loc_new=='checkout':print(f'here2   {cm.id}    {cm.current_coor_x}   {cm.current_coor_y}')
                        elif(cm.current_coor_x == cm.target_coor_x):
                            while(cm.current_coor_y!=cm.target_coor_y): 
                                cm.current_coor_y += doodl.jump*np.sign(cm.target_coor_y - cm.current_coor_y) 
                                # if cm.loc_new=='checkout': print(f'here3   {cm.id}   {cm.current_coor_x}   {cm.current_coor_y}')
                        elif (cm.target_coor_x == cm.current_coor_x)&(cm.current_coor_y==cm.target_coor_y):
                            # if cm.loc_new=='checkout':print(f'here4   {cm.id}    {cm.current_coor_x}   {cm.current_coor_y}')
                            cm.reach_target=1    

        Save_Frame(doodl)
            # doodl.draw()

            # img_pil = Image.fromarray(doodl.frame)
            # draw = ImageDraw.Draw(img_pil)
            # # font = ImageFont.truetype(36)
            # text_color = (0, 0, 0)  # Red
            # position = (80, 20)
            # frame_title = f'{doodl.time}'
            # font_size = 20
            # font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", font_size)

            # draw.text(position, doodl.time_str, font=font,fill=text_color)#, font=font
            # draw.text((80, 60), f'Now #Customer at --> fruit: {doodl.section_num["fruit"]}, spices: {doodl.section_num["spices"]}, dairy: {doodl.section_num["dairy"]}, drinks: {doodl.section_num["drinks"]}, checkout: {doodl.section_num["checkout"]}', font=font,fill=text_color)#, font=font
            # draw.text((80, 100), f'Tot #Customer at --> fruit: {doodl.section_totnum["fruit"]}, spices: {doodl.section_totnum["spices"]}, dairy: {doodl.section_totnum["dairy"]}, drinks: {doodl.section_totnum["drinks"]}, checkout: {doodl.section_totnum["checkout"]}', font=font,fill=text_color)#, font=font
            # image_with_text = np.array(img_pil)

            # # cv2.imshow(frame_title, image_with_text)
            # cv2.imshow(doodl.time_str, image_with_text)

            # doodl.images.append(image_with_text)
        if cv2.waitKey(5) & 0xFF == ord('q'):  #stops if q is pressed
            break

        mult=1
        for cm in doodl.custom:
            mult *= cm.reach_target


# -----------------------

def move_customers_jump(doodl):
    for cm in doodl.custom:
            cm.target_coor_x = cm.current_coor_x
            cm.target_coor_y = cm.current_coor_y

            doodl.draw()


            img_pil = Image.fromarray(doodl.frame)
            draw = ImageDraw.Draw(img_pil)
            # font = ImageFont.truetype(36)
            text_color = (0, 0, 0)  # Red
            position = (100, 100)
            text = f'{doodl.time}'
            frame_title = f'{doodl.time}'

            draw.text(position, text, fill=text_color)#, font=font
            image_with_text = np.array(img_pil)

            cv2.imshow(frame_title, image_with_text)
            doodl.images.append(image_with_text)
            if cv2.waitKey(5) & 0xFF == ord('q'):  #stops if q is pressed
                break

# ----------------
def Save_Frame(doodl):
    doodl.draw()

    img_pil = Image.fromarray(doodl.frame)


    font_size = 20
    font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", font_size)

    draw = ImageDraw.Draw(img_pil)

    text_color = (0, 0, 0)  # Red
    position = (80, 20)
    frame_title = f'{doodl.time}'

    draw.text(position, doodl.time_str, font=font,fill=text_color)#, font=font
    draw.text((80, 60), f'Now #Customer at --> fruit: {doodl.section_num["fruit"]}, spices: {doodl.section_num["spices"]}, dairy: {doodl.section_num["dairy"]}, drinks: {doodl.section_num["drinks"]}, checkout: {doodl.section_num["checkout"]}', font=font,fill=text_color)#, font=font
    draw.text((80, 100), f'Tot #Customer at --> fruit: {doodl.section_totnum["fruit"]}, spices: {doodl.section_totnum["spices"]}, dairy: {doodl.section_totnum["dairy"]}, drinks: {doodl.section_totnum["drinks"]}, checkout: {doodl.section_totnum["checkout"]}', font=font,fill=text_color)#, font=font

    image_with_text = np.array(img_pil)

    # cv2.imshow(frame_title, image_with_text)
    cv2.imshow(doodl.time_str, image_with_text)


    doodl.images.append(image_with_text)
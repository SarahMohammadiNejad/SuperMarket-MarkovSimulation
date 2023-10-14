import cv2
import random
import numpy as np

import datetime
from datetime import timedelta  

from random import choices

import pandas as pd
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore")

import datetime 
# import preprocessing
from preprocessing import read_files
from preprocessing import produce_customer_image_male

random.seed(4)
import imageio
from PIL import Image, ImageDraw, ImageFont
from customer_class import Customers
from supermarket_class import Supermarket
from funcs import move_customers_smooth, move_customers_jump,Save_Frame


if __name__ == "__main__":


    transition_matrix1 = read_files()

    supermarket_image = cv2.imread('files/market.png')

    doodl = Supermarket(supermarket_image,transition_matrix1)#,customer_image
    move_style = 'Smooth' #'Jump'#'Smooth'

    if move_style == 'Smooth': 
        minutes = (8-7)*10
        num_entry_per_min = 10
        save_every = 10

    if move_style == 'Jump': 
        minutes = (18-8)*6
        num_entry_per_min = 5
        save_every = 50


    customer_id = 0

    for i in range(minutes):

        h = int(i/60) + 8
        m = i%60
        print(f'--------- time = {h}:{m} -----------')
        time= datetime.datetime(2020, 11,11, h,m,0)
        doodl.time_str= f'{time.time()}'

        doodl.section_num = {'fruit':0,'spices':0,'dairy':0,'drinks':0,'checkout':0}


        # create one customer every minute at entrance
        for j in range(num_entry_per_min):
            customer_id += 1
            doodl.create_customer(customer_id)

        if move_style == 'Jump': Save_Frame(doodl)

        for cm in doodl.custom:

            cm.loc_old = cm.location
            cm.change_location()
            cm.loc_new = cm.location
            doodl.section_num[cm.loc_new]+=1
            doodl.section_totnum[cm.loc_new]+=1

        
            if move_style == 'Jump': 
                cm.current_coor_x = cm.target_coor_x
                cm.current_coor_y = cm.target_coor_y
                
        if move_style == 'Jump': 
            Save_Frame(doodl)
            if cv2.waitKey(5) & 0xFF == ord('q'):  #stops if q is pressed
                break
            



        if move_style == 'Smooth' : move_customers_smooth(doodl)
        if((i+1)%save_every==0): imageio.mimsave(f'results/{move_style}_{i+1}.gif', doodl.images, duration=200)

        for cm in doodl.custom:
            if (cm.location=='checkout'): 
                doodl.remove_customer(cm)  

    imageio.mimsave(f'results/{move_style}_f.gif', doodl.images, duration=200)   
    cv2.destroyAllWindows()






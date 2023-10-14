import cv2
import random
import numpy as np
from preprocessing import read_files,produce_customer_image_male
from random import choices

class Customers:

    def __init__(self,transition_matrix1,location,jump,customer_id=1):
        self.id = customer_id
        self.image = produce_customer_image_male(self.id)
        self.transition_matrix1 = transition_matrix1
        self.location = location
        self.jump_step = jump
        self.current_coor_y, self.current_coor_x = self.get_coord(self.location)
        self.target_coor_y, self.target_coor_x = self.get_coord(self.location)


        self.reach_target = 0

    def __repr__(self):
        return f'customer number {self.id} is in {self.location}'

    def change_location(self):
        states_list = ['checkout','dairy', 'drinks','entrance','fruit','spices']
        self.location = choices(states_list,self.transition_matrix1[self.transition_matrix1.index == self.location].values[0])[0]
        self.target_coor_y, self.target_coor_x = self.get_coord(self.location)


    def get_coord(self, aisle):
        """turning aisles into coordinates in the supermarket"""
        y0 = int(150/self.jump_step)
        y1 = int(420/self.jump_step)

        if aisle == 'entrance':

            ty, tx = [630,self.jump_step*random.randint(23, 29)]

        if aisle == 'drinks':

            ty, tx = [self.jump_step*random.randint(y0, y1), self.jump_step*random.randint(3, 5)]

            # print('there_drinks')
        elif aisle == 'dairy':
            # print('here_dairy')
            # ty, tx = [self.jump_step*random.randint(y0, y1), self.jump_step*random.randint(30, 40)]
            ty, tx = [self.jump_step*random.randint(y0, y1), self.jump_step*random.randint(10, 13)]

        elif aisle == 'spices':
            # print('here_spices')
            ty, tx = [self.jump_step*random.randint(y0, y1), self.jump_step*random.randint(18, 21)]
        elif aisle == 'fruit':
            # print('here_fruit')
            ty, tx = [self.jump_step*random.randint(y0, y1), self.jump_step*random.randint(26, 28)]
        elif aisle == 'checkout':
            # print('here_checkout')
            # ty, tx = [555, random.choice([100, 250, 400, 535])]
            # ty, tx = [550, random.choice([100, 250, 400, 530])]
            ty, tx = [540, random.choice([90, 240, 390, 510])]

        return ty, tx

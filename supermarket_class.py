import cv2
import random
import numpy as np
from customer_class import Customers


class Supermarket:
    # list of customers
    def __init__(self,supermarket_image,transition_matrix1):
        self.supermarket_image = supermarket_image
        self.frame = self.supermarket_image.copy()
        self.transition_matrix1 = transition_matrix1
        self.loc_old = ["entrance"]*5000
        self.loc_new = ["entrance"]*5000
        self.time = 0
        self.time_str = '7:00' 
        self.custom = []
        self.images = [self.supermarket_image]
        self.jump = 30
        self.section_num = {'fruit':0,'spices':0,'dairy':0,'drinks':0,'checkout':0}
        self.section_totnum = {'fruit':0,'spices':0,'dairy':0,'drinks':0,'checkout':0}



    # create new customer whenever we want
    def create_customer(self,i):
        c = Customers(self.transition_matrix1,'entrance',self.jump,i)
        self.custom.append(c)
        
    # reove a customer (I use it at checkout)
    def remove_customer(self,cstmr):
        self.custom.remove(cstmr)
        
    def draw(self):
        self.frame = self.supermarket_image.copy()

        for customer in self.custom:

            y = customer.current_coor_y
            x = customer.current_coor_x
            self.frame[y:y+20, x:x+15, :] = customer.image
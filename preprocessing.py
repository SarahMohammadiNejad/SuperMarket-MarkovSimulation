import pandas as pd
import numpy as np

from datetime import timedelta  

def read_files(): 
    df_monday = pd.read_csv('data/monday.csv', sep = ';')
    df_tuesday = pd.read_csv('data/tuesday.csv', sep = ';')
    df_wednesday = pd.read_csv('data/wednesday.csv', sep = ';')
    df_thursday = pd.read_csv('data/thursday.csv', sep = ';')
    df_friday = pd.read_csv('data/friday.csv', sep = ';')

    df_monday['day'] = 1
    df_tuesday['day'] = 2
    df_wednesday['day'] = 3
    df_thursday['day'] = 4
    df_friday['day'] = 5

    df = pd.concat([df_monday, df_tuesday,df_wednesday,df_thursday,df_friday])
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['hour'] = df['timestamp'].dt.hour
    df['minute'] = df['timestamp'].dt.minute

    # separate 'checkout' and 'non checkout' customers
    df_checkout = pd.DataFrame()
    df_no_checkout = pd.DataFrame()

    for d,df_temp in df.groupby(['day']):
        checkouts = df_temp[(df_temp['location'] == 'checkout')]

        checkout_records = df_temp[df_temp['customer_no'].isin(checkouts['customer_no'])]
        no_checkout_records = df_temp[~df_temp['customer_no'].isin(checkouts['customer_no'])]

        df_checkout = pd.concat([df_checkout,checkout_records])
        df_no_checkout = pd.concat([df_no_checkout,no_checkout_records])


    first_visit = df_checkout.drop_duplicates(subset=['day','customer_no'])
    first_visit['location'] = 'entrance'
    first_visit['timestamp'] -= timedelta(minutes=1)
    
    df_checkout_entry_sorted = pd.concat([first_visit,df_checkout])
    df_checkout_entry_sorted = df_checkout_entry_sorted.sort_values(by=['day','customer_no','timestamp'])

    df_resampled = df_checkout_entry_sorted.set_index("timestamp").groupby(['day','customer_no'])[["location"]].resample('min').ffill()

    df_resampled['nlocation'] = df_resampled['location'].shift(-1)
    df_temp = df_resampled

    transition_matrix1 = pd.crosstab(df_temp['location'],df_temp['nlocation'],normalize = 0)
    #after checkout it is always entrance which is not correct and we need to correct it by hand
    transition_matrix1.loc['checkout', :] = 0
    transition_matrix1.loc['checkout', 'checkout'] = 1

    return transition_matrix1


# -----------------------


def produce_customer_image_square(i):
    customer_image = np.zeros((15, 15, 3), dtype=np.uint8)
    customer_image[:,:,0] = ((i%10)*155)%255
    customer_image[:,:,1] = ((i%10)*128)%255
    customer_image[:,:,2] = ((i%10)*82)%255

    return customer_image
# -------------------------------
def produce_customer_image_male(i):
    # Define the dimensions of your 2D array (e.g., 10x10)
    width = 20
    height = 15
    color = 125

    # Initialize an empty 2D array
    customer_image = np.zeros((width, height, 3), dtype=np.uint8)#[[0 for _ in range(width)] for _ in range(height)]
    customer_image[:,:,0] = 255
    customer_image[:,:,1] = 255
    customer_image[:,:,2] = 255
    c = np.zeros(3)
    c[0] = ((i%10)*155)%255
    c[1] = ((i%10)*128)%255
    c[2] = ((i%10)*82)%255

    for j in [0,1,2]:
        # Add head
        hx =4
        hy = 5 
        x0 = 0
        y0 = 4
        for x in range(x0,x0+hx+1):
            customer_image[x,y0:y0+hy+1,j] = c[j]


        # Add torso and arms
        arm_x = 3
        x0 = x0+hx
        for x in range(x0,x0+arm_x+1):
            customer_image[x,:,j] = c[j]

        # Add torso
        x0 = hx + arm_x
        tx = 6
        for x in range(x0,x0+tx+1):
            customer_image[x,y0:y0+hy+1,j] = c[j]

        # Add legs
        lx = 6
        x0 = hx + arm_x+tx
        y01 = 3
        y02 = 8
        for x in range(x0,x0+lx+1):
            customer_image[x,y01:y01+3,j] = c[j]
            customer_image[x,y02:y02+3,j] = c[j]

    return customer_image

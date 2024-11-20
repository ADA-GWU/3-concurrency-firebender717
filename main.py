import cv2
import time
import numpy as np
from threading import Thread
from typing import Literal
import argparse

def display_img(cv2_img  : np.ndarray, 
                disp_name: str ="image", 
                quit_key : str ="q"
                ) -> None:
    display_name = f"{disp_name}. Press '{quit_key}' to exit"
    try:
        while True:
            img_copy = cv2_img.copy()
            while img_copy.shape[0] > 1200: # As images are usually wider than taller, it is better to check width size
                img_copy = cv2.resize(img_copy, (img_copy.shape[1]//2, img_copy.shape[0]//2))
            cv2.imshow(display_name, img_copy)
            key = cv2.waitKey(1)
            del img_copy
            if key == ord(quit_key):
                break
    
    except:
        print(f"Error occurred with displaying the window, named '{disp_name}'")
        
    finally:
        cv2.destroyWindow(display_name)

def quantize(cv2_image   : np.ndarray, 
             row_interval: tuple[int, int], 
             col_interval: tuple[int, int], 
             block_size  : int,  
             delay       : float,
             )    -> None:
    """
    Quantize an image of by averaging pixel values in blocks.
    Updates the shared output image progressively.
    """
    for row in range(row_interval[0], row_interval[1], block_size):
        for col in range(col_interval[0], col_interval[1], block_size):
            m = cv2_image[row:row + block_size, 
                          col:col + block_size]\
                            .mean(axis=(0, 1)).astype(np.uint8)

            cv2_image[row:row + block_size, col:col + block_size] = m

            time.sleep(delay)

def find_range_pairs(max_num:int, n_partitions:int, n_divisible:int):
    divisible_nums = [x for x in range(0, max_num, n_divisible)]
    list_ids = []

    for i in range(n_partitions):
        list_ids.append(divisible_nums[i*(len(divisible_nums)//n_partitions)])
    list_ids.append(max_num)

    pairs = []
    for i in range(len(list_ids)-1):
        pairs.append((list_ids[i], list_ids[i+1]))
    
    return pairs

def q_supervisor(image_path  : str, 
                 block_size  : int  =50,
                 mode        : str  =Literal["S", "M"],
                 process_dim : str  ="4x2",
                 display_name: str  ="Processing the image", 
                 quit_key    : str  ="q",
                 delay       : float=0.05
                 )    -> None:
    
    image = cv2.imread(image_path)

    disp_thread = Thread(target=display_img, 
                         args=(image, display_name, quit_key))
    
    disp_thread.start()

    if mode == "S":
        quantize(image, 
                 (0, image.shape[0]), 
                 (0, image.shape[1]), 
                 block_size, delay)
        
    elif mode == "M":
        n_row_parts, n_col_parts = map(int, process_dim.split("x"))

        r_index_pairs = find_range_pairs(image.shape[0], n_row_parts, block_size)
        c_index_pairs = find_range_pairs(image.shape[1], n_col_parts, block_size)

        threads = []
        for r in r_index_pairs:
            for c in c_index_pairs:
                threads.append(
                    Thread(target=quantize, 
                           args=(image, r, c, block_size, delay)))

        for t in threads:
            t.start()
            




parser = argparse.ArgumentParser()

parser.add_argument("--image_path", type=str, 
           help="Full path to the image that will be quantized")
parser.add_argument("--block_size", type=int, default=50,
           help="Size of final image pixel size. Ex: 50 for 50x50 result")
parser.add_argument("--mode", type=str, default="M",
           help="Processing mode. M for multithreaded, S for single threaded processing")
parser.add_argument("--process_dim", type=str, default="4x3",
           help="shape of the processing dimension. Ex: 4x3 to split the image into 12 portions, 4 rows 3 columns, to process")
parser.add_argument("--display_name", type=str, default="Processing the image",
           help="Name to show on th etop bar of the image window")
parser.add_argument("--quit_key", type=str, default="q",
           help="Choose a character that corresponds to a key to close the window")
parser.add_argument("--delay", type=float, default=0.01,
           help="Choose a float value to set the delay time after each process")

args = parser.parse_args()

q_supervisor(image_path=args.image_path,
             block_size=args.block_size, 
             mode=args.mode,
             process_dim=args.process_dim,
             display_name=args.display_name,
             quit_key=args.quit_key,
             delay=args.delay)


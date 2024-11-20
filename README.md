[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/YybNWfh8)

## Concurrecy. Image Quantization
### Advanced Software Pradigms

#### Introduction
The aim of the task is to show the perfoemance increase that can be obtained in higher dimentional problems, where the task can be split into multiple parts to be processes parallely, that would be processed sequentially under notmal circumstances.
Python threading package will be utilized to tackle this problem and the OpenCV package will be used for image reading and displaying purposes. 
#### Main
The code consists of multiple functions: image display, quantize, find range pairs, quantization supervisor. The required arguments are taken from the user via the CLI, which will  be discussed shortly. 
Process steps:
1. the image is read via OpenCV via the given path
2. a display is intialized and the image is displayed throughout the process. If the size of the image is too large, it will be downscaled by hald to make it fit intop the screen. Just for simplicity, the image is resized into half for displaying. But the image that is actually processed is not changed. As the function is started via a thread, it allows other operations to be continued on the same image while it is beiung displayed.
3. If the sequential mode is chosen, the image will be processed, and its small portions are changed step by step. However, if the multithreaded mode is chosen, the image is split into multiple parts (the grid option can be altered by the user) and each part is processed in its own thread. (The sections that are given to each thread is processed with the `find_range_pairs` function.)
4. After all threads have finished execution, the program is terminated. 

#### Usage
The user can simply, execute the help command to see the impact each input makes.

Help commad:
```
python main.py --help
```

Help output:
```
usage: main.py [-h] [--image_path IMAGE_PATH] [--block_size BLOCK_SIZE] [--mode MODE] [--process_dim PROCESS_DIM] [--display_name DISPLAY_NAME]
               [--quit_key QUIT_KEY] [--delay DELAY]

options:
  -h, --help            show this help message and exit
  --image_path IMAGE_PATH
                        Full path to the image that will be quantized
  --block_size BLOCK_SIZE
                        Size of final image pixel size. Ex: 50 for 50x50 resul. Default: 50
  --mode MODE           Processing mode. M for multithreaded, S for single threaded processing. Default: M
  --process_dim PROCESS_DIM
                        shape of the processing dimension. Ex: 4x3 to split the image into 12 portions, 4 rows 3 columns, to process. Default: 4x3
  --display_name DISPLAY_NAME
                        Name to show on th etop bar of the image window. Default string: Processing the image
  --quit_key QUIT_KEY   Choose a character that corresponds to a key to close the window. Default key: q
  --delay DELAY         Choose a float value to set the delay time after each process. Default value: 0.01

```


Example usage:
```
python main.py --image_path <full_path_to_the_image> --block_size 50 --mode M --process_dim 3x5 --quit_key q --delay 0.01
```




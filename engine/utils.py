import os
import logging
import json, yaml
from datetime import datetime, date

def yaml_read(filename): 
    if '.yaml' not in filename: 
        raise "Invalid format"
    with open(filename) as f:
        my_dict = yaml.safe_load(f)
    return my_dict
    
def write_data(dir, content): 
    with open(dir, 'a') as f: 
        f.writelines(content + '\n')

def set_logger(filename:str='./log/app.log'): 
    # Create an empty log file if not exist
    if not os.path.exists(filename):
        open(filename, 'a')
    else:
        pass
    # Set logging config
    logging.basicConfig(
                        level=logging.DEBUG, 
                        format='[%(asctime)s] - %(levelname)7s --- %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S', 
                        filename=filename, 
                        filemode='w'
                        )
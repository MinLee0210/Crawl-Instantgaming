import os
import logging
import yaml
import time                                                

def dir_exist(dir, create:bool=True) -> bool: 
    existence = os.path.exists(dir)
    if existence ==False and create == True: 
        os.mkdir(dir)
        existence = True
    return existence

# ===== READ DATA FORMAT =====
def yaml_read(filename): 
    if '.yaml' not in filename: 
        raise "Invalid format"
    with open(filename) as f:
        my_dict = yaml.safe_load(f)
    return my_dict
    
def write_data(dir, content): 
    with open(dir, 'a') as f: 
        f.writelines(content + '\n')


# ===== LOGGING SYSTEM =====
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

# ===== SOME DECORATOR =====
def timer_func(func): 
    def wrap_func(*args, **kwargs): 
        t1 = time() 
        result = func(*args, **kwargs) 
        t2 = time() 
        print(f'Function {func.__name__!r} executed in {(t2-t1):.4f}s') 
        return result 
    return wrap_func 
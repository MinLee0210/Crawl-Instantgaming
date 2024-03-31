import pandas as pd


def write_df(dataset:list[dict]) -> pd.DataFrame: 
    df = pd.DataFrame(dataset)
    return df

def to_csv(df:pd.DataFrame, dir): 
    if '.csv' in dir: 
        df.to_csv(dir)
    else: 
        raise "Invalid format"
    
def write_log(dir, content): 
    with open(dir, 'a') as f: 
        f.writelines(content + '\n')

# ===== Running bash script =====
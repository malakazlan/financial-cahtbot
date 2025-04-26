import sqlite3
import pandas as pd

def save_to_db(df:pd.DataFrame,db_name="stocks.db"):
    conn = sqlite3.connect(db_name)
    df.to_sql("stocks_data",conn,if_exists="replace",index=False)
    conn.close()
    
def load_from_db(db_name="stocks.db")-> pd.DataFrame:
    conn = sqlite3.connect(db_name)
    df=pd.read_sql("SELECT * FROM stocks_data",conn)
    conn.close()
    return df 
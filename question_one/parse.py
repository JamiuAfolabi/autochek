import pandas as pd
import datetime
from datetime import date
import configparser
from sqlalchemy import create_engine
import sqlalchemy
import urllib.parse

from helper_function import handle_exception

class Parse:
    
    def parse_url(self,url: str) -> str:
        """
        Parse Url into a format suitable for extracting with pandas

        Parameters
        ----------------------
        url : str 

        Returns
        ----------------------
        parsed_url: str
            
        """
        action_type = url.split('/')[-1]

        if action_type[:4] == 'edit':
            parsed_url = url.replace('/edit#gid=', '/export?format=csv&gid=')
        else:
            parsed_url = 'https://drive.google.com/uc?id=' + url.split('/')[-2]
        
        return parsed_url

    def get_correct_date(self,date_value: str) -> str: 
        
        """
        The function parses dates and replace with correct dates
        EXAMPLE:
        02/29/2023 is not a valid date. On execution:

            get_correct_date(02/29/2023): 02/28/2023

        Parameters
        ----------------------
        date_value : str 

        Returns
        ----------------------
        date_val : str
        
        """
        
        month,day,year = date_value.split('/')
        month,day,year = int(month),int(day),int(year)

        print(day,month,year)
        try:
            datetime.datetime(year=year,month=month,day=day)
            return date_value
        except Exception as err:
            handle_exception(err.with_traceback())
            leap_year = False
            if year % 400 == 0 and year % 4 == 0:
                leap_year = True
            # if year % 100 == 0:
            #     leap_year = False

            month_dict = {1:31,
                        2: 29 if leap_year else 28,
                        3:31,
                        4:30,
                        5:31,
                        6:30,
                        7:31,
                        8:31,
                        9:30,
                        10:31,
                        11:30,
                        12:31
                        }
            date_val = f'{month}/{str(month_dict[month])}/{year}'
            return date_val

            
        

    def change_column_dtype(self,df):
        """
        This function change column type of dataframe to appropriate datatypes
        
        Parameters
        ----------------------
        df : Dataframe

        Returns
        ----------------------
        df : Dataframe
        

        
        """
        columns = list(df.head().select_dtypes('object').columns)
        for col in columns:
            try: 
                df[col] = pd.to_datetime(df[col])
            except Exception as err:
                handle_exception(err)
                try:
                    df[col] = df[col].apply(self.get_correct_date)
                    df[col] = pd.to_datetime(df[col])
                except Exception as err:
                    handle_exception(err)
                    try:
                        df[col] = df[col].apply('double')
                    except Exception as err:
                        handle_exception(err)
        return df


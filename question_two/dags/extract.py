
import requests
import pandas as pd
import json

import os

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)
os.chdir('..')



print(os.path.join(os.getcwd(),'result/response.json'))

def get_exchange(currencies,account_id,api_key):

    """
        returns the exchange rate for a list of currncies from  https://www.xe.com/xecurrencydata/

        Parameters
        ----------
        currencies : List
            list of currencies to load

        account_id : str
           account id key
        
        api_key : str
            api key for a user's account
            
        Returns
            -------
            DataFrame 
                a dataframe containing the following columns timestamp , currency_from, USD_to_currency, currency_to_USD ,currency_to of the target currecies
    """

    all_currency_data = pd.DataFrame()
    #iterate over each currecy
    for currency in currencies:
        temp_data = {}
        params = (
            ('to', 'USD'),
            ('from', currency),
            ('amount', '1'),
        )
        # get the currency rate for  destination currency to 1 USD 
        from_response = requests.get("https://xecdapi.xe.com/v1/convert_to.json",auth = (account_id,api_key), params=params)
        # return the response in json format
        response1 = from_response.json()
        # get the currency rate for 1 USD to destination currency 
        to_response = requests.get("https://xecdapi.xe.com/v1/convert_from.json",auth = (account_id,api_key), params=params)
        # return the response in json format
        response2 = to_response.json()

        with open(f'{dir_path}/response_from.json', 'w') as f:
            json.dump(response1, f)

        with open(f'{dir_path}/response_to.json', 'w') as f:
            json.dump(response2, f)
            
        
        # mapping response to a dictionary 
        temp_data['timestamp'] = response2['timestamp']
        temp_data['currency_from'] = response2['to'][0]['quotecurrency']
        temp_data['USD_to_currency'] = response2['to'][0]['mid']
        temp_data['currency_to_USD'] = response1['from'][0]['mid']
        temp_data['currency_to'] = response1['from'][0]['quotecurrency']
        # converting the dictionary record to a dataframe
        single_currency_data = pd.DataFrame([temp_data])
        # appeding each currency record the universal currency dataframe 
        all_currency_data = pd.concat([all_currency_data,single_currency_data],axis = 0)
    #return the currency exchange
    return all_currency_data


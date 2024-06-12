# Which columns will you use?
# Clean your columns
# Concatenate the columns needed for your embedding
# Create new column with concatenated and clean text
import pandas as pd
import random
import string
from create_dataset import return_dataframe
import yaml
import os
import json

# print(df)


def read_yaml(path_to_yaml:str) -> dict:
    with open(path_to_yaml) as yaml_file:
        content = yaml.safe_load(yaml_file)

        return content

def preprocess():

    print("Started peprocess")

    
    print("Starting to download")
    df=return_dataframe()

    overview_new=[]
    for overvw,title,star1,star2,star3,star4,director in zip(df['Overview'],df['Series_Title'],df['Star1'],df['Star2'],df['Star3'],df['Star4'],df['Director']):
        add_series_title=" Movie name is "
        add_stars=" Stars are "
        add_director=" Director's name is "
        add_series_title+=title
        add_series_title+=" . "
        add_stars+=star1+" , "
        add_stars+=star2+" , "
        add_stars+=star3+" , "
        add_stars+=star4
        add_stars+=" ."
        add_director+=director+" . "
        overvw+=add_series_title
        overvw+=add_stars
        overvw+=add_director
        overview_new.append(overvw)
 

    df['Overview_new']=overview_new
    # print(df.columns)
    df.sample(frac=1)
    df.reset_index(drop=True)
    
    # Define the set of characters to use for generating random values
    characters = string.ascii_letters + string.digits

    # Initialize an empty set to store unique values
    unique_values = set()

    # Generate and add unique values until reaching the desired count
    while len(unique_values) < 1000:
        random_value = ''.join(random.choice(characters) for _ in range(10))  # Adjust the length as needed
        unique_values.add(random_value)

    # Convert the set to a list if needed
    unique_values_list = list(unique_values)

    # Print the first few unique values as an example
    df['MovieID']=unique_values_list







    df.drop(['Poster_Link', 'Released_Year', 'Certificate',
       'Runtime', 'Genre', 'IMDB_Rating', 'Meta_score', 'No_of_Votes', 'Gross'],axis=1,inplace=True)
    print(df.columns)
    n=read_yaml("./constants.yaml")
    no_of_rows_to_be_used=n['no_of_rows_to_be_used']
    new_df=df.iloc[:no_of_rows_to_be_used,:]



    print("No of rows in new_Df")
    print(new_df.shape)
    return new_df
        
        
        

if __name__=="__main__":
    df=preprocess()
    print("Preprocess Done")


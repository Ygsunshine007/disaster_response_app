"""
PREPROCESSING DATA
Disaster Response Pipeline Project
Udacity - Data Science Nanodegree
Sample Script Execution:
> python process_data.py disaster_messages.csv disaster_categories.csv DisasterResponse.db
Arguments:
    1) CSV file containing messages (disaster_messages.csv)
    2) CSV file containing categories (disaster_categories.csv)
    3) SQLite destination database (DisasterResponse.db)
"""


import sys
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

def load_data(messages_filepath, categories_filepath):
    messages = pd.read_csv(messages_filepath)
    categories = pd.read_csv(categories_filepath)
    df = pd.merge(messages,categories,on='id')
    return df


def clean_data(df):
    """
    Clean Data function
    
    Arguments:
        df -> raw data Pandas DataFrame
    Outputs:
        df -> clean data Pandas DataFrame
    """
    # Split categories into separate category columns
    categories = df['categories'].str.split(";",\
                                            expand = True)
    
    # select the first row of the categories dataframe
    row = categories.iloc[0,:].values
    
    # use this row to extract a list of new column names for categories.
    new_cols = [r[:-2] for r in row]

    # rename the columns of `categories`
    categories.columns = new_cols

    # Convert category values to just numbers 0 or 1.
    for column in categories:

        # set each value to be the last character of the string
        categories[column] = categories[column].str[-1]
        
        # convert column from string to numeric
        categories[column] = pd.to_numeric(categories[column])
    
    # drop the original categories column from `df`
    df.drop('categories', axis = 1, inplace = True)

    # concatenate the original dataframe with the new `categories` dataframe
    df[categories.columns] = categories
    
    # remove non binary values
    df= df [df['related']!=2]
    # drop duplicates
    df.drop_duplicates(inplace = True)

    return df

def save_data(df, database_filename):
    """
    Save Data function
    
    Arguments:
        df -> Clean data Pandas DataFrame
        database_filename -> database file (.db) destination path
    """
    engine = create_engine('sqlite:///'+ database_filename)
    df.to_sql('df', engine, index=False, if_exists='replace')  


def main():
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)
        
        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)
        
        print('Cleaned data saved to database!')
    
    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')


if __name__ == '__main__':
    main()

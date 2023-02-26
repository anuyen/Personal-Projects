import pandas as pd
import numpy as np
import tldextract
import json
import openai
import time
import re

from location_guesser.location_country_checker import LocationChecker, LocationData
from gender_guesser import gender_guesser
from namecleaner import (
    remove_special_chars,
    remove_all_info_after_comma,
    remove_words_after_slash,
    remove_second_first_name_with_quotations,
    remove_enclosed_words,
    keep_first_name_if_two,
    normalize_name,
    remove_honorifics,
    remove_solo_char,
    intake_data,
    get_main_domain,
    name_cleaning_phase1,
    swap_first_and_last_name,
    separate_names,
    remove_non_ascii_rows,
    name_cleaning_phase2
)

def main(
        headers: list[str],
        filename: str,
        num_of_col: int,
        duplicate_subsets_to_drop: list[str],
        openai_apikey: str,
        country_list: list[str],
        countries_file_location: str,
        location_countries_file_location: str,
        main_output_file_name: str,
        single_letter_name_output_file_name: str,
        gender_guesser_data_file_name: str
    )-> None:
    # Step 0: Intake data
    df = intake_data(filename, headers, num_of_col)

    # Step 1: Drop duplicates from columns given in duplicate_subsets_to_drop
    df = df.drop_duplicates(subset=duplicate_subsets_to_drop)

    # Step 2: Domain(website) column cleaning
    # This step automatically gives null value if the link is invalid
    df['website'] = df['website'].apply(lambda x: get_main_domain(str(x)))
    df['website'] = df['website'].replace('nan.', np.nan)

    # Step 3: Remove "null" values in "overview" and "website" columns
    # This is already done in the intake step 0 and step 2

    # Step 4: Location cleaning
    # if data in country column is NA, fill it with data from the auxillary columns
    df['country'] = df['country'].fillna(df['countr_to_be_dropped'])

    # drop this column because it is not needed
    df.drop('countr_to_be_dropped',axis=1,inplace=True)

    # load country data for location checking
    data = LocationData(
        countries_file_location, 
        location_countries_file_location
    )
    countries_set = data.countries_set
    location_country_dict = data.location_country_dict

    # intialize location checker
    lc = LocationChecker(openai_apikey, countries_set, location_country_dict, country_list)

    # enrich country column with data from location column and chatgpt
    df['country'] = df['country'].fillna(df['location'].apply(lambda x: lc.check_location(str(x))))

    # Save updated list of location-country
    with open(location_countries_file_location,'w') as file:
        json.dump(lc.location_country_dict, file)

    # Step 5: Clean first and last name

    # Extract first and last name to a different df for cleaning
    name_df = df[['first_name','last_name']]

    # Initiate phase 1 of name cleaning
    name_df['first_name_cleaned'] = name_df['first_name'].apply(lambda x: name_cleaning_phase1(str(x)))
    name_df['last_name_cleaned'] = name_df['last_name'].apply(lambda x: name_cleaning_phase1(str(x)))

    # Separate name if first name has a comma at the end and contains two names
    name_df = name_df.apply(separate_names,axis=1)

    # Swap first and last name if first name ends with a comma
    name_df = swap_first_and_last_name(name_df)

    # Remove all rows with non_ASCII characters
    name_df = remove_non_ascii_rows(name_df)

    # Initiate phase 2 of name cleaning
    name_df['first_name_cleaned'] = name_df['first_name_cleaned'].apply(lambda x: name_cleaning_phase2(str(x)))
    name_df['last_name_cleaned'] = name_df['last_name_cleaned'].apply(lambda x: name_cleaning_phase2(str(x)))

    # Merge data from step 5 back to the original DataFrame
    df[['first_name_cleaned','last_name_cleaned']] = name_df[['first_name_cleaned','last_name_cleaned']]

    # extract the data from columns 'first_name_cleaned' and 'last_name_cleaned' if they are a single letter or a single letter + period
    single_letter_mask = df['first_name_cleaned'].str.match(r'^[A-Za-z]\.?$') | df['last_name_cleaned'].str.match(r'^[A-Za-z]\.?$')
    single_letter_data = df.loc[single_letter_mask]

    # Output single letter data for further work
    single_letter_data.to_csv(single_letter_name_output_file_name,header=True,index=False)

    # Extract data whose name is not single letter
    df = df.loc[~single_letter_mask]

    # Step 6: Guess gender based on first name
    data_dict: dict = {}
    with open(gender_guesser_data_file_name,'r') as file:
        data_dict = json.load(file)

    gg = gender_guesser.GenderGuesser(data_dict,openai_apikey)

    df['guessed_gender'] = df['first_name_cleaned'].apply(lambda x: gg.gender_guesser(x))

    with open(gender_guesser_data_file_name,'w') as file:
        json.dump(gg.data_dict,file)

    # Finally: Output data
    df.to_csv(main_output_file_name, header=True, index=False)

if __name__ == "__main__":
    # load settings from external file and call main function with parameters
    with open("./data/settings.json",'r') as file:
        settings = json.load(file)

    main(
        headers=settings['headers'],
        filename=settings['input_file_location'],
        num_of_col=settings['number_of_columns'],
        duplicate_subsets_to_drop=['linkedin_id','job_title'],
        openai_apikey=settings['openai_apikey'],
        country_list=settings['country_list_to_search'],
        countries_file_location=settings['countries_database_file_location'],
        location_countries_file_location=settings['location_countries_database_file_location'],
        main_output_file_name=settings['cleaned_data_output_file_name'],
        single_letter_name_output_file_name=settings['single_letter_name_output_file_name'],
        gender_guesser_data_file_name=settings['gender_guesser_data_file_name']
    )
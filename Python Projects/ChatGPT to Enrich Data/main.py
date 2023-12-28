import pandas as pd
import numpy as np
import tldextract
import json
import openai
import time
import re
import requests

from multiprocessing import Pool
from cleanco import basename
from location_guesser.location_country_checker import LocationChecker, LocationData
from gender_guesser.gender_guesser import GenderGuesser

from thecompaniapi.thecompanyapi import TheCompanyAPI
from location_guesser.reset_database import reset_location_database
from namecleaner.namecleaner import (
    intake_data,
    get_main_domain,
    name_cleaning_phase1,
    swap_first_and_last_name,
    separate_names,
    name_cleaning_phase2,
    clean_company_name
)
from namecleaner.postcleanup import (
    company_name_post_clean_up,
    last_name_post_clean_up,
)

def parallelize_dataframe(df, func, n_cores=4):
    df_split = np.array_split(df, n_cores)
    pool = Pool(n_cores)
    df = pd.concat(pool.map(func, df_split))
    pool.close()
    pool.join()
    return df

def main(
        headers: list[str],
        filename: str,
        num_of_col: int,
        duplicate_subsets_to_drop: list[str],
        openai_apikey: str,
        country_list: list[str],
        countries_file_location: str,
        location_countries_file_location: str,
        location_countries_backup_file_location: str,
        main_output_file_name: str,
        single_letter_name_output_file_name: str,
        gender_guesser_data_file_name: str,
        de_set: set,
        honorifics: set,
        white_list_companies: set,
        country_names_to_remove_from_end: set,
        comma_exception_set: set,
        thecompanyapi_columns_to_keep: list,
        thecompanyapi_token: str,
        thecompanyapi_cached_file_location: str,
        thecompanyapi_columns_to_drop: list,
        company_domain_file_location: str
    )-> None:
    time_start = time.time()

    print("""
    Script to Clean and Enrich LinkedIn Data:
    🍓🍓🍓🍓🍓🍓🍓🍓🍓🍓🍓🍓🍓🍓🍓🍓
    Powered by:
   ___                      _    ___                       
  / _ \ _ __   ___ _ __    / \  |_ _|_                     
 | | | | '_ \ / _ \ '_ \  / _ \  | |(_)                    
 | |_| | |_) |  __/ | | |/ ___ \ | | _                     
  \___/| .__/ \___|_| |_/_/   \_\___(_)                    
  ____ |_|  __     ___            _        ___   ___ _____ 
 |  _ \  __ \ \   / (_)_ __   ___(_)      / _ \ / _ \___ / 
 | | | |/ _` \ \ / /| | '_ \ / __| |_____| | | | | | ||_ \ 
 | |_| | (_| |\ V / | | | | | (__| |_____| |_| | |_| |__) |
 |____/ \__,_| \_/  |_|_| |_|\___|_|      \___/ \___/____/
 
 And other APIs's...""")

#####################################################################################################
    # Step 0: Intake data
    df = intake_data(filename, headers, num_of_col)

    # Step 1: Drop duplicates from columns given in duplicate_subsets_to_drop
    df = df.drop_duplicates(subset=duplicate_subsets_to_drop)

    # Step 2: Domain(website) column cleaning/enrichment
    # This step automatically gives null value if the link is invalid
    df.insert(1,'website_cleaned', df['website'].apply(lambda x: get_main_domain(str(x))))
    df['website_cleaned'] = df['website_cleaned'].replace('nan.', np.nan)

    # Step 3: Remove "null" values in "overview" and "website" columns
    # This is already done in the intake step 0 and step 2

#####################################################################################################
    # Step 4: Location cleaning
    # Check if country column exists
    if 'country' not in df.keys():
        df['country'] = np.nan
    else:
        # if data in country column is NA, fill it with data from the auxillary columns
        df['country'] = df['country'].fillna(df['countr_to_be_dropped'])

        # drop this column because it is not needed
        df.drop('countr_to_be_dropped',axis=1,inplace=True)

    print("\nExtracting country from location... 🌍🌍")
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
    lc.save_data(location_countries_file_location)
    
    print(f"Running clean-up scripts for database...")

    # function below saves a backup and then reset the database
    reset_location_database(location_countries_file_location,location_countries_backup_file_location)
    print("Done extracting country from location data ✅")

#####################################################################################################
    print("\nCleaning company name...🏢🏢")
    # Step 7: Clean company name using cleanco lib
    df['company_name'] = df['company_name'].apply(lambda x: basename(str(x)))

    # Make company names look nice
    # df['company_name_cleaned'] = df['company_name'].apply(lambda x: clean_company_name(x))
    df.insert(1, 'company_name_cleaned', df['company_name'].apply(lambda x: clean_company_name(x)))
    df['company_name_cleaned'] = df['company_name'].apply(lambda x: company_name_post_clean_up(x, 
                                                                                               white_list_companies, 
                                                                                               country_names_to_remove_from_end,
                                                                                               comma_exception_set))

    print("Done cleaning company names ✅")

#####################################################################################################
    # Extract website domains from main df, drop duplicates to reduce the number of
    #total websites before using theCOMPANYAPI to retrieve data given a domain (gucci.com)
    #the retrieved data is then cached

    # Supplement corrupt website_cleaned data with company_name_cleaned data
    tca = TheCompanyAPI(
        thecompanyapi_token = thecompanyapi_token,
        thecompanyapi_cached_file_location = thecompanyapi_cached_file_location,
        company_domain_file_location = company_domain_file_location,
        columns_to_keep = thecompanyapi_columns_to_keep
    )

    df = tca.fill_domain(df)
    tca.save_data(which_file="company_domain")

    website_df = df[['website_filled']].drop_duplicates(subset=['website_filled']).dropna(subset=['website_filled'])
    website_df['website_filled'].apply(lambda x: tca.check_company(company_domain=str(x)))
    tca.save_data(which_file="tca")
    
    print(f"""
    Done checking unique domains against thecompany api ✅
    Total unique domains = {tca.total_domain_count}
    Total unqique company names used in place of missing domains = {tca.total_company_name_count}
    Total cached domains = {tca.total_already_cached}""")

    print("\nMerging thecompanyapi data with our main dataFrame...")
    # Turn data from tca into a Dataframe with column "website_cleaned"
    tca_df = pd.json_normalize(
        list(tca.thecompanyapi_cached.values())
    )
    # print(tca_df.keys())
    tca_df.index = tca.thecompanyapi_cached.keys()
    tca_df = tca_df.drop(thecompanyapi_columns_to_drop, axis=1)
    tca_df = tca_df.add_prefix("company.")
    tca_df = tca_df.reset_index().rename(columns={'index':'website_filled'})
    tca.save_data(which_file="tca")

    df = pd.merge(df, tca_df, on="website_filled", how="left")
    df.loc[df['website'].isna(),'website'] = df['website_filled']
    df.drop('website_filled',axis=1,inplace=True)
    print("Done merging ✅")
#####################################################################################################

    # Step 5: Clean first and last name
    print("\nCleaning first and last name...🧍🧘")
    # Extract first and last name to a different df for cleaning
    name_df = df[['first_name','last_name']]

    # Initiate phase 1 of name cleaning
    name_df.insert(1,'first_name_cleaned',name_df['first_name'].apply(lambda x: name_cleaning_phase1(str(x), honorifics)))
    name_df.insert(1,'last_name_cleaned',name_df['last_name'].apply(lambda x: name_cleaning_phase1(str(x), honorifics)))

    # Separate name if first name has a comma at the end and contains two names
    name_df = name_df.apply(separate_names,axis=1)

    # Swap first and last name if first name ends with a comma
    name_df = swap_first_and_last_name(name_df)

    # Skipping this below
    # Remove all rows with non_ASCII characters
    # name_df = remove_non_ascii_rows(name_df)

    # Initiate phase 2 of name cleaning
    name_df['first_name_cleaned'] = name_df['first_name_cleaned'].apply(lambda x: name_cleaning_phase2(str(x),de_set,honorifics))
    name_df['last_name_cleaned'] = name_df['last_name_cleaned'].apply(lambda x: name_cleaning_phase2(str(x),de_set,honorifics))

    # Post clean up for last names
    name_df['last_name_cleaned'] = name_df['last_name_cleaned'].apply(lambda x: last_name_post_clean_up(str(x),de_set))

    # Merge data from step 5 back to the original DataFrame
    # df[['first_name_cleaned','last_name_cleaned']] = name_df[['first_name_cleaned','last_name_cleaned']]
    df.insert(1,"first_name_cleaned", name_df['first_name_cleaned'])
    df.insert(1,"last_name_cleaned", name_df['last_name_cleaned'])

#####################################################################################################
    # Drop unwanted columns
    df.drop([
        "first_name",
        "last_name",
        "company_name",
        "website_cleaned",
        "profile_url",
        "location",
        "twitter_handle"
        ], axis=1, inplace=True)

    # Rename columns
    df.rename(columns={"guessed_gender":"gender",
               "first_name_cleaned":"first_name",
               "last_name_cleaned":"last_name",
               "company_name_cleaned":"company_name",
               "phone":"mobile_phone",
                'company.revenue': 'revenue', 
                'company.industries': 'industries', 
                'company.monthlyVisitors': 'monthlyVisitors', 
                'company.codeNaics': 'codeNaics', 
                'company.codeSic': 'codeSic', 
                'company.phoneNumber': 'phoneNumber', 
                'company.logo': 'logo', 
                'company.technologies': 'technologies', 
                'company.technologyCategories': 'technologyCategories', 
                'company.companiesSubsidiaries': 'companiesSubsidiaries', 
                'company.companyParent': 'companyParent', 
                'company.facebook': 'facebook', 
                'company.linkedin': 'linkedin', 
                'company.twitter': 'twitter'
               }, inplace=True)
    
    # Insert Pseudo columns
    df.insert(2,"email","")
    df.insert(2,"email_status","")
    df.insert(2,"time_in_role","")
    df.insert(2,"time_in_company","")

    # Rearrange columns
    df = df.reindex(columns=[
        "first_name", "last_name", "company_name", "job_title", 
        "email", "email_status", "department","profile_url.1", "time_in_role", 
        "time_in_company", "mobile_phone", "company_url", "country", "website", 
        "general_industry", "Industry", "overview", "connections", "company_name_page", 
        "linkedin_id", "company_id", "headcount", "employee_on_linkedin", 'revenue', 
        "followers", "headquarter", "year_founded", "specialities", "company_location", 
        'phoneNumber', 'industries', 'codeNaics', 'codeSic', 'monthlyVisitors', 'logo', 
        'technologies', 'technologyCategories', 'companiesSubsidiaries', 'companyParent', 
        'facebook', 'linkedin', 'twitter'])
#####################################################################################################

    # extract the data from columns 'first_name_cleaned' and 'last_name_cleaned' if they are a single letter or a single letter + period
    single_letter_mask = df['first_name'].str.match(r'^[A-Za-z]\.?$') | df['last_name'].str.match(r'^[A-Za-z]\.?$')
    single_letter_data = df.loc[single_letter_mask]

    # Output single letter data for further work
    single_letter_data.to_csv(single_letter_name_output_file_name,header=True,index=False)

    # Extract data whose name is not single letter
    df = df.loc[~single_letter_mask]

    print("Done cleaning first and last names ✅")

    print("\nGuessing gender based on first name...⚧️⚤")
#####################################################################################################
    # Step 6: Guess gender based on first name
    gg = GenderGuesser(openai_apikey, gender_guesser_data_file_name)
    
    gg.intake_data()

    # df['guessed_gender'] = df['first_name_cleaned'].apply(lambda x: gg.gender_guesser(x))
    df.insert(0,"gender", df['first_name'].apply(lambda x: gg.gender_guesser(x)))

    gg.save_data()

    print(f"All names processed ✅, total new names = {gg.total_count}\n")
    
#####################################################################################################
    # Finally: Output data
    df.to_csv(main_output_file_name, header=True, index=False)

    time_end = time.time()

    print(f"Total time elapsed = {time_end-time_start}")

    print(f"Rows processed = {df.shape[0]}")

if __name__ == "__main__":
    # load settings from external file and call main function with parameters
    with open("./settings/settings.json",'r') as file:
        settings = json.load(file)

    with open("./settings/name_clean_settings.json",'r') as file:
        namecleaning_settings = json.load(file)

    main(
        headers=settings['headers'],

        filename=settings['input_file_location'],

        num_of_col=settings['number_of_columns'],

        duplicate_subsets_to_drop=['linkedin_id','job_title'],

        openai_apikey=settings['openai_apikey'],

        country_list=settings['country_list_to_search'],

        countries_file_location=settings['countries_database_file_location'],

        location_countries_file_location=settings['location_countries_database_file_location'],

        location_countries_backup_file_location=settings['location_countries_backup_file_location'],

        main_output_file_name=settings['cleaned_data_output_file_name'],

        single_letter_name_output_file_name=settings['single_letter_name_output_file_name'],

        gender_guesser_data_file_name=settings['gender_guesser_data_file_name'],

        thecompanyapi_columns_to_keep=settings['thecompanyapi_columns_to_keep'],

        thecompanyapi_token=settings['thecompanyapi_token'],

        thecompanyapi_cached_file_location=settings['thecompanyapi_cached_file_location'],

        company_domain_file_location= settings["company_domain_file_location"],

        thecompanyapi_columns_to_drop= list(settings['thecompanyapi_columns_to_drop']),

        de_set = set(namecleaning_settings['de_set']),

        honorifics= set(namecleaning_settings['honorifics']),

        white_list_companies= set(namecleaning_settings['white_list_companies']),

        country_names_to_remove_from_end= set(namecleaning_settings['country_names_to_remove_from_end']),

        comma_exception_set= set(namecleaning_settings['comma_exception_set'])
    )
import re
import pandas as pd
import tldextract

def remove_blank_space(string: str)-> str:
    """
    Remove all blank space at the beginning and end of cell
    """
    return string.strip()

def remove_special_chars(string: str, chars_for_removal: list[str])-> str:
    """
    Removes specified characters from a string.
    """
    for char in chars_for_removal:
        string = string.replace(char, "")
    return string

def remove_all_info_after_comma(string: str)-> str:
    """
    Removes info after comma
    """
    if string.endswith(','):
        return string
    elif string.split(', ') is None:
        return string
    else:
        return string.split(',')[0]


def remove_words_after_slash(text):
    # Define a regular expression to match words following "/"
    pattern = r"/\w+"

    # Use the re.sub() function to replace matched words with a space
    result = re.sub(pattern, '', text)

    return result

# Example usage
text = "Ron/ATA Bourne"
result = remove_words_after_slash(text)


def remove_second_first_name_with_quotations(string: str)-> str:
    """
    When there is a first name with 2 names and "" at the end of the second first name, remove that second first name
    """
    words = string.split()
    if len(words) > 1:
        for i in range(1, len(words)):
            if '"' in words[i]:
                words[i] = ""
    return ' '.join(words)

def remove_enclosed_words(string: str)-> str:
    # Remove words enclosed in parentheses
    string = re.sub(r'\([^)]*\)', '', string)

    # Remove words enclosed in square brackets
    string = re.sub(r'\[[^]]*\]', '', string)

    # Remove words enclosed in double quotes
    string = re.sub(r'"[^"]*"', '', string)

    # Remove any remaining enclosing characters
    string = re.sub(r'[()\[\]""]', '', string)

    return string.strip()

strings = ["This is (a) test.", "Remove [these] words.", '"And" also remove "these" words.']
for string in strings:
    print(remove_enclosed_words(string))

def keep_first_name_if_two(string: str) -> str:
    name_list = string.split()
    if name_list is None or len(name_list) < 1:
        return string
    else:
        return name_list[0]

def normalize_name(s):
    """
    Normalizes a string so that the first letter is capitalized and the rest are lowercase.
    
    """
    return s.lower().capitalize()

print(normalize_name("adpfBIBi ibisadASDw"))


def remove_honorifics(s):
    """
    Removes honorifics such as "Dr.", "Mr.", and "Sr." from a string.
    """
    honorifics = ["Major", "Lieutenant Colonel",
                "Colonel", "Admiral", "Brigadier",
                "Capt","Mr.", "Mrs.", "Ms.", "Dr.",
                "Prof.", "Rev.", "Hon.", "Maj.", "Capt.",
                "Lt.", "Col.", "Sgt.", "Sir", "Madam",
                "Dame", "Lord", "Lady", "Esq.",
                "Jr.", "Sr.", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]
    for honorific in honorifics:
        s = s.replace(honorific, "")
    return s.strip()

def remove_solo_char(s: str)-> str:
    """
    Remove solo char or char followed by punctuation signs
    However, if string consist of only one solo character, leave it as is
    """
    if len(s.split()) == 1:
        return s
    else:
        pattern = r'\b[a-zA-Z](?=[^a-zA-Z]|$)\b'
        s = re.sub(pattern, '', s)
        s = re.sub(r'[^a-zA-Z0-9\s]', '', s)
        return s.strip()

def remove_any_commas(s: str)-> str:
    return s.replace(",","")

def intake_data(filename: str, headers: list[str], num_of_col: int)-> pd.DataFrame:
    """
    Takes in filename type = csv, and a list of headers

    Returns pandas dataframe
    """
    if len(headers) != num_of_col:
        # Check if num of headers matches num of columns
        print("\nThe number of column and headers is not the same! Please make sure they match\n")
        return pd.DataFrame # return empty dataframe if fails
    else:
        df = pd.read_csv(filename,names = headers, low_memory=False)
        df.drop([0], inplace=True)

        return df 

def get_main_domain(link: str) -> str:
    """
    Extract main domain from link

    Example usage:

    link1 = 'www.google.com/images'
    link2 = 'https://facebook.fr/fuiewfwefuib'
    link3 = 'not-a-valid-link'
    link4 = 'https://career.stackoverflow.com/jobs/12345/data-scientist'

    print(get_main_domain(link1))  # Output: www.google.com
    print(get_main_domain(link2))  # Output: facebook.fr
    print(get_main_domain(link3))  # Output: N/A
    print(get_main_domain(link4))  # Output: stackoverflow.com
    """
    try:
        extracted = tldextract.extract(link)
    except Exception:
        # Return "N/A" if the input is not a valid link
        return None

    subdomain = extracted.subdomain
    if subdomain == 'www':
        main_domain = '.'.join([subdomain, extracted.domain, extracted.suffix])
    else:
        main_domain = '.'.join([extracted.domain, extracted.suffix])

    # Remove "career." from the main domain if it is present
    if main_domain.startswith("career."):
        main_domain = main_domain.replace("career.", "", 1)

    return main_domain

def name_cleaning_phase1(string: str)-> str:
    """
    Function to initiate the first phase of cleaning
    """
    # removes space as well as special character
    string = remove_special_chars(string.strip(),["�", "®", "~"])

    # check if name is TRUE or FALSE
    if string.lower() in ['true','false']:
        return ""
    
    # remove all info after a comma and slash
    string = remove_words_after_slash(remove_all_info_after_comma(string))

    # remove name with double quotations
    string = remove_second_first_name_with_quotations(string)

    # remove enclosed words
    string = remove_enclosed_words(string)

    return string

def swap_first_and_last_name(df: pd.DataFrame)-> pd.DataFrame:
    """
    Swaps the first and last name in a DataFrame if the first name in a row ends with a comma,
    and removes the comma from the first name and last name if present.
    
    Args:
    df (pandas.DataFrame): The DataFrame to modify.
    
    Returns:
    pandas.DataFrame: The modified DataFrame with swapped first and last names.
    """
    # Identify rows where the first name ends with a comma
    mask = df['first_name_cleaned'].str.endswith(',')
    
    # Swap first and last name in those rows
    df.loc[mask, 'first_name_cleaned'] = df.loc[mask, 'first_name_cleaned'].str[:-1]  # remove comma from first name
    df.loc[mask, ['first_name_cleaned', 'last_name_cleaned']] = df.loc[mask, ['last_name_cleaned', 'first_name_cleaned']].values
    
    # Remove commas from last name in all rows
    df['last_name_cleaned'] = df['last_name_cleaned'].str.replace(',', '')
    
    return df

def separate_names(row):
    """
    if first_name_cleaned column has 2 names and ends with a comma, 
    separate the two names, remove the comma, and puts the second 
    name into the last_name_cleaned column
    """
    if row['first_name_cleaned'].count(' ') == 1 and row['first_name_cleaned'].endswith(','):
        names = row['first_name_cleaned'].split(' ')
        row['first_name_cleaned'] = names[0]
        row['last_name_cleaned'] = names[1].strip(',').strip()
    return row

def remove_non_ascii_rows(df: pd.DataFrame)-> pd.DataFrame:
    """
    Removes all rows from a DataFrame if they contain non-ASCII characters.

    """
    # Identify non-ASCII rows using the str.contains() method with a regular expression
    mask = df.apply(lambda x: x.str.contains('[^\x00-\x7F]')).any(axis=1)
    
    # Filter DataFrame to keep only ASCII rows
    df = df[~mask]
    
    return df

def name_cleaning_phase2(string: str)-> str:
    """
    Function to initiate second phase of cleaning
    """
    # If first or last name has two names, keep the first one
    string = keep_first_name_if_two(string)

    # Normalize name format
    string = normalize_name(string)

    # Remove English honorifics
    string = remove_honorifics(string)

    # Remove solo letters followed by punctuation
    string = remove_solo_char(string)

    # Final capitalization
    string = str(string).capitalize()

    return string
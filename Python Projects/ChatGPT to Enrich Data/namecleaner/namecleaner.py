import re
import pandas as pd
import tldextract

def remove_blank_space(string: str)-> str:
    """
    Remove all blank space at the beginning and end of cell
    """
    return string.strip()

def remove_special_chars(string: str)-> str:
    """
    Removes specified characters from a string.
    """
    for char in {"�", "®", "~"}:
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

def remove_words_after_slash(string: str) -> str:
    index = string.find('/')
    if index == -1:
        return string
    else:
        return string[:index].strip()


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

def remove_enclosed_words(text):
    # Define the characters to remove
    chars_to_remove = {"(", ")", "[", "]", "{", "}"}

    # Remove each character in turn using the str.replace() method
    for char in chars_to_remove:
        text = text.replace(char, " ")

    return text.strip()

def keep_first_name_if_two(string: str, de_set: set) -> str:
    """
    If two names in name, 
    """
    # de_set = {'el','am', 'le', 'van der', 'du', 'im', 'de la', 'do', 'aus der', 'den', 'vander', 'op den', 'von der', 'y', 'auf', "dall'", 'von und zu', 'das', 'dei', 'de', 'di', 't’', 'della', 'auf der', 'des', 'del', 'degli', "dell'", 'an', 'zur', 'de los', 'zu', 'af', 'de las', 'vanden', 'dos', 'van den', 'ten', 'ter', 'te', 'lo', 'a', 'd’', 'av', 'zum', 'op de', 'van', "d'", '‘t', 'da', 'von'}
    name_list = string.split()
    for x in name_list:
        if x.lower() in de_set:
            return string
        else: 
            pass
    if name_list is None or len(name_list) < 1:
        return string
    else:
        return name_list[0]

def normalize_name(name: str)-> str:
    """
    Normalize names    
    """
    if name == name.upper():
        if "." in name:
            return name
        else:
            return name.capitalize()
    elif name == name.lower():
        return name.capitalize()
    else:
        return name

def remove_honorifics(s: str, honorifics: set)-> str:
    """
    Removes honorifics such as "Dr.", "Mr.", and "Sr." from a string.
    """
    if s == "Majors":
        return s

    #honorifics = {"Major","Majors", "Lieutenant Colonel",
    #            "Colonel", "Admiral", "Brigadier",
    #            "Captain","Mr.", "Mrs.", "Ms.", "Dr.",'DR.','dr.',
    #            "Prof.", "Rev.", "Hon.", "Maj.", "Capt.",
    #            "Lt.", "Col.", "Sgt.", "Sir", "Madam", "Lord", "Lady", "Esq.",
    #            "Jr.", "Sr.", "Sc.", "El."}

    for honorific in honorifics:
        s = s.replace(honorific, "")
    return s.strip()

def remove_solo_char(s: str)-> str:
    """
    Remove solo char or char followed by punctuation signs
    However, if string consist of only one solo character, leave it as is
    """
    s_list = s.split()
    if len(s_list) == 1:
        return s
    else:
        for i in range(len(s_list)):
            if "." in s_list[i]:
                if len(s_list[i]) == 2:
                    s_list[i] = ""
                else:
                    pass
            else:
                pass
        return " ".join([x for x in s_list if x != ""])

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

def remove_period_at_the_end(string: str)-> str:
    if "." == string[-1:] and len(string) > 2:
        return string.replace(".","")
    else:
        return string

def name_cleaning_phase1(
        string: str, 
        honorifics: set
        )-> str:
    """
    Function to initiate the first phase of cleaning
    """
    # Remove English honorifics
    string = remove_honorifics(string, honorifics)

    # removes space as well as special character
    string = remove_special_chars(string.strip())

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

def capitalize_hyphenated_name(name: str) -> str:
    name_list = name.split('-')
    if len(name_list) == 1:
        return name
    else:
        name_list = [x.capitalize() for x in name_list]
        return '-'.join(name_list)
    
def remove_special_chars2(input_string):
    # remove characters after '|' character
    input_string = input_string.split('|')[0]
    
    # remove characters after '\' character
    input_string = input_string.split('\\')[0]
    
    # remove characters after '/' character
    input_string = input_string.split('/')[0]
    
    return input_string

def remove_single_letter(name: str)-> str:
    name_list = name.split()
    name_list = [x.replace('.','') for x in name_list]
    if len(name_list) == 1:
        return name
    else:
        for i in range(len(name_list)):
            if len(name_list[i]) == 1:
                name_list[i] = ""
            else:
                pass
        return ' '.join(name_list).strip()

def name_cleaning_phase2(
        string: str,
        de_set: set,
        honorifics: set,
        )-> str:
    """
    Function to initiate second phase of cleaning
    """
    # Remove English honorifics
    string = remove_honorifics(string, honorifics)

    string = remove_period_at_the_end(string)

    # Remove single letter
    string = remove_single_letter(string)

    # If first or last name has two names, keep the first one
    string = keep_first_name_if_two(string, de_set)

    # Normalize names
    string = normalize_name(string)

    # Remove solo letters followed by punctuation
    string = remove_solo_char(string)

    # Capitalize hyphenated names
    string = capitalize_hyphenated_name(string)

    return string

def remove_enclosures(text):
    # Regular expression to match words enclosed in parentheses, quotes, square brackets, and curly braces
    pattern = re.compile(r'(\((.*?)\)|\"(.*?)\"|\'(.*?)\'|\[(.*?)\]|\{(.*?)\})')

    # Remove all instances of the pattern in the text
    result = re.sub(pattern, '', text)

    return result.strip()

def capitalize_hyphenated_company_name(string: str)-> str:
    if "-" in string:
        string_list = string.split()
        for i in range(len(string_list)):
            if "-" in string_list[i]:
                string_list[i] = capitalize_hyphenated_name(string_list[i])
            else:
                pass
        return ' '.join(string_list)
    else:
        return string

def clean_company_name(company: str)-> str:
    company = remove_enclosures(company)
    company = remove_enclosed_words(company)
    company = remove_all_info_after_comma(company)
    company = remove_words_after_slash(company)
    company = remove_special_chars2(company)
    company = capitalize_hyphenated_company_name(company)
    return company


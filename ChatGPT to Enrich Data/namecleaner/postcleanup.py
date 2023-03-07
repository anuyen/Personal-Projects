def keep_first_hyphenated(name: str, de_set: set):
    if "-" in name:
        if name.split('-')[0].lower() in de_set:
            return name
        else:
            return name.split('-')[0]
    else:
        return name
    
def obrien_function(name: str)-> str:
    """
    in: O'brian
    out: O'Brian
    """
    if "'" in name:
        name_list = name.split("'")
        name_list = [x.capitalize() if len(x) > 1 else x for x in name_list]
        return "'".join(name_list)
    else:
        return name

def mcdonald_function(name: str)-> str:
    """
    in: mcdonald, Mcdonald
    out: McDonald
    """
    if "mc" == name.lower()[:2]:
        return name[:2].capitalize() + name[2:].capitalize()
    else:
        return name

def capitalize_potential_acronyms(name: str)-> str:
    """
    in: gkn Aerospace
    out: GKN Aerospace

    in: U.s Army
    out: U.S Army
    """
    name_list = name.split()
    if len(name_list) == 1:
        if len(name) <= 4:
            if name == name.capitalize():
                return name
            elif name == name.upper():
                return name
            elif len(name) <= 2:
                return name.upper()
            elif len(name) == 3:
                return name
            else:
                return name.capitalize()
        else:
            if '.com' in name.lower():
                return name
            if '.' in name:
                if "." == name[0]:
                    return name[1:]
                if '.' == name[len(name)-1:] and name.count(".") == 1:
                    return name.capitalize()
                else:
                    if ".com" in name.lower():
                        return name
                    else:
                        sub_list = name.split(".")
                        for j in range(len(sub_list)):
                            if len(str(sub_list[j])) >= 3:
                                pass
                            else:
                                sub_list[j] = sub_list[j].upper()
                        return ".".join(sub_list)
            if name == name.upper():
                return name.capitalize()
            elif name == name.lower():
                return name.capitalize()
            else:
                return name
    else:
        for i in range(len(name_list)):
            if name_list[i].lower() == "and":
                pass
            if len(name_list[i]) <= 4:
                if name_list[i].lower() == "air":
                    name_list[i] = name_list[i].capitalize()
                if name_list[i] == name_list[i].capitalize():
                    pass
                elif name_list[i] == name_list[i].upper():
                    pass
                else:
                    name_list[i] = name_list[i].capitalize()
            else:
                if name_list[i] == name_list[i].upper():
                    name_list[i] = name_list[i].capitalize()
                elif name_list[i] == name_list[i].lower():
                    name_list[i] = name_list[i].capitalize()
                else:
                    pass
        for i in range(len(name_list)):
            if '.com' in name_list[i].lower():
                pass
            if 'www.' in name_list[i].lower():
                pass
            if '.net' in name_list[i].lower():
                pass
            if '.' in name_list[i]:
                if name_list[i].lower() in {"st.","co.","no."}:
                    name_list[i] = name_list[i].capitalize()
                if '.' == name_list[i][len(name_list[i])-1:] and name_list[i].count(".") == 1:
                    name_list[i] = name_list[i].capitalize()
                else:
                    if ".com" in name_list[i].lower():
                        pass
                    else:
                        sub_list = name_list[i].split(".")
                        for j in range(len(sub_list)):
                            if len(str(sub_list[j])) >= 3:
                                pass
                            else:
                                sub_list[j] = sub_list[j].upper()
                        name_list[i] = ".".join(sub_list)
        return ' '.join(name_list)
    
def last_capitalization(name: str, de_set: set)-> str:
    name_list = name.split()
    if len(name_list) == 1:
        return name
    else:
        for i in range(len(name_list)):
            if name_list[i].lower() in de_set:
                pass
            elif name_list[i] == name_list[i].lower():
                name_list[i] = name_list[i].capitalize()
            elif name_list[i] == name_list[i].upper():
                name_list[i] = name_list[i].capitalize()
            else:
                pass
        return " ".join(name_list)
    
def last_name_post_clean_up(name: str, de_set: set)-> str:
    name = keep_first_hyphenated(name, de_set)
    name = last_capitalization(name, de_set)
    name = obrien_function(name)
    name = mcdonald_function(name)

    return name

def remove_after_long_hypen(string: str)-> str:
    if " - " in string:
        return string.split(' - ')[0]
    else:
        return string
    
def remove_after_long_hypen2(string: str)-> str:
    if "- " in string:
        return string.split('- ')[0]
    else:
        return string
    
def remove_after_long_hypen3(string: str)-> str:
    if " -" in string:
        return string.split(' -')[0]
    else:
        return string

def remove_what_comes_after_a_single_parenthensis(string: str) -> str:
    """
    in: Your Momma (she
    out: Your Momma
    """
    index = string.find('(')
    if index == -1:
        return string
    else:
        return string[:index-1]

def remove_what_comes_after_a_single_bracket(string: str) -> str:
    index = string.find('[')
    if index == -1:
        return string
    else:
        return string[:index-1]

def remove_what_comes_after_a_fwdslash_and_space(string: str) -> str:
    index = string.find('/ ')
    if index == -1:
        return string
    else:
        return string[:index]

def remove_what_comes_after_a_fwdslash(string: str) -> str:
    index = string.find('/')
    if index == -1:
        return string
    else:
        return string[:index]

def remove_what_comes_after_a_comma(string: str, comma_exception_set: set) -> str:
    if string in comma_exception_set:
        return string   
    index = string.find(',')
    if index == -1:
        return string
    else:
        return string[:index]
    
def remove_what_comes_after_an_and(string: str) -> str:
    index = string.find(' & ')
    if index == -1:
        return string
    else:
        return string[:index]
    
def remove_what_comes_after_an_at(string: str) -> str:
    index = string.find('@')
    if index == -1:
        return string
    else:
        return string[:index].strip()
    
def remove_what_comes_after_a_vertical_bar(string: str) -> str:
    """
    in: Your Momma (she
    out: Your Momma
    """
    index = string.find('|')
    if index == -1:
        return string
    else:
        return string[:index].strip()
    
def remove_what_comes_after_a_semicolon(string: str) -> str:
    """
    in: Your Momma (she
    out: Your Momma
    """
    index = string.find(';')
    if index == -1:
        return string
    else:
        return string[:index]
    
def capitalize_hyphenated(string: str)-> str:
    if "-" in string:
        string_list = [x.capitalize() if x == x.lower() else x for x in string.split('-')]
        return '-'.join(string_list)
    else:
        return string
    
def remove_after_inc_ltd(string: str)-> str:
    li = {'inc','inc.','ltd'}
    name_list = string.split()

    for i in range(len(name_list)):
        if name_list[i].lower() in li:
            name_list = name_list[:i]
            break
        else:
            pass
    
    return ' '.join(name_list)

def remove_country_name_if_at_the_end(
        string: str,
        white_list_companies: set,
        country_names_to_remove_from_end: set
        )-> str:
    if string == "":
        return string
    if " North America" in string:
        return string.replace(" North America",'')
    if " N. America" in string:
        return string.replace(" N. America",'')
    if " N America" in string:
        return string.replace(" N. America",'')

    # include companies to "whitelist" below
    if string.strip().lower() in white_list_companies:
        return string
    
    # include companies to remove from the end below
    #country_names_to_remove_from_end = {'canada','usa','india','france','italy','england','ireland','us','na','uk','china',
    #                 'russia','mexico','vietnam','germany','japan','korea','brazil'}

    name_list = string.split()
    if len(name_list) == 1:
        return string

    if name_list[-1:][0].lower() in country_names_to_remove_from_end:
        return " ".join(name_list[:-1])
    else:
        return string
    
def remove_stuffs(string: str)-> str:
    if "-KLM" in string:
        return string.replace("-KLM","")
    if string == "Air France KLM":
        return "Air France"
    if ",Inc" in string:
        return string.replace(",Inc","")
    else:
        return string


def company_name_post_clean_up(
        name: str,
        white_list_companies: set,
        country_names_to_remove_from_end: set,
        comma_exception_set: set
        )-> str:
    name = remove_after_long_hypen(name)
    name = remove_after_long_hypen2(name)
    name = remove_after_long_hypen3(name)
    name = remove_what_comes_after_a_single_parenthensis(name)
    name = remove_what_comes_after_a_single_bracket(name)
    name = remove_what_comes_after_a_fwdslash_and_space(name)
    name = remove_what_comes_after_a_fwdslash(name)
    name = remove_what_comes_after_a_semicolon(name)
    name = remove_what_comes_after_a_vertical_bar(name)
    name = remove_what_comes_after_an_at(name)
    name = remove_country_name_if_at_the_end(name,white_list_companies,country_names_to_remove_from_end)
    name = remove_after_inc_ltd(name)
    name = capitalize_hyphenated(name)
    name = capitalize_potential_acronyms(name)
    name = remove_country_name_if_at_the_end(name,white_list_companies,country_names_to_remove_from_end)
    name = remove_stuffs(name)
    name = remove_what_comes_after_a_comma(name, comma_exception_set)

    name_list = [mcdonald_function(obrien_function(capitalize_hyphenated(x))) for x in name.split()]

    return " ".join(name_list)
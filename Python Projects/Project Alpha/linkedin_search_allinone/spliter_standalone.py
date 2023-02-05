import os
import time
import sys
import json
import jsonpath
import traceback

from datetime import datetime
from threading import Thread

def read_settings():
    settings = []
    if os.path.exists("settings_clean.json"):
        with open("settings_clean.json", "r", encoding="utf-8") as r:
            text = r.read()
            #text = text[1:]
            settings = json.loads(text)
    return settings


def split(file, country, number):

    if not os.path.exists(file):
        print("File {0} doesn't exists, do nothing...".format(file))

    if not os.path.exists(country):
        os.mkdir(country)
    
    print("Now spliting file {0} into smaller batches, {1} lines per batch.".format(file, number))
    spliter = "\\" if "win32" in sys.platform else "/"
    batch_file_name = file.split(spliter)[-1].replace(".json", "")

    current_files = list(os.listdir(country))
    # remove previous files (xlsx)
    results_previous_run = [t for t in current_files if t.endswith("xlsx")]
    for t in results_previous_run:
        full_name = "{0}{1}{2}".format(country, spliter, t)
        os.remove(full_name)
    # try to find the smaller batch files (smaller json)
    batch_files = [t for t in os.listdir(country) if t.startswith("{0}_".format(batch_file_name)) and t.endswith(".json")]
    if len(batch_files) > 0:
        print(">>> File {0} is already split into smaller batches, do nothing for now.".format(file))
        return

    cache = []
    batch_idx = 1
    with open(file, "r", encoding="utf8") as f:
        for line in f:
            l = line.strip()
            if len(l) == 0:
                continue
            #if '"linkedin_connections":null' in l:
            #    continue
            
            cache.append(l)
            if len(cache) == number:
                batch_file = "{0}/{1}_{2}.json".format(country, batch_file_name, batch_idx)
                with open(batch_file, "w", encoding="utf8") as w:
                    w.write("\n".join(cache))
                print("Batch {0} saved.".format(batch_file))
                batch_idx += 1
                cache = []

    if len(cache) > 0:
        batch_file = "{0}/{1}_{2}.json".format(country, batch_file_name, batch_idx)
        with open(batch_file, "w", encoding="utf8") as w:
            w.write("\n".join(cache))
        print("Batch {0} saved.".format(batch_file))


def split_files():

    start_date = datetime.now()
    print(">>> Split process started at {0}.".format(start_date))

    settings = read_settings()
    filtered_folder = []
    for setting in settings:
        spliter = "\\" if "win32" in sys.platform else "/"
        input_folder = setting["input_folder"]
        batch_size = setting["batch_size"]
        input_files = ["{0}{1}{2}".format(input_folder, spliter, t) for t in os.listdir(input_folder) if t.endswith(".json")]
        print(">>> There are {0} files to split in input folder...".format(len(input_files)))
        for input_file in input_files:
            print("> Start split file {0}.".format(input_file))
            split(input_file, setting["country_name"], batch_size)

        print(">>> Start clean data by linkedin_connections...")
        folder = setting["country_name"]
        if folder not in filtered_folder:
            filter_files(setting)
            filtered_folder.append(setting["country_name"])
        else:
            print("\r\n>>> Folder {0} is already processed, don't repeat!\r\n".format(folder))

    end_date = datetime.now()
    print("Split process ended at {0}. Time cost: {1}.".format(end_date, (end_date - start_date)))


def filter_files(setting):
    spliter = "\\" if "win32" in sys.platform else "/"
    input_folder = setting["input_folder"]
    threads = setting["spliter_thread"]
    connections_number = setting["connections"]
    country_folder = setting["country_name"]
    files = [t for t in os.listdir(country_folder) if t.endswith(".json")]
    files = ["{0}{1}{2}".format(country_folder, spliter, t) for t in files]
    thread_list = []
    while True:
        if len(files) == 0:
            break

        if len(thread_list) < threads:
            file = files[0]
            files.remove(file)
            thread = Thread(target=filter_a_file, args=(file, connections_number, ), name=file.split(spliter)[-1])
            thread.start()
            print("Thread {0} is started.".format(thread.name))
            thread_list.append(thread)
        
        thread_list = [t for t in thread_list if t.is_alive()]
        print("{0} converting threads running...".format(len(thread_list)))
        time.sleep(5)

    while True:
        thread_list = [t for t in thread_list if t.is_alive()]
        print("{0} converting threads running...".format(len(thread_list)))
        time.sleep(5)
        if len(thread_list) == 0:
            print("No acitve threads, stop!")
            break


def filter_a_file(file_name, connection_number):
    new_lines = []
    with open(file_name, "r", encoding="utf8") as f:
        for line in f:
            try:
                data_json = None
                try:
                    data_json = json.loads(line.strip(), strict=False)
                except:
                    print("\r\n\r\n")
                    print("Failed to load json, skip this people...")
                    print(line)
                    print("\r\n\r\n")
                    continue

                if data_json["linkedin_connections"] is None:
                    line = process_email(line, data_json)
                    new_lines.append(line.strip())
                    continue
                if data_json["linkedin_connections"] >= connection_number:
                    line = process_email(line, data_json)
                    new_lines.append(line.strip())
            except:
                print(traceback.format_exc())
                continue
    with open(file_name, "w", encoding="utf8") as w:
        w.write("\n".join(new_lines))


def process_email(line, data_json):
    #data_json = json.loads(line.strip())
    job_company_website_node = jsonpath.jsonpath(data_json, "$.job_company_website")
    if job_company_website_node == False:
        return line
    company_website = job_company_website_node[0]
    if company_website is None or len(company_website) == 0:
        return line
    company_website = company_website.lower()
    work_email_node = jsonpath.jsonpath(data_json, "$.work_email")
    work_email = "" if work_email_node == False else work_email_node[0]
    professional_email_node = jsonpath.jsonpath(data_json, "$.emails[?(@.type=='professional')].address")
    professional_email = "" if professional_email_node == False else professional_email_node[0]
    current_professional_email_node = jsonpath.jsonpath(data_json, "$.emails[?(@.type=='current_professional')].address")
    current_professional_email = "" if current_professional_email_node == False else current_professional_email_node[0]
    personal_email_node = jsonpath.jsonpath(data_json, "$.emails[?(@.type=='personal')].address")
    personal_email = "" if personal_email_node == False else personal_email_node[0]
    none_type_email_node = jsonpath.jsonpath(data_json, "$.emails[?(@.type==None)].address")
    none_type_email = "" if none_type_email_node == False else none_type_email_node[0]
    other_emails = [professional_email, current_professional_email, personal_email, none_type_email]
    other_emails = [t for t in other_emails if t is not None and "@" in t]

    if work_email is not None and len(work_email) > 0:
        domain = work_email.split('@')[-1].lower()
        if domain in company_website:
            print("Email {0} match website {1}, don't change...".format(work_email, company_website))
            return line
        else:
            if len(other_emails) == 0:
                return line
            else:
                for email in other_emails:
                    domain = email.split('@')[-1].lower()
                    if domain in company_website:
                        print("Change work email from {0} to {1}.".format(work_email, email))
                        data_json["work_email"] = email
                        new_line = json.dumps(data_json)
                        return new_line

    else:
        if len(other_emails) == 0:
            return line
        else:
            for email in other_emails:
                domain = email.split('@')[-1].lower()
                if domain in company_website:
                    print("Change work email from {0} to {1}.".format(work_email, email))
                    data_json["work_email"] = email
                    new_line = json.dumps(data_json)
                    return new_line
    return line
    


split_files()


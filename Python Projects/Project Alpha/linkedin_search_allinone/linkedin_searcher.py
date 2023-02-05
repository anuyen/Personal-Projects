import os 
import json
import time
import sys
import traceback

from sys import argv
from spliter import split
from converter import *
from datetime import datetime
from threading import Thread


def read_settings():
    settings = []
    if os.path.exists("settings.json"):
        with open("settings.json", "r", encoding="utf-8") as r:
            text = r.read()
            text = text[1:]
            settings = json.loads(text)
    return settings


def read_cleaned_folders():
    clean_folders = []
    if os.path.exists("cleaned_folders.txt"):
        with open("cleaned_folders.txt", "r", encoding="utf8") as r:
            clean_folders = [t.strip() for t in r.readlines() if len(t.strip()) > 0]
    return clean_folders

def convert_to_table(files, setting, mode):

    raw_folder = setting["raw_folder"]
    thread_number = setting["thread_number"]
    thread_list = []
    spliter = "\\" if "win32" in sys.platform else "/"
    if mode == "clean":
        if os.path.exists(raw_folder):
            shutil.rmtree(raw_folder)
        time.sleep(2)
        os.mkdir(raw_folder)
    if not os.path.exists(raw_folder):
        os.mkdir(raw_folder)

    while True:
        if len(files) == 0:
            break

        if len(thread_list) < thread_number:
            file = files[0]
            files.remove(file)
            thread = Thread(target=convert_a_file, args=(file, setting, ), name=file.split(spliter)[-1])
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


def split_the_input_files(setting):
    spliter = "\\" if "win32" in sys.platform else "/"
    input_folder = setting["input_folder"]
    batch_size = setting["batch_size"]
    input_files = ["{0}{1}{2}".format(input_folder, spliter, t) for t in os.listdir(input_folder) if t.endswith(".json")]
    print(">>> There are {0} files to split in input folder...".format(len(input_files)))
    for input_file in input_files:
        print("> Start split file {0}.".format(input_file))
        split(input_file, setting["country_name"], batch_size)


def merge_final_results(setting):
    raw_folder = setting["raw_folder"]
    if not os.path.exists(raw_folder):
        return

    spliter = "\\" if "win32" in sys.platform else "/"
    raw_output_files = [t for t in os.listdir(raw_folder) if t.endswith(".json")]
    
    batch_size = setting["output_tab_size"]
    print(">>> Split final results into batches, {0} per batch.".format(batch_size))
    raw_list = []
    batch_list = []
    for raw_file in raw_output_files:
        raw_path = "{0}{1}{2}".format(raw_folder, spliter, raw_file)
        reading_list = []
        with open(raw_path, "r", encoding="utf-8") as r:
            reading_list = json.loads(r.read())
        for reading_item in reading_list:
            batch_list.append(reading_item)
            if len(batch_list) == batch_size:
                raw_list.append(batch_list)
                batch_list = []
        os.remove(raw_path)
    
    if len(batch_list) > 0:
        raw_list.append(batch_list)

    print("Generated {0} batches, {1} rows per batch.".format(len(raw_list), batch_size))
    file_name = "{0}{1}raw_final.json".format(raw_folder, spliter)
    with open(file_name, "w", encoding="utf-8") as w:
        w.write(json.dumps(raw_list))
    print(">>> Start converting final results to excel files...")
    index = 0
    for batch_list in raw_list:
        index = index + 1
        file_name = "{0}_final_{1}.json".format(setting["run"], index)
        try:
            convert_results(file_name, batch_list, setting)
        except Exception as e:
            print(traceback.format_exc())
    print("Files are generated.")



def Start(mode):

    start_time = datetime.now()

    spliter = "\\" if "win32" in sys.platform else "/"
    print("\r\n> Read settings...\r\n")
    settings = read_settings()
    cleaned_folders = read_cleaned_folders()
    for setting in settings:
        apply_thread = Thread(target=apply_setting, args=(setting, spliter, cleaned_folders, ), name='apply_thread_{0}'.format(setting["run"]))
        apply_thread.start()
        #apply_setting(setting)

    end_date = datetime.now()
    time_cost = end_date - start_time
    print("\r\n>>> Start at {0}, end at {1}, time cost {2}.\r\n".format(start_time, end_date, time_cost))


def apply_setting(setting, spliter, cleaned_folders):
    print("\r\n> Start working on setting {0}.\r\n".format(setting["country_name"]))
    print("\r\n>>> Split input files into smaller list...\r\n")
    #split(setting["input_file"], setting["country_name"], 50000)
    country_folder = setting["country_name"]
    if country_folder not in cleaned_folders:
        split_the_input_files(setting)
    else:
        print("Folder {0} is confirmed cleaned before starting, don't double check!".format(country_folder))
    print("\r\n>>> Convert JSON lines into table format...\r\n")
    country_folder = setting["country_name"]
    country_files = ["{0}{1}{2}".format(country_folder, spliter, t) for t in os.listdir(country_folder) if t.endswith(".json")]
    convert_to_table(country_files, setting, mode)
    print("\r\n>>> Generating final excel files...\r\n")
    merge_final_results(setting)


mode = "" if len(argv) == 1 else argv[1]
Start(mode)

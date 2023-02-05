import os
import time
import sys

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
            if len(line.strip()) == 0:
                continue
            cache.append(line.strip())
            
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



#split("bolivia-4.txt", "bolivia", 10000)

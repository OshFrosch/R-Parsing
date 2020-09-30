import fileinput
import json
import logging
import os
import re
from collections import OrderedDict
from os import listdir
from os.path import join, isfile
from time import strptime

import pandas as pd

from src.core.util.string_utils.diverse import get_page_number


def save_to_json(directory, filenames, *objects):
    if isinstance(filenames, str):
        single_save_to_json(directory, filenames, objects)
    else:
        group_save_to_json(directory, filenames, objects)


def single_save_to_json(directory, filename, obj):
    if len(obj) > 1:
        raise ValueError("There has to be the same amount of filenames" +
                         f"({1}) and objects({len(obj)}).")

    if isinstance(obj, pd.DataFrame):
        save_dataframe_to_json(directory, filename, obj[0])
    else:
        save_object_to_json(directory, filename, obj[0])


def group_save_to_json(directory, filenames, objects):
    if len(filenames) != len(objects):
        raise ValueError("There has to be the same amount of filenames" +
                         f"({len(filenames)}) and objects({len(objects)}).")

    for i in range(len(objects)):
        if isinstance(objects[i], pd.DataFrame):
            save_dataframe_to_json(directory, filenames[i], objects[i])
        else:
            save_object_to_json(directory, filenames[i], objects[i])


def save_dataframe_to_json(directory, filename, data_frame):
    create_folder_if_necessary(directory)
    json_file = json.dumps([row.dropna().to_dict()
                            for index, row in data_frame.iterrows()])
    with open(directory + filename, "w") as f:
        f.write(json_file)


def save_object_to_json(directory, filename, obj):
    create_folder_if_necessary(directory)
    with open(directory + filename, 'w') as file:
        file.write(json.dumps(obj))


def json_to_list(json_file):
    with open(json_file, "r") as file:
        file_string = file.read()
    dic_list = json.loads(file_string)
    return dic_list


def json_to_dic(json_file, reverse=False):
    dic_list = json_to_list(json_file)
    dic = dic_list
    if reverse:
        dic = {v: k for k, v in dic.items()}
    return dic


def json_to_ordered_dic(json_file):
    return json.load(open(json_file), object_pairs_hook=OrderedDict)


def join_all_jsons_to_list_from(directory):
    jsons_list = []
    for filename in listdir(directory):
        full_path = join(directory, filename)
        if isfile(full_path):
            jsons_list.extend(json_to_list(full_path))

    return jsons_list


def create_folder_if_necessary(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory.' + directory)


def log_current_page(url):
    page_number = get_page_number(url)
    log_string_in('../res/logs/', 'last_page_number.log', page_number)


def log_preprocess_started(filename, process_id=os.getpid()):
    log_entry = f"Preprocessing: {filename}"
    log_string_in('../res/logs/preprocessing/',
                  f'preprocess_process{process_id}.log',
                  log_entry)


def log_preprocess_finished(filename, process_id=os.getpid()):
    log_entry = f"Finished preprocessing: {filename} on process {process_id}"
    log_string_in('../res/logs/preprocessing/',
                  f'preprocess_process{process_id}.log',
                  log_entry)


def log_string_in(directory, filename, string):
    create_folder_if_necessary(directory)
    logging.basicConfig(
        format="%(asctime)s %(levelname)-8s %(message)s",
        filename=os.path.join(directory, filename),
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S")
    logging.info(string)


def merge_preprocess_logs():
    lines = list(fileinput.input(os.listdir('../res/logs/preprocessing/')))
    delete_old_preprocess_logfiles()
    time_format = "%Y-%m-%d %H:%M:%S"
    time_extract_regex = re.compile(r'\[(.+?)\]')
    with open(f'../res/logs/merged_preprocessing.log', "a") as file:
        file.write("\n".join(
            sorted(lines,
                   key=lambda l: strptime(time_extract_regex
                                          .search(l)
                                          .group(1),
                                          time_format)
                   )
        ))


def delete_old_preprocess_logfiles():
    for file in os.listdir('../res/logs/preprocessing/'):
        os.remove(file)


def get_last_fetched_page():
    result = 1
    if isfile('../res/logs/last_page_number.log'):
        with open('../res/logs/last_page_number.log', 'r') as file:
            string = file.read()
            lines = string.split("\n")
        words = lines[-2].rstrip().split(":")
        number = [element for element in words if element.isdigit()]
        result = number[0]
    return result


def get_last_fetched_repo_index():
    max_index = 0
    if os.path.isdir("../res/generated/download_links/"):
        with os.scandir("../res/generated/download_links/") as it:
            for entry in it:
                if entry.is_file():
                    indicies = list(map(int, re.findall(r'\d+', entry.name)))
                    if max_index < indicies[-1]:
                        max_index = indicies[-1]
    return max_index


def get_last_downloaded_repo_index(repo_names):
    res = 0
    if os.path.isdir("../res/data"):
        with os.scandir("../res/data") as it:
            for entry in it:
                if entry.is_dir():
                    if entry.name in repo_names:
                        res += 1
    return res

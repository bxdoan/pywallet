#!/usr/bin/env python3
import base64
import hashlib
import os
import sys
import time
import subprocess
import sys
from itertools import cycle, zip_longest
from random import randint, seed

import base58
from cryptography.hazmat.primitives.ciphers.algorithms import AES
from web3 import Web3
from cryptography.fernet import Fernet
from pywallet.constants import TMP_DIR


def type_writer(message, delay_time):
    for char in message:
        print(char, end='')
        sys.stdout.flush()
        time.sleep(delay_time)

    time.sleep(0.1)


def get_filename_from_path(path):
    return os.path.basename(path)


def get_list_of_files_in_folder(folder_path):
    return os.listdir(folder_path)


# get list of name files without ext in folder
def get_list_of_name_files_without_ext_in_folder(folder_path):
    list_of_files = get_list_of_files_in_folder(folder_path)
    list_of_name_files = []
    for file in list_of_files:
        name_file = file.split('.')[0]
        list_of_name_files.append(name_file)
    return list_of_name_files


def run_bash(cmd : str = '') -> tuple:
    # mix stdout and stderr into a single string ref. https://stackoverflow.com/a/41172862/248616
    sp  = subprocess.run(cmd.split(' '), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    r   = sp.stdout.decode('utf-8')
    err = sp.returncode
    return r, err


# diff two dict and add more key to the first dict
def diff_dict_and_add_more_key(sample_dict : dict, real_dict : dict) -> dict:
    for key, value_sample_by_key in sample_dict.items():
        if not value_sample_by_key:
            continue
        elif isinstance(value_sample_by_key, dict):
            value_real_by_key = real_dict.get(key)
            if isinstance(value_real_by_key, dict):
                val_after = diff_dict_and_add_more_key(value_sample_by_key, value_real_by_key)
                real_dict = do_change_val(real_dict, key, val_after)
            else:
                real_dict = do_change_val(real_dict, key, value_sample_by_key)
        else:
            value_real_by_key = real_dict.get(key)
            if not value_real_by_key:
                real_dict = do_change_val(real_dict, key, value_sample_by_key)
    return real_dict


def do_change_val(data : dict, k : str, v=None) -> dict:
    data.update({
        k: v
    })
    return data


def halt_if_run_bash_failed(run_bash_result):
    output_text, error_code = run_bash_result
    if error_code != 0 :
        raise Exception(f'Failed run_bash()\nError:\n{output_text}')


def to_checksum_address(address):
    return Web3.toChecksumAddress(address)


def get_length_of_longest_string_value_in_list_of_dict(list_of_dict : list = [], key : str = '') -> int:
    longest = 0
    for d in list_of_dict:
        if len(d[key]) > longest:
            longest = len(d[key])
    return longest


# check string in list of string and add more if not exited
def check_string_in_list_of_string_and_add_more_if_not_exited(list_of_string : list = [], string : str = '') -> list:
    if string not in list_of_string:
        list_of_string.append(string)
    return list_of_string

# check string in list of string and remove if exited
def check_string_in_list_of_string_and_remove_if_exited(list_of_string : list = [], string : str = '') -> list:
    if string in list_of_string:
        list_of_string.remove(string)
    return list_of_string


def get_list_of_name_dir_in_folder(folder_path):
    list_of_dir = os.listdir(folder_path)
    list_of_name_dir = []
    for dir in list_of_dir:
        name_dir = dir.split('.')[0]
        list_of_name_dir.append(name_dir)
    return list_of_name_dir


def run_bash_complex(target_cmd, custom_name=None):
    """
    complex means some bash commands have piping |, redirect >, etc. that cannot run via run_bash()
    we will right the :target_cmd,
    i.e the complex bash command, to a bash file and run it
    """
    if custom_name is None:
        custom_name = hash(target_cmd)

    # prepare :sh_file to store :target_cmd
    sh_file_dir = f'{TMP_DIR}/run_bash_complex'
    sh_file     = f'{sh_file_dir}/{custom_name}.sh'  # sh file stored here

    os.makedirs(sh_file_dir, exist_ok=True)  # prepare folder path

    # write :target_cmd to .sh file
    with open(sh_file, 'w') as f:
        f.write(
            f'#!/bin/bash\n'
            f'{target_cmd} | tee {sh_file}.log'
        )

    # add +x permission to it
    _ = run_bash(f'chmod +x {sh_file}')
    halt_if_run_bash_failed(_)

    # run the created .sh file
    assert os.path.isfile(sh_file)
    _ = run_bash(sh_file)
    halt_if_run_bash_failed(_)
    return _


def normalize_to_bool(input):
    if isinstance(input, bool):
        return input

    elif isinstance(input, str):
        #TODO consider to replace below block by
        # if   v in TRUE_VALUE_AS_STR:  data[k]=True
        # elif v in FALSE_VALUE_AS_STR: data[k]=False

        if input.lower().strip() == 'true': return True
        if input.lower().strip() == 't':    return True
        if input.lower().strip() == 'True': return True
        if input.lower().strip() == 'T':    return True
        if input.lower().strip() == 'yes':  return True
        if input.lower().strip() == 'Yes':  return True
        if input.lower().strip() == 'y':    return True
        return False

    else:
        return False

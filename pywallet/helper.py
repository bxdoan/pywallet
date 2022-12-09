#!/usr/bin/env python3
import os
import sys
import time
import subprocess
from web3 import Web3
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

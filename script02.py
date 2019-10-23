#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import logging
import subprocess
import re
import requests
import json
import sys

TUTORIAL_PATH = "/home/rg3915/gh/pybr19/tutorial-monitorando-django-pybr2019/"

logging.basicConfig(filename=TUTORIAL_PATH + "logfile_read_files.log",
                    format="%(asctime)s %(message)s",
                    filemode="a")

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.debug("Iniciando o tutorial")


def check_disk():
    logger.debug("Iniciando a funcao check_disk")
    reponse = subprocess.check_output(
        ["df -h --output=pcent /home/fcarval | tail -n 1"],
        shell=True)
    return re.search("(\d+)", reponse.decode("utf-8")).group(1)


def get_latency():
    logger.debug("Iniciando a funcao get_latency")
    response = subprocess.check_output(["ping -c 1 8.8.8.8"], shell=True)
    return re.search("time=(.*) ms", response.decode("utf-8")).group(1)


def read_files_in_repo(repo_path, files_list):
    logger.debug("Iniciando a funcao read_files_in_repo")
    os.chdir(repo_path)
    value = 0
    for file in files_list:
        f = open(file, "r")
        value += int(f.read())
    return value


def main(rack_name):
    logger.debug("Iniciando a funcao main")
    os.chdir(TUTORIAL_PATH)
    total_value = 0
    for root, dirs, files in os.walk(TUTORIAL_PATH):
        if len(dirs) == 0:
            total_value += read_files_in_repo(root, files)
    disk_usage = check_disk()
    latency = get_latency()
    data = {'rack_name': rack_name, 'total_value': total_value,
            'disk_usage': disk_usage, 'latency': latency}
    request = requests.post(
        'http://localhost:8000/api/reports', data=json.dumps(data))


if __name__ == "__main__":
    rack_name = sys.argv[1]  # argv 0 eh o nome o
    main(rack_name)

#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import os
import random
import shutil
import datetime

# substitua pelo caminho completo em sua máquina
TUTORIAL_PATH = "/home/rg3915/gh/pybr19/tutorial-monitorando-django-pybr2019/"

logging.basicConfig(filename=TUTORIAL_PATH + "logfile_generate_files.log",
                    format="%(asctime)s %(message)s",
                    filemode="a")

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.debug("Iniciando o tutorial")
logger.info("Uma informação")
logger.warning("Um aviso")
logger.error("Dividir zero por zero dá ruim")
logger.critical("Acabou o café")


def create_files():
    logger.debug("Iniciando a funcao create_files")
    for i in range(1, 101):
        new_value = random.randint(101, 1000)
        try:
            file = open("report" + str(i) + ".txt", "r+")
            content = int(file.read())
            file.seek(0)
            file.truncate()
            file.write(str(new_value + content))

        # python2 usa IOError
        except FileNotFoundError:
            logger.error("Arquivo nao encontrado. Criando arquivo")
            file = open("report" + str(i) + ".txt", "w")
            file.write(str(new_value))

        file.close()


def clean_repos(now):
    logger.debug("Iniciando a funcao clean_repos")
    time_ago = now - datetime.timedelta(minutes=5)

    for repo in os.listdir(TUTORIAL_PATH):
        if os.path.isdir(repo) and repo.startswith('repo'):
            name_to_datetime = datetime.datetime.strptime(
                repo, 'repo%Y%m%d_%H%M')
            if name_to_datetime < time_ago:
                shutil.make_archive(repo, 'zip', TUTORIAL_PATH, repo)
                shutil.rmtree(repo)


def main():
    logger.debug("Iniciando a funcao main")
    os.chdir(TUTORIAL_PATH)
    now = datetime.datetime.now()
    clean_repos(now)

    dirname = "repo" + now.strftime("%Y%m%d_%H%M")
    logger.info("Nome do diretorio: " + dirname)

    if not os.path.exists(dirname):
        os.mkdir(dirname)

    os.chdir(dirname)
    create_files()


if __name__ == "__main__":
    main()

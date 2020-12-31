#! /home/roman/anaconda3/bin/python3

import configparser
import sys
import logging
import daemon

from server import server


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read(sys.argv[1])
    log_path = config["LOG"]["Path"]
    port = int(config["SERVER"]["Port"])
    max_conn = int(config["SERVER"]["Backlog"])
    timeout = int(config["SERVER"]["Timeout"])
    is_daemon = config["SERVER"]["Daemon"]
    if is_daemon == 'True':
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        fh = logging.FileHandler(log_path)
        logger.addHandler(fh)
        context = daemon.DaemonContext(
            working_directory='/home/roman/work/Питон/Техносфера/HW_5',
            files_preserve=[fh.stream])
        with context:
            server(port=port, max_conn=max_conn, timeout=timeout)
    else:
        if log_path == '':
            logging.basicConfig(stream=sys.stdout, level=logging.INFO)
        else:
            logging.basicConfig(filename=log_path, level=logging.INFO)
            server(port=port, max_conn=max_conn, timeout=timeout)

#!/usr/bin/python

import extractData as exd
from dotenv import load_dotenv
import logs as log
import gpioControl as gc
import uuid
import os


ENV_FILE = f'/boot/.env'
LOG_FILE = f'/boot/gate.log'

def setUp():
 
    # try load env
    if not load_dotenv(dotenv_path=ENV_FILE):
        log(LOG_FILE).info("fail loading env file")
        exit(1)
    
    endpoint = os.getenv("ENDPOINT")

    # cheak for valide endpoint env 
    if not endpoint:
        log(LOG_FILE).info("None valide Endpoit")
        exit(2)

    token_in = os.getenv("TOKEN_IN")
    token_out = os.getenv("TOKEN_OUT")
    # cheak for valide token env 
    if token_in == None and token_out == None:
        log(LOG_FILE).info("None valide Token")
        exit(3)

    # initialize GPIO
    gc.initGpio()

    hostname = os.getenv("HOSTNAME")

    if not hostname:
        hostname = str(uuid.uuid4())

    with open("/etc/hosts", 'a') as file:
        file.write("127.0.1.1\t\t" + hostname)
    
    with open("/etc/hostname", 'w') as file:
        file.write(hostname)

    log(LOG_FILE).info(f"{hostname} - is set as Hostname")

    interface_details = exd.get_interface_details()
    for interface in interface_details:
        log(LOG_FILE).info(f"{interface['interface']} - {interface['mac_address']} - {interface['ip_address']}")

    if os.path.exists(logs.LOG_FILE):
        return
           
    os.mkdir(logs.LOG_FILE[0:-9])

    # Create the file
    with open(logs.LOG_FILE, 'w') as file:
        pass
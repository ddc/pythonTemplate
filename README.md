# TEMPLATE
[<img src="https://img.shields.io/badge/python-3.6-blue.svg?style=plastic">](https://www.python.org/downloads)
[<img src="https://img.shields.io/github/license/ddc/pythonTemplate.svg?style=plastic">](https://github.com/ddc/pythonTemplate/blob/master/LICENSE)


## LOCATION
    Git: 
    Host: 
    Path: 
    Logs: 


## ABOUT
    1) 


## OBS



## PARAMETERS
    project.py  --a
                --b
                --c

    Arguments:
        --a     [OPTIONAL]
        --b     [REQUIRED]
        --c     Path

    EXAMPLE:
        --a 127.0.0.1 --b 27017 --c /opt


## CONFIG FILE VARIABLES
    [main]
    LOG_BACKUP_DAYS = Time IN DAYS of compressed log files
    
    [mongo]
    HOST = Mongo Host / IP
    PORT = Mongo port
    DATABASE = Database / Schema
    AUTHSOURCE = Authorization user
    USER = Mongo User
    PASSW = Mongo user password

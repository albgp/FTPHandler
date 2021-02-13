from ftplib import FTP
import configparser 
import os
from pathlib import Path

def readConfig():
    config = configparser.ConfigParser()
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    config_file=os.path.join(__location__,'ftp.config')
    config.read(config_file)
    return config['FTPSERVER']

def connectFTP(config):
    print(config['ftpaddr'])
    ftp = FTP()
    ftp.connect(
        config['ftpaddr'],
        int(config['port'])
        )
    ftp.login(
        config['user'],
        config['passwd']
        )
    ftp.cwd(config['path'])
    return ftp
    
def doOverFTP(f):
    config=readConfig()
    print(config)
    ftp=connectFTP(config)
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    images_path = os.path.join(Path(__location__).parent,'Images')
    filenames = ftp.nlst() # get filenames within the directory
    for filename in filenames:
        local_filename=os.path.join(images_path, filename)
        file = open(local_filename, 'wb')
        ftp.retrbinary('RETR '+ filename, file.write)
        file.close
        f(local_filename)

    






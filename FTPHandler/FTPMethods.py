from ftplib import FTP
import configparser 
import os
from pathlib import Path

from collections import defaultdict

class TrieNode():

    def __init__(self):
        self.children = defaultdict()
        self.terminating = False


class Trie():

    def __init__(self):
        self.root = self.get_node()

    def get_node(self):
        return TrieNode()

    def get_index(self, ch):
        return ord(ch) - ord('a')

    def insert(self, word):

        root = self.root
        len1 = len(word)

        for i in range(len1):
            index = self.get_index(word[i])

            if index not in root.children:
                root.children[index] = self.get_node()
            root = root.children.get(index)

        root.terminating = True

    def search(self, word):
        root = self.root
        len1 = len(word)

        for i in range(len1):
            index = self.get_index(word[i])
            if not root:
                return False
            root = root.children.get(index)

        return True if root and root.terminating else False

    def delete(self, word):

        root = self.root
        len1 = len(word)

        for i in range(len1):
            index = self.get_index(word[i])

            if not root:
                print ("Word not found")
                return -1
            root = root.children.get(index)

        if not root:
            print ("Word not found")
            return -1
        else:
            root.terminating = False
            return 0

    def update(self, old_word, new_word):
        val = self.delete(old_word)
        if val == 0:
            self.insert(new_word)

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
    trie = Trie()
    config=readConfig()
    print(config)
    ftp=connectFTP(config)
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    images_path = os.path.join(Path(__location__).parent,'Images')
    already_processed=[]
    while True:
        filenames = ftp.nlst() # get filenames within the directory
        for filename in filenames:
            if not trie.search(filename):
                trie.insert(filename)
                already_processed.append(filename)
                local_filename=os.path.join(images_path, filename)
                file = open(local_filename, 'wb')
                ftp.retrbinary('RETR '+ filename, file.write)
                file.close
                f(local_filename)
        if config['watch']=="false":
            print("Not watching: exiting")
            break

    






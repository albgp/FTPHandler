# FTP Handler

Simple Python script for processing files in a remote FTP server.

## Usage 

The configuration for the FTP server, this including the server adress, port, and access credentials are stored in a ftp.config file inside the FTPHandler module's subdirectory.

Once the FTP server is proverly configured the main usage for this tool is to add the import ```from FTPHandler.FTPMethods import doOverFTP```  and the 
```@doOverFTP``` callback decorator in the function later used to process the file retrieved from the FTP server.
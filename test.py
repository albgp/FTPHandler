from FTPHandler.FTPMethods import doOverFTP

@doOverFTP
def processImages(imgname):
    print("Processing "+imgname)
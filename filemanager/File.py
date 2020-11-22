import os
import fnmatch

class File():
    '''
    File object
    Properties:
    - File: can include no path, relative or absolute paths
    - Directory: location of the file
    '''
    def __init__(self,file:str, directory:str = None):

        if directory is None:
            path,filename = os.path.split(file)
            if len(path) < 1 :
                path = os.curdir
        else:
            filename = file
            path = directory

        if os.path.isdir(path):
            self.path = path
            self.abspath = os.path.abspath(path)
        else:
            raise NotADirectoryError(f"{path}")

        self.file = os.path.join(self.abspath, filename)
        if os.path.isfile(self.file):
            self.filename = filename
            self.exists = True
        else:
            self.exists = False
            raise FileNotFoundError(f"{filename} --> {self.abspath}")

        # full name with revision control: <name>.<ext>.<revision>

        self.extension, self.revision = File.__getExtensionRevision(self.file)


    def __repr__(self):
        return f"File({self.filename} | {self.file})" 
    
    def __str__(self):
        return f"{self.filename}"

    @staticmethod
    def isFile(file:str, filepath:str = None):
        exist = os.path.isfile(file) if (filepath is None) else os.path.isfile(os.path.join(filepath,file))
        return exist
    
    @staticmethod
    def isExtension(file:str,extensions:str):
        if fnmatch.fnmatch(File.fileExtension(file),extensions):
            return True
        return False

    @staticmethod
    def __getExtensionRevision(file):

        # full name with revision control: <name>.<ext>.<revision>
        _,filename = os.path.split(file)        
        fname = filename.rsplit(".",2)
        
        try:
            revision = int(fname[-1]) #try casting revision, it fails if there is no revision
            extension = fname[-2]
        except ValueError:
            revision = -1
            extension = fname[-1]
        
        extension = "." + extension
        return extension, revision

    @staticmethod
    def fileExtension(file:str):
        # full name with revision control: <name>.<ext>.<revision>
        extension, _ = File.__getExtensionRevision(file)

        return extension
        
    @staticmethod
    def hasRevision(file:str):
        # full name with revision control: <name>.<ext>.<revision>
        _, revision = File.__getExtensionRevision(file)
        
        return revision>=0
    
    def removeRevision(self, Purge:bool = False):
        if self.revision:
            newname = self.filename.rsplit(".",1)[0]
            try:
                os.rename(self.file, os.path.join(self.abspath,newname))
            except:
                if Purge:
                    os.replace(self.file, os.path.join(self.abspath,newname))
            self.filename = newname
            self.revision = 0


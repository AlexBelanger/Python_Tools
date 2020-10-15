import os
import fnmatch

class file():
    '''
    File object
    '''
    def __init__(self,file:str, filepath:str = None, cwd:bool = False):
        
        if filepath is None and not cwd:
            path,filename = os.path.split(file)
        else:
            filename = file
            if cwd:
                path = os.getcwd()
            elif filepath is not None:
                path = filepath
            else:
                path = "."
            
        if os.path.isdir(path):
            self.filepath = path
        else:
            raise NotADirectoryError

        self.fullpath = os.path.join(path, filename)
        if os.path.isfile(self.fullpath):
            self.filename = filename
            self.exists = True
        else:
            self.exists = False
            raise FileNotFoundError
        
        try:
            # revision control: <name>.<ext>.<revision>
            rev = self.filename.rsplit(".",1)[-1]
            self.revision = int(rev)>0
        except:
            self.revision = False
    
    @staticmethod
    def isFile(file:str, filepath:str = None):
        if filepath is None:
            exist = os.path.isfile(file)
        else:
            exist = os.path.isfile(os.path.join(filepath,file))
        return exist

    def removeRevision(self):
        if self.revision:
            newname = self.filename.rsplit(".",1)[0]
            try:
                os.rename(self.fullpath, os.path.join(self.filepath,newname))
            except:
                os.replace(self.fullpath, os.path.join(self.filepath,newname))
            self.filename = newname
            self.fullpath = os.path.join(self.filepath, newname)
            

    def __repr__(self):
        return f"{self.filename} | {self.fullpath}"
        
class filemanager():

    def __init__(self, workingdirectory = False):
        if workingdirectory is True:
            self.workingdirectory = os.getcwd()
        else:
            self.workingdirectory = workingdirectory

        self.files = [file(f,filepath=self.workingdirectory) for f in os.listdir(self.workingdirectory) if os.path.isfile(f)]

    def __repr__(self):
        return f"Working Directory -> {self.workingdirectory}"
    
    def removeRevision(self):
        for fileobj in self.files:
            fileobj.removeRevision()

fm = filemanager(workingdirectory=True)
fm.removeRevision()
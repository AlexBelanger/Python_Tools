import os
import fnmatch

class File():
    '''
    File object
    '''
    def __init__(self,file:str, filepath:str = None, cwd:bool = False):

        if filepath is None and not cwd:
            path,filename = os.path.split(file)
            if len(path) < 1 :
                path = os.curdir
        else:
            filename = file
            if cwd:
                path = os.getcwd()
            elif filepath is not None:
                path = filepath
            else:
                path = os.curdir
            
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

        # full name with revision control: <name>.<ext>.<revision>
        last = self.filename.rsplit(".",2)
        
        try:
            self.revision = int(last[-1])>0
            self.extension = last[-2]
        except:
            self.revision = False
            self.extension = last[-1]
    
    def __repr__(self):
        return f"{self.filename} | {self.fullpath}" 
    
    def __str__(self):
        return f"{self.filename}"

    @staticmethod
    def isFile(file:str, filepath:str = None):
        if filepath is None:
            exist = os.path.isfile(file)
        else:
            exist = os.path.isfile(os.path.join(filepath,file))
        return exist
    
    @staticmethod
    def fileExtension(file:str):
        # full name with revision control: <name>.<ext>.<revision>
        last = file.rsplit(".",2)
        
        try:
            if(int(last[-1])>0):
                extension = last[-2]
            else:
                extension = last[-1]
        except:
            extension = last[-1]

        return extension
    
    @staticmethod
    def isExtension(file:str,extensions:str):
        valid = list()
        for ext in extensions:
            clean_ext = ext.strip(".")
            valid.append(fnmatch.fnmatch(File.fileExtension(file),ext.strip(".")))
        return any(valid)

    def removeRevision(self):
        if self.revision:
            newname = self.filename.rsplit(".",1)[0]
            try:
                os.rename(self.fullpath, os.path.join(self.filepath,newname))
            except:
                os.replace(self.fullpath, os.path.join(self.filepath,newname))
            self.filename = newname
            self.fullpath = os.path.join(self.filepath, newname)
            self.revision = False
        
class Filemanager():

    def __init__(self, workingdirectory = False, extensions:str = "*"):
        if workingdirectory is True:
            self.workingdirectory = os.getcwd()
        else:
            self.workingdirectory = workingdirectory
        self.extensions = extensions
        
        self.__updatefiles()

    def __repr__(self):
        return f"Working Directory -> {self.workingdirectory} | #Files: {len(self.files)} | File Extensions: {self.extensions}"
    
    def __iter__(self):
        self._fileindex = 0
        return self
    
    def __next__(self):
        cur = self._fileindex
        if cur < len(self.files):
            self._fileindex+=1
            return self.files[cur]
        
        raise StopIteration
    
    def __updatefiles(self):
        self.files = [File(f,filepath=self.workingdirectory) for f in os.listdir(self.workingdirectory) if (os.path.isfile(f) and File.isExtension(f,self.extensions))]
        self.files.sort(key=lambda f: f.filename)

    def removeRevision(self):
        for file in self:
            file.removeRevision()
        #update the filemanager
        self.__updatefiles()

fm = Filemanager(workingdirectory=True)

for file in fm:
    print(file)
print("\nCleaning\n")
fm.removeRevision()
for file in fm:
    print(file)
import os
import fnmatch
import File as File

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
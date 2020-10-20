from File import File 
import os
import pytest

def test_init_direrror():
    dummydir = "notvalid_directory"
    dummyfile = "invalid.file"
    with pytest.raises(NotADirectoryError) as dirError:
        assert File(dummyfile,dummydir)
    
def test_init_fileexisterror():
    valid_directory = "."
    dummyfile = "invalid.file"
    with pytest.raises(FileNotFoundError) as fileError:
        assert File(dummyfile,valid_directory)


def test_init_extension():
    fname = "file.py"
    f = File(fname)
    assert f.extension == ".py"
    assert File.fileExtension(fname) == ".py"
    fname = "file.test.2"
    assert File.fileExtension(fname) == ".test"

def test_init_revision():
    fname = "file.py"
    f = File(fname)
    assert f.revision == -1
    assert File.hasRevision(fname) == False
    fname = "file.test.2"
    assert File.hasRevision(fname) == True

def test_remove_revision():
    fname = "test.for.2"
    norev = "test.for"
    with open(fname, 'a') as f:
        f.write("Pytest!\n")
    file = File(fname)
    assert file.exists == True
    assert file.filename == fname
    assert file.revision == 2
    assert file.extension == ".for"
    file.removeRevision(Purge=True)
    assert file.filename == norev
    assert file.revision == -1
    assert file.extension == ".for"
    os.remove(norev)


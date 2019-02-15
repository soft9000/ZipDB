#!/usr/bin/env python3

from zipfile import ZipFile


class ZipArchiveBase():

    '''
    Once a file has been written to a zip archive, the enarchived file is no longer updatable.
    To update any file in an archive, that archive will need to be re-created so as to use
    any updatable file content.
    '''

    def __init__(self, archive_file="Enigma.zip"):
        ''' Define an archive file. '''
        self._file = archive_file


    def destroy(self):
        ''' Destroy any existing archive file. True when archive no longer exists.
        False is returned upon archive removal error. '''
        import os
        try:
            if self.exists():
                os.unlink(self._file)
                if self.exists():
                    return False
            return True
        except:
            return False


    def exists(self):
        ''' Check to see if an archive file exists. '''
        import os
        try:
            return os.path.exists(self._file)
        except:
            return False


    def _en(self, string):
        ''' Encoding can present several opportunites. Here we are
        simply converting an archive payload to bytes. '''
        return bytes(string, 'utf-8')


    def _de(self, string):
        ''' Decoding can present several opportunites. Here we are
        simply converting our previously encoded bytes, back to a Unicode
        string. '''
        return str(string, 'utf-8')


    def list(self):
        ''' An archive can contain many files. Here is how to list contained files. '''
        with ZipFile(self._file, 'r') as zZip:
            return zZip.namelist()


    def read_archive(self, file):
        ''' Read a previously archived file, by name. Use list() to query archive content. '''
        try:
            with ZipFile(self._file, 'r') as zZip:
                with zZip.open(file) as fh:
                    return self._de(fh.read())
        except Exception as ex:
            return False


    def archive_first(self, message, file, overwrite=False):
        ''' Our strategy will not create an empty archive. Neither will we allow an archive
        to be accidently overwritten. '''
        try:
            if not overwrite and self.exists():
                return False
            with ZipFile(self._file, 'w') as zZip:
                with zZip.open(file, 'w') as fh:
                    fh.write(self._en(message)) # Also: .writestr()
                if zZip.testzip() is None:
                    return True
        except Exception as ex:
            raise ex
        return False


    def archive_next(self, message, file):
        ''' Once created via .archive_first() we can add more files to the archive. '''
        try:
            with ZipFile(self._file, 'a') as zZip:
                with zZip.open(file, 'w') as fh:
                    fh.write(self._en(message))
                if zZip.testzip() is None:
                    return True
        except Exception as ex:
            pass
        return False


    @staticmethod
    def TestCase(test, cleanup=True):
        ''' Re-usable test case for child classes. '''
        assert(isinstance(test, ZipArchiveBase))
        zPatterns = [
            "Test Pattern\n\r\noNe!",
            "This\tis\r '\v' a\r\n\t\t\ttest!"
            ]

        # Basic / single file archive creation:    
        zfile = "MyFile.dat"
        assert(test.destroy())
        assert(test.archive_first(zPatterns[0], zfile))
        assert(test.exists())
        assert(test.read_archive(zfile) == zPatterns[0])
        assert(test.archive_first(zPatterns[0], zfile, overwrite=False) == False)
        assert(test.read_archive(zfile) == zPatterns[0])
        assert(test.archive_first(zPatterns[0], zfile, overwrite=True))
        assert(test.read_archive(zfile) == zPatterns[0])
        assert(test.destroy())
        assert(test.exists() == False)
        assert(test.read_archive(zfile) != zPatterns[0])

        assert(test.archive_first(zPatterns[0], zfile))
        nfiles = "One.TXT", "Two.bin", "3next", "4545.654.322"
        for ss, nfile in enumerate(nfiles, 2):
            assert(test.archive_next(zPatterns[1], file=nfile))
            assert(test.read_archive(nfile) == zPatterns[1])
            assert(len(test.list()) == ss)
            assert(test.exists())
        if cleanup:
            assert(test.destroy())
            assert(test.exists() == False)
        else:
            assert(test.exists())

    
if __name__ == "__main__":
    test = ZipArchiveBase()
    ZipArchiveBase.TestCase(test)
        

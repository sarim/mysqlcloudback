try:
    from cloudapp.cloud import Cloud
except Exception:
    raise Exception("pycloudapp module not found, cloudapp support unavailable")

import subprocess
import sys
import os
from datetime import datetime
from glob import glob


class mysqlcloudback:

    def backtik(self, cmd):
        p = subprocess.Popen(['/bin/sh', '-c', cmd], stdout=subprocess.PIPE)
        p.wait()
        return p.stdout.read()

    def generatefilename(self, nprefix, format, nsuffix):
        return nprefix + datetime.now().strftime(format) + nsuffix

    def compressbackup(self, filepath, cformat):
        if cformat not in ['bzip2', 'gzip']:
            raise Exception("Unsupported compression format")
        output = self.backtik("%s %s" % (cformat, filepath))
        if output != "":
            raise Exception("%s said %s" % (cformat, output))
        if cformat == "bzip2":
            compressedfile = filepath + ".bz2"
        elif cformat == "gzip":
            compressedfile = filepath + ".gz"
        if not os.path.exists(compressedfile):
            raise Exception("Compressed file not created or someone ate it up")
        return compressedfile

    def runmysqldump(self, filepath, mhost, mdb, muser, mpass):
        self.backtik("mysqldump -h %s -u '%s' -p'%s' %s > %s" % (mhost,
                     muser, mpass, mdb, filepath))

    def splitfile(self, filepath, sizemb, suffix, deleteorig):
        self.backtik("split -b %i %s %s" % (int(sizemb * 1024 * 1024),
                     filepath, filepath + suffix))
        if deleteorig:
            self.backtik("rm -f %s" % filepath)
        return glob("%s%s*" % (filepath, suffix))

    def logincloudapp(self, email, password):
        if hasattr(self, 'mycloud'):
            if self.mycloud.auth_success == 1:
                return True

        self.mycloud = Cloud()
        return self.mycloud.auth(email, password)

    def encryptfile(self, filename, passphrase, deleteorig, cypher='aes-128-cbc'):
        self.backtik("openssl %s -pass pass:%s -in %s -out %s" % (cypher,
                     passphrase, filename, filename + ".aes"))
        if os.path.exists(filename + ".aes"):
            if deleteorig:
                self.backtik("rm -f %s" % filename)
            return filename + ".aes"
        else:
            raise Exception("Encryption Failed")

    def decryptfile(self, filename, passphrase, deleteorig, cypher='aes-128-cbc'):
        self.backtik("openssl %s -d -pass pass:%s -in %s -out %s" % (cypher,
                     passphrase, filename + ".aes", filename))
        if os.path.exists(filename):
            if deleteorig:
                self.backtik("rm -f %s" % filename + ".aes")
            return filename
        else:
            raise Exception("Decryption Failed")

    def uploadcloudapp(self, filelist):
        uploadlist = []
        for files in filelist:
            res = self.mycloud.upload_file(files, True)
            if 'download_url' in res:
                uploadlist.append(res['download_url'])
            else:
                raise Exception("Upload Failed")
        return uploadlist

    def downloadfile(self):
        raise Exception("TODO: Not implemented yet")

    def joinfiles(self, filename, suffix):
        raise Exception("TODO: Not implemented yet")

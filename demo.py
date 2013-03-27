from mysqlcloudback import mysqlcloudback

#usage example
mybackup = mysqlcloudback()
filename = mybackup.generatefilename("db","%Y_%m_%d",".sql")
mybackup.runmysqldump(filename,"localhost","database","username","password")
compressedfile = mybackup.compressbackup(filename,"gzip")
encfile = mybackup.encryptfile(compressedfile,"passphrase",True)
splits = mybackup.splitfile(encfile,24,".part_")

mybackup.logincloudapp('johndoe@foobar.com','cloudpassword')
uploads = mybackup.uploadcloudapp(splits)

print "Uploaded %i Files" % len(uploads)
for upld in uploads:
    print upld

Mysql Cloud Backup
==


##Introduction
This task of this __python__ script is to provide some helper functions to painlessly take backup of mysql database, compress, encrypt, decrypt it, or split it into smaller files, upload it to [cloudapp](http://cl.ly) storage…
My aim is to create a Swiss Army knife for backup related tasks.

##Features
Features are implemented as independent functions. You can use them as you wish. Use them in any order or skip some when not needed.

- Easily run shell commands and capture their output.
- Generate filenames based of date and time.
- Compress files using bzip2 or gzip.
- Backup your database using mysqldump.
- Split bigger files into parts.
- Encrypt and Decrypt files using openssl.
- Login and Upload files to cloudapp.


##Installation

- Install pycloudapp module for [cloudapp](http://cl.ly) support.

	If `pip` not installed, first get `easy_install` (also get git)
	
		# For RPM based distro
		yum install python-setuptools git

		# For Debian based distro
		apt-get install python-setuptools git

		# For Mac OSX
		echo "Mac is awesome"

	Now install `pip`

		easy_install pip	
	
	Now use pip to install pycloudapp

		pip install -e git+git://github.com/sarim/pycloudapp.git#egg=cloudapp

- Now get mysqlcloudback

		git clone https://github.com/sarim/mysqlcloudback.git

##Usage	

Using mysqlcloudback is easy, check the source for example. When writing this mysqlcloudback, the thing that i specially cared for is, every function is independent, So you can encrypt your backup file first (or any file, it wont mind) then compress it, or split it first then compress it and forget to encrypt, anything you wish.


Usage included in demo.py is preety self explanatory.

``` python
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
```
Here i generated a filename based on year-month-day then took mysqldump,compressed it,encrypted it,splited it as 24MB parts then uploaded them to cloudup.
It may called from crontab for scheduled backup tasks.

##Contribution and TODO
Feel free to hack into the code and be sure to send pull request. The "downloadfile" and "joinfiles" functions are not implemented(TODO). New features can be "uploaddropbox" or "uploaddroplr" or "uploadrsync" or "uploadscp" etc . . .
Or "backuporacle", "backupFooDb" etc . . .


##LICENCE
Copyright © 2013 __Sarim Khan__ <sarim2005@gmail.com>
_Licensed under Mozilla Public License 1.1 ("MPL"), an open source/free software license._
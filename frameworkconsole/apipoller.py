#!/usr/bin/python
version = "0.1.7"
import os
from os import system
import sys
import re
import serial
from time import sleep
import struct
import pexpect
from lib.serial import read_modem
from lib.config import Config
from lib.db import DB, DBException
config = Config('config')

ipaddress = config.get('IPADDRESS')
webserver = config.get('WEBSERVER')
path = sys.argv[1]
key = sys.argv[2]

sqlserver = config.get('MYSQLSERVER')

while True:
    fullpath5 = webserver + path + "/putfunc"
    PUTFILE = open(fullpath5, 'r+')
    line = PUTFILE.readline()
    line = line.strip()
    PUTFILE.close()
    PUTFILE2 = open(fullpath5, 'w')
    PUTFILE2.close()
    arsplit = line.split(' ')

    if  arsplit[0] == key :
	 if  arsplit[1] == "phish" :
		numbers = len(arsplit) - 2
		print numbers
		numbersarray = [0] * numbers
		for x in range (0, numbers):
			numbersarray[x] = arsplit[x+2]
		print '[%s]' % ', '.join(map(str, numbersarray))
		webserver = config.get('WEBSERVER')
            	sqlserver = config.get('MYSQLSERVER')
            	ipaddress = config.get('IPADDRESS')
            	localpath = "/phish"
            	for x in numbersarray: 
			filename  = "/" + x + ".php"
            		link   = "http://" + ipaddress + localpath + filename
            		fullpath  = webserver + localpath
            		command1  = "mkdir " + fullpath
            		system(command1)
            		sploitfile = webserver + localpath + filename
            		command8   = "touch " + sploitfile
            		system(command8)
            		command9 = "chmod 777 " + sploitfile
            		system(command9)
			results = webserver + localpath + "/results"
            		command8   = "touch " + results
            		system(command8)
            		command9 = "chmod 777 " + results
            		system(command9)
            		sploitfiletext = "<?php\necho \"You Got Phished!\";\n$agent = $_SERVER['HTTP_USER_AGENT'];\n$page = " + x + ";\n$thing = $page . \" \" . $agent;\n$file = results;\n$current = file_get_contents($file);\n$current .= $thing . \"\\n\";\nfile_put_contents($file, $current);\n?>"
    			SPLOITFILE = open(sploitfile, 'w')
    			SPLOITFILE.write(sploitfiletext)
    			SPLOITFILE.close()
			modem = 1
			db = DB(config=config)

                	db.query("SELECT path from modems where id=%s", (modem,))
               		path2 = db.fetchone()[0].replace('"', '')
			print path2

                	db.query("SELECT controlkey from modems where id=%s", (modem,))
                	key2 = db.fetchone()[0]
			print key2
                	db.query("SELECT type from modems where id=%s", (modem,))
                	modemtype2 = db.fetchone()[0]
			control = webserver + path2 + "/getfunc"
			sleep(5)
                    	with open(control, 'w') as f:
                                msg = "This is a cool page: "
                            	command2 = key2 + " " + "SEND" + " " + x + " " + msg + link
				f.write(command2)
	

	 print "Endloop\n"
    sleep(1)
print "broke\n"
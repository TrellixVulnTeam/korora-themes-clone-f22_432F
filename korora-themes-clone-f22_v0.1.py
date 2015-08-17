#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
#  korora-themes-clone-f22_v0.1
#  
#  Copyright 2015 youcef <youssef.m.sourani@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
from __future__ import print_function
import os
import sys
import subprocess
import platform
import time
import shutil
import urllib
import zipfile
import tarfile

if os.geteuid() == 0:
    sys.exit("Please run script Without root privileges  (sudo,su)")


if platform.dist()[0]!="fedora" and platform.dist()[1]!="22":
	sys.exit("Your os Is Not Fedora 22")

if os.getenv("DESKTOP_SESSION")!="gnome":
	sys.exit("You Desktop Is Not gnome shell")



home=os.getenv("HOME")
home_Downloads="%s/Downloads/yucef"%home

link="https://github.com/kororaproject/kp-korora-repos/archive/master.zip"
link2="https://copy.com/Ad3Uj0dKgM42AhRy/Breeze-Blue.tgz"
link3="https://github.com/optimisme/gnome-shell-simple-dock/archive/master.zip"

repo22="korora.repo"
gpg=["RPM-GPG-KEY-korora-22-primary","RPM-GPG-KEY-korora-22-secondary"]

gnome_shell=["user-theme@gnome-shell-extensions.gcampax.github.com","alternate-tab@gnome-shell-extensions.gcampax.github.com",\
"apps-menu@gnome-shell-extensions.gcampax.github.com","background-logo@fedorahosted.org","launch-new-instance@gnome-shell-extensions.gcampax.github.com",\
"places-menu@gnome-shell-extensions.gcampax.github.com","simple-dock@nothing.org"]

gsettings=["gsettings set org.gnome.desktop.background show-desktop-icons false","gsettings set org.gnome.desktop.background  picture-uri \
'file:///usr/share/backgrounds/korora/default/korora.xml' ",\
"gsettings set org.gnome.desktop.screensaver picture-uri 'file:///usr/share/backgrounds/korora/default/korora.xml' ",\
"gsettings set org.gnome.desktop.interface icon-theme 'korora' ","gsettings set org.gnome.shell.extensions.user-theme name 'Korora' ",\
"gsettings set org.gnome.nautilus.preferences sort-directories-first true",\
"gsettings set org.gnome.nautilus.preferences executable-text-activation ask","gsettings set org.gnome.desktop.peripherals.touchpad scroll-method 'two-finger-scrolling' ",\
"gsettings set org.gnome.desktop.peripherals.touchpad tap-to-click true",\
"gsettings set org.gnome.shell always-show-log-out true","gsettings set org.gnome.desktop.interface clock-show-date true",\
"gsettings set org.gnome.settings-daemon.peripherals.mouse locate-pointer false","gsettings set  org.gnome.desktop.interface gtk-theme  Adwaita","gsettings set org.gnome.desktop.interface enable-animations true",\
"gsettings set org.gnome.nautilus.preferences always-use-location-entry true","gsettings set org.gnome.desktop.wm.preferences button-layout ':minimize,maximize,close' "]


favorite_apps=['firefox.desktop','org.gnome.Nautilus.desktop','org.gnome.Terminal.desktop','evolution.desktop', 'shotwell.desktop', 'libreoffice-writer.desktop', 'org.gnome.Screenshot.desktop', 'org.gnome.gedit.desktop','gnome-calculator.desktop',\
"virtualbox.desktop","geany.desktop","booksorg.desktop","gnome-tweak-tool.desktop","gnome-control-center.desktop"]

if not os.path.isdir(home_Downloads):
	os.mkdir(home_Downloads)


def clean_repo():
	if os.path.isfile("/etc/yum.repos.d/korora.repo"):
		subprocess.call("sudo rm /etc/yum.repos.d/korora.repo",shell=True)
	for i in gpg :
		if os.path.isfile("/etc/pki/rpm-gpg/%s"%i):
			subprocess.call("sudo rm /etc/pki/rpm-gpg/%s"%i,shell=True)
	
	
def dnf_install():
	try:
		check=subprocess.call("sudo dnf install korora-backgrounds-extras-gnome korora-backgrounds-gnome korora-icon-theme-base plank plank-theme-korora plymouth-theme-korora korora-icon-theme  gnome-shell-theme-korora   gnome-tweak-tool korora-settings-gnome pharlap pharlap-modaliases \
nautilus-terminal gnome-terminal-nautilus -y",shell=True)
	except (KeyboardInterrupt, SystemExit):
		 clean_repo()
		 sys.exit()
	clean_repo()
	
	if check!=0:
		sys.exit("Downloads  Fail Check Your Connection And Try Again")



def get_all_extensions():
	result=[]
	if os.path.isdir("%s/.local/share/gnome-shell/extensions"%home):
		for filee in os.listdir("%s/.local/share/gnome-shell/extensions"%home):
			if filee not in result:
				result.append(filee)

	for filee in os.listdir("/usr/share/gnome-shell/extensions"):
		if filee not in result:
			result.append(filee)

	if len(result)==0:
		return None
	else:
		return result
	

def get_applications():
	result=[]
	if os.path.isdir("%s/.local/share/applications"%home):
		for filee in os.listdir("%s/.local/share/applications"%home):
			if filee not in result :
				result.append(filee)
                                
	if os.path.isdir("/usr/local/share/applications"):
		for filee in os.listdir("/usr/local/share/applications"):
			if filee not in result :
				result.append(filee)
                                
	for filee in os.listdir("/usr/share/applications"):
		if filee not in result:
			result.append(filee)

	for filee in favorite_apps:
		if filee not in result:
			favorite_apps.remove(filee)
				
	if len(favorite_apps)==0:
		return None
	else:
		return favorite_apps

def down_korora_repo():
	os.chdir(home_Downloads)
	try:
		urllib.urlretrieve (link, "master.zip")
	except:
		if os.path.isfile("master.zip"):
			os.remove("master.zip")
		sys.exit("Downloads Fail")
	with zipfile.ZipFile('master.zip', "r") as z:
		z.extractall()
	if not os.path.isfile("/etc/yum.repos.d/korora.repo"):
		subprocess.call("sudo cp %s/kp-korora-repos-master/upstream/korora.repo /etc/yum.repos.d"%home_Downloads,shell=True)
	for i in gpg :
		if not os.path.isfile("/etc/pki/rpm-gpg/%s"%i):
			subprocess.call("sudo cp %s/kp-korora-repos-master/upstream/%s /etc/pki/rpm-gpg/%s"%(home_Downloads,i,i),shell=True)
			

	if os.path.isfile("master.zip"):
		os.remove("master.zip")
	if os.path.isdir("kp-korora-repos-master"):
		 shutil.rmtree("kp-korora-repos-master")
		

	


def down_mouse_cursor():
	if os.path.isdir("%s/.local/share/icons/Breeze-Blue"%home):
	        subprocess.call("rm -r %s/.local/share/icons/Breeze-Blue"%home,shell=True)
	if  os.path.isdir("/usr/share/icons/Breeze-Blue")==False:
		os.chdir(home_Downloads)
		try:
			urllib.urlretrieve (link2, "Breeze-Blue.tgz")
		except:
			if os.path.isfile("Breeze-Blue.tgz"):
				os.remove("Breeze-Blue.tgz")
			sys.exit("Downloads Fail")
		with tarfile.open("Breeze-Blue.tgz",'r:gz') as t:
			t.extractall()
		if not os.path.isdir("%s/.local/share/icons"%home):
			os.mkdir("%s/.local/share/icons"%home)
		subprocess.call("sudo cp -r %s/Breeze-Blue /usr/share/icons"%home_Downloads,shell=True)
		
		if os.path.isfile("Breeze-Blue.tgz"):
			os.remove("Breeze-Blue.tgz")
		if os.path.isdir("Breeze-Blue"):
			 shutil.rmtree("Breeze-Blue")
		if  os.path.isdir("/usr/share/icons/Breeze-Blue"):
			subprocess.call("gsettings set org.gnome.desktop.interface cursor-theme  'Breeze-Blue' ",shell=True)
			
			
	else:
		subprocess.call("gsettings set org.gnome.desktop.interface cursor-theme  'Breeze-Blue' ",shell=True)
		







def down_simple_dock():
	if  os.path.isdir("/usr/share/gnome-shell/extensions/simple-dock@nothing.org")==False and os.path.isdir("%s/.local/share/gnome-shell/extensions/simple-dock@nothing.org"%home)==False:
		os.chdir(home_Downloads)
		try:
			urllib.urlretrieve (link3, "master.zip")
		except :
			if os.path.isfile("master.zip"):
				os.remove("master.zip")
			sys.exit("Downloads Fail")
		with zipfile.ZipFile('master.zip', "r") as z:
			z.extractall()
		if not os.path.isdir("%s/.local/share/gnome-shell/extensions"%home):
			os.mkdir("%s/.local/share/gnome-shell/extensions"%home)
		subprocess.call("cp -r  %s/gnome-shell-simple-dock-master/simple-dock@nothing.org %s/.local/share/gnome-shell/extensions"%(home_Downloads,home),shell=True)
		if os.path.isdir("gnome-shell-simple-dock-master"):
			shutil.rmtree("gnome-shell-simple-dock-master")
		if os.path.isfile("master.zip"):
			os.remove("master.zip")
			
			
			





print ("Downloading Please Wait...")
down_korora_repo()
dnf_install()
	
print ("Downloading Please Wait...")
down_mouse_cursor()
	
	
print ("Downloading Please Wait...")
down_simple_dock()
	
if os.path.isdir("%s/.local/share/gnome-shell/extensions/simple-dock@nothing.org"%home)==False and os.path.isdir("/usr/share/gnome-shell/extensions/simple-dock@nothing.org")==False:
	sys.exit()

if  os.path.isdir("/usr/share/icons/korora")==False and os.path.isdir("%s/.local/share/icons/korora"%home)==False:
	sys.exit()

if  os.path.isdir("/usr/share/themes/Korora")==False and os.path.isdir("%s/.local/share/themes/Korora"%home)==False:
	sys.exit()

if  os.path.isfile("/usr/share/backgrounds/korora/default/korora.xml")==False:
	sys.exit()



old_extension=get_all_extensions()

if old_extension!=None:
	for i in old_extension:
		subprocess.call("gnome-shell-extension-tool -d %s"%i,shell=True)
		time.sleep(2)


get_applications=get_applications()
if  get_applications!=None:
	subprocess.call("""gsettings set org.gnome.shell favorite-apps "%s" """%get_applications,shell=True)


for i in gnome_shell:
	if os.path.isdir("%s/.local/share/gnome-shell/extensions/%s"%(home,i)) or  os.path.isdir("/usr/share/gnome-shell/extensions/%s"%i):
		subprocess.call("gnome-shell-extension-tool -e  %s"%i,shell=True)
		time.sleep(2)



for filee in gsettings:
	subprocess.call("%s"%filee,shell=True)
	time.sleep(2)



os.chdir(home)
shutil.rmtree("Downloads/yucef")

print ("\n\n")
print ("finish Please Reboot")
	




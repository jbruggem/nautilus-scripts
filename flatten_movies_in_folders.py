#! /usr/bin/python
# -*- coding: utf-8 -*-

DEBUG = False or 0 < sys.argv.count('debug')
DRYRUN = False or 0 < sys.argv.count('dryrun')
LOGSTDOUT = False or 0 < sys.argv.count('stdout')

import os, errno
from os.path import join, basename,dirname,getsize
#from subprocess import call
files = os.environ.get('NAUTILUS_SCRIPT_SELECTED_FILE_PATHS')

if DEBUG:
	logfile = open(os.environ.get('HOME')+"/flatten_movies_in_folders.log",'a')
	logfile.write("========================================\n")

def log(msg):
	if LOGSTDOUT:
		print msg
	if DEBUG:
		logfile.write(msg+"\n")

def getMoveToRoot(root):
	def moveToRoot(filepath):
		log("moveToRoot "+basename(filepath)+" -> "+root)
		if not DRYRUN:
			os.rename(filepath, join(root, basename(filepath)))
	return moveToRoot

def deleteElem(filepath):
	log("deleteElem "+filepath)
	if not DRYRUN:
		os.remove(filepath)

def deleteEmptyDir(path):
	if not DRYRUN:
		try:
			os.rmdir(path)
			log("delete empty folder "+path)
		except OSError as exc:
			if exc.errno == errno.ENOTEMPTY: pass
			else: raise

def filterdir(directoryPath, keepFunction, deleteFunction, dirDeleteFunction):
	log("\n----------- "+directoryPath)
	for root, dirs, files in os.walk(directoryPath):
		for f in files:
			if( f.endswith('.srt')
			  or getsize(join(root, f)) > 1000*1000*100):
				keepFunction(join(root, f))
			else:
				deleteFunction(join(root, f))
		for d in dirs:
			filterdir(join(root, d), keepFunction, deleteFunction, dirDeleteFunction)
			dirDeleteFunction(join(root, d))
	pass

if files:
	files = files.split('\n')
	for f in files:
		#log(""+f+"\n")
		if not f:
			continue
		if os.path.isdir(f):
			moveToRoot = getMoveToRoot(dirname(f))
			filterdir(f, moveToRoot, deleteElem, deleteEmptyDir)
			deleteEmptyDir(f)

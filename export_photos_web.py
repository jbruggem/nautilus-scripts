#! /usr/bin/python
# -*- coding: utf-8 -*-

exportFolder = os.environ.get('EXPORT_PHOTOS_WEB_TARGET_FOLDER')

import os, os.path, errno
from subprocess import call
files = os.environ.get('NAUTILUS_SCRIPT_SELECTED_FILE_PATHS')

if(files):
	files = files.split('\n')

	for f in files:
		if not f:
			continue
		fold = os.path.join(exportFolder,os.path.basename(os.path.dirname(f.replace('/outputJpeg',''))))
		try:
			os.makedirs(fold)
		except OSError as exc: # Python >2.5
			if exc.errno == errno.EEXIST and os.path.isdir(fold):
				pass
			else:
				raise
		n = os.path.join(fold,os.path.basename(f))
		cmd = 'convert "'+f+'" -resize 2200x1660^ -quality 85 "'+n+'"'
		print cmd
		os.system(cmd)

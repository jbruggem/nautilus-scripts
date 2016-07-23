#! /usr/bin/python
# -*- coding: utf-8 -*-

import os, errno, re, sys
from os.path import join,basename,dirname,getsize,commonprefix

DEBUG = False or 0 < sys.argv.count('debug')
DRYRUN = False or 0 < sys.argv.count('dryrun')
LOGSTDOUT = False or 0 < sys.argv.count('stdout')


def main():
	files = os.environ.get('NAUTILUS_SCRIPT_SELECTED_FILE_PATHS')
	log("debug: "+str(DEBUG))
	log("dryrun: "+str(DRYRUN))

	if files:
		log("===============================================")
		(file_paths, folders) = extractFilesAndFolders(files.split('\n'))
		files_and_prefix = filesAndPrefixes(file_paths, folders)
		[log(a) for a in files_and_prefix]
		prefixes = filteredPrefixes(files_and_prefix, folders)
		log("-----------------------------------------------")
		[log(a) for a in prefixes]
		moveable_files = [t for t in files_and_prefix if 0 < prefixes.count(t[1]) ]
		log("-----------------------------------------------")
		for t in moveable_files:
			#print("* "+t[1]+" <- "+t[0])
			dest = join(dirname(t[0]),t[1])

			log(" * " + basename(dest) + " <- " + t[0])
			if not DRYRUN:
				mkdir_p(dest)
				os.rename(t[0],join(dest,basename(t[0])))

def log(msg):
	if LOGSTDOUT:
		print msg
	if DEBUG:
		logfile.write(msg+"\n")

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def longestPrefix(f,files):
	prefixes = [commonprefix([f,f2]) for f2 in files]
	return reduce(lambda p1, p2: (p1,p2)[len(p1)<len(p2)], prefixes)

def prettifyPrefix(p):
	return p.replace("."," ").strip().title()

def prepareForCompare(filepath):
	return prettifyPrefix(
		re.split("[a-z]?\d{1,3}[a-z]\d{1,3}",
			basename(filepath.lower())
		)[0]
	)

def extractFilesAndFolders(root_list):
	file_paths = [f for f in root_list if f and os.path.isfile(f) ]
	folders = [basename(d) for d in root_list if os.path.isdir(d) ]
	return (file_paths, folders)

def filesAndPrefixes(file_paths, folders):
	# folders in ref list, but not subtitles
	ref_list = set(folders + [prepareForCompare(f) for f in file_paths if not f.endswith('.srt')])
	return [(f,longestPrefix(prepareForCompare(f),ref_list)) for f in file_paths]

def filteredPrefixes(files_and_prefix,folders):
	prefixes = folders + [ (p[1]) for p in files_and_prefix  if 2 < len(p[1]) ]
	return filter(lambda p: 1 < prefixes.count(p),prefixes)


main()

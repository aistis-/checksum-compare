from os import listdir, rename, walk
from os.path import isfile, join, basename, abspath, dirname

import sys
import hashlib

def sha1OfFile(filepath):
	filepath = abspath(filepath)
	with open(filepath, 'rb') as f:
		return hashlib.sha1(f.read()).hexdigest()

if sys.argv[1][len(sys.argv[1]) - 1] == '/':
	sys.argv[1] = sys.argv[1][:-1]

if sys.argv[2][len(sys.argv[2]) - 1] == '/':
	sys.argv[2] = sys.argv[2][:-1]

original_files = {}

for root, subFolders, files in walk(sys.argv[1]):
	for f in files:
		p = join(root, f)
		f = abspath(p)
		original_files[sha1OfFile(f)] = basename(f)

found = 0;
not_found = 0;

for root, subFolders, files in walk(sys.argv[2]):
	for f in files:
		p = join(root, f)
		f = abspath(p)

		if isfile(join(sys.argv[2], f)):
			if sha1OfFile(f) in original_files:
				found += 1
				
				rename(f, dirname(abspath(f)) + '/' + original_files[sha1OfFile(f)])
			else:
				not_found += 1

print 'Total original files: ' + str(len(original_files))
print 'Total recovered files found: ' + str(found)
print 'Total not recovered files found: ' + str(not_found)

#!/usr/bin/env python

import os
import hashlib
import sys

def walk(dir, datdir):
   for root, dirs, files in os.walk(dir):
      print "Current directory", root
      # print "Sub directories", dirs
      # print "Files", files

      for file in files:
         path = os.path.join(root, file)
         hash = hashfile(path)
         print path, hash

         d = os.path.join(datdir, hash[0], hash[0:2])
         if os.path.exists(d):
            print d, "exists"
         else:
            os.makedirs(d)

         f = os.path.join(d, hash)
         if os.path.exists(f):
            os.unlink(path)
            print "file duplicated", path, hash
         else:
            os.rename(path, f)

         os.link(f, path)

def hashfile(filepath):
   sha1 = hashlib.sha1()
   f = open(filepath, 'rb')
   try:
      sha1.update(f.read())
   finally:
      f.close()
   return sha1.hexdigest()

def main():
   print sys.argv
   srcdir, datadir = [os.path.realpath(x) for x in sys.argv[1:3]]
   print srcdir, datadir
   assert os.path.isdir(srcdir), "directory not existing: " + srcdir
   if os.path.exists(datadir):
      assert os.path.isdir(datadir), "specified path is not a directory: " + datadir
      assert not os.path.samefile(srcdir, datadir), "specified directories identical"

   comm = os.path.commonprefix([srcdir, datadir])
   assert comm != srcdir and comm != datadir, "directories inclusive"
   walk(srcdir, datadir)

main()

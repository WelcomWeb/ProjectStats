#!/usr/bin/python
# -*- coding: UTF-8

"""
Author: Björn Wikström <bjorn@welcom.se>
Copyright 2013 Welcom Web i Göteborg AB

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os, sys, time

def get_file_ext_from_cmd(args):
    for cmd in args:
        if cmd.startswith('-ext='):
            return list(cmd.replace('-ext=', '').split(','))
    
    return None

def get_standard_ext():
    return ['.htaccess', '.txt', '.ini', '.php', '.java', '.jsp', '.html', '.htm', '.xml', '.xsl', '.css', '.js', '.phtml', '.cs', '.aspx', '.ascx', '.asax', '.tpl', '.inc', '.py', '.rb']

def read_directory(dir, file_ext):
    num_files = 0
    num_lines = 0
    earliest = None
    latest = None
    
    for f in os.listdir(dir):
        if os.path.isdir(os.path.join(dir, f)):
            result = read_directory(os.path.join(dir, f), file_ext)
            num_files = num_files + result['num_files']
            num_lines = num_lines + result['num_lines']
        if os.path.isfile(os.path.join(dir, f)):
            available = False
            for ext in file_ext:
                if f.endswith(ext):
                    available = True
                    break
            
            if not available:
                continue
            
            num_files = num_files + 1
            handle    = open(os.path.join(dir, f), 'r')
            num_lines = num_lines + len(handle.readlines())

            current_ctime = os.path.getctime(os.path.join(dir, f))
            current_mtime = os.path.getmtime(os.path.join(dir, f))
            
            if earliest == None or current_ctime < earliest:
                earliest = current_ctime
            if latest == None or current_mtime > latest:
                latest = current_mtime
    
    return {'num_files': num_files, 'num_lines': num_lines, 'earliest': earliest, 'latest': latest}

if __name__ == "__main__":
    start_path = os.getcwd()
    file_ext = get_file_ext_from_cmd(sys.argv) or get_standard_ext()
    result = read_directory(start_path, file_ext)
    
    print "The project contains", result['num_files'], "file(s) with a total of", result['num_lines'], "lines."
    print "The earliest file is from %s\nhe latest change to a file was %s\n\n" % (time.ctime(result['earliest']), time.ctime(result['latest']))

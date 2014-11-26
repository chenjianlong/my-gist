#!/usr/bin/env python
# -*- coding: utf8 -*-
# vim:fenc=utf-8:et
"""file utilities
"""

import re
import os
import sys
import shutil

__author__ = [
        "Jianlong Chen <jianlong99@gmail.com>"
        ]
__date__ = "2013-06-06"
__license__ = "MIT License"
__all__ = ['read_file', 'write_file', 'replace_file_word', 'replace_file_list_word',
        're_file_search', 'clear_read_only_attr', 'rm_path', 'rm_path_list', 'rm_dir',
        'copy_tree', 'copy_dir', 'copy_file', 'copy_path_list', 'make_dirs', 'touch' ]

def error(msg):
    if msg[-1] != '\n':
        msg += '\n'
        
    if msg.find('bootstrap:') == -1:
        msg = 'bootstrap: ' + msg

    sys.stderr.write(msg)
    sys.exit(-1)

def to_two_tuple(param):
    """convert param to tuple with len two"""
    if isinstance(param, str):
        return (param, param)
    elif (isinstance(param, tuple) or isinstance(param, list)) and len(param) == 2:
        return param
    else:
        error('wrong parameter param:%s' % param)

def read_file(path):
    """return the content of the file"""
    content = ""
    with open(path, 'rb') as f:
        content = f.read()
        return content

def write_file(path, content):
    """write the content to file with path
    (truncating the file if it already exists)"""
    make_dirs(os.path.dirname(path))
    
    with open(path, 'wb') as f:
        f.write(content)

def replace_file_word(src_dst, word_list):
    """replace the src file srcWord with dstWord and save it to dst file
    Args:
        src_dst: the path of file
        example:
        1.  'c:/test.txt'
        2.  ('c:/src.txt','c:/dst.txt')
        3.  ['c:/src.txt','c:/dst.txt']
        
        word_list: the list of word
        example: (('srcword1','dstword1'),('srcword2','dstword2'),...)
    """
    (src, dst) = to_two_tuple(src_dst)
    
    content = read_file(src)
    for (src_word, dst_word) in word_list:
        content = content.replace(src_word, dst_word)
        
    write_file(dst, content)
    return True

def replace_file_list_word(file_list, word_list):
    """replace the src file srcWord with dstWord and save it to dst file
    Args:
        file_list: the list of file
        example: (('srcfile1','dstfile1'),('srcfile2','dstfile2'),...)
        
        word_list: the list of word
        example: (('srcword1','dstword1'),('srcword2','dstword2'),...)
    """
    for src_dst in file_list:
        replace_file_word(src_dst, word_list)
        
def replace_file_list_word(base_dir, file_list, word_list):
    """replace the src file srcWord with dstWord and save it to dst file
    Args:
        base_dir: the base dir of the file_list

        file_list: the list of ile
        example: (('srcfile1','dstfile1'),('srcfile2','dstfile2'),...)
        
        word_list: the list of word
        example: (('srcword1','dstword1'),('srcword2','dstword2'),...)
    """
    (src_base, dst_base) = to_two_tuple(base_dir)
    
    for src_dst in file_list:
        (src, dst) = to_two_tuple(src_dst)
        src = os.path.join(src_base, src)
        dst = os.path.join(dst_base, dst)
        replace_file_word((src, dst), word_list)
        
def re_file_search(path, pattern, group_idx = 1):
    """search the pattern in path
    Args:
        path: file to search
        pattern: can be a RegexObject or string
        group_idx: the index of group to return
    """
    content = read_file(path)
    m = None
    
    if isinstance(pattern,str):
        m = re.search(pattern, content, re.M)
    else:
        m = pattern.search(content)
        
    if m and m.lastindex >= group_idx:
        return m.group(group_idx)
    else:
        error(r"can't find: %s from file {%s} with group_idx:%d"\
                % (pattern, path, group_idx))
        
def clear_read_only_attr(path):
    """remove the dir read only attribute"""
    path = path.rstrip(r'\/')
    attrib_cmd = None
    if os.path.isdir(path):
        attrib_cmd = r'attrib -r %s\*.* /S' % path
    elif os.path.isfile(path):
        attrib_cmd = r'attrib -r %s /S' % path
        
    if attrib_cmd and os.system(attrib_cmd):
        error(r'change {%s} attribute fail' % path)
        
def rm_path(path):
    """remove the dir/file it will use attrib to remove the readonly attribute first"""
    if os.path.isdir(path):
        shutil.rmtree(path)
    elif os.path.isfile(path):
        os.remove(path)
        
def rm_path_list(base, path_list):
    """remove the path list
    Args:
        base: the base dir
        path_list: the list of path need to remove include file or directory
    """
    for path in path_list:
        rm_path(os.path.join(base,path))
        
def rm_dir(src, dst, ignore = None):
    """remove the dst dir's file that it exist in src dir with the same relative path"""
    src = src.rstrip(r'\/')
    dst = dst.rstrip(r'\/')
    for root, dirnames, filenames in os.walk(src):
        if ignore and (ignore in root):
            continue
        
        for filename in filenames:
            src_path = os.path.join(root, filename)
            dst_path = os.path.join(dst, src_path[len(src)+1:])
            os.path.exists(dst_path) and os.remove(dst_path)
            
def copy_tree(src, dst, igPattern = None):
    """copy src dir to dst dir
       if the dst dir already exist it will remove it first"""
    if isinstance(igPattern,str):
        igPattern = shutil.ignore_patterns(igPattern)
        
    if not os.path.isdir(src):
        error(r'src: {%} is not a directory' % src)
        
    if os.path.exists(dst):
        shutil.rmtree(dst)
        
    shutil.copytree(src, dst, ignore=igPattern)
    
def copy_dir(src, dst, ignore = None):
    """copy the src dir to dst dir
        if the dst dir alrady exist it will not remove it"""
    src = src.rstrip(r'\/')
    dst = dst.rstrip(r'\/')
    for root, dirnames, filenames in os.walk(src):
        if ignore and (ignore in root):
            continue
        
        for filename in filenames:
            src_path = os.path.join(root, filename)
            dst_path = os.path.join(dst, src_path[len(src)+1:])
            parent = os.path.dirname(dst_path) (not os.path.exists(parent)) and os.makedirs(parent)
            shutil.copyfile(src_path, dst_path)

def copy_file(src, dst):
    """copy file from src to dst
        it will create the parent directory if it's not exist"""
    if not os.path.isfile(src):
        error(r'src: {%s} is not a file' % src)
        
    parent = os.path.dirname(dst)
    if not os.path.isdir(parent):
        os.makedirs(parent)
        
    shutil.copyfile(src, dst)
    
def copy_path_list(src_base, dst_base, path_list, igPattern = None):
    """copy file/directory
    Args:
        path_list: is something like
        example: (('src1','dst1'),('src2','dst2'),...)"""
    for (src, dst) in path_list:
        src = os.path.join(src_base, src)
        dst = os.path.join(dst_base, dst)
        if os.path.isdir(src):
            copy_tree(src, dst, igPattern)
        elif os.path.isfile(src):
            copy_file(src, dst)
        else:
            error(r'src: {%s} is not a file or directory' % src)
            
def make_dirs(path):
    """make the directory if any of the parent directory
        doesn't exist it will make it first"""
    (not os.path.exists(path)) and os.makedirs(path)
    
def touch(fname, times=None):
    with file(fname, 'a'):
        os.utime(fname, times)

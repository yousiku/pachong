#-*- coding:utf-8 -*-
import glob,os,sys,lucene,PyLucene
from lucene import SimpleFSDiretory


def luceneIndexer(docdir,indir):
    lucene.initVM()
    DIRTOINDEX = docdir
    INDEXDIR = indir
    indexdir = lucene.SimpleFSDirectory
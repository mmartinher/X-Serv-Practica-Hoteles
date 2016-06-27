#!/usr/bin/python
# -*- coding: utf-8 -*-

#XML Parser given an url

from xml.sax.handler import ContentHandler
from xml.sax import make_parser

class myContentHandler(ContentHandler):

    def __init__ (self):
        self.data = {'name': [], 'web': [], 'address': [], 'latitude': [], 'longitude': [],
                     'body': [], 'images': [], 'category': []}
        self.imagelist = []
        self.categorylist = []
        self.section = ['basicData', 'geoData', 'multimedia', 'categoria']
        self.inSection = [False] * len(self.section)
        self.tags = ['name', 'web', 'body', 'address', 'latitude', 'longitude', 'url', 'item']
        self.inTags = [False] * len(self.tags)
        self.theContent = ""
        self.imageflag = False
        self.itemflag = False
        self.flag = False

    def startElement(self, name, attrs):
        if name in self.section:
            self.inSection[self.section.index(name)] = 1
            self.flag = True
        elif self.inSection:
            if name in self.tags:
                self.inTags[self.tags.index(name)] = 1
                self.flag = False

    def endElement(self, name):
        position = 0
        if name in self.section:
            if self.inSection[2] and self.flag:
                self.data['images'] += [[""]]
            self.inSection[self.section.index(name)] = False
        elif self.inTags:
            for i,j in enumerate(self.inTags):
                if j:
                    position = i
                    break
            if name == self.tags[position]:
                if name == 'url':
                    self.imagelist.append(self.theContent)
                    self.imageflag = True
                elif name == 'item':
                    self.categorylist.append(self.theContent)
                    self.itemflag = True
                else:
                    try:
                        self.data[name] += [self.theContent]
                    except KeyError:
                        pass
                    if self.imageflag:
                        self.data['images'] += [self.imagelist]
                        self.imagelist = []
                        self.imageflag = False
                    elif self.itemflag:
                        self.categorylist = [self.categorylist[3], self.categorylist[5]]
                        self.data['category'] += [self.categorylist]
                        self.categorylist = []
                        self.itemflag = False
            self.theContent = ""
            try:
                self.inTags[self.tags.index(name)] = False
            except ValueError:
                pass
        self.flag = False

    def characters (self, chars):
        if self.inTags:
            self.theContent = self.theContent + chars

def getHotels(url):
    theParser = make_parser()
    theHandler = myContentHandler()
    theParser.setContentHandler(theHandler)
    theParser.parse(url)
    theHandler.data['images'] += [theHandler.imagelist]
    theHandler.data['category'] += [[theHandler.categorylist[3], theHandler.categorylist[5]]]
    return (theHandler.data)
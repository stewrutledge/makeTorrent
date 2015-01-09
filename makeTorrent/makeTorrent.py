#!/usr/bin/env python

from bencode import bencode
from hashlib import md5, sha1
from os import path, walk
from time import time
from urllib2 import urlparse


class makeTorrent:
    """
    Create single or multi-file torrents
    keywords:
      announcelist: a list of lists with announceurls [['http://example.com/announce']]
      httpseeds: a list of urls ['http://1.com/file', http://2.com/file]
      comment: text comment for torrent
    Several values are generated automtically:
      name: based on filename or path
      techincal info: generates when a sinlge or multi file is added
    """
    def __init__(self, announce, piece_length=262144, **kw):
        self.piece_length = piece_length
        if not bool(urlparse.urlparse(announce).scheme):
            raise ValueError('No schema present for url')
        self.tdict = {
            'announce': announce,
            'creation date': int(time()),
            'info': {
                'piece length': self.piece_length
            }
        }
        if kw.get('comment'):
            self.tdict.update({'comment': kw.get('comment')})
        if kw.get('httpseeds'):
            if not isinstance(kw.get('httpseeds'), list):
                raise TypeError('httpseeds must be a list')
            else:
                self.tdict.update({'httpseeds': kw.get('httpseeds')})
        if kw.get('announcelist'):
            if not isinstance(kw.get('announcelist'), list):
                raise TypeError('announcelist must be a list of lists')
            if False in [isinstance(l, list) for l in kw.get('announcelist')]:
                raise TypeError('announcelist must be a list of lists')
            if False in [bool(urlparse.urlparse(f[0]).scheme) for f in kw.get('announcelist')]:
                raise ValueError('No schema present for url')
            else:
                self.tdict.update({'announce-list': kw.get('announcelist')})

    def getDict(self):
        return(self.tdict)

    def getBencoded(self):
        return(bencode(self.tdict))

    def multi_file(self, basePath, check_md5=False):
        """
        Generate multi-file torrent
          check_md5: adds md5sum to the torrentlist
          basePath: path to folder
        Torrent name will automatically be basePath
        """
        if 'length' in self.tdict['info']:
            raise TypeError('Cannot add multi-file to single-file torrent')
        if basePath.endswith('/'):
            basePath = basePath[:-1]
        realPath = path.abspath(basePath)
        toGet = []
        fileList = []
        info_pieces = ''
        data = ''
        for root, subdirs, files in walk(realPath):
            for f in files:
                subPath = path.relpath(root, start=realPath).split('/')
                subPath.append(f)
                toGet.append(subPath)
        for pathList in toGet:
            length = 0
            filePath = ('/').join(pathList)
            if check_md5:
                md5sum = md5()
            fileDict = {
                'path': pathList,
                'length': len(open(path.join(basePath, filePath)).read())
            }
            with open(path.join(basePath, filePath)) as fn:
                while True:
                    filedata = fn.read(self.piece_length)

                    if len(filedata) == 0:
                        break

                    length += len(filedata)

                    data += filedata

                    if len(data) >= self.piece_length:
                        info_pieces += sha1(data[:self.piece_length]).digest()
                        data = data[self.piece_length:]

                    if check_md5:
                        md5sum.update(filedata)
                        fileDict['md5sum'] = md5sum.hexdigest()
            fileList.append(fileDict)
        if len(data) > 0:
            info_pieces += sha1(data).digest()
        self.tdict['info'].update(
            {
                'name': path.basename(realPath),
                'files': fileList,
                'pieces': info_pieces
            }
        )
        return('Updated')
        #return(info_pieces, fileList)

    def single_file(self, fileName, check_md5=False):
        if 'files' in self.tdict['info']:
            raise TypeError('Cannot add single file to multi-file torrent')
        info_pieces = ''
        data = ''
        realPath = path.abspath(fileName)
        length = len(open(realPath).read())
        if check_md5:
            md5sum = md5()
        with open(realPath) as fn:
            while True:
                filedata = fn.read(self.piece_length)

                if len(filedata) == 0:
                    break

                length += len(filedata)

                data += filedata

                if len(data) >= self.piece_length:
                    info_pieces += sha1(data[:self.piece_length]).digest()
                    data = data[self.piece_length:]

                if check_md5:
                    md5sum.update(filedata)
        if len(data) > 0:
            info_pieces += sha1(data).digest()

        self.tdict['info'].update(
            {
                'length': length,
                'pieces': info_pieces,
                'name': path.basename(realPath)
            }
        )
        if check_md5:
            self.tdict['info'].update(
                {
                    'md5sum': md5sum.hexdigest()
                }
            )
        return('Updated')

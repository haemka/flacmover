#!/usr/bin/env python3
# flacmover.py -i sourcedir -o -destdir -f formatstring

import sys, getopt, os, fnmatch
import shutil, re
from mutagen import File
from mutagen.flac import FLAC, Picture

def walk(root):
    for root, dirnames, filenames in os.walk(root):
        cover = None
        for filename in fnmatch.filter(filenames, '*.flac'):
            filepath = root + '/' + filename
            print(filename)
            tag = File(filepath)
            ext = os.path.splitext(filename)[1]
            directory, filename = buildpath(tag, ext)
            new_path = outpath + directory + '/'
            new_filepath = new_path + filename
            new_coverpath = new_path + 'folder.jpg'
            print(new_filepath)
            copy(filepath, new_filepath)
            if not os.path.isfile(new_coverpath):
                cover = getcover(filepath)
                if cover != None:
                    print('Writing Albumart to {}'.format(new_coverpath))
                    cdata = open(new_coverpath, 'wb')
                    cdata.write(cover.data)
                    cdata.close()

def getcover(filepath):
    covers = FLAC(filepath).pictures
    for cover in covers:
        if cover.type == 3:
            print(str(cover))
            return(cover)
    return None

def buildpath(tag, ext):
    parts = filenameformat.split('%')
    for index, part in enumerate(parts):
        if part != '':
            if part in tag:
                if part == 'tracknumber':
                    parts[index] = tag[part][0].zfill(2)
                else:
                    parts[index] = replacer(tag[part][0])
            else:
                parts[index] = part
        else:
            parts[index] = part
    path = ''.join(parts) + ext
    directory = '/'.join(path.split('/')[:-1])
    filename = ''.join(path.split('/')[-1])

    return directory, filename

def replacer(content):
    table = {
        ord(u'Å'): 'Aa',
        ord(u'Å'): 'aa',
        ord(u'Ä'): 'Ae',
        ord(u'ä'): 'ae',
        ord(u'Æ'): 'Ae',
        ord(u'æ'): 'ae',
        ord(u'Á'): 'A',
        ord(u'á'): 'a',
        ord(u'À'): 'A',
        ord(u'à'): 'a',
        ord(u'Ã'): 'a',
        ord(u'ã'): 'a',
        ord(u'Ć'): 'C',
        ord(u'ć'): 'c',
        ord(u'Ç'): 'C',
        ord(u'ç'): 'c',
        ord(u'¢'): 'c',
        ord(u'Ð'): 'D',
        ord(u'ð'): 'd',
        ord(u'É'): 'E',
        ord(u'é'): 'e',
        ord(u'È'): 'E',
        ord(u'è'): 'e',
        ord(u'Ẽ'): 'E',
        ord(u'ẽ'): 'e',
        ord(u'Í'): 'I',
        ord(u'í'): 'i',
        ord(u'Í'): 'I',
        ord(u'í'): 'i',
        ord(u'Ì'): 'I',
        ord(u'ì'): 'i',
        ord(u'Ĩ'): 'I',
        ord(u'ĩ'): 'i',
        ord(u'Ñ'): 'N',
        ord(u'ñ'): 'n',
        ord(u'Ö'): 'Oe',
        ord(u'ö'): 'oe',
        ord(u'Ø'): 'Oe',
        ord(u'ø'): 'oe',
        ord(u'Œ'): 'Oe',
        ord(u'œ'): 'oe',
        ord(u'Ó'): 'O',
        ord(u'ó'): 'o',
        ord(u'Ò'): 'O',
        ord(u'ò'): 'o',
        ord(u'Õ'): 'O',
        ord(u'õ'): 'o',
        ord(u'Ü'): 'Ue',
        ord(u'ü'): 'ue',
        ord(u'Ú'): 'U',
        ord(u'ú'): 'u',
        ord(u'Ù'): 'U',
        ord(u'ù'): 'u',
        ord(u'Ũ'): 'U',
        ord(u'ũ'): 'u',
        ord(u'ß'): 'ss',
    }
    content = content.translate(table)
    content = re.sub('[^\w\-_\. ]','_', content)
    return content


def copy(srcfile, dstfile):
    if not os.path.exists(os.path.dirname(dstfile)):
        try:
            os.makedirs(os.path.dirname(dstfile))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    print('Copying {} to {}'.format(srcfile, dstfile))
    shutil.copy(srcfile, dstfile)

def usage(help = False):
    if help:
        print('This program is intended to copy FLAC music libraries into another directory using a defined structure.\n')
        print('Copies all files within a source directory recursively to another directory and (re)names directories and filenames according to a specified format taken from the files Metadata.\nFor each folder in source an albumart image is exported from a FLAC file if possible.\n')
    print('flacmover.py -i SRCDIR -o DESTDIR -f FORMATSTRING \n'
        + ' -i SRCDIR   source root of files; defaults to current dir \n'
        + ' -o DESTDIR  destination root of the renamed dirs and files \n'
        + ' -f FORMATSTRING any format of directory file structure \n'
        + '     with / as dir delimiter and %variable% for any variable \n'
        + '     found in FLAC file tags as used by mutagen. \n'
        + '     ex.: \n'
        + '         %albumartist%/%albumartist%.%originalyear%.%album%/%discnumber%.%tracknumber%.%artist%.%title%')
    exit(1)


def main(argv):
    global inpath, outpath, filenameformat
    inpath = os.getcwd()
    outpath = None
    filenameformat = None

    try:
        opts, args = getopt.getopt(argv,'hi:o:f:',['input=','output=','format='])
    except getopt.GetoptError:
        usage()
    for opt, arg in opts:
        if opt == '-h':
            usage(True)
        elif opt in ('-i', '--input'):
            inpath = arg
        elif opt in ('-o', '--output'):
            outpath = arg
        elif opt in ('-f', '--format'):
            filenameformat = arg
        else:
            usage()

    print('Input path is {}'.format(inpath))

    if outpath == None:
        print('No output directory set!')
        usage()
    if not outpath.endswith('/'):
        outpath = outpath + '/'

    walk(inpath)

if __name__ == '__main__':
    main(sys.argv[1:])

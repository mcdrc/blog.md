#!/usr/bin/python

'''Static blog/website builder. 

    Copyright 2015 Eric Thrift.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import os, time, glob, subprocess, re, sys

def generateHtml(mdFile, htmlFile):
    '''Convert Markdown to HTML using pandoc.'''
    
    print 'processing %s...' % mdFile
    subprocess.call(['pandoc', '--filter', 'internal-references', '-o',
        htmlFile, '--smart', '--standalone', 
        '--bibliography="%s"' % os.path.join('data','bibliography.bib'),
        '--css=data/buttondown.css', '-f', 'markdown+mmd_title_block',
        mdFile, os.path.join('data','footer.md')])
    return

def getMeta(md, key):
    '''Retrieve metadata from a Markdown document. The document must have
    MultiMarkDown style headers, with continuation lines indented by at least
    four spaces.'''
    
    m = None
    descStart = ''
    for line in md:
        if m:
            break
        if line.lower().startswith('%s: ' % key.lower()):
            descStart = line.partition(':')[2].strip(' \r\n')
            continue
        if descStart:
            if line.startswith ('    '):
                descStart = descStart + ' ' + line.strip(' \r\n')
            else:
                m = descStart
    return m

def getIndexData(mdFile):
    '''Retrieve title and description metadata from a Markdown
    document. Prepare a thumbnail image based on the first image in the 
    document.'''
    
    description = None
    img = None
    thumb = None
    title = None
    thumbFile = None

    with open(mdFile, 'r') as mdF:
        md = mdF.readlines()
    description = getMeta(md, 'description')
    title = getMeta(md, 'title')
    for line in md:
        if not img:
            img = re.match('.*?\]\((img/.*?)\)', line)
    
    if img:        
        #resize the image
        inFile = img.group(1)
        throot, thext = os.path.splitext(inFile)
        
        if 'SVG' in thext.upper():
            thumbFile = '%s-thumb%s' % (throot, '.png')
            subprocess.call(['inkscape', '-e', thumbFile, '-w', '200',
                inFile])
            
        else:
            thumbFile = '%s-thumb%s' % (throot, thext)
            if not os.path.exists(thumbFile):
                subprocess.call(['convert', inFile, '-resize', '200x200', 
                    thumbFile])
        
    return (thumbFile, title, description, mdFile)

def writeIndex(articles, indexNumber=0, prevlink=False):
    nextIndexFile = False
    if indexNumber:
        indexFile = 'archive%03d.html' % indexNumber
        if indexNumber == 1:
            nextIndexFile = 'index.html'
        else:
            nextIndexFile = 'archive%03d.html' % indexNumber
    else:
        indexFile = 'index.html'
    prevIndexFile = 'archive%03d.html' % (indexNumber+1)
    

    with open('index.md', 'w') as indexFileStream:
        headerFile = os.path.join('data', 'indexheader.md')
        if os.path.exists(headerFile):
            with open(headerFile, 'r') as header:
                indexFileStream.write(header.read())
        indexFileStream.write('\n\n----\n\n'.join(articles))\
        
        links = list()
        if prevlink:
            links.append('[Previous articles](%s)' % prevIndexFile)
        if nextIndexFile:
            links.append('[Next articles](%s)' % nextIndexFile)
        if links:
            indexFileStream.write('\n\n---\n\n%s' % ' | '.join(links))
    generateHtml('index.md', indexFile)
    os.unlink('index.md')

def run(blogpath):

    os.chdir(blogpath)

    curtime = time.time()
    
    if not os.path.exists('index.html'):
        ts = 0
    else:
        ts = os.path.getmtime('index.html')
    
    filenames = glob.glob('*.md')
    filenames.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    
    indexData = list()
    
    for mdFile in filenames:
        root, ext = os.path.splitext(mdFile)
        htmlFile = '%s.html' % root
        if os.path.getmtime(mdFile) > ts:
            generateHtml(mdFile, htmlFile)
        indexData.append(getIndexData(mdFile))
    
    articles = list()
    
    for i in indexData:
        txt = list()
        htmlFile = os.path.splitext(i[3])[0]+'.html'
        if i[0]:
            txt.append('![](%s) ' % i[0])
        txt.append('**[%s](%s)**' % (i[1], htmlFile))
        if i[2]:
            txt.append('\n-- ')
            txt.append(i[2])
        articles.append(''.join(txt))
    
    # split into 20 articles per page
    offset = 0
    count = 20
    indexNumber = 0
    prevlink = True
    
    while len(articles) > offset:
        if offset + count >= len(articles):
            prevlink = False
        writeIndex(articles[offset:offset+count], indexNumber, prevlink)
        offset = offset+count
        indexNumber = indexNumber + 1

    return

if __name__ == "__main__":
    if not sys.argv[1]:
        blogpath = os.getcwd()
    else:
        blogpath = sys.argv[1]
    run(blogpath)

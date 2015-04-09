# blog.md

This script generates a static blog, based on pages written in Markdown, with a 
paginated index that lists articles in reverse chronological order and provides 
descriptions and thumbnail images for each article. There is no commenting, no 
version control, no tagging. Just content.

This minimalist script is intended to support a scenario where Internet access 
is absent or intermittent, preventing the use of a web-based content management 
system such as Wordpress. In a collaborative setup, plain text files and images 
simply need to be dumped by users into a shared directory (by sneakernet or 
file-synchronization utility), and one machine in the network runs a cron job 
to generate the static content.

There are other static website builders that do much the same thing, but they 
have their own drawbacks -- requiring knowledge of git, for example, or else 
having a format that requires too much work to customize. With this script in 
place, anyone who can write Markdown can be a blogger. 

## Requirements

- python
- [pandoc] -- to convert Markdown to HTML
- imagemagick  -- to generate thumbnails from raster images
- inkscape -- to generate thumbnails from SVG images
- pandoc [internal-references filter] -- to allow cross-references


Bibliography and cross-referencing support is hard-coded into the script, but 
can easily be removed if installing the internal-references filter is too much 
trouble. Just modify the pandoc command in `generateHtml()` at the top of the 
file as needed. Otherwise, the following should work:

    pip install git+https://github.com/aaren/pandoc-reference-filter.git


## Setup and usage

To initialize a blog, unzip `blog_template` into a directory and edit the files 
in the `data/` subdirectory.

The `data` directory should contain the following files (they can be blank):

  - indexheader.md -- Text or headers that go at the top of the index page.
  
  - footer.md -- Text that goes at the bottom of every page, such as a 
    copyright notice or link to the front page.

  - bibliography.bib -- for bibliographic references. Add BibTeX format
    references here if you need them.

The script expects images to be in an `img/` subdirectory. Articles will be 
generated from Markdown files (`*.md`) in the top-level directory.

The first image in the `img/` directory that is referenced in an article will 
be used as a thumbnail in the index. To force the use of a thumbnail, put the 
image in an html comment at the beginning of the Markdown source:
    
    <!-- ![](img/myImage.png) -->

Raster formats (png, jpeg) and svg will work.

[pandoc]: http://johnmacfarlane.net/pandoc/README.html
[internal-references filter]: https://github.com/aaren/pandoc-reference-filter



To build the blog:

    ./blog.py  PATH/TO/DIRECTORY

This rebuilds the index and missing thumbnails, as well as processing any pages
whose source has been updated since the index was last generated.

To regenerate everything, simply delete the `index.html` file.


## TODO:

Make a setup file.


## License

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

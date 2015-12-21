ctrlp-py-matcher
================

A CtrlP matcher plugin with sane ranking

CtrlP is cool, but it doesn't do a great job finding the best match for the
thing you typed.  (Or maybe I'm just not good enough at configuring it.)

This plugin attempts to fix this by applying some heuristics.  Basically, we
prefer matches that hit the beginning or end of the filename.  When we can't do
that, we prefer matches that begin or end at a word boundary (non-lower-case
alpha char).

With these changes, the thing I want is almost always the first hit.

This plugin doesn't currently support most of CtrlP's fancy search modes.  No
regexp, no switching from filename to full-path searches.  It's really just a
hack.

This plugin is a fork of [another](https://github.com/FelikZ/ctrlp-py-matcher)
ctrlp-py-matcher, whose goal was to be faster than CtrlP's vimscript-based
matcher.  I don't have benchmarks, but unscientifically, this version also feels
faster than the native vimscript matcher when you have 50k+ files.

Prerequisites
-------------

You'll need Vim compiled with the `+python` flag:
```
vim --version | grep python
```

This plugin should be compatible with vim **7.x** and
[NeoVIM](http://neovim.io), although I haven't tested it.

Installation
------------

First get the package, using your favorite tool:

Pathogen (https://github.com/tpope/vim-pathogen)

    $ git clone https://github.com/FelikZ/ctrlp-py-matcher ~/.vim/bundle/ctrlp-py-matcher

Vundle (https://github.com/gmarik/vundle)

    Plugin 'jlebar/ctrlp-py-matcher'

NeoBundle (https://github.com/Shougo/neobundle.vim)

    NeoBundle 'jlebar/ctrlp-py-matcher'

Then add the following line to your vimrc:

    if has('python')
        let g:ctrlp_match_func = { 'match': 'pymatcher#PyMatch' }
    endif

Troubleshooting
---------------

If you have performance issues, it can be caused by
[bufferline](https://github.com/bling/vim-bufferline) or similar plugins. For
bufferline specifically, try switching to
[airline](https://github.com/bling/vim-airline) and adding the following to your
vimrc:

    let g:airline#extensions#tabline#enabled = 1

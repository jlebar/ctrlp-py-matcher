" Python Matcher

if !has('python') && !has('python3')
    echo 'In order to use pymatcher plugin, you need +python or +python3 compiled vim'
endif

let s:plugin_path = escape(expand('<sfile>:p:h'), '\')

if has('python3')
  execute 'py3file ' . s:plugin_path . '/pymatcher.py'
else
  execute 'pyfile ' . s:plugin_path . '/pymatcher.py'
endif

function! pymatcher#PyMatch(items, str, limit, mmode, ispath, crfile, regex)
    call clearmatches()
    if a:str == ''
        return a:items[0:a:limit]
    endif

    let s:rez = []
    execute 'python' . (has('python3') ? '3' : '') . ' CtrlPPyMatch()'
    call matchadd('CtrlPMatch', '\v\c' . a:str)
    return s:rez
endfunction

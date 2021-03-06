import heapq
import os
import re

# If the search string does not contain "/", we consider only filenames;
# otherwise we consider the full path.
def ItemRanks(search, items):
  """
  Get (sort_key, item) tuples for entries in items.

  For each element of items which matches search, generate a tuple (sort_key,
  item) such that elements with larget sort_keys are better matches for search.

  Matches are ranked as follows:
  1) Full matches.
  2) Matches anchored at the beginning.
  3) Matches which begin with a capital letter (e.g. matching "bar" in
     "FooBar.cpp") or for which the preceeding char is non-alpha.
  4) Matches anchored at the end.
  5) Matches anchored right before ".".
  6) Matches which are immediately followed by a non-lower-case-alpha char.
  7) Matches with shorter filenames.

  >>> list(ItemRanks('tool', ['dir/Tool.cpp']))[0][1] > list(ItemRanks('tool', ['dir/Tools.cpp']))[0][1]
  True
  >>> list(ItemRanks('tool', ['dir/ToolFoo']))[0][1] > list(ItemRanks('tool', ['dir/Toolfoo']))[0][1]
  True
  >>> list(ItemRanks('tool', ['dir/Tool.cpp']))[0][1] > list(ItemRanks('tool', ['dir/ToolFoo.cpp']))[0][1]
  True
  >>> len(list(ItemRanks('tool', ['dir/Toool.cpp'])))
  0
  """
  search_lower = search.lower()

  for i in items:
    f = i.lower()
    if search_lower not in f:
      # Bail early if we can, to avoid calling os.path.basename.
      continue

    if '/' not in search_lower:
      f = os.path.basename(f)

    start_idx = f.lower().find(search_lower)
    end_idx = start_idx + len(search_lower)  # exclusive
    if start_idx == -1:
      continue
    beg_match = start_idx == 0
    end_match = end_idx == len(f)
    full_match = beg_match and end_match
    beg_token = f[start_idx].isupper() or start_idx == 0 or (
        start_idx > 0 and not f[start_idx - 1].isalpha())
    end_dot = end_idx < len(f) and f[end_idx] == '.'
    end_token = end_idx < len(f) and not f[end_idx].islower()
    filename_len = len(os.path.basename(f))
    yield ((True, full_match, beg_match, beg_token,
            end_match, end_dot, end_token, -filename_len), i)

def CtrlPPyMatch():
  import vim

  items = vim.eval('a:items')
  astr = vim.eval('a:str')
  limit = int(vim.eval('a:limit'))
  mmode = vim.eval('a:mmode')
  aregex = int(vim.eval('a:regex'))
  rez = vim.eval('s:rez')

  if aregex == 1:
    raise ValueError('Regexp matches are not supported.')

  # TODO: Do something with mmode.  Possible values are 'filename-only',
  # 'first-non-tab', 'until-last-tab', and one other (unsure what).

  rez = (f for (k, f)
         in heapq.nlargest(limit, ItemRanks(astr, items), lambda kp: kp[0]))

  # Use double quoted vim strings, and escape \
  vimrez = ('"%s"' % f.replace('\\', '\\\\').replace('"', '\\"') for f in rez)

  vim.command('let s:rez = [%s]' % ','.join(vimrez))


if __name__ == "__main__":
    import doctest
    doctest.testmod()

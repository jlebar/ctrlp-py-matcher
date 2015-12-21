import heapq
import os
import re
import vim

# Now take the n best matches from amongst the filenames which contain
# search, ranked as follows:
# 1) Full matches.
# 2) Matches anchored at the beginning.
# 3) Matches which begin with a capital letter (e.g. matching "bar" in
#    "FooBar.cpp") or for which the preceeding char is non-alpha.
# 4) Matches anchored at the end.
# 5) Matches which end right before the final ".".
# 6) Matches that end with ".h" (so header files come first).
#
# If the search string does not contain "/", we consider only filenames;
# otherwise we consider the full path.
def ItemRank(f, search_lower):
  if '/' not in search_lower:
    f = os.path.basename(f)

  start_idx = f.lower().find(search_lower)
  end_idx = start_idx + len(search_lower)
  if start_idx == -1:
    return (False,)
  beg_match = start_idx == 0
  end_match = end_idx == len(f)
  full_match = beg_match and end_match
  beg_token = f[start_idx].isupper() or start_idx == 0 or (
      start_idx > 0 and not f[start_idx - 1].isalpha())
  end_dot = end_idx < len(f) - 1 and f[end_idx + 1] == '.'
  dot_h = f.endswith('.h')
  return (True, full_match, beg_match, beg_token, end_match, end_dot, dot_h)

def CtrlPPyMatch():
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

  key_pairs = ((ItemRank(f, astr.lower()), f) for f in items)
  rez = (f for (k, f)
         in heapq.nlargest(limit, key_pairs, lambda kp: kp[0])
         if k[0])  # filter out non-matches

  # Use double quoted vim strings, and escape \
  vimrez = ('"%s"' % f.replace('\\', '\\\\').replace('"', '\\"') for f in rez)

  vim.command('let s:rez = [%s]' % ','.join(vimrez))


if __name__ == "__main__":
    import doctest
    doctest.testmod()

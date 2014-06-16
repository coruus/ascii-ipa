# coding=utf-8
"""Convert Kirshenbaum's ASCII IPA to Unicode IPA.
"""
from __future__ import division, print_function

import re

PHONEMIC_RE = re.compile(r'/[^/]+/')
PHONETIC_RE = re.compile(r'\[[^\]+\]')


def _sort(it):
  """Sort by reverse-length, then alphabetically"""
  return sorted(it, key=lambda s: (-len(s[0]), s[0]))


# The segment list from [KPDF]
SEGLIST = _sort(\
          [('m',      u'm'),
           ('p',      u'p'),
           ('b',      u'b'),
           ('P',      u'Φ'),
           ('B',      u'β'),
           ('b<trl>', u'ʙ'),
           ('p`',     u'pʼ'),
           ('b`',     u'ɓ'),
           ('p!',     u'ʘ'),
           ('M',      u'ɱ'),
           ('f',      u'f'),
           ('v',      u'v'),
           ('r<lbd>', u'ʋ'),
           ('n[',     u'n\u032a'),
           ('t[',     u't\u032a'),
           ('T',      u'θ'),
           ('D',      u'ð'),
           ('r[',     u'r\u032a'),
           ('l[',     u'l\u032a'),
           ('t[`',    u't\u032a\u02bc'),
           ('d`',     u'ɗ'),
           ('t!',     u'ʇ'),
           ('n',      u'n'),
           ('t',      u't'),
           ('d',      u'd'),
           ('s',      u's'),
           ('z',      u'z'),
           ('s<lat>', u'ɬ'),
           ('z<lat>', u'ɮ'),
           ('r',      u'ɹ'),
           ('l',      u'l'),
           ('r<trl>', u'ʀ'),
           ('*',      u'ɾ'),
           ('*<lat>', u'ɺ'),
           ('t`',     u't\u02bc'),
           ('d`',     u'ɗ'),
           ('c!',     u'ʗ'),
           ('l!',     u'ʖ'),
           ('n.',     u'ɳ'),
           ('t.',     u'ʈ'),
           ('d.',     u'ɖ'),
           ('s.',     u'ʂ'),
           ('z.',     u'ʐ'),
           ('r.',     u'ɖ'),
           ('l.',     u'ɭ'),
           ('*.',     u'ɽ'),
           ('S',      u'ʃ'),
           ('Z',      u'ʒ'),
           ('n^',     u'n^'), ######
           ('c',      u'c'),
           ('J',      u'ɟ'),
           ('C',      u'ç'),
           ('C<vcd>', u'ʝ'),
           ('j',      u'j'),
           ('j<rnd>', u'ɥ'),
           ('l^',     u'ʎ'),
           ('J`',     u'ʄ'),
           ('c!',     u'ʗ'),
           ('N',      u'ŋ'),
           ('k',      u'k'),
           ('g',      u'g'),
           ('x',      u'x'),
           ('Q',      u'ɣ'),
           ('j<vel>', u'ɰ'),
           ('L',      u'ɫ'),
           ('{vls,alv,lat,frc}', u'ɬ'),
           ('k`',     u'k\u02bc'),
           ('g`',     u'g\u02bc'),
           ('k!',     u'ʞ'),
           ('n<lbv>', u'n\u2030g'),
           ('t<lbv>', u'k\u2030p'),
           ('n<lbv>', u'g\u2030b'),
           ('w<vls>', u'ʍ'),
           ('w',      u'w'),
           ('n"',     u'ɴ'),
           ('q',      u'q'),
           ('G',      u'ɢ'),
           ('X',      u'χ'),
           ('g"',     u'ʁ'),
           ('r"',     u'ʀ'),
           ('q`',     u'ʠ'),
           ('G`',     u'ʛ'),
           ('H',      u'ħ'),
           ('H<vcd>', u'ʕ'),
           ('?',      u'ʔ'),
           ('h',      u'h'),
           ('h<?>',   u'ɦ'),
           ('i',      u'i'),
           ('y',      u'y'),
           ('I',      u'ɪ'),
           ('I.',     u'ʏ'),
           ('e',      u'e'),
           ('Y',      u'ø'),
           ('E',      u'ɛ'),
           ('W',      u'œ'),
           ('&',      u'æ'),
           ('&.',     u'ɶ'),
           ('i"',     u'ɨ'),
           ('u"',     u'ʉ'),
           ('@<umd>', u'ɘ'),
           ('R<umd>', u'ɝ'),
           ('@',      u'ə'),
           ('R',      u'ɚ'),
           ('@.',     u'ɵ'),
           ('V"',     u'ɜ'),
           ('O"',     u'ɞ'),
           ('a',      u'a'),
           ('u-',     u'ɯ'),
           ('u',      u'u'),
           ('U',      u'ʊ'),
           ('o-',     u'ɤ'),
           ('o',      u'o'),
           ('V',      u'ʌ'),
           ('O',      u'ɔ'),
           ('A',      u'ɑ'),
           ('A.',     u'ɒ')])

VOWELS = ['@<umd>', 'R<umd>', '&.', '@.', 'A.', 'I.', 'O"', 'V"', 'i"', 'o-',
          'u"', 'u-', '&', '@', 'A', 'E', 'I', 'O', 'R', 'U', 'V', 'W', 'Y',
          'a', 'e', 'i', 'o', 'u', 'y']
INVVOW = [uni for seg, uni in SEGLIST if seg in VOWELS]

# Diacritics which do not depend on voice
DIACRITICS = [(':', u'ː'),
              ('.', u'\u0322'),
              ('`', u'\u02bc'),
              ('[', u'\u032a'),
              (';', u'\u02b2'),
              ('"', u'"'),
              ('^', u'^'),
              ('<H>', u'\u0334'),
              ('<h>', u'\u02b0'),
              ('<unx>', u'\u02da'),
              ('<vls>', u'\u0325'),
              ('<o>', u'\u02da'),
              ('<r>', u'\u02b3'),
              ('<w>', u'\u02b7'),
              ('<?>', u'\u02b1')]
DIACRITICS_VOWEL = [('~', u'\u0303')]
DIACRITICS_CONSONANT = [('~', u'\u0334')]

STRESS = {"'": u"ˈ", ",": u"ˌ", ' ': u' ', '\n': u'\n'}
INVSTRESS = {u"ˈ": "'",
             u"ˌ": ",",
             u' ': ' ',
             u'\n': '\n'}


INVDIA = _sort([(b, a) for (a, b) in \
          [(':', u'ː'),
           ('.', u'\u0322'),
           ('.', u'\u0323'),
           ('`', u'\u02bc'),
           ('[', u'\u032a'),
           (';', u'\u02b2'),
           (';', u'\u0321'),
           ('"', u'"'),
           ('^', u'^'),
           ('<H>', u'\u0334'),
           ('<h>', u'\u02b0'),
           ('<unx>', u'\u02da'),
           ('<vls>', u'\u0325'),
           ('<o>', u'\u02da'),
           ('<r>', u'\u02b3'),
           ('<w>', u'\u02b7'),
           ('<?>', u'\u02b1'),
           ('~', u'\u0303'),
           ('~', u'\u0334')]
                ])
INVSEGLIST = _sort((b, a) for (a, b) in SEGLIST)


def _ascii_to_unicode(s):
  """ASCII-IPA to Unicode IPA. Note: because of the simple syntax,
     the peculiar control flow is fine.
  """
  vowel = True
  t = u''
  lasts = ''
  while s:
    # Guarantees progress
    if lasts == s:
      t += s[0]
      s = s[1:]
    lasts = s

    if s[0] in STRESS:
      t += STRESS[s[0]]
      s = s[1:]

    for seg, uni in SEGLIST:
      if s.startswith(seg):
        s = s[len(seg):]
        t += uni
        vowel = seg in VOWELS

    for dia, uni in DIACRITICS:
      if s.startswith(dia):
        s = s[len(dia):]
        t += uni

    if s and s[0] == '~':
      t += DIACRITICS_VOWEL['~'] if vowel else DIACRITICS_CONSONANT['~']
      s = s[1:]

  return t


def _unicode_to_ascii(s):
  """Unicode IPA to ASCII-IPA"""
  vowel = True
  t = ''
  lasts = u''
  while s:
    # Guarantees progress
    if lasts == s:
      t += s[0]
      s = s[1:]
    lasts = s

    if s[0] in INVSTRESS:
      t += bytes(INVSTRESS[s[0]])
      s = s[1:]

    for seg, uni in INVSEGLIST:
      if s.startswith(seg):
        s = s[len(seg):]
        t += uni
        vowel = seg in INVVOW

    for dia, uni in INVDIA:
      if s.startswith(dia):
        s = s[len(dia):]
        t += uni

  return t


# TODO: test cases
# phrase = u'''
# ai hir D@ 'sEkrI,t&ri
# aI hi@ DI 'sEkrVtri
# t<h>&:g<o>
# t!
# R<umd>
# '''

# ipa = u'''ˈeːɪjaˌfjatl̥aˌjœːkʏtl̥''
# hɔrs hoʊrs
# hɔrs
# '''

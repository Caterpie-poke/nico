import unittest # unittest
import tests # __init__.pyを読んでexTestが使えるようになる
from pegpy.gparser.gnez import *
from pathlib import Path

class TestNPEG(unittest.TestCase):

    def test_math(self):
        g = Grammar("")
        g.load('gpt.gpeg')
        g.example('Source', '[ABC]', "[#Input [#C 'A'] [#C 'B'] [#C 'C']]")
        g.example('Source', '[あいう]', "[#Input [#C 'あ'] [#C 'い'] [#C 'う']]")
        g.example('Source', '[あ]', "[#Input [#C 'あ']")
        self.exTest(g, nnez)


"""
実行結果
======================================================================
FAIL: test_math (tests.test_mine.TestNPEG) (example='Source')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/apple/Dropbox/pegpy-master/tests/__init__.py", line 20, in exTest
    self.assertEqual(t, output)
AssertionError: "[#err '']" != "[#Input [#C 'あ']"
- [#err '']
+ [#Input [#C 'あ']


----------------------------------------------------------------------
Ran 1 test in 0.005s

FAILED (failures=1)
"""

import unittest
from datetime import datetime

from commenters import *

param_list_gtb = [(19, 29, 'first'), (20, 15, 0), (20, 45, 1), (21, 45, 2), (23, 44, 6), (23, 59, 'last')]
param_list2 = [(5, 29, 'first'), (5, 30, 0), (6, 30, 1), (7, 30, 3), (8, 2, 4), (12, 1, 'last')]

def add_h_m(dtime, h, m):
    return dtime.replace(hour=h, minute=m)

class TestWakeupComment(unittest.TestCase):

    def setUp(self):
        self.comment = WakeupComment((5, 30), (11, 30), [[5, 30, i18n.t('comment.w1')], [6, 30, i18n.t('comment.w2')], [7, 0, i18n.t('comment.w3')], [8, 0, i18n.t('comment.w4')], [9, 0, i18n.t('comment.w5')], [10, 0, i18n.t('comment.w6')], [11, 0, i18n.t('comment.w7')], [12, 0, i18n.t('comment.w8')]])

    def test_parameterized(self):
        for h, m, expected in param_list2:
            with self.subTest():
                now = datetime.now()
                dtime = add_h_m(now, h, m)
                idx, msg = self.comment.get_msg(dtime)
                self.assertEqual(idx, expected)

    def test_first(self):
        now = datetime.now()
        dtime = add_h_m(now, 5, 29)

        idx, msg = self.comment.get_msg(dtime)

        self.assertEqual('foo'.upper(), 'FOO')


class TestGotoBedComment(unittest.TestCase):

    def setUp(self):
        self.comment = GotoBedComment((19, 30), (3, 0), [[20, 16, i18n.t('comment.b1')], [21, 00, i18n.t('comment.b2')], [21, 46, i18n.t('comment.b3')], [22, 15, i18n.t('comment.b4')], [23, 00, i18n.t('comment.b5')], [23, 40, i18n.t('comment.b6')], [23, 56, i18n.t('comment.b6')]])

    def test_parameterized(self):
        for h, m, expected in param_list_gtb:
            with self.subTest():
                now = datetime.now()
                dtime = add_h_m(now, h, m)
                idx, msg = self.comment.get_msg(dtime)
                self.assertEqual(idx, expected)


if __name__ == '__main__':
    unittest.main()

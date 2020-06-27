from helpers import *
import i18n
import os

i18n.load_path.append('msgs')

i18n.set('locale', 'en')
if "SYSTEM" in os.environ:
    if os.environ['SYSTEM'] == "PRD":
        i18n.set('locale', 'de')


class SleepComment:
    def __init__(self, first, last, mylist):
        self.first = first
        self.last = last
        self.list = mylist
    
    def update(self):
        self.time = datetime.now()

    def compare_first(self, dtime):
        if dtime < replace_h_m(dtime, self.first[0], self.first[1]):
            return "Vor: " + dtime.strftime("%H:%M") + i18n.t('comment.earliest')

    def compare_last(self, dtime):
        if dtime > replace_h_m(dtime, self.last[0], self.last[1]):
            return dtime.strftime("%H:%M") + i18n.t('comment.latest')

    def get_msg(self, dtime):

        msg = self.compare_first(dtime)
        if msg:
            return 'first', msg

        for i, e in enumerate(self.list):
            if dtime <= replace_h_m(dtime, e[0], e[1]):
                return i, dtime.strftime("%H:%M") + e[2]

        msg = self.compare_last(dtime)
        if msg:
            return 'last', msg

class WakeupComment(SleepComment):
    pass

class GotoBedComment(SleepComment):
    pass

waC = WakeupComment((5, 30), (12, 2), [[5, 30, i18n.t('comment.w1')], [6, 30, i18n.t('comment.w2')], [7, 0, i18n.t('comment.w3')], [8, 0, i18n.t('comment.w4')], [9, 0, i18n.t('comment.w5')], [10, 0, i18n.t('comment.w6')], [11, 0, i18n.t('comment.w7')], [12, 0, i18n.t('comment.w8')]])
gbC = GotoBedComment((19, 30), (23, 59), [[20, 15, i18n.t('comment.b1')], [20, 45, i18n.t('comment.b2')], [21, 45, i18n.t('comment.b3')], [22, 15, i18n.t('comment.b4')], [23, 00, i18n.t('comment.b5')]])

def get_time_comment(time, typ):

    if typ == ("wakeup" or "standup" or "breakfast" or "toothbrush_morning"):
        waC.update()
        return waC.get_msg(time)
    elif typ == ("gotobed" or "handyaway" or "toothbrush_evening"):
        gbC.update()
        return gbC.get_msg(time)
    else:
        return ""

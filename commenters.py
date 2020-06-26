from helpers import *
import i18n
import os

i18n.load_path.append('msgs')

i18n.set('locale', 'en')
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
            return msg
        
        msg = self.compare_last(dtime)
        if msg:
            return msg

        for e in self.list:
            if dtime > replace_h_m(dtime, e[0], e[1]):
                return dtime.strftime("%H:%M") + e[2]


class WakeupComment(SleepComment):
    pass

class GotoBedComment(SleepComment):
    def get_msg(self, dtime):
        
        msg = self.compare_first(dtime)
        if msg:
            return msg
        
        for e in self.list:
            if dtime < replace_h_m(dtime, e[0], e[1]):
                return dtime.strftime("%H:%M") + e[2]
        
        msg = self.compare_last(dtime)
        if msg:
            return msg

waC = WakeupComment((5, 30), (11, 30), [[6, 0, i18n.t('comment.w1')], [7, 0, i18n.t('comment.w2')], [8, 0, i18n.t('comment.w3')]])
gbC = GotoBedComment((19, 30), (1, 30), [[20, 15, i18n.t('comment.b1')], [20, 45, i18n.t('comment.b2')], [21, 45, i18n.t('comment.b3')], [22, 15, i18n.t('comment.b4')], [23, 00, i18n.t('comment.b5')]])

def get_time_comment(time, typ):
    dtime = get_time_from_string(time)

    if typ == ("wakeup" or "standup" or "toothbrush_morning"):
        waC.update()
        return waC.get_msg(dtime)
    elif typ == ("gotobed" or "handyaway" or "toothbrush_evening"):
        gbC.update()
        return gbC.get_msg(dtime)
    else:
        return ""

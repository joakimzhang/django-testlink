# -*- coding: utf-8 -*-

import switch_stream


class switch_stream_Worker():
    def __init__(self):
        self.data = {}

    def run_switch_one(self, ts_card, ts_file):
        print "the ts path is:%s" % ts_file
        print "the ts card is %s" % ts_card
        ts_file = r'%s' % ts_file
        argv_stream = ["-H", ts_card, "-P", "7777", "-f",
                       ts_file, '--std=custom', "-F", "578"]
        result_num = switch_stream.exec_switch(argv_stream)
        return result_num
        print "switch stream successfully  run_switch_one"

    # 切换码流卡模式
    def run_switch_mode(self, ts_card, modulation,
                        frame_rate, code_rate, carrier_mode):
        print "the ts card is %s" % ts_card
        argv_stream = ["-H", ts_card, "-P", "7777", '--std=mode',
                       "-M", modulation, "--FM=%s" % frame_rate,
                       "--CR=%s" % code_rate, "--CM=%s" % carrier_mode]
        result_num = switch_stream.exec_switch(argv_stream)
        return result_num
        print "switch stream successfully run_switch_mode "

    def run_switch(self, ts_card, ts_file, modulation,
                   frame_rate, code_rate, band_width):
        print "the ts path is:%s" % ts_file
        print "the ts card is %s" % ts_card
        ts_file = r'%s' % ts_file
        argv_stream = ["-H", ts_card, "-P", "7777", "-f",
                       ts_file, '--std=DTMB', "-F", "578",
                       "-M", modulation, "--FM=%s" % frame_rate,
                       "--CR=%s" % code_rate, "--BW=%s" % band_width]
        result_num = switch_stream.exec_switch(argv_stream)
        return result_num
        print "switch stream successfully run_switch"

if __name__ == "__main__":
    #test = switch_stream_Worker()
    '''test.run_switch(r"bjdittest",
                    r"\\10.209.156.47\scannedfiles\zhangq\yanquan.ts")'''

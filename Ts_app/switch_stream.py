# -*- coding=UTF-8 -*-

import socket
import sys

import re
from optparse import OptionParser
import time


class ConnectSocket(object):

    def __init__(self, ip_addr, port):

        self.host = ip_addr
        self.port = port
        self.socket_fd = None

        try:
            self.socket_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket_fd.connect((self.host, self.port))
        except socket.error, msg:
            print 'Failed to create socket. Error code: ' + str(msg[0])\
             + ' , Error message : ' + msg[1]
            sys.exit()

    def recevieResult(self):
        result = ''
        self.socket_fd.settimeout(5)
        while 1:
            try:
                result = result + self.socket_fd.recv(1)
            except socket.timeout:
                # print 'timeout exception'
                break
                # print 'sss',unicode(result, 'utf-16le')

        return unicode(result, 'utf-16le')

    def sendCmd(self, cmd):
        cmd_str = cmd.encode('utf-16le')
        self.socket_fd.send(cmd_str)

    def closeSocket(self):
        self.socket_fd.close()


def arguParse(argus):
    parser = OptionParser(usage=("usage:%prog [OPTIONS]"
                                 " -H hostname "
                                 " -P port "
                                 " -f test stream location"
                                 " --std test stream standard"
                                 " -F frequency number"
                                 " -S symbol number"))

    parser.add_option("-H", "--HOSTNAME",
                      action="store",
                      dest="hostname",
                      default=None,
                      help="Specify host name"
                      )

    parser.add_option("-P", "--PORT",
                      action="store",
                      type='int',
                      dest="port",
                      default=None,
                      help="Specify port number"
                      )

    parser.add_option("-f", "--TS",
                      action="store",
                      dest="ts",
                      default=None,
                      help="Specify test stream location"
                      )

    parser.add_option("--std", "--STD",
                      action="store",
                      dest="std",
                      default=None,
                      help="Specify test stream standard"
                      )

    parser.add_option("-F", "--FREQ",
                      action="store",
                      type='int',
                      dest="freq",
                      default=None,
                      help="Specify frequence number"
                      )
    '''DVB-S mode'''
    parser.add_option("-S", "--syml",
                      action="store",
                      type='int',
                      dest="syml",
                      default=27500,
                      help="Specify symbol number"
                      )
    '''DTMB mode'''
    parser.add_option("--BW", "--BandWidth",
                      action="store",
                      type='int',
                      dest="bandwidth",
                      default=None,
                      help="Specify bandwidth number"
                      )
    parser.add_option("-M", "--Modulation",
                      action="store",
                      type='int',
                      dest="modulation",
                      default=None,
                      help="Specify Modulation number"
                      )
    parser.add_option("--FM", "--FrameMode",
                      action="store",
                      type='int',
                      dest="framemode",
                      default=None,
                      help="Specify framemode number"
                      )
    parser.add_option("--CR", "--CodeRate",
                      action="store",
                      type='int',
                      dest="coderate",
                      default=None,
                      help="Specify coderate number"
                      )
    parser.add_option("--CM", "--CarrierMode",
                      action="store",
                      type='int',
                      dest="carriermode",
                      default=None,
                      help="Specify carriermode number"
                      )
    '''
    parser.add_option("-u", "--url",
                    action = "store_true",
                    dest = "url",
                    default = False,
                    help = "Specify if the target is an URL"
                    )
    '''
    options, _ = parser.parse_args(argus)
    if options.hostname is None:
        parser.description
        print 'Hostname is incorrect'
        print parser.usage
        sys.exit()
    elif options.port is None:
        parser.description
        print 'Port is incorrect'
        print parser.usage
        sys.exit()
    elif options.ts is None:
        parser.description
        print 'Test stream location is incorrect'
        print parser.usage
        # sys.exit()
    elif options.std is None:
        parser.description
        print 'Test stream standard is incorrect'
        print parser.usage
        sys.exit()

    if options.std == 'DVB-S':
        if options.freq is None:
            parser.description
            print 'Frequency number is incorrect'
            print parser.usage
            sys.exit()
        elif options.syml is None:
            parser.description
            print 'Symbol number is incorrect'
            print parser.usage
            sys.exit()
    elif options.std == 'DTMB':
        if options.freq is None:
            parser.description
            print 'Frequency number is incorrect'
            print parser.usage
            sys.exit()
#        elif options.modulation is None:
#            parser.description
#            print 'Modulation number is incorrect'
#            print  parser.usage
#            sys.exit()

    '''
    print options.hostname
    print options.port
    print options.ts
    print options.freq
    print options.syml
    '''
    return options


def exec_switch(argv_stream):
    options = arguParse(argv_stream)
    result_message = []

    # Connect remote server
#    socket_con = ConnectSocket(options.hostname,options.port)
#    socket_con.recevieResult()
    try:
        socket_con = ConnectSocket(options.hostname, options.port)
    except:
        # return -99
        return ["can not connect to: %s" % options.hostname]
    res = socket_con.recevieResult()
    if re.search('Welcome', res):
        pass
    else:
        # return -99
        return res

    # Stop ts
#    socket_con.sendCmd('stop')
#   socket_con.recevieResult()

    if options.std == 'DVBS':
        # Set std value
        std_name = 'dvbs'
        print 'std %s' % std_name
        socket_con.sendCmd('chstd %s' % std_name)
        res = socket_con.recevieResult()
        if re.search('Change STD', res):
            pass
        else:
            socket_con.closeSocket()
            return -2

        # Load ts to TSRunner
        print 'loadfile %s' % options.ts
        socket_con.sendCmd('loadfile %s' % options.ts)
        res = socket_con.recevieResult()
        if re.search('Success', res):
            pass
        else:
            socket_con.closeSocket()
            return -3

        # Set frequency value
        print 'freq %d' % options.freq
        socket_con.sendCmd('freq %d' % options.freq)
        res = socket_con.recevieResult()
        if re.search('Set Frequence', res):
            pass
        else:
            socket_con.closeSocket()
            return -4
        # Set symbol rate value
        print 'Syml %d' % options.syml
        socket_con.sendCmd('chpara SymbolRate  %d' % options.syml)
        res = socket_con.recevieResult()
        if re.search('Set', res):
            pass
        else:
            socket_con.closeSocket()
            return -9

        # Set code rate value
        socket_con.sendCmd('chpara Coderate %d' % (options.coderate-1))
        res = socket_con.recevieResult()
        if re.search('Para Name Error', res):
            print "Code Rate is failed for setting 2/3,\
                the code rate will use default value"
            socket_con.closeSocket()
            return -10

    elif options.std == 'DTMB':
        # Set std value
        std_name = 'dtmb'
        print 'std %s' % options.std
        socket_con.sendCmd('chstd %s' % std_name)
        res = socket_con.recevieResult()
        result_message.append(res)
        if re.search('Change STD', res):
            pass
        else:
            socket_con.closeSocket()
            return [-2]
        # Load ts to TSRunner
        print 'loadfile %s' % options.ts
        socket_con.sendCmd('loadfile %s' % options.ts)
        for i in range(5):
            res = socket_con.recevieResult()
            if re.search('Success', res):
                # pass
                break
            else:
                # socket_con.closeSocket()
                time.sleep(1)
                if i == 4:
                    socket_con.closeSocket()
                    # return -3
                    return ['load file fail:', options.ts]
        # result_message = result_message + res + '<br/>'
        result_message.append(res)
        result_message.append(options.ts)

        # Set frequency value
        print 'freq %d' % options.freq
        socket_con.sendCmd('freq %d' % options.freq)
        res = socket_con.recevieResult()
        # result_message = result_message + res + '\n'
        result_message.append(res)
        if re.search('Set Frequence', res):
            pass
        else:
            socket_con.closeSocket()
            return [-4]
        # Set bandwith value
        if options.bandwidth:
            print 'bandwidth %d' % options.bandwidth
            cmd_bw = ''
            if options.bandwidth == 1:
                cmd_bw = 'chpara BandWidth 3'
            elif options.bandwidth == 2:
                cmd_bw = 'chpara BandWidth 2'
            elif options.bandwidth == 3:
                cmd_bw = 'chpara BandWidth 1'
            elif options.bandwidth == 4:
                cmd_bw = 'chpara BandWidth 0'
            socket_con.sendCmd(cmd_bw)
            res = socket_con.recevieResult()
            # result_message = result_message + res + '\n'
            result_message.append(res)
            if re.search('Set BandWidth', res):
                pass
            else:
                socket_con.closeSocket()
                return [-5]
        # Set modulation value
        if options.modulation:
            print 'modulation %d' % options.modulation
            socket_con.sendCmd('chpara Modulation %d' % (options.modulation-1))
            res = socket_con.recevieResult()
            result_message.append(res)
            # result_message = result_message + res + '\n'
            if re.search('Set Modulation', res):
                pass
            else:
                socket_con.closeSocket()
                return [-6]
        # Set modulation value
        if options.framemode:
            print 'framemode %d' % options.framemode
            socket_con.sendCmd('chpara FrameMode %d' % (options.framemode-1))
            res = socket_con.recevieResult()
            # result_message = result_message + res + '\n'
            result_message.append(res)
            if re.search('Set FrameMode', res):
                pass
            else:
                socket_con.closeSocket()
                return [-8]

        # Set coderate value
        if options.coderate:
            print 'coderate %d' % options.coderate
            socket_con.sendCmd('chpara CodeRate %d' % (options.coderate-1))
            res = socket_con.recevieResult()
            # result_message = result_message + res + '\n'
            result_message.append(res)
            if re.search('Set CodeRate', res):
                pass
            else:
                socket_con.closeSocket()
                return [-7]

        # Set carriermode value
        if options.carriermode:
            print 'carriermode %d' % options.carriermode
            socket_con.sendCmd(
                'chpara CarrierMode %d' % (options.carriermode-1))
            res = socket_con.recevieResult()
            result_message.append(res)
            if re.search('Set CarrierMode', res):
                pass
            else:
                socket_con.closeSocket()
                return [-9]
    elif options.std == "custom":
        socket_con.sendCmd('loadfile %s' % options.ts)
        for i in range(5):
            res = socket_con.recevieResult()
            if re.search('Success', res):
                # pass
                break
            else:
                # socket_con.closeSocket()
                time.sleep(1)
                if i == 4:
                    socket_con.closeSocket()
                    # return -3
                    return ['load file fail:', options.ts]
        # result_message = result_message + res + '<br/>'
        result_message.append(res)
        result_message.append(options.ts)
    elif options.std == "mode":
        if options.modulation:
            print 'modulation %d' % options.modulation
            socket_con.sendCmd('chpara Modulation %d' % (options.modulation-1))
            res = socket_con.recevieResult()
            result_message.append(res)
            # result_message = result_message + res + '\n'
            if re.search('Set Modulation', res):
                pass
            else:
                socket_con.closeSocket()
                return [-6]

        # Set modulation value
        if options.framemode:
            print 'framemode %d' % options.framemode
            socket_con.sendCmd(
                'chpara FrameMode %d' % (options.framemode-1))
            res = socket_con.recevieResult()
            # result_message = result_message + res + '\n'
            result_message.append(res)
            if re.search('Set FrameMode', res):
                pass
            else:
                socket_con.closeSocket()
                return [-8]

        # Set coderate value
        if options.coderate:
            print 'coderate %d' % options.coderate
            socket_con.sendCmd(
                'chpara CodeRate %d' % (options.coderate-1))
            res = socket_con.recevieResult()
            # result_message = result_message + res + '\n'
            result_message.append(res)
            if re.search('Set CodeRate', res):
                pass
            else:
                socket_con.closeSocket()
                return [-7]
        if options.carriermode:
            print 'carriermode %d' % options.carriermode
            socket_con.sendCmd(
                'chpara CarrierMode %d' % (options.carriermode-1))
            res = socket_con.recevieResult()
            result_message.append(res)
            if re.search('Set CarrierMode', res):
                pass
            else:
                socket_con.closeSocket()
                return [-9]

    # Play ts
    socket_con.sendCmd('play')
    res = socket_con.recevieResult()
    if re.search('Success', res) or re.search('Already Playing!', res):
        pass
    else:
        socket_con.closeSocket()
        return [-1]
    socket_con.closeSocket()
    return result_message
    # return 0

if __name__ == '__main__':
    r = exec_switch()
    print r

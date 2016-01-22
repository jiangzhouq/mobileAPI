#!/usr/bin/python
# -*- coding: utf-8 -*-
# Description: 多线程有用方法模块
# Create: 2008-8-30
# Author: MK2[fengmk2@gmail.com]

import threading, time
import sys
from werkzeug.wrappers import Request, Response
from threading import Thread
import HttpActionProcessor
class KThread(threading.Thread):
    """A subclass of threading.Thread, with a kill()
    method.
    
    Come from:
    Kill a thread in Python: 
    http://mail.python.org/pipermail/python-list/2004-May/260937.html
    """
    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        self.killed = False
        self.exception = None

    def start(self):
        """Start the thread."""
        self.__run_backup = self.run
        self.run = self.__run      # Force the Thread to install our trace.
        threading.Thread.start(self)

    def __run(self):
        """Hacked run function, which installs the
        trace."""
        sys.settrace(self.globaltrace)
        try:
            self.__run_backup()
        except Exception, e:
            self.exception = e
        self.run = self.__run_backup

    def globaltrace(self, frame, why, arg):
        if why == 'call':
            return self.localtrace
        else:
            return None

    def localtrace(self, frame, why, arg):
        if self.killed:
            if why == 'line':
                raise SystemExit()
        return self.localtrace

    def kill(self):
        self.killed = True


class Timeout(Exception):
    """function run timeout"""
    
def timeout(seconds):
    """超时装饰器，指定超时时间
    若被装饰的方法在指定的时间内未返回，则抛出Timeout异常"""
    def timeout_decorator(func):
        """真正的装饰器"""
        
        def _new_func(oldfunc, result, oldfunc_args, oldfunc_kwargs):
            result.append(oldfunc(*oldfunc_args, **oldfunc_kwargs))
        
        def _(*args, **kwargs):
            result = []
            # create new args for _new_func, because we want to get the func return val to result list
            new_kwargs = { 
                'oldfunc': func,
                'result': result,
                'oldfunc_args': args,
                'oldfunc_kwargs': kwargs
            }
            thd = KThread(target=_new_func, kwargs=new_kwargs)
            thd.start()
            thd.join(seconds)
            alive = thd.isAlive()
            thd.kill() # kill the child thread
            if alive:
                raise Timeout(u'function run too long, timeout %d seconds.' % seconds)
            elif thd.exception is not None:
#                print thd.exception.error_detail
                raise thd.exception
            return result[0]
        _.__name__ = func.__name__
        _.__doc__ = func.__doc__
        return _
    return timeout_decorator

# @timeout(5)
# def method_timeout(seconds, text):
#     print 'start', seconds, text
#     time.sleep(seconds)
#     print 'finish', seconds, text
#     return seconds
    
@timeout(5)
def test_exception():
    raise Exception('test timeout')

@Request.application
def application(request):
    if request.method == 'GET' and len(request.args) >= 1:
        action = request.args.get('action',0)
        if action == 1:
            if len(request.args) == 1:
                t = GetUrlThread(int(action))
                t.start()
                t.join()
                return Response(t.res)
            else:
                return Response('0')
        elif action == 2:
            if len(request.args) == 3:
                username = request.args.get('username', '')
                passwd = request.args.get('passwd', '')
                t = GetUrlThread(int(action), str(username), str(passwd))
                t.start()
                t.join()
                return Response(t.res)
            else:
                return Response('0')
        elif action == 3:
            if len(request.args) == 4:
                email = request.args.get('email', '')
                username = request.args.get('username', '')
                passwd = request.args.get('passwd', '')
                t = GetUrlThread(int(action),str(email), str(username), str(passwd))
                t.start()
                t.join()
                return Response(t.res)
            else:
                return Response('0')
        elif action == 4:
            if len(request.args) == 2:
                email = request.args.get('email', '')
                t = GetUrlThread(int(action),str(email))
                t.start()
                t.join()
                return Response(t.res)
            else:
                return Response('0')
        elif action == 21:
            if len(request.args) == 5:
                access_token = request.args.get('access_token', '')
                key_word = request.args.get('key_word', '')
                begin = request.args.get('begin', 0)
                number = request.args.get('number', 20)
                t = GetUrlThread(int(action), str(access_token), str(key_word), int(begin), int(number))
                t.start()
                t.join()
                return Response(t.res)
            else:
                return Response('0')
        elif action == 22:
            if len(request.args) == 5:
                access_token = request.args.get('access_token', '')
                key_word = request.args.get('key_word', '')
                begin = request.args.get('begin', 0)
                number = request.args.get('number', 20)
                t = GetUrlThread(int(action), str(access_token), str(key_word), int(begin), int(number))
                t.start()
                t.join()
                return Response(t.res)
            else:
                return Response('0')
        elif action == 23:
            if len(request.args) == 5:
                return Response('0')
            else:
                return Response('0')
        elif action == 24:
            if len(request.args) == 5:
                access_token = request.args.get('access_token', '')
                key_word = request.args.get('key_word', '')
                begin = request.args.get('begin', 0)
                number = request.args.get('number', 20)
                t = GetUrlThread(int(action), str(access_token), str(key_word), int(begin), int(number))
                t.start()
                t.join()
                return Response(t.res)
            else:
                return Response('0')
        elif action == 19:
            if len(request.args) == 4:
                order = request.args.get('order', 1)
                begin = request.args.get('begin', 0)
                number = request.args.get('number', 20)
                t = GetUrlThread(int(action), int(order), int(begin), int(number))
                t.start()
                t.join()
                return Response(t.res)
            else:
                return Response('0')
        elif action == 20:
            if len(request.args) == 4:
                order = request.args.get('order', 1)
                begin = request.args.get('begin', 0)
                number = request.args.get('number', 20)
                t = GetUrlThread(int(action), int(order), int(begin), int(number))
                t.start()
                t.join()
                return Response(t.res)
            else:
                return Response('0')
        elif action == 5:
            if len(request.args) == 2:
                uid = request.args.get('uid', -1)
                t = GetUrlThread(int(action), int(uid))
                t.start()
                t.join()
                return Response(t.res)
            else:
                return Response('0')
        elif action == 7:
            if len(request.args) == 4:
                uid = request.args.get('uid', -1)
                begin = request.args.get('begin', 0)
                number = request.args.get('number', 20)
                t = GetUrlThread(int(action), int(uid), int(begin), int(number))
                t.start()
                t.join()
                return Response(t.res)
            else:
                return Response('0')
        elif action == 8:
            if len(request.args) == 2:
                uid = request.args.get('uid', -1)
                t = GetUrlThread(int(action), int(uid))
                t.start()
                t.join()
                return Response(t.res)
            else:
                return Response('0')
    else:
        return Response('0')


class GetUrlThread(Thread):
    def __init__(self, action, arg1, arg2, arg3, arg4):
        self.action = action 
        self.res = ''
        self.uid = 0
        self.access_token = ''
        self.username = ''
        self.passwd = ''
        self.email = ''
        self.key_word = ''
        self.begin = 0
        self.number = 20
        self.order = 1
        if action == 1:

        elif action ==2:
            self.username = arg1
            self.passwd = arg2
        elif action ==3:
            self.email = arg1
            self.username = arg2
            self.passwd = arg3
        elif action ==4:
            self.email = arg1
        elif action ==21:
            self.access_token = arg1
            self.key_word = arg2
            self.begin = arg3
            self.number = arg4
        elif action ==22:
            self.access_token = arg1
            self.key_word = arg2
            self.begin = arg3
            self.number = arg4
        elif action ==23:
            self.access_token = arg1
            self.key_word = arg2
            self.begin = arg3
            self.number = arg4
        elif action ==24:
            self.access_token = arg1
            self.key_word = arg2
            self.begin = arg3
            self.number = arg4
        elif action ==19:
            self.order = arg1
            self.begin = arg2
            self.number = arg3
        elif action ==20:
            self.order = arg1
            self.begin = arg2
            self.number = arg3
        elif action ==5:
            self.uid = arg1
        elif action ==7:
            self.uid = arg1
            self.begin = arg2
            self.number = arg3
        elif action ==8: 
            self.uid = arg1

        super(GetUrlThread, self).__init__()
    @timeout(20) 
    def run(self):
        print 'hello:',self.action
        self.res = '400'        
        if action == 1:
            self.res = HttpActionProcessor.process1(self.action)
        elif action ==2:
            self.res = HttpActionProcessor.process2(self.action, self.username, self.res)
        elif action ==3:
            self.res = HttpActionProcessor.process3(self.action, self.email, self.username, self.passwd)
        elif action ==4:
            self.res = HttpActionProcessor.process4(self.action, self.email)
        elif action ==21:
            self.res = HttpActionProcessor.process21(self.action, self.access_token, self.key_word, self.begin, self.number)
        elif action ==22:
            self.res = HttpActionProcessor.process22(self.action, self.access_token, self.key_word, self.begin, self.number)
        elif action ==23:
            self.res = HttpActionProcessor.process23(self.action, self.access_token, self.key_word, self.begin, self.number)
        elif action ==24:
            self.res = HttpActionProcessor.process24(self.action, self.access_token, self.key_word, self.begin, self.number)
        elif action ==19:    
            self.res = HttpActionProcessor.process19(self.action, self.order, self.begin, self.number)
        elif action ==20:
            self.res = HttpActionProcessor.process20(self.action, self.order,  self.begin, self.number)
        elif action ==5:
            self.res = HttpActionProcessor.process5(self.action, self.uid)           
        elif action ==7:        
            self.res = HttpActionProcessor.process7(self.action, self.uid, self.begin, self.number)
        elif action ==8: 
            self.res = HttpActionProcessor.process8(self.action, self.uid)
        

if __name__ == '__main__':
    try:
        test_exception()
    except Exception, e:
        assert 'test timeout' == str(e)
    from werkzeug.serving import run_simple    
    run_simple('0.0.0.0', 12343, application)

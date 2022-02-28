import sys
import time
from enum import Enum

class State(Enum):
    none = 0
    Symbol = 1
    Sublist = 2

class SExpressionReader:
    
    def __init__(self, stream, length):
        if stream == None or stream == State.none:
            raise(BaseException('stream'))
        if length <= 0:
            raise(BaseException('Length ' + str(length) + ' Must be greater than zero.'))
        self._stream = stream
        self.length  = length
        self._pushed_char = -1
        self._rubbish = [State.none for i in range(1024)]
    
    def try_read_char(self):

        if self._pushed_char != -1:
            c = self._pushed_char
            self._pushed_char = -1
            return True, c

        if self._bytes_read == self.length:
            c = 0x00
            return False, c
        i = self._stream.recv(1)
        while i == -1:

            time.sleep(1)
        self._bytes_read += 1
        c = str(i)
        return True, c
    
    def push(self):
        if self._pushed_char != -1:
            raise(BaseException('A pushed character already exists'))
        return self._pushed_char


    def skip_white_space(self):
        while True:
            c = self.try_read_char()
            if not c[0]:
                return
            if not c[1].isspace():
                self.push(c[1])
                return 

    def skip(self,count):
        open_brace_count = 0
        state = State.none

        while True:
            c = self.try_read_char()

            if not c[0]:
                return False
            if c[1] == '(':
                if state == State.none:
                    state = State.Sublist
                    open_brace_count += 1
                    break
                elif state == State.Symbol:
                    count -= 1
                    if count ==0:
                        self.push(c[1])
                        return True
                    state = State.Sublist
                    open_brace_count += 1
                    break
                elif state == State.Sublist:
                    open_brace_count += 1
                    break

            elif c == ")":
                if state == State.none:
                    self.push(c)
                    return False
                elif state == State.Symbol:
                    count -= 1
                    if count == 0:
                        self.push(c[1])
                    self.push(c[1])
                    return False
                elif state == State.Sublist:
                    assert open_brace_count > 0
                    open_brace_count -= 1
                    if open_brace_count == 0:
                        count -= 1
                        if count == 0:
                            return True
                        state = State.none
                    break

            elif c[1].isspace():
                if state == State.none:
                    break
                elif state == State.Symbol:
                    count -= 1
                    if count == 0:
                        return True
                    state = State.none
                    break
                elif state == State.Sublist:
                    break
            
            else:
                if state == State.none:
                    state = State.Symbol
                    break
                elif state == State.Symbol:
                    break
                elif state == State.Sublist:
                    break
                
    def In(self, level_count):
        while level_count > 0:
            c = self.try_read_char()
            if not c[0]:
                return False
            if c[1] == '(':
                level_count -= 1
        return True
    
    def out(self, level_count):
        while level_count > 0:
            c = self.try_read_char()
            if not c[0]:
                return False
            if c[1] == ")":
                level_count -= 1
            elif c[1] == "(":
                level_count += 1
        return True

    def take(self):
        open_brace_count = 0
        self.skip_white_space()

        sb = str()

        while True:
            c = self.try_read_char()
            if not c[0]:
                return sb
            if c[1] == ')':
                if open_brace_count == 0:
                    self.push(c[1])
                    return sb

                open_brace_count -= 1

                if open_brace_count == 0:
                    sb += c[1]
                    return sb
                
            elif c[1] == "(":
                open_brace_count += 1
            elif c[1].isspace():
                if open_brace_count == 0:
                    return sb
            sb += c[1]

    def skip_to_end(self):
        while self._bytes_read < self.length:
            diff = min(1024,self.length - self._bytes_read)
            read = self._stream(self._rubbish, 0, diff)
            self._bytes_read += read
        assert self._bytes_read == self.length
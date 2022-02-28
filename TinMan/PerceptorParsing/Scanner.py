import sys
from PerceptorParsing import switch_case
import io,math

class Token:
    def __init__(self):
        self.kind = int()
        self.pos = int()
        self.col = int()
        self.line = int()
        self.val = str()
        self.next = None
    
class Buffer:
    EOF = sys.maxsize + 1

class StringBuffer:

    def __init__(self, str):
        self.string = str
        self.pos =0

    def read(self):
        if self.pos == len(self.string):
            return Buffer.EOF
        self.pos += 1
        return self.string[self.pos-1]
    
    def peek(self):
        return self.string[self.pos]

class StreamBuffer:
    min_buffer_length = 1024
    max_buffer_length = 1024 * 64
    '''
    buf = []
    buf_start = int()
    file_len = int()
    buf_pos = int()
    stream = io.StringIO()
    '''
    def __init__(self, s):
        self.stream = s
        if self.stream.seekable():
            self.file_len = len(self.stream)
            self.buf_len = math.min(self.file_len, StreamBuffer.max_buffer_length)
            self.buf_start = 2147483647
        else:
            self.file_len, self.buf_len,self.buf_start = 0,0,0
         
        if self.buf_len > 0:
            self.buf = [None for i in range(self.buf_len)]
        else:
            self.buf = [None for i in range(StreamBuffer.min_buffer_length)]
        
        if self.file_len > 0:
            self.pos = 0
        else:
            self.buf_pos = 0
        
    def read(self):
        if self.buf_pos < self.buf_len:
            self.buf_pos += 1
            return self.buf[self.buf_pos-1]
        elif self.pos < self.file_len:
            self.buf_pos  = self.pos
            self.buf_pos += 1
            return self.buf[self.buf_pos-1]
        elif not self.stream and not self.stream.seekable() and self.read_next_stream_chunk() > 0:
            self.buf_pos += 1
            return self.buf[self.buf_pos-1]
        else:
            return Buffer.EOF
        
    def peek(self):
        self.curpos = self.pos
        ch = self.read()
        self.pos = self.curpos
        return ch
    
    def _pos_getter(self):
        return self.buf_pos + self.buf_start
    
    def _pos_setter(self,value):
        if value >= self.file_len and not self.stream and not self.stream.seekable():
            while value >= self.file_len and self.read_next_stream_chunk() > 0:
                continue
        if value < 0 or value > self.file_len:
            raise BaseException('Buffer out of bounds access, position: ' + value)
        if value >= self.buf_start and value < self.buf_start + self.buf_len:
            self.buf_pos = value - self.buf_start
        elif not self.stream:
            self.stream.seek(value)
            self.buf_len = self.stream.read(self.buf,0,len(self.buf))
            self.buf_start = value
            self.buf_pos = 0
        else:
            self.buf_pos = self.file_len - self.buf_start
    
    def read_next_stream_chunk(self):
        free = len(self.buf) - self.buf_len
        if free == 0:
            new_buf = [None for i in self.buf_len*2]
        for i in range(len(self.buf)):
            new_buf[i] = self.buf[i]
        read = self.stream.Read(self.buf, self.buf_len, free)
        if read > 0:
            self.file_len, self.buf_len = self.buflen + read, self.buflen + read
            return read
        return 0

class Scanner:
    EOL = '\n'
    eof_sym = 0
    max_t = 50
    no_sym = 50

    def __init__(self, *args):
        self.t = Token()
        self.pt = Token()
        self.tokens = Token()
        self.start = dict()
        for i in range(48,58):
            self.start[i] = 2
        for i in range(65,91):
            self.start[i] = 5
        for i in range(97,122):
            self.start[i] = 5
        self.start[45], self.start[40], self.start[41],self.start[Buffer.EOF] = 1,53,9,-1
        self.tval = [None for i in range(128)]
        self.tlen = int()
        if args:
            if type(args[0]) == str:
                self.buffer = StringBuffer(args[0])
                self.init()
            elif type(args[0]) == StringBuffer or type(args[0]) == StreamBuffer:
                self.buffer = args[0]
                self.init()

    def init(self):
        self.pos = -1
        self.line = 1
        self.col = 0
        self.old_eols = 0
        self.next_ch()

        self.pt = Token()
        self.tokens = Token()

    def next_ch(self):
        if self.old_eols >0:
            self.ch = Scanner.EOL
            self.old_eols -= 1
        else:
            self.pos = self.buffer.pos
            self.ch = self.buffer.read()
            self.col += 1
            if self.ch == '\r' and self.buffer.Peek() != '\n':
                self.ch = Scanner.EOL
            if self.ch == Scanner.EOL:
                self.line+= 1
                col = 0

    def add_ch(self):
        if self.tlen >= len(self.tval):
            new_buf = [None for i in range(2*len(self.tval))]
            for i in range(len(self.tval)):
                new_buf[i] = self.tval[i]
                self.tval = new_buf
        if self.ch != Buffer.EOF:
            self.tval[self.tlen] = self.ch
            self.tlen += 1
            self.next_ch()
        
    def check_literal(self):
        mapper = {'nan':3,'now':8,'left':12,'right':13,'t':14,'pm':15,'n':17,'rt':18,'a':20,'ax':22, 'ax1':24, 'ax2':25, 'val':27, 'c':29, 'f':30, 'temp':32, 
        'battery': 33, 'F1L': 35, 'F2L': 36, 'F1R':37, 'F2R':38, 'G1L': 39, 'G2L': 40, 'G1R': 41, 'G2R':42, 'B':43, 'P':44, 'mypos':46, 'L':47, 'self':49}
        self.t.kind = mapper[self.t.val]
        
    def next_token(self):
        while self.ch == ' ':
            self.next_ch()
        self.rec_kind = Scanner.no_sym
        self.rec_end = self.pos
        self.t = Token()
        self.t.pos = self.pos
        self.t.col = self.col
        self.t.line = self.line
        if not self.start.get(self.ch, int()):
            state = 0
        else:
            state = self.start[self.ch]
        self.tlen = 0
        self.add_ch()
        #kwargs = {self : self, t : self.t,eof_sym : 0, max_t : 50, no_sym : 50}
        return switch_case.SwitchCase(state).check(self)

    def set_scanner_behind_t(self):
        self.buffer.pos = self.t.pos
        self.next_ch()
        self.line = self.t.line
        self.col = self.t.col
        for i in range(self.tlen):
            self.next_ch()
    
    '''
    Token Methods left
    '''

    def scan(self):
        if self.tokens.next == None:
            return self.next_token()
        else:
            self.tokens = self.tokens.next
            self.pt = self.tokens
            return self.tokens
        
    def peek(self):
        while True:
            if self.pt.next == None:
                self.pt.next = self.next_token()
            self.pt = self.pt.next
            if not self.pt.kind > self.max_t:
                break
        return self.pt

    def reset_peek(self):
        self.pt = self.tokens

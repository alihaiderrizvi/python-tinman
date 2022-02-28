from sty import fg, bg, ef, rs

class Log:

    _instance = None

    def create():
        if Log._instance == None:
            Log._instance = Log()
        
        return Log._instance
    
    def __init__(self):
        pass
    
    def verbose(self,m):
        self.write_console(m, fg.gray, bg.black)

    def info(self,m):
        self.write_console(m, fg.white, bg.black)

    def warn(self,m):
        self.write_console(m, fg.magenta, bg.black)
    
    def error(self,m,ex=None):
        self.write_console(m + '\n' + str(ex), fg.white, bg.red)

    def write_console(self, m, foreground, background):
        print(foreground + background + m)

        


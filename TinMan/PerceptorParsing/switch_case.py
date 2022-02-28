class SwitchCase:
    def __init__(self, num):
        self.state = num
    def check(self,args):
        num = self.state
        
        string = "SwitchCase.case_" + str(num).replace("-","_") + "(self = args, t = args.t, eof_sym = 0, max_t = 50, no_sym = 50)"
        out = eval(string)
        if out == None:
            args.t.val = str(args.tval)
            
            return args.t
        
        return out
    
    def case__1(**kwargs):
        kwargs['t'].kind = kwargs['eof_sym']
        
    
    def case_0(**kwargs):
        if kwargs['self'].rec_kind != kwargs['no_sym']:
            kwargs['self'].tlen = kwargs['self'].rec_end - kwargs['t'].pos
            kwargs['self'].set_scanner_behind()
        kwargs['t'].kind = kwargs['self'].rec_kind
        
    
    def case_1(**kwargs):
        if (kwargs['self'].ch >= '0' and kwargs['self'].ch <= "9"):
            kwargs['self'].add_ch()
            SwitchCase.case_2(kwargs = kwargs)
        else:
            SwitchCase.case_0(kwargs = kwargs)
    
    def case_2(**kwargs):
        kwargs['self'].rec_end = kwargs['self'].pos
        kwargs['self'].rec_kind = 1
        if (kwargs['self'].ch >= '0' and kwargs['self'].ch <= '9'):
            kwargs['self'].add_ch()
            SwitchCase.case_2(kwargs = kwargs)
        elif kwargs['self'].ch == '.':
            kwargs['self'].add_ch()
            SwitchCase.case_3(kwargs = kwargs)
        else:
            kwargs['t'].kind = 1
            
    
    def case_3(**kwargs):
        if kwargs['self'].ch >= '0' and kwargs['self'].ch <= '9':
            kwargs['self'].add_ch()    
            SwitchCase.case_4(kwargs = kwargs)
        else:
            SwitchCase.case_0(kwargs = kwargs)

    def case_4(**kwargs):
        kwargs['self'].rec_end = kwargs['self'].pos
        kwargs['self'].rec_kind = 1
        if kwargs['self'].ch >= '0' and kwargs['self'].ch <= '9':
            kwargs['self'].add_ch()
            SwitchCase.case_4(kwargs = kwargs)
        else:
            kwargs['t'].kind = 1
            
    def case_5(**kwargs):
        kwargs['self'].rec_end = kwargs['self'].pos
        kwargs['self'].rec_kind = 2
        if kwargs['self'].ch == '-' or (kwargs['self'].ch >= '0' and kwargs['self'].ch <= '9') or (kwargs['self'].ch >= 'A' and kwargs['self'].ch <= 'Z') or (kwargs['self'].ch >= 'a' and kwargs['self'].ch <= 'z'):
            kwargs['self'].add_ch()
            SwitchCase.case_5(kwargs = kwargs)
        else:
            kwargs['t'].kind = 2
            kwargs['t'].val = str(kwargs['self'].tval)
            kwargs['self'].check_literal()
            return kwargs['t']
        
    def case_6(**kwargs):
        if kwargs['self'].ch == 'o':
            kwargs['self'].add_ch()
            SwitchCase.case_7(kwargs = kwargs)
        else:
            SwitchCase.case_0(kwargs= kwargs)
    
    def case_7(**kwargs):
        if kwargs['self'].ch == 'l':
            kwargs['self'].add_ch()
            SwitchCase.case_8(kwargs= kwargs)
        else:
            SwitchCase.case_0(kwargs= kwargs)

    def case_8(**kwargs):
        kwargs['t'].kind = 4
        
    
    def case_9(**kwargs):
        kwargs['t'].kind = 5
        
    
    def case_10(**kwargs):
        if kwargs['self'].ch == 'm':
            kwargs['self'].add_ch()
            SwitchCase.case_11(kwargs= kwargs)
        else:
            SwitchCase.case_0(kwargs= kwargs)
    
    def case_11(**kwargs):
        if kwargs['self'].ch == 'e':
            kwargs['self'].add_ch()
            SwitchCase.case_12(kwargs= kwargs)
        else:
            SwitchCase.case_0(kwargs= kwargs)
    
    def case_12(**kwargs):
        kwargs['t'].kind = 6
        
    
    def case_13(**kwargs):
        kwargs['t'].kind = 9
    
    def case_14(**kwargs):
        if kwargs['self'].ch == 'n':
            kwargs['self'].add_ch()
            SwitchCase.case_15(kwargs= kwargs)
        else:
            SwitchCase.case_0(kwargs= kwargs)
    
    def case_15(**kwargs):
        if kwargs['self'].ch == 'u':
            kwargs['self'].add_ch()
            SwitchCase.case_16(kwargs= kwargs)
        else:
            SwitchCase.case_0(kwargs= kwargs)
    
    def case_16(**kwargs):
        if kwargs['self'].ch == 'm':
            kwargs['self'].add_ch()
            SwitchCase.case_17(kwargs= kwargs)
        else:
            SwitchCase.case_0(kwargs= kwargs)
    
    def case_17(**kwargs):
        kwargs['t'].kind = 10
        
    
    def case_18(**kwargs):
        if kwargs['self'].ch == 'a':
            kwargs['self'].add_ch()
            SwitchCase.case_19(kwargs= kwargs)
        else:
            SwitchCase.case_0(kwargs= kwargs)
    
    def case_19(**kwargs):
        if kwargs['self'].ch == 'm':
            kwargs['self'].add_ch()
            SwitchCase.case_20(kwargs= kwargs)
        else:
            SwitchCase.case_0(kwargs= kwargs)
    
    def case_20(**kwargs):
        kwargs['t'].kind = 11
        
    
    def case_21(**kwargs):
        if kwargs['self'].ch == 'R':
            kwargs['self'].add_ch()
            SwitchCase.case_22(kwargs= kwargs)
        else:
            SwitchCase.case_0(kwargs= kwargs)
    
    def case_22(**kwargs):
        kwargs['t'].kind = 16
        
    
    def case_23(**kwargs):
        if kwargs['self'].ch == 'C':
            kwargs['self'].add_ch()
            SwitchCase.case_24(kwargs= kwargs)
        else:
            SwitchCase.case_0(kwargs= kwargs)
    
    def case_24(**kwargs):
        kwargs['t'].kind = 19
            
    def case_25(**kwargs):
        if kwargs['self'].ch == 'J':
            kwargs['self'].add_ch()
            SwitchCase.case_26(kwargs= kwargs)
        else:
            SwitchCase.case_0(kwargs= kwargs)
    
    def case_26(**kwargs):
        kwargs['t'].kind = 21
        

    def case_27(**kwargs):
        if kwargs['self'].ch == 'J':
            kwargs['self'].add_ch()
            SwitchCase.case_28(kwargs= kwargs)
        else:
            SwitchCase.case_0(kwargs= kwargs)
    
    def case_28(**kwargs):
        kwargs['t'].kind = 23
        
    
    def case_29(**kwargs):
        if kwargs['self'].ch == 'C':
            kwargs['self'].add_ch()
            SwitchCase.case_30(kwargs= kwargs)
        else:
            SwitchCase.case_0(kwargs= kwargs)
    
    def case_30(**kwargs):
        if kwargs['self'].ch == 'H':
            kwargs['self'].add_ch()
            SwitchCase.case_31(kwargs= kwargs)
        else:
            SwitchCase.case_0(kwargs= kwargs)
    
    def case_31(**kwargs):
        kwargs['t'].kind = 26
        
    
    def case_32(**kwargs):
        if kwargs['self'].ch == 'R':
            kwargs['self'].add_ch()
            SwitchCase.case_33(kwargs= kwargs)
        else:
            SwitchCase.case_0(kwargs= kwargs)
    
    def case_33(**kwargs):
        if kwargs['self'].ch == 'P':
            kwargs['self'].add_ch()
            SwitchCase.case_34(kwargs= kwargs)
        else:
            SwitchCase.case_0(kwargs= kwargs)
    
    def case_34(**kwargs):
        kwargs['t'].kind = 28
        
    
    def case_35(**kwargs):
        if kwargs['self'].ch == 'e':
            kwargs['self'].add_ch()
            SwitchCase.case_36(kwargs= kwargs)
        else:
            SwitchCase.case_0(kwargs= kwargs)
    
    def case_36(**kwargs):
        if kwargs['self'].ch == 'n':
            kwargs['self'].add_ch()
            SwitchCase.case_37(kwargs= kwargs)
        else:
            SwitchCase.case_0(kwargs= kwargs)

    def case_37(**kwargs):
        if kwargs['self'].ch == 't':
            kwargs['self'].add_ch()
            SwitchCase.case_38(kwargs= kwargs)
        else:
            SwitchCase.case_0(kwargs= kwargs)
    
    def case_38(**kwargs):
        if kwargs['self'].ch == 'S':
            kwargs['self'].add_ch()
            SwitchCase.case_39(kwargs= kwargs)
        else:
            SwitchCase.case_0(kwargs= kwargs)
    
    def case_39(**kwargs):
        if kwargs['self'].ch == 't':
            kwargs['self'].add_ch()
            SwitchCase.case_40(kwargs= kwargs)
        else:
            SwitchCase.case_0(kwargs= kwargs)
    
    def case_40(**kwargs):
        if kwargs['self'].ch == 'a':
            kwargs['self'].add_ch()
            SwitchCase.case_41(kwargs= kwargs)
        else:
            SwitchCase.case_0(kwargs= kwargs)
    
    def case_41(**kwargs):
        if kwargs['self'].ch == 't':
            kwargs['self'].add_ch()
            SwitchCase.case_42(kwargs= kwargs)
        else:
            SwitchCase.case_0(kwargs= kwargs)
    
    def case_42(**kwargs):
        if kwargs['self'].ch == 'e':
            kwargs['self'].add_ch()
            SwitchCase.case_43(kwargs= kwargs)
        else:
            SwitchCase.case_0(kwargs= kwargs)
    
    def case_43(**kwargs):
        kwargs['t'].kind = 31
        
    
    def case_44(**kwargs):
        if kwargs['self'].ch == 'e':
            kwargs['self'].add_ch()
            SwitchCase.case_45(kwargs= kwargs)
        else:
            SwitchCase.case_0(kwargs= kwargs)
    
    def case_45(**kwargs):
        if kwargs['self'].ch == 'e':
            kwargs['self'].add_ch()
            SwitchCase.case_46(kwargs= kwargs)
        else:
            SwitchCase.case_0(kwargs= kwargs)
    
    def case_46(**kwargs):
        kwargs['t'].kind = 34
        
    
    def case_47(**kwargs):
        if kwargs['self'].ch == 'd':
            kwargs['self'].add_ch()
            SwitchCase.case_48(kwargs= kwargs)
        else:
            SwitchCase.case_0(kwargs= kwargs)
    
    def case_48(**kwargs):
        kwargs['t'].kind = 45
        
    
    def case_49(**kwargs):
        if kwargs['self'].ch == 'e':
            kwargs['self'].add_ch()
            SwitchCase.case_50(kwargs= kwargs)
        else:
            SwitchCase.case_0(kwargs= kwargs)
    
    def case_50(**kwargs):
        if kwargs['self'].ch =='a':
            kwargs['self'].add_ch()
            SwitchCase.case_51(kwargs= kwargs)
        else:
            SwitchCase.case_0(kwargs= kwargs)
    
    def case_51(**kwargs):
        if kwargs['self'].ch == 'r':
            kwargs['self'].add_ch()
            SwitchCase.case_52(kwargs= kwargs)
        else:
            SwitchCase.case_0(kwargs= kwargs)
    
    def case_52(**kwargs):
        kwargs['t'].kind = 48
        

    def case_53(**kwargs):
        kwargs['self'].rec_end = kwargs['self'].pos
        kwargs['self'].rec_kind = 7
        if kwargs['self'].ch == 'p':
            kwargs['self'].add_ch()
            SwitchCase.case_6(kwargs= kwargs)
        elif kwargs['self'].ch == 't':
            kwargs['self'].add_ch()
            SwitchCase.case_54(kwargs= kwargs)
        elif kwargs['self'].ch == 'G':
            kwargs['self'].add_ch()
            SwitchCase.case_55(kwargs= kwargs)
        elif kwargs['self'].ch == 'u':
            kwargs['self'].add_ch()
            SwitchCase.case_14(kwargs= kwargs)
        elif kwargs['self'].ch == 'A':
            kwargs['self'].add_ch()
            SwitchCase.case_56(kwargs= kwargs)
        elif kwargs['self'].ch == 'H':
            kwargs['self'].add_ch()
            SwitchCase.case_25(kwargs= kwargs)
        elif kwargs['self'].ch == 'U':
            kwargs['self'].add_ch()
            SwitchCase.case_27(kwargs= kwargs)
        elif kwargs['self'].ch == 'T':
            kwargs['self'].add_ch()
            SwitchCase.case_29(kwargs= kwargs)
        elif kwargs['self'].ch == 'F':
            kwargs['self'].add_ch()
            SwitchCase.case_32(kwargs= kwargs)
        elif kwargs['self'].ch == 'S':
            kwargs['self'].add_ch()
            SwitchCase.case_44(kwargs= kwargs)
        elif kwargs['self'].ch == 'i':
            kwargs['self'].add_ch()
            SwitchCase.case_47(kwargs= kwargs)
        elif kwargs['self'].ch == 'h':
            kwargs['self'].add_ch()
            SwitchCase.case_49(kwargs= kwargs)
        else:
            kwargs['t'].kind = 7
            
    
    def case_54(**kwargs):
        if kwargs['self'].ch == 'i':
            kwargs['self'].add_ch()
            SwitchCase.case_10(kwargs= kwargs)
        elif kwargs['self'].ch == 'e':
            kwargs['self'].add_ch()
            SwitchCase.case_18(kwargs= kwargs)
        else:
            SwitchCase.case_0(kwargs= kwargs)
    
    def case_55(**kwargs):
        if kwargs['self'].ch == 'S':
            kwargs['self'].add_ch()
            SwitchCase.case_13(kwargs= kwargs)
        elif kwargs['self'].ch == 'Y':
            kwargs['self'].add_ch()
            SwitchCase.case_21(kwargs= kwargs)
        else:
            SwitchCase.case_0(kwargs= kwargs)
    
    def case_56(**kwargs):
        if kwargs['self'].ch == 'C':
            kwargs['self'].add_ch()
            SwitchCase.case_23(kwargs= kwargs)
        elif kwargs['self'].ch == 'g':
            kwargs['self'].add_ch()
            SwitchCase.case_35(kwargs= kwargs)
        else:
            SwitchCase.case_0(kwargs= kwargs)
    
    






            
    
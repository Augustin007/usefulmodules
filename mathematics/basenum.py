'''
basenum

A basenum class, can hold numbers in a any counting system

LICENSE PLATAFORMS and INSTALLATION:
This is a section of usefulpy. See usefulpy.__init__ and usefulpy license
file

RELEASE NOTES:
1
 1.1
  Version 1.1.1
   Basenum class can hold a number in a certain counting system
  Version 1.1.2
   Some bug fixes and implementation of __pow__
'''
##UPDATED TO: Usefulpy 1.2.1
##PREREQUISITE1.2.2: basenum 1.2.1

### INFO ###
__version__ = '1.1.2'
__author__ = 'Austin Garcia'
__package__ = 'usefulpy.mathematics'

### IMPORTS ###
from .. import validation as _validation
#from .PrimeComposite import *


### BASENUM ###
def fromNumBaseFormat(text):
    '''return a basenum from text:
>>> fromNumBaseFormat('14_5')
14₅
>>> '''
    if '_' in text:
        index = text.find('_')
        num, base = text[:index],text[index+1:]
        if not base.isdigit(): raise ValueError('This could not be converted into a basenum object')
        return basenum(num, int(base))
    else:
        if _validation.is_float(text): return eval(text)
        else: raise ValueError('This could not be converted into a basenum object')

class basenum(object):
    '''Stores numbers of different bases'''
    base:int
    num:str
    floatpart:str
    Negative:bool
    ### INITIALIZING ###
    def __new__(cls, strint, base = 10):
        '''__new__ for basenum class:
>>> x = basenum('3a2', 16)
>>> x
3a2₁₆
>>> y = x/2
>>> y
1d1₁₆
>>> float(x)
930.0
>>> int(y)
465
>>> '''
        self = super(basenum, cls).__new__(cls)
        
        if 'e' in strint and base == 10:
            nindex = strint.index('e')
            before = strint[:nindex]
            sn = strint[nindex+1]
            try: after = int(strint[nindex+2:])
            except: raise ValueError('This is not a base', str(base), 'number')
            if sn == '-':
                if '.' in before:
                    nlen = before.index('.')
                    before = before[:nlen]+before[nlen+1:]
                else:
                    nlen = len(before)
                strint = '0.'+('0'*(after-nlen))+before
            elif sn == '+':
                if '.' in before:
                    nlen = before.rindex('.')
                    before = before[:-(nlen+1)]+before[-nlen:]
                else: nlen = 0
                strint = before + '0'*(after-nlen)
        if base not in range(0x2, 0x25): raise ValueError('This base is not within the range(0x2, 0x25)')
        if base < 10: maximum = str(base)
        else: maximum = chr(ord('a')+(base-10))
        self.Negative = False
        while strint[0] == '-':
            self.Negative = not(self.Negative)
            strint = strint[1:]
        for s in strint:
            if s >= maximum: raise ValueError('This is not a base', str(base), 'number')
            elif s == '.': pass
            elif ord(s)<ord('0'): raise ValueError('This is not a base', str(base), 'number')
            elif ord(s)>ord('9') and ord(s)<ord('a'):raise ValueError('This is not a base', str(base), 'number')
        while strint.startswith('0') and strint != '0': strint = strint[1:]
        if '.' in strint:
            if strint.count('.')!=1: raise ValueError('Too many "."s')
            else:
                index = strint.find('.')
                self.floatpart = strint[index+1:]
                strint = strint[:index]
                while self.floatpart.endswith('0'):self.floatpart = self.floatpart[:-1]
        else: self.floatpart = ''
        self.base = base
        self.num = strint
        return self

    ### Conversions ###
    def __float__(self):
        '''return float(self)'''
        decimal, num, base, floatpart = 0, self.num, self.base, self.floatpart
        exponent = len(num)-1
        num = (num+floatpart)
        for digit in num:
            if digit >= 'a': digit = str(ord(digit)-ord('a')+10)
            decimal += (float(digit)*base**exponent)
            exponent-=1
        if self.Negative: decimal = 0-decimal
        return float(decimal)

    def __int__(self):
        '''return int(self)'''
        return int(self.num, self.base)

    def __str__(self):
        '''return str(self)'''
        SUB = str.maketrans('0123456789', '₀₁₂₃₄₅₆₇₈₉')
        if self.base != 10: base = str(self.base).translate(SUB)
        else: base = ''
        num = str(self.num)
        if self.floatpart != '': num += '.' + self.floatpart
        if self.Negative: num = '-' + num
        return(num+base)

    def convert(self, base):
        '''return a basenum of another base with same value'''
        if base not in range(0x2, 0x25): raise ValueError('This base is not within the range(0x2, 0x25)')
        if base == self.base: return self
        number = abs(float(self))
        if number == 0: return basenum('0', base)
        if base == 10: return basenum(str(_validation.trynumber(self)))
        strint, n = "", 0
        if number >= 1:
            while (base**n)<= number: n+=1
            n-=1
        while number > 0:
            if n == -1: strint += '.'
            elif n < -16: break
            value = base**n
            digit = int(number//value)
            strdigit = str(digit)
            if digit >= 10: strdigit = chr(ord('a')+(digit-10))
            strint += strdigit
            number -= (value*digit)
            n-=1
        if n >= 0: strint += '0'*(n+1)
        if self.Negative: strint = '-'+strint
        return basenum(strint, base)

    ### ARITHMETIC OPERATIONS ###
    def __add__(self, other):
        '''return self+other'''
        decanum = float(self) + float(other)
        floatbase = basenum(str(decanum))
        basenumb = (floatbase.convert(self.base))
        return basenumb

    def __radd__(self, other):
        '''return self+other'''
        return _validation.tryint(self+float(other))

    def __mul__(self, other):
        '''return self*other'''
        decanum = float(self) * float(other)
        floatbase = basenum(str(decanum))
        basenumb = (floatbase.convert(self.base))
        return basenumb

    def __pow__(self, other):
        '''return self**other'''
        decanum = float(self)**float(other)
        floatbase = basenum(str(decanum))
        basenumb = (floatbase.convert(self.base))
        return basenumb

    def __rpow__(self, other):
        '''return self**other'''
        return _validation.tryint(other**float(self))

    def __rmul__(other, self):
        '''return self*other'''
        return _validation.tryint(float(self)*float(other))

    def __sub__(self, other):
        '''return self-other'''
        decanum = float(self) - float(other)
        floatbase = basenum(str(decanum))
        basenumb = (floatbase.convert(self.base))
        return basenumb

    def __rsub__(other, self):
        '''return self-other'''
        return _validation.tryint(float(self)-float(other))

    def __truediv__(self, other):
        '''return self/other'''
        decanum = float(self)/float(other)
        floatbase = basenum(str(decanum))
        basenumb = (floatbase.convert(self.base))
        return basenumb

    def __rtruediv__(other, self):
        '''return self/other'''
        return float(self)/float(other)

    def __abs__(self):
        '''return the abs(self)'''
        return abs(float(self))

    def floor(self):
        if not self.Negative:
            return int(self)
        else:
            if _validation.is_integer(self):
                return int(self)
            return int(self)-1
        
    def ceil(self):
        if self.Negative:
            return int(self)
        else:
            if _validation.is_integer(self):
                return int(self)
            return int(self)+1

##TODO: Fix this area.
    def __floordiv__(self, other):
        self = self/other
        return floor(self)

    def __rfloordiv__(self, other):
        self = other/self
        return floor(self)

    def __gcd__(self, other, /):
        return findgcd(self, other)

    def __rgcd__(self, other, /):
        return self.__gcd__(other)
    

    ### COMPARISON OPERATOR ###

    def __lt__(self, other):
        '''return self<other'''
        return float(self)<float(other)

    def __gt__(self, other):
        '''return self>other'''
        return float(self)>float(other)

    def __le__(self, other):
        '''return self<=other'''
        return float(self)<=float(other)

    def __ge__(self, other):
        '''return self>=other'''
        return float(self)>=float(other)

    def __eq__(self, other):
        '''return self==other'''
        try: return float(self)==float(other)
        except: return False

    def __ne__(self, other):
        '''return self!=other'''
        try: return float(self)!=float(other)
        except: return True

    def __repr__(self):
        '''IDLE representation'''
        return str(self)

#eof

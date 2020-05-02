from typing import Union, Text, Type, Optional

from fastutils import strutils


class AdvString(str):
    def __init__(self, value: str):
        str.__init__(value)

    def hash(self):
        return AdvInteger(self.__hash__())

    def contains(self, value: str):
        return AdvBoolean(self.__contains__(value))

    def size(self):
        return AdvInteger(self.__sizeof__())
    
    def to_bool(self):
        return AdvBoolean(bool(self))
    
    def to_integer(self):
        return AdvInteger(int(self))
    
    def to_float(self):
        return AdvFloat(float(self))
    
    def to_bytes(self):
        return AdvBytes(bytes(self))
    
    def to_list(self):
        return AdvList(list(self))
    
    def to_tuple(self):
        return AdvTuple(tuple(self))

    def encode(self, encoding: Text = ..., errors: Text = ...):
        return AdvBytes(super(AdvString, self).encode(encoding, errors))

    def length(self):
        return AdvInteger(self.__len__())
    
    def add(self, value: str):
        return AdvString(self.__add__(value))
    
    def equals(self, obj: object):
        return AdvBoolean(self.__eq__(obj))
    
    def representation(self):
        return AdvString(self.__repr__())

    def join_lines(self):
        return AdvString(strutils.join_lines(self))
        
    def isbase64(self):
        return AdvBoolean(strutils.is_base64_decodable(self))
    
    def ishex(self):
        return AdvBoolean(strutils.is_hex_digits(self))
    
    def isurlsafeb64(self):
        return AdvBoolean(strutils.is_urlsafeb64_decodable(self))
    
    def isunhexlifable(self):
        return AdvBoolean(strutils.is_unhexlifiable(self))

    def pickle(self):
        import pickle
        return AdvBytes(pickle.dumps(self))


class AdvFloat(float):
    def __init__(self, value: float):
        float.__init__(value)

    def hash(self):
        return AdvInteger(self.__hash__())

    def size(self):
        return AdvInteger(self.__sizeof__())

    def add(self, value: Union[int, float]):
        return AdvFloat(self.__add__(value))

    def substact(self, value: Union[int, float]):
        return AdvFloat(self.__sub__(value))

    def to_string(self):
        return self.__str__()

    def to_boolean(self):
        return self.__bool__()

    def to_integer(self):
        return self.__int__()

    def representation(self):
        return self.__repr__()

    def square(self):
        import math
        return AdvFloat(math.sqrt(self))

    def acos(self):
        import math
        return AdvFloat(math.acos(self))

    def asin(self):
        import math
        return AdvFloat(math.asin(self))

    def atan(self):
        import math
        return AdvFloat(math.atan(self))

    def acosh(self):
        import math
        return AdvFloat(math.acosh(self))

    def asinh(self):
        import math
        return AdvFloat(math.asinh(self))

    def atanh(self):
        import math
        return AdvFloat(math.atanh(self))

    def ceil(self):
        import math
        return AdvFloat(math.ceil(self))

    def cos(self):
        import math
        return AdvFloat(math.cos(self))

    def sin(self):
        import math
        return AdvFloat(math.sin(self))

    def tan(self):
        import math
        return AdvFloat(math.tan(self))

    def cosh(self):
        import math
        return AdvFloat(math.cosh(self))

    def sinh(self):
        import math
        return AdvFloat(math.sinh(self))

    def tanh(self):
        import math
        return AdvFloat(math.tanh(self))

    def degrees(self):
        import math
        return AdvFloat(math.degrees(self))

    def radians(self):
        import math
        return AdvFloat(math.radians(self))

    def log(self, base: Union[int, float] = 10):
        import math
        return AdvFloat(math.log(self, base))

    def log1p(self):
        import math
        return AdvFloat(math.log1p(self))

    def log2(self):
        import math
        return AdvFloat(math.log2(self))

    def log10(self):
        import math
        return AdvFloat(math.log10(self))

    def erf(self):
        import math
        return AdvFloat(math.erf(self))

    def erfc(self):
        import math
        return AdvFloat(math.erfc(self))

    def exp(self):
        import math
        return AdvFloat(math.exp(self))

    def expm1(self):
        import math
        return AdvFloat(math.expm1(self))

    def frexp(self):
        import math
        return math.frexp(self)

    def ldexp(self, i: int):
        import math
        return AdvFloat(math.ldexp(self, i))

    def fabs(self):
        import math
        return AdvFloat(math.fabs(self))

    def factorial(self):
        import math
        return AdvFloat(math.factorial(self))

    def floor(self):
        import math
        return AdvFloat(math.floor(self))

    def gamma(self):
        import math
        return AdvFloat(math.gamma(self))

    def lgamma(self):
        import math
        return AdvFloat(math.lgamma(self))

    def isinfinte(self):
        import math
        return AdvFloat(math.isfinite(self))

    def modf(self):
        import math
        return math.modf(self)

    def mod(self, x):
        self.__mod__(x)

    def power(self, y):
        import math
        return AdvFloat(math.pow(self, y))

    def remainder(self, y):
        import math
        return AdvFloat(math.remainder(self, y))

    def square_root(self):
        import math
        return AdvFloat(math.sqrt(self))

    def sqrt(self):
        import math
        return AdvFloat(math.sqrt(self))

    def trunc(self):
        import math
        return AdvFloat(math.trunc(self))

    def pickle(self):
        import pickle
        return AdvBytes(pickle.dumps(self))

    def equals(self, other: float):
        return AdvBoolean(self.__eq__(other))


class AdvInteger(int):
    def __init__(self, value: int):
        int.__init__(value)

    def hash(self):
        return AdvInteger(self.__hash__())

    def size(self):
        return AdvInteger(self.__sizeof__())
        
    def add(self, value: Union[int, float]):
        return AdvInteger(self.__add__(value))
    
    def substact(self, value: Union[int, float]):
        return AdvInteger(self.__sub__(value))
    
    def to_string(self):
        return AdvString(self.__str__())
    
    def to_boolean(self):
        return AdvBoolean(self.__bool__())
    
    def to_float(self):
        return AdvFloat(self.__float__())

    def repr(self):
        return AdvString(self.__repr__())

    def representation(self):
        return AdvString(self.__repr__())

    def abs(self):
        return AdvInteger(self.__abs__())

    def absolute(self):
        return AdvInteger(self.__abs__())

    def negative(self):
        return AdvInteger(self.__neg__())

    def positive(self):
        return self.__pos__()

    def square(self):
        import math
        return AdvFloat(math.sqrt(self))
    
    def acos(self):
        import math
        return AdvFloat(math.acos(self))
    
    def asin(self):
        import math
        return AdvFloat(math.asin(self))
    
    def atan(self):
        import math
        return AdvFloat(math.atan(self))
    
    def acosh(self):
        import math
        return AdvFloat(math.acosh(self))
    
    def asinh(self):
        import math
        return AdvFloat(math.asinh(self))

    def atanh(self):
        import math
        return AdvFloat(math.atanh(self))

    def ceil(self):
        import math
        return AdvFloat(math.ceil(self))
    
    def cos(self):
        import math
        return AdvFloat(math.cos(self))
        
    def sin(self):
        import math
        return AdvFloat(math.sin(self))
    
    def tan(self):
        import math
        return AdvFloat(math.tan(self))
    
    def cosh(self):
        import math
        return AdvFloat(math.cosh(self))
    
    def sinh(self):
        import math
        return AdvFloat(math.sinh(self))
    
    def tanh(self):
        import math
        return AdvFloat(math.tanh(self))
    
    def degrees(self):
        import math
        return AdvFloat(math.degrees(self))
        
    def radians(self):
        import math
        return AdvFloat(math.radians(self))
    
    def log(self, base: Union[int, float] = 10):
        import math
        return AdvFloat(math.log(self, base))
    
    def log1p(self):
        import math
        return AdvFloat(math.log1p(self))
    
    def log2(self):
        import math
        return AdvFloat(math.log2(self))
    
    def log10(self):
        import math
        return AdvFloat(math.log10(self))
    
    def erf(self):
        import math
        return AdvFloat(math.erf(self))

    def erfc(self):
        import math
        return AdvFloat(math.erfc(self))

    def exp(self):
        import math
        return AdvFloat(math.exp(self))

    def expm1(self):
        import math
        return AdvFloat(math.expm1(self))

    def frexp(self):
        import math
        return AdvTuple(math.frexp(self))

    def ldexp(self, i: int):
        import math
        return AdvFloat(math.ldexp(self, i))

    def fabs(self):
        import math
        return AdvFloat(math.fabs(self))
        
    def factorial(self):
        import math
        return AdvInteger(math.factorial(self))

    def floor(self):
        import math
        return AdvInteger(math.floor(self))

    def gamma(self):
        import math
        return AdvFloat(math.gamma(self))

    def lgamma(self):
        import math
        return AdvFloat(math.lgamma(self))

    def isinfinte(self):
        import math
        return AdvBoolean(math.isfinite(self))

    def modf(self):
        import math
        return AdvTuple(math.modf(self))

    def mod(self, x):
        return AdvInteger(self.__mod__(x))

    def power(self, y):
        import math
        return AdvFloat(math.pow(self, y))

    def remainder(self, y):
        import math
        return AdvFloat(math.remainder(self, y))

    def square_root(self):
        import math
        return AdvFloat(math.sqrt(self))

    def sqrt(self):
        import math
        return AdvFloat(math.sqrt(self))

    def isqrt(self):
        import math
        return AdvInteger(math.isqrt(self))

    def trunc(self):
        import math
        return AdvInteger(math.trunc(self))

    def pickle(self):
        import pickle
        return AdvBytes(pickle.dumps(self))

    def equals(self, other: int):
        return AdvBoolean(self.__eq__(other))


class AdvBoolean(int):
    def __init__(self, bool_: bool):
        int.__init__(bool_)

    def hash(self):
        return AdvInteger(self.__hash__())

    def size(self):
        return AdvInteger(bool(self).__sizeof__())

    def to_integer(self):
        return AdvInteger(bool(self).__int__())

    def to_string(self):
        return AdvString(str(bool(self)))

    def to_float(self):
        return AdvFloat(bool(self).__float__())

    def abs(self):
        return AdvInteger(bool(self).__abs__())

    def absolute(self):
        return AdvInteger(bool(self).__abs__())

    def repr(self):
        return AdvString(bool(self).__repr__())

    def representation(self):
        return AdvString(bool(self).__repr__())

    def __repr__(self):
        return AdvString(bool(self).__repr__())

    def __str__(self):
        return AdvString(bool(self).__str__())

    def equals(self, other: int):
        return AdvBoolean(bool(self).__eq__(other))

    def pickle(self):
        import pickle
        return AdvBytes(pickle.dumps(bool(self)))

    def __and__(self, other):
        return AdvBoolean(bool(self).__and__(other))

    def __or__(self, other):
        return AdvBoolean(bool(self).__or__(other))

    def __xor__(self, other):
        return AdvBoolean(bool(self).__xor__(other))

    def __getnewargs__(self):
        return AdvTuple(bool(self).__getnewargs__())

    def __rand__(self, other):
        return AdvBoolean(bool(self).__rand__(other))

    def __ror__(self, other):
        return AdvBoolean(bool(self).__ror__(other))

    def __rxor__(self, other):
        return AdvBoolean(bool(self).__xor__(other))


class AdvDictionary(dict):
    def __init__(self, value: dict):
        dict.__init__(value)

    def length(self):
        return AdvInteger(self.__len__())

    def hash(self):
        return AdvInteger(self.__hash__())

    def size(self):
        return AdvInteger(self.__sizeof__())

    def to_tuple(self):
        return AdvTuple(tuple(self))

    def to_list(self):
        return AdvList(list(self))

    def add(self, **objects):
        for key, value in objects.items():
            self[key] = value

    def append(self, key, value):
        self[key] = value

    def contains(self, value):
        return AdvBoolean(self.__contains__(value))

    def repr(self):
        return AdvString(self.__repr__())

    def representation(self):
        return AdvString(self.__repr__())

    def equals(self, other):
        return AdvBoolean(self.__eq__(other))

    def pickle(self):
        import pickle
        return AdvBytes(pickle.dumps(self))


class AdvTuple(tuple):
    def __init__(self, value: tuple):
        tuple.__init__(value)

    def length(self):
        return AdvInteger(self.__len__())

    def hash(self):
        return AdvInteger(self.__hash__())

    def contains(self, value):
        return AdvBoolean(self.__contains__(value))

    def size(self):
        return AdvInteger(self.__sizeof__())

    def repr(self):
        return AdvString(self.__repr__())

    def representation(self):
        return AdvString(self.__repr__())

    def to_string(self):
        return AdvString(self.__str__())

    def to_list(self):
        return AdvList(list(self))

    def to_dictionary(self):
        return AdvDictionary(dict(self))

    def equals(self, other):
        return AdvBoolean(self.__eq__(other))

    def pickle(self):
        import pickle
        return AdvBytes(pickle.dumps(self))


class AdvBytes(bytes):
    def __init__(self, value: bytes):
        bytes.__init__(value)

    def length(self):
        return AdvInteger(self.__len__())

    def hash(self):
        return AdvInteger(self.__hash__())

    def size(self):
        return AdvInteger(self.__sizeof__())

    def repr(self):
        return AdvString(self.__repr__())

    def representation(self):
        return AdvString(self.__repr__())

    def to_string(self):
        return AdvString(self.__str__())

    def to_float(self):
        return AdvFloat(self.__float__())

    def to_int(self):
        return AdvInteger(self.__int__())

    def to_list(self):
        return AdvList(list(self))

    def mod(self, value):
        return self.__mod__(value)

    def decode(self, encoding: str = "utf-8", errors: str = None) -> AdvString:
        return AdvString(super(AdvBytes, self).decode(encoding, errors))

    def contains(self, other: bytes):
        return AdvBoolean(self.__contains__(other))

    def equals(self, other):
        return AdvBoolean(self.__eq__(other))

    def pickle(self):
        import pickle
        return AdvBytes(pickle.dumps(self))


class AdvList(list):
    def __init__(self, value: list):
        list.__init__(value)

    def length(self):
        return AdvInteger(self.__len__())

    def hash(self):
        return AdvInteger(self.__hash__())

    def contains(self, item):
        return AdvBoolean(self.__contains__(item))

    def add(self, *objects):
        self.extend(objects)

    def expand(self, amount, value=None):
        self.add(*(value for _ in range(amount)))

    def repr(self):
        return AdvString(self.__repr__())

    def representation(self):
        return AdvString(self.__repr__())

    def to_string(self):
        return AdvString(self.__str__())

    def to_tuple(self):
        return AdvTuple(tuple(self))

    def to_dictionary(self):
        return AdvDictionary(dict(self))

    def join(self, sep=""):
        return AdvString(sep.join(self))

    def equals(self, other: list):
        return AdvBoolean(self.__eq__(other))

    def pickle(self):
        import pickle
        return AdvBytes(pickle.dumps(self))


def adv_input(prompt: str = "", return_type: Type[Union[int, str, bool, float, bytes]] = None) -> \
        Optional[Union[int, str, bool, float, bytes, AdvInteger, AdvString, AdvBoolean, AdvFloat, AdvBytes]]:
    a = input(prompt)
    try:
        if return_type == bytes:
            return a.encode()
        elif return_type == AdvBytes:
            return AdvBytes(a.encode())
        elif return_type == int:
            return int(a)
        elif return_type == AdvInteger:
            return AdvInteger(int(a))
        elif return_type == str:
            return a
        elif return_type == AdvString:
            return AdvString(a)
        elif return_type == float:
            return float(a)
        elif return_type == AdvFloat:
            return AdvFloat(float(a))
        elif return_type == bool:
            return bool(a)
        elif return_type == AdvBoolean:
            return AdvBoolean(bool(a))
    except TypeError:
        return None
    except ValueError:
        return None
    except UnicodeEncodeError:
        return None
    return return_type(a)


if __name__ == '__main__':
    some_int = AdvInteger(9)
    print(some_int.square().square().square().square().square().square().square().square().square().square().square())
    print(some_int.to_string())

    some_str = AdvString("Woord1 Woord2")
    print(some_str.contains("Woord"))
    print(some_str.ishex())

    some_hex = AdvString("98474f39e83cc73e")
    print(some_hex.pickle())

    import pickle
    with open("test.dat") as file:
        pickle.dump({(345, 35): lambda: str()}, file)
    dit_is_een_var = pickle.dumps({(345, 35): lambda: str()})

    while True:
        a = ...
        if a == 43:
            break

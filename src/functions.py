import math

from inspect import signature
functions = []

def registerfunc(name=""):
  def decorator(f):
    argc = 0
    sig = str(signature(f))

    if "=" in sig:
      raise Exception("[SEL] Error: Named parameters not supported")

    if "*" in sig:
      argc = -1 # variadic
    else:
      if  len(sig) > 2:
        argc = len(sig.split(","))

    functions.append({ "name": name if name else f.__name__, "argc": argc, "func": f })
    return f
  return decorator

#####################
# Math & Arithmetic #
#####################

@registerfunc()
def sum(*args):
  res = 0
  for arg in args:
    res += arg
  return res

@registerfunc()
def mul(*args):
  res = 1
  for arg in args:
    res *= arg
  return res 

@registerfunc()
def sub(*args):
  res = args[0]
  for arg in args:
    res -= arg
  return res

@registerfunc()
def div(a, b):
  return a / b

@registerfunc()
def mod(a, b):
  return a % b

@registerfunc()
def square(a):
  return a**2

@registerfunc()
def cube(a):
  return a**3

@registerfunc()
def pow(b, p):
  return b**p

@registerfunc()
def sqrt(a):
  return math.sqrt(a)

@registerfunc()
def cbrt(a):
  return math.cbrt(a)

@registerfunc()
def pi():
  return math.pi

@registerfunc()
def sin(a):
  return math.sin(a)

@registerfunc()
def cos(a):
  return math.cos(a)

@registerfunc()
def tan(a):
  return math.tan(a)

@registerfunc()
def asin(a):
  return math.asin(a)

@registerfunc()
def acos(a):
  return math.acos(a)

@registerfunc()
def atan(a):
  return math.atan(a)

# convert from radians to degrees
@registerfunc()
def deg(r):
  return r * 180/math.pi

################
# Side Effects #
################

@registerfunc(name="print")
def sel_print(msg):
  print(msg)

@registerfunc(name="input")
def sel_input():
  return input()

###################
# Type Conversion #
###################

@registerfunc(name="int")
def sel_int(a):
  return int(a)

@registerfunc(name="str")
def sel_str(a):
  return str(a)

###########
# Strings #
###########

@registerfunc()
def concat(a, b):
  return a+b

# format with `"%s" % (...)` syntax
@registerfunc()
def format(f, *args):
  return f % args

@registerfunc()
def split(sep, s):
  return tuple(s.split(sep))

@registerfunc()
def join(sep, *strs):
  return sep.join(strs)

@registerfunc(name="len")
def sel_len(s):
  return len(s)

#########
# Lists #
#########

# get element with index i in array a
@registerfunc()
def select(a, i):
  return a[i]

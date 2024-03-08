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
def square(a):
  return a**2

@registerfunc()
def pi():
  return math.pi

@registerfunc(name="print")
def sel_print(msg):
  print(msg)

@registerfunc(name="input")
def sel_input():
  return input()

@registerfunc(name="int")
def sel_int(a):
  return int(a)

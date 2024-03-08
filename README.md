# SEL

SEL stands for Simple Expression Language.

## How to use

```py
import sel

sel.eval("(print 'Hello World')")
```

## Language

SEL is a language that consists of linear expressions. There's no nesting. The only way expressions can 'depend' on each other is by [pointers](#pointers).

- [Expressions](#expressions)
  - [Numbers](#numbers)
  - [Strings](#strings)
- [Pointers](#pointers)
  - [Labels](#labels)
- [Function Calls](#function-calls)
- [Functions](#functions)
  - [Builtin Functions](#builtin-functions)
- [Example](#example)
- [Eval](#eval)

### Expressions

Expressions are the building block of any SEL program - they're even in the acronym Simple Expression Language. Expressions are wrapped inside parenthesis `(` and `)` and contain a value.

```
(5)
```

In the example there's an expression containing the numeric value of 5. Values include:

- Numbers
- Strings
- Pointers
- Function calls

#### Numbers

Numbers can be:

```
1
1.3
0.3
.3
-1
-1.3
-0.3
-.3
```

#### Strings

Strings accept `'` and `"`. You can always escape quotes using `\"` and `\'`.
**Note** that there's no support for other escape sequences:

- `\n` just expands to the letter `n`.
- There's no way to escape `\` itself, as the character `\` is always ignored by the parser and only affects the character after it.

However, these are easy to fix and will hopefully be fixed soon.

### Pointers

Pointers are fundamental in SEL. They allow expressions to depend on each other, resulting in more complex programs.

```
# Without pointers only single values can be returned:

2
3
4
pi

# With pointers there's much more potential

2 + 2/3
4**2 + 3
2 * pi * r**2
```

The following program utilizes pointers to add 3 to the value of the previous expression:

```
(2)(sum $ 3)
```

Resulting in `2+3 = 5`.

Pointers basically _refer_ to another expression.

```
Relative reference:

(2)(4)(6)($)   -> 6
      ^^^
(2)(4)(6)($-1) -> 4
   ^^^
(2)(4)(6)($-2) -> 2
^^^
(2)(4)(6)($-3) -> Error

Absolute reference (zero-based indexing):

(2)(4)(6)($+0) -> 2
^^^
(2)(4)(6)($+1) -> 4
   ^^^
(2)(4)(6)($+2) -> 6
      ^^^
```

#### Labels

Labels offer a more friendly way to use pointers.

```
(num: 8)
(sum $num 3)
```

### Function Calls

Function calls consist of the function name and its arguments.

```
(func a b)  # 2 args
(func a)    # 1 args
(func)      # no args

Examples:
(add 3 4)   -> 7
(cube 3)    -> 27
(pi)        -> 3.14
```

Some functions are variadic - they get an indefinite number of arguments:

```
(sum 1 2 3 4 5 6 7 8 9 ...)
```

### Functions

Functions are predefined in `sel/functions.py`. To define a new function go to the end of the file and write:

```py
@registerfunc()
def myfunc(a, b):
  return a+b
```

Then you can do:

```py
import sel

sel.eval("myfunc 3 4") # yields 7
```

`registerfunc()` optionally takes one argument: `name`. Which is specified to give the function a different name in SEL rather than its actual name.

```py
@registerfunc(name="print")
def sel_print(msg):
  print(msg)
```

If `print` is the function name:

- Builtin `print` overriden
- Recursion

So `sel_print` is used instead, and registered as `print`.

**Note**: Underscores are not allowed in function/label names.

Functions can also be variadic:

```py
@registerfunc()
def sum(*numbers):
  total = 0
  for num in numbers:
    total += num
  return total
```

```
(sum 1 2 3 4 5 12)  -> 27
(sum 4)             -> 4
(sum 3 4)           -> 7
```

#### Builtin functions

All builtin functions are found in `sel/functions.py`. They are:

- `sum` - Addition (Variadic)
- `mul` - Multiplication (Variadic)
- `square` - x^2
- `pi` - Constant, 3.14...
- `print` [defined as `sel_print`] - Print
- `input` [defined as `sel_input`] - Python `input()` function
- `int` [defined as `sel_int`] - String to Int

You can add more if you want.

### Example

Get area of a circle

```
(pi: pi)
(print "Radius?")
(input)
(radius: int $)
(print "Result:")
(square $radius)
(mul $pi $)
```

### Eval

`sel.eval` returns the value of the last expression.

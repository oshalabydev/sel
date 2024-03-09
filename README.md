<h1 align="center">SEL</h1>
<p align="center"><strong>Simple Expression Language, SEL, is a tiny but powerful language.</strong></p>

## Introduction

Simple Expression Language (or SEL) is a minimal and tiny language. It consists of expressions enclosed in parenthesis linearly arranged without nesting. The expressions may contain constants, function calls and pointers - they _point_ (refer) to other expressions.

```
(sum 1 1)(mul $ 2)
```

The code above is equivalent to this calculation:

$$2(1+1)$$

So it will return $4$. The dollar (`$`) character in the second expression is substituted by the interpreter with the value of the expression before it (i.e. the first expression, which has a value of $(1 + 1 =) 2$).

SEL is entirely built around this idea, i.e. the use of pointers for expressions to depend on each other. SEL has no nesting, however, pointers _simulate_ nesting; you can rewrite the code above to:

```
(mul (sum 1 1) 2)
```

Here, we substituted `$` with the first expression `(sum 1 1)`. This will give you a better idea of how pointers work, however, it is invalid in SEL since nesting is not allowed.

## Install

Currently, the package is not published; you cannot use `pip` to install it. However, you can clone the repository:

```sh
$ git clone https://github.com/oshalabydev/sel.git
```

and use the package with:

```py
import sel
```

## How To Use

SEL is entirely written in Python, and so it has a Python API (the details of the API are listed in the [wiki](https://github.com/oshalabydev/sel/wiki)).

To run some SEL code, make sure you have [installed](#install) the package.

```py
import sel

sel.eval("(print 'Hello World')")
```

_Prints 'Hello World'_

The example above uses the built-in function `print`, however, `print` doesn't return anything - it has a side effect instead.

The SEL interpreter (i.e. `sel.eval`) always returns the value of the last expression. Since `print` doesn't return anything, `sel.eval` returns $0$.

```py
out = sel.eval("(12)(sum $ 2)")
print(out) # -> 14
```

More information on the SEL language and the SEL Python API can be found in the [wiki](https://github.com/oshalabydev/sel/wiki).

<hr>
<p align="center"><em>Contribution is highly appreciated</em></p>

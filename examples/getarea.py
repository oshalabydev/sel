import sel

code = """
(print "Radius?")
(pi: pi)
(input)
(radius: int $)
(print "Results:")
(square $radius)
(result: mul $pi $)
(print $result)
"""

def main():
  sel.eval(code)

if __name__ == "__main__":
  main()
labels = {}

def sel_validate_before_tokenizer(input):
  string = list(input)
  paren_open = 0
  paren_close = 0
  current = 0
  
  while current < len(string):
    if (string[current] == "("):
      paren_open += 1
    
    if (string[current] == ")"):
      paren_close += 1

    current += 1
  
  if paren_open == 0 and paren_close == 0:
    raise Exception("[SEL] Error: No parenthesis in non-empty string")
  
  if paren_open != paren_close:
    raise Exception("[SEL] Error: Invalid combination/order of parenthesis")

def sel_tokenize(input):
  string = list(input)
  tokens = []
  current = 0

  while current < len(string):
    char = string[current]

    if char == " " or char == "\t" or char == "\n":
      current += 1
      continue

    if char == "(":
      tokens.append({ "type": "paren", "value": "(" })
      current += 1
      continue

    if char == ")":
      tokens.append({ "type": "paren", "value": ")" })
      current += 1
      continue

    if char == "$":
      offset = 1

      if (string[current+1] == "-" or string[current+1] == "+") and string[current+2].isnumeric():
        absolute = True if string[current+1] == "+" else False
        value = []
        current += 2

        while string[current].isnumeric():
          value.append(string[current])
          current += 1
        
        if absolute:
          tokens.append({ "type": "pointer", "mode": "absolute", "pos": int("".join(value)) })
        else:
          offset += int("".join(value))
          tokens.append({ "type": "pointer", "mode": "relative", "offset": offset })
      elif string[current+1].isalpha():
        value = []
        current += 1

        while string[current].isalpha():
          value.append(string[current])
          current += 1
        
        tokens.append({ "type": "pointer", "mode": "label", "label": "".join(value) })
      else:
        current += 1
        tokens.append({ "type": "pointer", "mode": "relative", "offset": offset })

      continue

    if char.isnumeric() or char == "." or (char == "-" and (string[current+1].isnumeric() or string[current+1] == ".")):
      isfloat = False
      value = []

      if char == ".":
        isfloat = True

      if char == "-":
        value.append(char)
        current += 1
        char = string[current]

      while char.isnumeric() or char == ".":
        if char == ".":
          isfloat = True

        value.append(char)
        current += 1
        char = string[current]

      if isfloat:
        tokens.append({ "type": "number", "numtype": "float", "value": "".join(value) })
      else:
        tokens.append({ "type": "number", "numtype": "int", "value": "".join(value) })

      continue

    if char == "'" or char == "\"":
      quote_style = char
      value = []
      current += 1
      char = string[current]

      while (char != quote_style or string[current-1] == "\\"):
        if (char == "\\" and string[current+1] == quote_style):
          current += 1
          char = string[current]
          continue
          
        value.append(char)
        current += 1
        char = string[current]

      current += 1
      char = string[current]
      tokens.append({ "type": "string", "value": "".join(value) })

      continue

    if char.isalpha():
      value = []

      while char.isalpha():
        value.append(char)
        current += 1
        char = string[current]
      
      if (char == ":"):
        tokens.append({ "type": "label", "value": "".join(value) })
        current += 1
        char = string[current]
      else:
        tokens.append({ "type": "name", "value": "".join(value) })

      continue

    raise Exception(f"[SEL] Error: Invalid token '{char}'")
  return tokens

def sel_token_validate(tokens):
  paren = 0
  paren_contains_tokens = False

  for i in range(len(tokens)):
    token = tokens[i]

    if token["type"] != "paren" and paren != 0:
      paren_contains_tokens = True

    if token["type"] == "paren":
      if token["value"] == "(": paren += 1
      if token["value"] == ")":
        paren -= 1

        if paren != 0:
          raise Exception("[SEL] Error: Invalid combination/order of parenthesis")

        if paren_contains_tokens:
          paren_contains_tokens = False
        else:
          raise Exception("[SEL] Error: Expression cannot be empty")

def sel_token_split(tokens):
  expressions = []
  expr_opened = False
  num_expr = 0

  for i in range(len(tokens)):
    token = tokens[i]

    if token["type"] == "paren":
      if token["value"] == "(":
        expr_opened = True
        expressions.append([])

      if token["value"] == ")":
        expr_opened = False
        num_expr += 1

      continue

    if expr_opened:
      if token["type"] == "label":
        if not token["value"] in labels:
          labels[token["value"]] = num_expr
        else:
          raise Exception("[SEL] Error: Label already exists")
      else:
        expressions[num_expr].append(token)

  return expressions

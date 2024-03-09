from sel.src.functions import functions as sel_funcs
from sel.src.lexer import labels

def sel_eval(expressions):
  values = []

  for i in range(len(expressions)):
    expr = expressions[i]

    match expr[0]["type"]:
      case "number":
        if expr[0]["numtype"] == "int":
          values.append(int(expr[0]["value"]))

        if expr[0]["numtype"] == "float":
          values.append(float(expr[0]["value"]))
      case "string":
        values.append(expr[0]["value"])
      case "pointer":
        if expr[0]["mode"] == "relative":
          if expr[0]["offset"] <= len(values):
            values.append(values[-1 - (expr[0]["offset"]-1)])
          else:
            raise Exception("[SEL] Error: Invalid reference; expression doesn't exist")
        elif expr[0]["mode"] == "absolute":
          if expr[0]["pos"] >= 0 and expr[0]["pos"] < len(values):
            values.append(values[expr[0]["pos"]])
          else:
            raise Exception("[SEL] Error: Invalid reference; expression doesn't exist")
        elif expr[0]["mode"] == "label":
          pos = labels.get(expr[0]["label"], None)
          if pos == None:
            raise Exception("[SEL] Error: Invalid reference; expression doesn't exist")
          if pos >= 0 and pos < len(values):
            values.append(values[pos])
          else:
            raise Exception("[SEL] Error: Invalid reference; expression doesn't exist")
      case "name":
        func_index = next((i for i, func in enumerate(sel_funcs) if func["name"] == expr[0]["value"]), None)
        expr_num_tokens = len(expr)

        if func_index == None:
          raise Exception(f"[SEL] Error: Undefined function '{expr[0]['value']}'")
        
        function = sel_funcs[func_index]
        argc = function["argc"]
        
        if argc < 0:
          if expr_num_tokens-1 < 1:
            raise Exception(f"[SEL] Error: No arguments for variadic function '{expr[0]['value']}'")
        else:
          if expr_num_tokens-1 > argc:
            raise Exception(f"[SEL] Error: Too many arguments for function '{expr[0]['value']}'")
          elif expr_num_tokens-1 < argc:
            raise Exception(f"[SEL] Error: Too few arguments for function '{expr[0]['value']}'")

        rng = argc if argc >= 0 else len(expr)-1
        args = []
        for j in range(rng):
          arg_expr = expr[j+1]

          if arg_expr["type"] == "pointer":
            if arg_expr["mode"] == "relative":
              if arg_expr["offset"] <= len(values):
                args.append(values[-1 - (arg_expr["offset"]-1)])
              else:
                raise Exception("[SEL] Error: Invalid reference; expression doesn't exist")
            elif arg_expr["mode"] == "absolute":
              if arg_expr["pos"] >= 0 and arg_expr["pos"] < len(values):
                args.append(values[arg_expr["pos"]])
              else:
                raise Exception("[SEL] Error: Invalid reference; expression doesn't exist")
            elif arg_expr["mode"] == "label":
              pos = labels.get(arg_expr["label"], None)
              if pos == None:
                raise Exception("[SEL] Error: Invalid reference; expression doesn't exist")
              if pos >= 0 and pos < len(values):
                args.append(values[pos])
              else:
                raise Exception("[SEL] Error: Invalid reference; expression doesn't exist")
          elif arg_expr["type"] == "number":
            if arg_expr["numtype"] == "int":
              args.append(int(arg_expr["value"]))
            elif arg_expr["numtype"] == "float":
              args.append(float(arg_expr["value"]))
          else:
            args.append(arg_expr["value"])

        ret = function["func"](*args)
        
        if ret == None:
          ret = 0

        values.append(ret)
  
  return values

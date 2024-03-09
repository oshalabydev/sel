import sel.src.lexer as sel_lexer
import sel.src.eval as sel_eval

def eval(input):
  sel_lexer.sel_validate_before_tokenizer(input)
  tokens = sel_lexer.sel_tokenize(input)
  sel_lexer.sel_token_validate(tokens)
  expressions = sel_lexer.sel_token_split(tokens)
  values = sel_eval.sel_eval(expressions)
  if len(values) > 0: return values[-1] # return value of last expression

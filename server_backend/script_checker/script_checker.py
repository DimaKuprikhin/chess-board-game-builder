import ast


def check_script(script: str) -> bool:
  '''
  Returns true if script is considered safe and
  contains no malware instructions.
  '''
  if not isinstance(script, str):
    return False
  node = ast.parse(script, '<usercode>', 'exec')
  return SafeAST().check_nodes(node)


class SafeAST(ast.NodeVisitor):
  def __init__(self):
    # List of allowed node types. Disallowed node types are commented out.
    self.allowed_nodes = [
        # Module.
        ast.Module,

        # Literals.
        ast.Constant,
        # ast.FormattedValue,
        # ast.JoinedStr,
        ast.List,
        ast.Tuple,
        ast.Set,
        ast.Dict,

        # Variables.
        ast.Name,
        ast.Load,
        ast.Store,
        ast.Del,
        ast.Starred,

        # Expressions.
        ast.Expr,
        ast.UnaryOp,
        ast.USub,
        ast.Not,
        ast.Invert,
        ast.BinOp,
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Div,
        ast.FloorDiv,
        ast.Mod,
        ast.Pow,
        ast.LShift,
        ast.RShift,
        ast.BitOr,
        ast.BitXor,
        ast.BitAnd,
        ast.MatMult,
        ast.BoolOp,
        ast.And,
        ast.Or,
        ast.Compare,
        ast.Eq,
        ast.NotEq,
        ast.Lt,
        ast.LtE,
        ast.Gt,
        ast.GtE,
        ast.Is,
        ast.IsNot,
        ast.In,
        ast.NotIn,
        # Call node is examined separately.
        ast.Call,
        ast.keyword,
        ast.IfExp,
        ast.Attribute,
        # ast.NamedExpr,

        # Subscripting.
        ast.Subscript,
        ast.Slice,

        # Comprehensions.
        ast.ListComp,
        ast.SetComp,
        ast.GeneratorExp,
        ast.DictComp,
        ast.comprehension,

        # Statements.
        ast.Assign,
        ast.AnnAssign,
        ast.AugAssign,
        # ast.Raise,
        # ast.Assert,
        ast.Delete,
        ast.Pass,

        # Imports.
        # ast.Import,
        # ast.ImportFrom,
        # ast.alias,

        # Control flow.
        ast.If,
        ast.For,
        ast.While,
        ast.Break,
        ast.Continue,
        # ast.Try,
        # ast.ExceptHandler,
        # ast.With,
        # ast.withitem,

        # Pattern matching is completely disabled.

        # Function and class definitions.
        ast.FunctionDef,
        # ast.Lambda,
        ast.arguments,
        ast.arg,
        ast.Return,
        # ast.Yield,
        # ast.YieldFrom,
        # ast.Global,
        # ast.Nonlocal,
        # ast.ClassDef,

        # Async and await is completely disabled.
    ]
    # List of functions that user script is allowed to call and contains of
    # some built-in functions and basic data structure methods.
    self.allowed_functions = [
        # Built-in functions.
        'abs',
        'all',
        'any',
        'chr',
        'divmod',
        'enumerate',
        'filter',
        'float',
        'int',
        'iter',
        'len',
        'max',
        'min',
        'next',
        'pow',
        'range',
        'reversed',
        'round',
        'sorted',
        'sum',
        'zip',

        # List methods.
        'append',
        'extend',
        'insert',
        'remove',
        'pop',
        'clear',
        'index',
        'count',
        'sort',
        'reverse',
        'copy',

        # Dict methods.
        'list',
        'len',
        'iter',
        'clear',
        'copy',
        'get',
        'items',
        'keys',
        'pop',
        'popitem',
        'reversed',
        'setdefault',
        'update',
        'values',
    ]

  def generic_visit(self, node: ast.AST):
    self.collected_nodes.append(node)
    if isinstance(node, ast.FunctionDef):
      self.defined_functions.append(node.name)
    ast.NodeVisitor.generic_visit(self, node)

  def check_nodes(self, root: ast.AST) -> bool:
    self.collected_nodes = []
    self.defined_functions = []
    # Walk through the ast and collect nodes and user-defined functions.
    self.visit(root)
    # Check valid node types and function names.
    for node in self.collected_nodes:
      if isinstance(node, ast.Call):
        if isinstance(node.func, ast.Name):
          if (not node.func.id in self.allowed_functions
              and not node.func.id in self.defined_functions):
            return False
        elif isinstance(node.func, ast.Attribute):
          if (not node.func.attr in self.allowed_functions
              and not node.func.attr in self.defined_functions):
            return False
        else:
          return False
      if not type(node) in self.allowed_nodes:
        return False
    return True

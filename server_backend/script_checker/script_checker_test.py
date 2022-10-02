import code
from server_backend.script_checker.script_checker import check_script


class TestCheckScript:
  def test_open(self):
    script = 'f = open("test.txt", "w")'
    assert not check_script(script)

  def test_raise_assert(self):
    script = 'raise TypeError'
    assert not check_script(script)
    script = 'assert False'
    assert not check_script(script)

  def test_import(self):
    script = 'import json'
    assert not check_script(script)
    script = 'import json as js'
    assert not check_script(script)
    script = 'from ast import AST'
    assert not check_script(script)
    script = 'from ast import AST as ASTree'
    assert not check_script(script)

  def test_try_except(self):
    script = 'try:\n'
    script += '  a = 4\n'
    script += 'except:\n'
    script += '  pass'
    assert not check_script(script)

  def test_class(self):
    script = 'class TestClass:\n'
    script += '  pass'
    assert not check_script(script)

  def test_disallowed_functions(self):
    # breakpoint().
    script = 'breakpoint()'
    assert not check_script(script)
    # compile().
    script = 'compile("source", "test.txt", "eval")'
    assert not check_script(script)
    # eval().
    script = 'eval("return False")'
    assert not check_script(script)
    # exec().
    script = 'eval("f = open(\'test.txt\', \'w\')")'
    assert not check_script(script)
    # input().
    script = 'input()'
    assert not check_script(script)
    # locals().
    script = 'locals()'
    assert not check_script(script)
    # open().
    script = 'open("Makefile", "r")'
    assert not check_script(script)
    # print().
    script = 'print(3)'
    assert not check_script(script)
    # __import__().
    script = '__import__("json")'
    assert not check_script(script)

  def test_segfault(self):
    # https://nedbatchelder.com/blog/201206/eval_really_is_dangerous.html
    script = """
(lambda fc=(
    lambda n: [
        c for c in 
            ().__class__.__bases__[0].__subclasses__() 
            if c.__name__ == n
        ][0]
    ):
    fc("function")(
        fc("code")(
            0,0,0,0,0,0,b"KABOOM",(),(),(),"","",0,b""
        ),{}
    )()
)()
"""
    assert not check_script(script)

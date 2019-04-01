from collections import namedtuple
import inspect
from pprint import pprint
import types

# Intermediate form. We probably don't need this, and can put metadata directly in the store
# but it makes this example simpler.
ClassDecl = namedtuple('ClassDecl', 'name base fields'.split())
FieldDecl = namedtuple('FieldDecl', 'name type default'.split())
FunctionDecl = namedtuple('FunctionDecl', 'name owner args'.split())
# where args are the same as fields

# These classes are purely descriptive. To be analyzed/introspected and added
# to the metainformation/ontology in the store.
class Color(object):
  """A named Color"""
  def __init__(self, name:str='white'):
    pass

class Element(object):
  """An Element in a Drawing/Diagram"""
  def __init__(self, id:int=0):
    pass

  def paint(self, color:Color):
    pass

def paint(element:Element, color:Color):
  pass

def introspect_class(klass):
  sig = inspect.signature(klass.__init__)
  def transform_parameter(parameter):
    return FieldDecl(name=parameter.name, type=parameter.annotation, default=parameter.default)
  fields = [transform_parameter(parameter) for parameter in sig.parameters.values()]
  return ClassDecl(name=klass.__name__, base=(object,), fields=fields[1:])

def introspect_function(func):
  sig = inspect.signature(func)
  def transform_parameter(parameter):
    return FieldDecl(name=parameter.name, type=parameter.annotation, default=parameter.default)
  fields = [transform_parameter(parameter) for parameter in list(sig.parameters.values())]
  # Should be fixed for methods on classes, this only works for instances.
  # None for a global function, otherwise should be a ref to class.
  owner = func.__self__ if type(func) == types.MethodType else None
  return FunctionDecl(name=func.__name__, owner=owner, args=fields)

if __name__ == '__main__':
  pprint(introspect_class(Element))
  pprint(introspect_function(paint))
  pprint(introspect_function(Element.paint))

from collections import namedtuple
import inspect
from pprint import pprint
import types

# Intermediate form. We probably don't need this, and pull metadata directly from the store
# but it makes this example simpler.
ClassDecl = namedtuple('ClassDecl', 'name base fields'.split())
FieldDecl = namedtuple('FieldDecl', 'name type default'.split())
FunctionDecl = namedtuple('FunctionDecl', 'name owner args'.split())

class MyBase(object):
  def __repr__(self):
    return '<%s at 0x%s %s>' % (self.__class__.__name__, id(self), str(self.__dict__))

# example decl
Element_class_decl = ClassDecl(name='Element', base=(MyBase,),
    fields=[FieldDecl(name='id', type=int, default=0), FieldDecl(name='name', type=str, default=inspect._empty)])

def synthesize_class(decl):
  """Given a description create the class"""
  def init(self, **kwargs):
    args_we_got = set(kwargs.keys())
    field_name_to_default = {field.name:field.default for field in decl.fields}
    args_we_need = set(field_name_to_default.keys())
    default_args = args_we_need - args_we_got
    self.__dict__.update(kwargs)

    # Should probably barf on inspect._empty defaults
    self.__dict__.update({name:field_name_to_default[name] for name in default_args})

  attrs = {'__init__': init}

  for field in decl.fields:
    attrs[field.name] = field.default
    assert field.default == inspect._empty or type(field.default) == field.type
  return type(decl.name, decl.base, attrs)

if __name__ == '__main__':
  Element = synthesize_class(Element_class_decl)
  element = Element(name='Root')
  print(element)
  print(element.__dict__)

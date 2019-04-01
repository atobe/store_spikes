from pyDatalog import pyDatalog

pyDatalog.create_terms('X, Y, Z, Id, Attr, Value, is_a, has_a, base, type, field, defval, named, attrval')

# eid/entity, attr, value -> attr/predicate(entity, value)

+ is_a('Element', 'Class')
+ base('Element', 'object')

+ is_a('Group', 'Class')
+ base('Group', 'Element')
+ has_a('Group', 'Group.children')

+ is_a('Group.children', list)
+ defval('Group.children', [])

+ is_a('Color', 'Class')
+ base('Element', 'object')
+ has_a('Color', 'Color.name')

+ is_a('Color.name', str)
+ defval('Color.name', 'white')


def add_base_class(name):
  + is_a(name, 'Class')
  + base(name, 'object')

add_base_class('Rectangle')

print('classes:')
print(is_a(X, 'Class'))
print()

print('fields of Color')
print(has_a('Color', X))
print()

class NameSupply(object):
  count = 0
  def __call__(self):
    self.count += 1
    return self.count
eid = NameSupply()

def create_instance(class_name):
  id_ = eid()
  + is_a(id_, class_name)

  # find the fields that have defvals and assert those defaults
  for name, value in list(has_a(class_name, Attr) & defval(Attr, Value)):
    + attrval(id_, name, value)

create_instance('Color')
print('instances of Color')
print(is_a(Id, 'Color'))
print(is_a(Id, 'Color') & attrval(Id, Attr, Value))
print()

# type all the things
print(is_a(X, Y))

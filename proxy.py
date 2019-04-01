from pprint import pprint

store = [
  ('a', 'b', 'c'),
]

class MyBase(object):
  def __repr__(self):
    return '<%s at 0x%s %s>' % (self.__class__.__name__, id(self), str(self.__dict__))

class Proxy(MyBase):
  """Demonstrate writing through state to triple store"""
  def __init__(self, **kwargs):
    super(Proxy, self).__init__()
    self.__dict__.update(kwargs)

if __name__ == '__main__':
  Counter = type('Counter', (Proxy,), {})

  # Shonky. For real this would use the init method synthesized from the description.
  counter = Counter(value=0)
  print(counter)

  counter.value += 1

  # ok, so now check the store
  pprint(store)

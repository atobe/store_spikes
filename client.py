import store

from project import class_decls
from project import function_lib

# this is probably tucked away somewhere in the project's startup script
store.analyze(class_decls)
store.analyze(function_lib)

# get the synthesized type from the store
Counter = store.get('Counter')

# make an instance
a_counter = Counter()

# increment the counter
a_counter.value += 1

# now, at_exit there will be (an anonymous) Counter instance in the store

# let's try with something richer
Person = store.get('Person')

toby = Person(name='Toby', city='SF')

# later...
from store import query_facade as q

toby2 = p.match(class=Person, name='Toby')
print(toby2.city) # -> 'SF'

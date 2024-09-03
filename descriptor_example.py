class SimpleDescr:

    def __get__(self, instance, owner):
        print(f'SimpleDescr: {instance}, {owner}')
        if isinstance(instance, type(None)):
            return self

        return '2'

    def __set__(self, instance, value):
        pass

    def __delete__(self, instance):
        pass

class Foo:
    desc = SimpleDescr()

print('\n\n\n')
print(f'class object: {Foo.desc}')
print(f'instance: {Foo().desc}')
print('\n\n\n')

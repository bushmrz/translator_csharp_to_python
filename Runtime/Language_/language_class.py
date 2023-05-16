from Runtime.Language_.language_callable import LanguageCallable
from Runtime.Language_.language_instance import LanguageInstance
class LanguageClass(LanguageCallable):
    def __init__(self, name, superclass, methods):
        self.name = name
        self.superclass = superclass
        self.methods = methods

    def find_method(self, name):
        method = self.methods.get(name)
        if method:
            return method

        if self.superclass:
            return self.superclass.find_method(name)

        return None

    def __str__(self):
        return f"<class {self.name}>"

    def call(self, interpreter, arguments):
        instance = LanguageInstance(cls=self)
        initializer = self.find_method("init")
        if initializer:
            initializer.bind(instance=instance).call(interpreter, arguments)
        return instance

    def arity(self):
        initializer = self.find_method("init")
        if not initializer:
            return 0
        return initializer.arity()

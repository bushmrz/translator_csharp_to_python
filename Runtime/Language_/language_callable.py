from abc import ABC, abstractmethod


class LanguageCallable(ABC):

    @abstractmethod
    def arity(self) -> int:
        pass

    @abstractmethod
    def call(self, interpreter, arguments: list):
        pass

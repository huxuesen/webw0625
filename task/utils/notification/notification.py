from abc import ABCMeta, abstractmethod


class Notification():
    __metaclass__ = ABCMeta

    @abstractmethod
    def send(self, to, header, content):
        pass

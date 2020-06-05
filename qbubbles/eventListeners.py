from typing import Callable, Dict, List

from qbubbles.events import Event, LanguageChangeEvent


class EventListener(object):
    eventListeners: Dict[Event, List[Callable]] = {}

    @classmethod
    def register(cls, event):
        def decorator(func):
            if event not in cls.eventListeners.keys():
                cls.eventListeners[event] = []
            cls.eventListeners[event].append(func)
            event.bind(func)
            return func
        return decorator

    @classmethod
    def destroy(cls, event, func):
        cls.eventListeners[event].remove(func)


# @EventListener.register(LanguageChangeEvent)
# class LanguageFileChanger(EventListener):
#     def __init__(self, evt: LanguageChangeEvent):
#         self.langid = evt.langid
#
#     def update_language(self):
#         pass

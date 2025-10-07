from typing import Callable
import asyncio

class Signal:
    def __init__(self):
        self.connections = []

    

    async def emit(self, *args, **kwargs):
        for func in self.connections:
            func(*args,**kwargs)
    
    def connect(self, func : Callable):
        self.connections.append(func)

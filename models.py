from typing import NamedTuple

# Using a NamedTuple is a quick and easy way of creating 
# simple classes in Python without having to use the __init__ method and properties.
class Book(NamedTuple):
    id: int
    name: str
    author: str
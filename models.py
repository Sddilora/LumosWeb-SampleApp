from LumosWeb.orm import Table, Column
# Using a NamedTuple is a quick and easy way of creating 
# simple classes in Python without having to use the __init__ method and properties.
class Book(Table):
    author = Column(str)
    name = Column(str)
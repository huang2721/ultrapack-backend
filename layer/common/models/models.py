import os
from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute,
    NumberAttribute,
    MapAttribute,
    ListAttribute,
    BooleanAttribute
)


class Item(MapAttribute):
    name = UnicodeAttribute()
    description = UnicodeAttribute(null=True)
    weight = NumberAttribute(null=True)
    unit = UnicodeAttribute(null=True)
    price = UnicodeAttribute(null=True)
    worn = BooleanAttribute(null=True)
    consumable = BooleanAttribute(null=True)
    quantity = NumberAttribute(default=1)
    image_link = UnicodeAttribute(null=True)
    category = UnicodeAttribute(null=True)


class PackList(Model):
    class Meta:
        table_name = os.environ.get('TABLE', 'packing-list-table')
        # host = 'http://localhost:8000'
    user_id = UnicodeAttribute(hash_key=True)
    list_id = UnicodeAttribute(range_key=True)
    name = UnicodeAttribute()
    description = UnicodeAttribute(null=True)
    last_edit_date = UnicodeAttribute()
    items = ListAttribute(of=Item)


# class PackingList():
#     '''A class for a packing list'''

#     def __init__(self) -> None:
#         self.id = ''
#         self.user_id = ''
#         self.name = ''
#         self.description = ''
#         self.last_edit_date = None
#         self.items = [ListItem]


# class ListItem():
#     '''A class for an item in a packing list'''

#     def __init__(self) -> None:
#         self.name = ''
#         self.description = ''
#         self.weight = 0
#         self.unit = ''
#         self.price = 0
#         self.worn = False
#         self.consumable = False
#         self.quantity = 0
#         self.image_link = None
#         self.category = None

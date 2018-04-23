from si.gui.room.item import Item
from si.gui.room.position import Position

all_items = []

all_items.extend([
    Item(
        name='Sofa',
        position=Position(10, 5, False),
        half_width=10,
        half_height=5
    ),
    Item(
        name='Wardrobe',
        position=Position(10, 5, True),
        half_width=4,
        half_height=3
    ),
    Item(
        name='TV',
        position=Position(5, 10, False),
        half_width=5,
        half_height=1
    )
])


def get_all_items():
    return all_items


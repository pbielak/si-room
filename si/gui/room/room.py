from si.gui.room.available_items import get_all_items


class Room(object):

    def __init__(self, width, height):
        self.items = get_all_items()
        self.width = width
        self.height = height

    def __repr__(self):
        fmt_str = "Room({items})"
        return fmt_str.format(items=self.items)

    def intersects(self, first_item, second_item):
        if first_item.position.flip:
            if second_item.position.flip:
                pass
            else:
                pass
        else:
            pass

    def is_correct_position(self, item_idx, pos_x, pos_y, flip):
        item = self.items[item_idx]

        if flip:
            return pos_x - item.half_height > 0 and \
                   pos_x + item.half_height < self.width and \
                   pos_y - item.half_width > 0 and \
                   pos_y + item.half_width < self.height
        else:
            return pos_x - item.half_width > 0 and \
                   pos_x + item.half_width < self.width and \
                   pos_y - item.half_height > 0 and \
                   pos_y + item.half_height < self.height

    def move(self, item_idx, step_x, step_y):
        item = self.items[item_idx]
        if self.is_correct_position(item_idx,
                                    item.position.x + step_x,
                                    item.position.y + step_y,
                                    item.position.flip):
            item.position.x += step_x
            item.position.y += step_y

            print("Item moved to new position")
        else:
            print("Can't move item to new position")

    def flip(self, item_idx):
        item = self.items[item_idx]
        flip = item.position.flip
        if self.is_correct_position(
                item_idx, item.position.x, item.position.y,
                not flip):

            item.position.flip = not flip
            print("Item flipped")
        else:
            print("Can't flip item")

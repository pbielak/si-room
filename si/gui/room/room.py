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

    def is_correct_position(self, item, step_x, step_y, flip=None):
        if flip is None:
            flip = item.flip

        if flip:
            return item.position.x + step_x - item.half_width > 0 and \
                   item.position.x + step_x + item.half_width < self.width and \
                   item.position.y + step_y - item.half_height > 0 and \
                   item.position.y + step_y + item.half_height < self.height
        else:
            return item.position.x + step_x - item.half_height > 0 and \
                   item.position.x + step_x + item.half_height < self.width and \
                   item.position.y + step_y - item.half_width > 0 and \
                   item.position.y + step_y + item.half_width < self.height

    def move(self, item, step_x, step_y):
        self.is_correct_position(item, step_x, step_y)

    def flip(self, item):
        self.is_correct_position(item, 0, 0, not item.flip)

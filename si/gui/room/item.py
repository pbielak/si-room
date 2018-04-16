class Item(object):

    def __init__(self, name, position, half_width, half_height):
        self.name = name
        self.position = position
        self.half_width = half_width
        self.half_height = half_height

    def __repr__(self):
        fmt_str = "Item({name}, {position}, {half_width}, {half_height})"
        return fmt_str.format(name=self.name,
                              position=self.position,
                              half_width=self.half_width,
                              half_height=self.half_height)

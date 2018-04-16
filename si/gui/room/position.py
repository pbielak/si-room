class Position(object):

    def __init__(self, x, y, flip):
        self.x = x
        self.y = y
        self.flip = flip

    def __repr__(self):
        fmt_str = "Position({x}, {y}, {flip})"
        return fmt_str.format(x=self.x,
                              y=self.y,
                              flip=self.flip
                              )

class EditorCamera:

    x_offset = 0
    y_offset = 0

    def __init__(self, begin_x, begin_y):
        self.begin_x = begin_x
        self.begin_y = begin_y

    def left(self):
        if self.begin_x:
            self.x_offset -= 50
            self.begin_x -= 50

    def right(self):
        self.x_offset += 50
        self.begin_x += 50

    def up(self):
        if self.begin_y:
            self.y_offset -= 50
            self.begin_y -= 50

    def down(self):
        self.y_offset += 50
        self.begin_y += 50

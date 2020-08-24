from tkinter import Canvas, Scrollbar
from PIL import Image, ImageTk
from math import hypot


class Editor(Canvas):
    def __init__(self, img_path,  **kwargs):
        self.img = Image.open(img_path)
        self.scale = 1

        while self.img.size[0] * self.scale >= kwargs["master"].winfo_width() or self.img.size[1] * self.scale >= kwargs["master"].winfo_height():
            self.scale -= 0.05

        self.render_img = self.img.copy()
        self.render_img.thumbnail(tuple(map(lambda x: int(x * self.scale), self.img.size)), Image.ANTIALIAS)
        super(Editor, self).__init__(width=self.render_img.size[0], height=self.render_img.size[1], **kwargs)
        self.render_img = ImageTk.PhotoImage(self.render_img)

        self.offset = 2
        self.rect = []
        self.rect_points = []
        self.rect_rendered = []
        self.captured = ""

    def pack(self, **kwargs):
        super(Editor, self).pack(fill="none", expand=1, **kwargs)
        self.create_image(self.offset, self.offset, image=self.render_img, anchor="nw")

        self.bind("<Button-1>", lambda e: self.edit_rect(e) if not self.rect else self.capture(e))
        self.bind("<ButtonRelease-1>", lambda e: self.capture(e, uncapture=True))
        self.bind("<B1-Motion>", self.edit_rect)

    def edit_rect(self, event):
        x = max(min(event.x, self.img.size[0] * self.scale), 0)
        y = max(min(event.y, self.img.size[1] * self.scale), 0)

        if not self.rect:
            self.captured = "se"
            self.rect.append([x, y])
            self.rect.append([x, y])
        else:
            if "w" in self.captured:
                self.rect[0][0] = x
            elif "e" in self.captured:
                self.rect[1][0] = x
            if "n" in self.captured:
                self.rect[0][1] = y
            elif "s" in self.captured:
                self.rect[1][1] = y

        if self.rect_rendered:
            for obj in self.rect_rendered:
                self.delete(obj)
        self.rect_rendered = tuple(self.draw_rect_borders())

    def capture(self, event, uncapture=False):
        if uncapture:
            self.captured = ""
        else:
            for i, point in enumerate(self.rect_points):
                if hypot(event.x - point[0], event.y - point[1]) <= 3:
                    self.captured = ("nw", "n", "ne", "e", "se", "s", "sw", "w")[i]
                    return

    def draw_rect_borders(self):
        yield self.create_rectangle(self.rect, outline="green", width=2, dash=(10, 2))

        self.rect_points = [
            self.rect[0],
            ((self.rect[0][0] + self.rect[1][0]) / 2, self.rect[0][1]),
            (self.rect[1][0], self.rect[0][1]),
            (self.rect[1][0], (self.rect[0][1] + self.rect[1][1]) / 2),
            self.rect[1],
            ((self.rect[0][0] + self.rect[1][0]) / 2, self.rect[1][1]),
            (self.rect[0][0], self.rect[1][1]),
            (self.rect[0][0], (self.rect[0][1] + self.rect[1][1]) / 2),
        ]

        for point in self.rect_points:
            rect = [(point[0] - 3, point[1] - 3), (point[0] + 3, point[1] + 3)]
            yield self.create_rectangle(rect, fill="green", width=0)

    def crop_image(self):
        if not self.rect:
            return

        scaled_rect = [
            self.rect[0][0] / self.scale,
            self.rect[0][1] / self.scale,
            self.rect[1][0] / self.scale,
            self.rect[1][1] / self.scale
        ]

        return self.img.crop(scaled_rect)


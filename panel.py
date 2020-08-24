from tkinter import Frame, Button


class Panel(Frame):
    def __init__(self, buttons: dict, btn_offset=1, btn_width=60, **kwargs):
        super(Panel, self).__init__(**kwargs)

        self.buttons = []

        for i, btn_name in enumerate(buttons.keys()):
            btn = Button(self, text=btn_name, command=buttons[btn_name])
            btn.place(
                x=(i + 1) * btn_offset + i * btn_width,
                y=btn_offset,
                width=btn_width,
                height=kwargs["height"] - 2 * btn_offset
            )
            self.buttons.append(btn)

    def pack(self, **kwargs):
        super(Panel, self).pack(side="top", fill="x", **kwargs)

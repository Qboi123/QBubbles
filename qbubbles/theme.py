import time

import yaml

from qbubbles.gui import QScrollableFrame, QInnerLabel, QCanvasList


class ThemeManager(object):
    def __init__(self):
        pass

    def add_theme(self, theme: 'Theme'):
        self.themes[theme.name] = theme


class Theme(object):
    def __init__(self, name, style: dict, config: dict, layout: dict, options: dict):
        self.name = name
        self.style = style
        self.config = config
        self.layout = layout
        self.options = options

        self.fix_styles()
        self.fix_layout()
        # print(self.style)
        # print(self.config)
        # print(self.layout)
        # print(self.options)

    def fix_styles(self):
        for ct_key, ct_value in self.style.items():
            if "map" not in ct_value.keys():
                continue
            for ma_key, ma_value in ct_value["map"].copy().items():
                ct_value["map"][ma_key] = list(ct_value["map"][ma_key].items())

    def _fix_layout(self, layout):
        fixed_layout = layout
        for key, value in fixed_layout.copy().items():
            for key2, value2 in value.items():
                if key2 == "children":
                    fixed_layout[key][key2] = self._fix_layout(fixed_layout[key][key2])
        fixed_layout = list(fixed_layout.items())
        return fixed_layout

    def fix_layout(self):
        fixed_layout = self.layout.copy()
        # for key, value in fixed_layout.copy().items():
        #     fixed_layout[key] = self._fix_layout(fixed_layout[key])
        #     fixed_layout[key] = list(fixed_layout[key].items())
        for key, value in fixed_layout.copy().items():
            for key2, value2 in value.items():
                for key3, value3 in value2.items():
                    if key3 == "children":
                        fixed_layout[key][key2][key3] = self._fix_layout(fixed_layout[key][key2][key3])
            fixed_layout[key] = list(fixed_layout[key].items())
        # fixed_layout = list(fixed_layout.items())
        self.layout = fixed_layout

    def apply(self, master):
        from tkinter import ttk
        style = ttk.Style(master)
        if self.name in style.theme_names():
            print(f"EXECUTING: style.theme_settings({repr(self.name)}, {repr(self.style)}")
            style.theme_settings(self.name, self.style)
        else:
            print(f"EXECUTING: style.theme_create({repr(self.name)}, \"default\"), {repr(self.style)}")
            style.theme_create(self.name, "default", self.style)

        style.theme_use(self.name)
        print(yaml.safe_dump(style.layout("TLabel")))
        for key, value in self.config.items():
            print(f"EXECUTING: style.configure({repr(key)}, " + ", ".join([f"{key2}={repr(value2)}" for key2, value2 in value.items()])+")")
            style.configure(key, **value)
        for key, value in self.layout.items():
            print(f"EXECUTING: style.layout({key}, {value}")
            style.layout(key, value)
        for key, value in self.options.items():
            if "*" in key:
                raise ValueError("Option key must not contain '*'")
            type_old = key.replace(".", "*")
            type_ = "*" + type_old + "*"
            # print("LOOP A:", type_, type_old, key, value)
            for key2, value2 in value.items():
                print(f"EXECUTING: master.option_add({repr(type_ + key2)}, {repr(value2)})")
                master.option_add(type_ + key2, value2)


def get_theme(theme, style, config, layout, options, variables):
    import yaml
    import io
    with io.StringIO(variables) as file:
        variables = yaml.safe_load(file)
    with io.StringIO(theme) as file:
        theme = yaml.safe_load(file)
    # print(style[00:472])
    # print(dict((key, repr(str(value))) for key, value in variables.items()))
    style = style % {**dict((key, repr(str(value))) for key, value in variables.items())}
    with io.StringIO(style) as file:
        style = yaml.safe_load(file)
    layout = layout % {**dict((key, repr(str(value))) for key, value in variables.items())}
    with io.StringIO(layout) as file:
        layout = yaml.safe_load(file)
    config = config % {**dict((key, repr(str(value))) for key, value in variables.items())}
    with io.StringIO(config) as file:
        config = yaml.safe_load(file)
    options = options % {**dict((key, repr(str(value))) for key, value in variables.items())}
    with io.StringIO(options) as file:
        options = yaml.safe_load(file)
    return Theme(theme["id"], style, config, layout, options)


def load_theme(theme: 'Theme', master):
    theme.apply(master)


if __name__ == '__main__':
    def test_theme():
        try:
            from gui import QAccentButton
        except ImportError:
            from .gui import QAccentButton

        with open("./theme/variables.yaml", "rb") as file:
            vars = file.read().decode("utf-8")
        with open("./theme/theme.yaml", "rb") as file:
            them = file.read().decode("utf-8")
        with open("./theme/style.yaml", "rb") as file:
            styl = file.read().decode("utf-8")
        with open("./theme/config.yaml", "rb") as file:
            conf = file.read().decode("utf-8")
        with open("./theme/options.yaml", "rb") as file:
            opts = file.read().decode("utf-8")
        with open("./theme/layout.yaml", "rb") as file:
            layo = file.read().decode("utf-8")

        # print(repr(chr(0xd)))

        theme = get_theme(them, styl, conf, layo, opts, vars)

        from tkinter import ttk as _ttk
        import tkinter as _tk
        root = _tk.Tk()
        root.geometry("400x300+20+20")
        load_theme(theme, root)
        frame = _ttk.Frame(root)
        label = _ttk.Label(frame, text="TLabel")
        label.pack(pady=1)
        button = _ttk.Button(frame, text="TButton", command=lambda: print("PRESS: TButton"))
        button.pack(pady=1)
        accentbutton = QAccentButton(frame, text="QAccentButton", command=lambda: print("PRESS: QAccentButton"))
        accentbutton.pack(pady=1)
        _prog_value = 0.0
        progressbar = _ttk.Progressbar(frame, value=int(round(_prog_value, 0)))
        progressbar.pack(pady=1)

        # qscrollable_frame = QScrollableFrame(frame, width=400, contentwidth=400, contentheight=800,
        #                                      scrollbarbg="#373737", scrollbarfg="#4f4f4f", fillcontents=True,
        #                                      hscrollbar=False, vscrollbar=True)
        # qs_labels = []
        # qs_cheight = 0
        # for index in range(0, 100):
        #     _templabel = QInnerLabel(qscrollable_frame, text=f"TLabel::{index}")
        #     _templabel.pack()
        #     qs_cheight += _templabel.winfo_reqheight()
        #     qs_labels.append(_templabel)
        # qscrollable_frame.configure(contentheight=qs_cheight)
        # qscrollable_frame.pack(fill="both", expand=True)

        frame.pack(fill="both", expand=True)
        t1 = time.time()

        root2 = _tk.Tk()
        root2.geometry("1200x900")
        load_theme(theme, root2)

        frame2 = _ttk.Frame(root2)
        qcanvas_list = QCanvasList(frame2, command=lambda _c, _i: print(f"Clicked Canvas {_i}"))
        for i in range(10):
            c, _ = qcanvas_list.append(highlightthickness=0)
            c.create_text(10, 10, text=f"QCanvasListItem{{{i}}}", anchor="nw", fill="#afafaf", font=("Consolas", 100))
            qcanvas_list.pack(fill="both", expand=True)
        frame2.pack(fill="both", expand=True)

        _prog_change = 50
        while True:
            try:
                dt = time.time() - t1
                t1 = time.time()
                _prog_value += dt * _prog_change
                # print(_prog_value, _prog_change)
                if _prog_value >= 100.0:
                    _prog_change = -50
                elif _prog_value <= 0.0:
                    _prog_change = 50
                # _prog_value = _prog_value % 100.0
                progressbar.config(value=int(round(_prog_value, 0)))
                root.update()
                root.update_idletasks()
            except _tk.TclError:
                break

    test_theme()

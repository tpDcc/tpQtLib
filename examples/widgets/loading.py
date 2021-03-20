import tpDcc
from tpDcc.libs.qt.widgets import layouts, label, loading, dividers


class LoadingExample(tpDcc.Window, object):
    def __init__(self):
        super(LoadingExample, self).__init__(title='Example for Loading Widgets')

    def ui(self):
        super(LoadingExample, self).ui()

        size_lyt = layouts.HorizontalLayout()
        size_list = [
            ('Tiny', loading.CircleLoading.tiny),
            ('Small', loading.CircleLoading.small),
            ('Medium', loading.CircleLoading.medium),
            ('Large', loading.CircleLoading.large),
            ('Huge', loading.CircleLoading.huge)
        ]
        for lbl, load_widget in size_list:
            size_lyt.addWidget(label.BaseLabel(lbl))
            size_lyt.addWidget(load_widget(parent=self))
            size_lyt.addSpacing(10)

        color_lyt = layouts.HorizontalLayout()
        color_list = [
            ('cyan', '#13c2c2'),
            ('green', '#52c41a'),
            ('magenta', '#eb2f96'),
            ('red', '#f5222d'),
            ('yellow', '#fadb14'),
            ('volcano', '#fa541c'),
        ]
        for lbl, load_color in color_list:
            color_lyt.addWidget(label.BaseLabel(lbl))
            color_lyt.addWidget(loading.CircleLoading(color=load_color, parent=self))
            color_lyt.addSpacing(10)

        self.main_layout.addWidget(dividers.Divider('different size'))
        self.main_layout.addLayout(size_lyt)
        self.main_layout.addWidget(dividers.Divider('different color'))
        self.main_layout.addLayout(color_lyt)


def run():
    return LoadingExample()

from functools import partial

from Qt.QtCore import *

import tpDcc
from tpDcc.libs.qt.core import mixin
from tpDcc.libs.qt.widgets import layouts, dividers, sliders, spinbox, group


class SlidersExample(tpDcc.Window, mixin.FieldMixin):
    def __init__(self):
        super(SlidersExample, self).__init__(title='Example for Sliders')

    def ui(self):
        super(SlidersExample, self).ui()

        slider1 = sliders.BaseSlider(orientation=Qt.Horizontal)
        slider1.setRange(1, 100)
        slider2 = sliders.BaseSlider(orientation=Qt.Vertical)
        slider2.setRange(1, 100)

        lyt3 = layouts.HorizontalLayout()
        spin_box = spinbox.BaseSpinBox()
        spin_box.setRange(1, 100)
        btn_grp = group.PushButtonGroup()
        btn_grp.set_button_list([
            {'text': '+', 'clicked': partial(self._on_change_value, 10)},
            {'text': '-', 'clicked': partial(self._on_change_value, -10)}
        ])
        lyt3.addWidget(spin_box)
        lyt3.addWidget(btn_grp)
        lyt3.addStretch()

        self.register_field('percent', 20)
        self.bind('percent', spin_box, 'value', signal='valueChanged')
        self.bind('percent', slider1, 'value')
        self.bind('percent', slider2, 'value')

        self.main_layout.addWidget(dividers.Divider('different orientation'))
        self.main_layout.addWidget(slider1)
        self.main_layout.addWidget(slider2)
        self.main_layout.addWidget(dividers.Divider('data bind'))
        self.main_layout.addLayout(lyt3)

    def _on_change_value(self, value):
        self.set_field('percent', max(0, min(self.field('percent') + value, 100)))


def run():
    return SlidersExample()

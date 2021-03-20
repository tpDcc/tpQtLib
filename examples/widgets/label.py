import random

from Qt.QtCore import *

import tpDcc
from tpDcc.libs.qt.core import base, mixin
from tpDcc.libs.qt.widgets import layouts, label, buttons, dividers


class LabelExample(tpDcc.Window, mixin.FieldMixin):
    def __init__(self):
        super(LabelExample, self).__init__(title='Example for Labels')

    def ui(self):
        super(LabelExample, self).ui()

        title_lyt = layouts.GridLayout()
        title_lyt.addWidget(label.BaseLabel('Label h1').h1(), 0, 0)
        title_lyt.addWidget(label.BaseLabel('Label h2').h2(), 1, 0)
        title_lyt.addWidget(label.BaseLabel('Label h3').h3(), 2, 0)
        title_lyt.addWidget(label.BaseLabel('Label h4').h4(), 3, 0)
        title_lyt.addWidget(label.BaseLabel('Label h1').h1(), 0, 1)
        title_lyt.addWidget(label.BaseLabel('Label h2').h2(), 1, 1)
        title_lyt.addWidget(label.BaseLabel('Label h3').h3(), 2, 1)
        title_lyt.addWidget(label.BaseLabel('Label h4').h4(), 3, 1)

        text_type_lyt = base.QHBoxLayout()
        text_type_lyt.addWidget(label.BaseLabel('Label: Normal'))
        text_type_lyt.addWidget(label.BaseLabel('Label: Secondary').secondary())
        text_type_lyt.addWidget(label.BaseLabel('Label: Warning').warning())
        text_type_lyt.addWidget(label.BaseLabel('Label: Dange').danger())
        disable_text = label.BaseLabel('Label: Disabled')
        disable_text.setEnabled(False)
        text_type_lyt.addWidget(disable_text)

        mix_lyt = layouts.HorizontalLayout()
        mix_lyt.addWidget(label.BaseLabel('Label: Strong & Underline').strong().underline())
        mix_lyt.addWidget(label.BaseLabel('Label: Danger & Delete').danger().delete())
        mix_lyt.addWidget(label.BaseLabel('Label: Warning & Strong').warning().strong())
        mix_lyt.addWidget(label.BaseLabel('Label: H4 & Mark').h4().mark())

        elide_lyt = layouts.VerticalLayout()
        label_none = label.BaseLabel('This is a elide NONE mode label. Ellipsis should NOT appear in the text.')
        label_left = label.BaseLabel(
            'This is a elide LEFT mode label. '
            'The ellipsis should appear at the beginning of the text. '
            'xiao mao xiao gou xiao ci wei')
        label_left.theme_elide_mode = Qt.ElideLeft
        label_middle = label.BaseLabel(
            'This is a elide MIDDLE mode label. '
            'The ellipsis should appear in the middle of the text. '
            'xiao mao xiao gou xiao ci wei')
        label_middle.theme_elide_mode = Qt.ElideMiddle
        label_right = label.BaseLabel()
        label_right.setText('This is a elide RIGHT mode label. '
                            'The ellipsis should appear at the end of the text. '
                            'Some text to fill the line bala bala bala.')
        label_right.theme_elide_mode = Qt.ElideRight
        elide_lyt.addWidget(label_none)
        elide_lyt.addWidget(label_left)
        elide_lyt.addWidget(label_middle)
        elide_lyt.addWidget(label_right)

        text_attr_lyt = layouts.HorizontalLayout()
        text_attr_lyt.addWidget(label.BaseLabel('Label: Mark').mark())
        text_attr_lyt.addWidget(label.BaseLabel('Label: Code').code())
        text_attr_lyt.addWidget(label.BaseLabel('Label: Underline').underline())
        text_attr_lyt.addWidget(label.BaseLabel('Label: Delete').delete())
        text_attr_lyt.addWidget(label.BaseLabel('Label: Strong').strong())

        data_bind_lyt = layouts.HorizontalLayout()
        data_bind_lbl = label.BaseLabel()
        btn = buttons.BaseButton('Randon an Animal').primary()
        btn.clicked.connect(self._on_change_text)
        data_bind_lyt.addWidget(data_bind_lbl)
        data_bind_lyt.addWidget(btn)
        data_bind_lyt.addStretch()
        self.register_field('show_text', 'Guess')
        self.bind('show_text', data_bind_lbl, 'text')

        self.main_layout.addWidget(dividers.Divider('different level'))
        self.main_layout.addLayout(title_lyt)
        self.main_layout.addWidget(dividers.Divider('different type'))
        self.main_layout.addLayout(text_type_lyt)
        self.main_layout.addWidget(dividers.Divider('different property'))
        self.main_layout.addLayout(text_attr_lyt)
        self.main_layout.addWidget(dividers.Divider('mix'))
        self.main_layout.addLayout(mix_lyt)
        self.main_layout.addWidget(dividers.Divider('elide mode'))
        self.main_layout.addLayout(elide_lyt)
        self.main_layout.addStretch()

    def _on_change_text(self):
        self.set_field('show_text', random.choice(['Dog', 'Cat', 'Rabbit', 'Cow']))

    def _on_link_text(self):
        self.set_field('is_link', not self.field('is_link'))


def run():
    return LabelExample()

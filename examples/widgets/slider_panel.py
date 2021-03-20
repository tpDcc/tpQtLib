from Qt.QtGui import *

import tpDcc
from tpDcc.libs.qt.core import base, mixin
from tpDcc.libs.qt.widgets import layouts, panel, label, buttons, group, dividers


class SliderPanelExample(tpDcc.Window, mixin.FieldMixin):
    def __init__(self):
        super(SliderPanelExample, self).__init__(title='Example for Slider Panel')

    def ui(self):
        super(SliderPanelExample, self).ui()

        add_icon = tpDcc.ResourcesMgr().icon('add', color=QColor(125, 0, 0))

        self._button_grp = group.RadioButtonGroup()
        self._button_grp.set_button_list(['top', {'text': 'right', 'checked': True}, 'bottom', 'left'])

        self._open_btn_2 = buttons.BaseButton('Open', parent=self).tiny()
        lyt = layouts.HorizontalLayout()
        lyt.addWidget(self._button_grp)
        lyt.addSpacing(20)
        lyt.addWidget(self._open_btn_2)
        lyt.addStretch()

        self._new_account_btn = buttons.BaseButton(text='New account', icon=add_icon).primary()
        lyt1 = layouts.HorizontalLayout()
        lyt1.addWidget(label.BaseLabel('Submit form in drawer'))
        lyt1.addWidget(self._new_account_btn)
        lyt1.addStretch()

        self.main_layout.addWidget(dividers.Divider('Custom Placement'))
        self.main_layout.addLayout(lyt)
        self.main_layout.addWidget(dividers.Divider('Submit form in drawer'))
        self.main_layout.addLayout(lyt1)

    def setup_signals(self):
        self._open_btn_2.clicked.connect(self._on_open_button_2)
        self._new_account_btn.clicked.connect(self._on_new_account)

    def _on_open_button_2(self):
        custom_widget = base.BaseWidget()
        custom_widget.main_layout.addWidget(label.BaseLabel('Some contentes ...'))
        custom_widget.main_layout.addWidget(label.BaseLabel('Some contentes ...'))
        custom_widget.main_layout.addWidget(label.BaseLabel('Some contentes ...'))

        slider_panel = panel.SliderPanel('Basic Panel', parent=self)
        slider_panel.position = self._button_grp.get_button_group().checkedButton().text()
        slider_panel.setFixedWidth(200)
        slider_panel.set_widget(custom_widget)
        slider_panel.show()

    def _on_new_account(self):
        pass


def run():
    return SliderPanelExample()

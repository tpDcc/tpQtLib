from Qt.QtCore import *

import tpDcc
from tpDcc.libs.qt.core import base, mixin
from tpDcc.libs.qt.widgets import layouts, label, checkbox, buttons, dividers


class CheckBoxExample(tpDcc.Window, mixin.FieldMixin):
    def __init__(self):
        super(CheckBoxExample, self).__init__(title='Example for Check Boxes')

    def ui(self):
        super(CheckBoxExample, self).ui()

        maya_icon = tpDcc.ResourcesMgr().icon('maya')
        nuke_icon = tpDcc.ResourcesMgr().icon('nuke')
        houdini_icon = tpDcc.ResourcesMgr().icon('houdini')

        grid_lyt = layouts.GridLayout()
        for index, (text, state) in enumerate(
                [('Unchecked', Qt.Unchecked), ('Checked', Qt.Checked), ('Partially', Qt.PartiallyChecked)]):
            normal_cbx = checkbox.BaseCheckBox(text)
            normal_cbx.setCheckState(state)
            disabled_cbx = checkbox.BaseCheckBox(text)
            disabled_cbx.setCheckState(state)
            disabled_cbx.setEnabled(False)
            grid_lyt.addWidget(normal_cbx, 0, index)
            grid_lyt.addWidget(disabled_cbx, 1, index)

        icon_lyt = layouts.HorizontalLayout()
        for text, icon in [('maya', maya_icon), ('Nuke', nuke_icon), ('Houdini', houdini_icon)]:
            cbx_icon = checkbox.BaseCheckBox(text)
            cbx_icon.setIcon(icon)
            icon_lyt.addWidget(cbx_icon)

        bind_cbx = checkbox.BaseCheckBox('Data Bind')
        lbl = label.BaseLabel()
        btn = buttons.BaseButton('Change State')
        btn.clicked.connect(lambda: self.set_field('checked', not self.field('checked')))
        self.register_field('checked', True)
        self.register_field('checked_text', lambda: 'Yes!' if self.field('checked') else 'No!!')
        self.bind('checked', bind_cbx, 'checked', signal='stateChanged')
        self.bind('checked_text', lbl, 'text')

        self.main_layout.addWidget(dividers.Divider('Basic'))
        self.main_layout.addLayout(grid_lyt)
        self.main_layout.addWidget(dividers.Divider('Icon'))
        self.main_layout.addLayout(icon_lyt)
        self.main_layout.addWidget(dividers.Divider('Data Bind'))
        self.main_layout.addWidget(bind_cbx)
        self.main_layout.addWidget(lbl)
        self.main_layout.addWidget(btn)
        self.main_layout.addStretch()


def run():
    return CheckBoxExample()

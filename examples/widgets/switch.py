import tpDcc
from tpDcc.libs.qt.core import mixin
from tpDcc.libs.qt.widgets import layouts, switch, dividers


class SwitchExample(tpDcc.Window, mixin.FieldMixin):
    def __init__(self):
        super(SwitchExample, self).__init__(title='Example for Switch Widget')

    def ui(self):
        super(SwitchExample, self).ui()

        switch1 = switch.SwitchWidget()
        switch1.setChecked(True)
        switch2 = switch.SwitchWidget()
        switch3 = switch.SwitchWidget()
        switch3.setEnabled(False)
        lyt = layouts.HorizontalLayout()
        lyt.addWidget(switch1)
        lyt.addWidget(switch2)
        lyt.addWidget(switch3)

        size_lyt = layouts.FormLayout()
        size_lyt.addRow('Tiny', switch.SwitchWidget().tiny())
        size_lyt.addRow('Small', switch.SwitchWidget().small())
        size_lyt.addRow('Medium', switch.SwitchWidget().medium())
        size_lyt.addRow('Large', switch.SwitchWidget().large())
        size_lyt.addRow('Huge', switch.SwitchWidget().huge())

        self.main_layout.addWidget(dividers.Divider('Basic'))
        self.main_layout.addLayout(lyt)
        self.main_layout.addWidget(dividers.Divider('different size'))
        self.main_layout.addLayout(size_lyt)


def run():
    return SwitchExample()

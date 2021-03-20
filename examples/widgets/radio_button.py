import tpDcc
from tpDcc.libs.qt.core import mixin
from tpDcc.libs.qt.widgets import layouts, label, buttons, dividers


class RadioButtonExample(tpDcc.Window, mixin.FieldMixin):
    def __init__(self):
        super(RadioButtonExample, self).__init__(title='Example for Radio Buttons')

    def ui(self):
        super(RadioButtonExample, self).ui()

        folder_icon = tpDcc.ResourcesMgr().icon('folder')
        play_icon = tpDcc.ResourcesMgr().icon('play')
        user_icon = tpDcc.ResourcesMgr().icon('user')

        lyt1 = layouts.HorizontalLayout()
        lyt1.addWidget(buttons.BaseRadioButton('Maya'))
        lyt1.addWidget(buttons.BaseRadioButton('Nuke'))
        lyt1.addWidget(buttons.BaseRadioButton('Houdini'))

        cbx_single = buttons.BaseRadioButton('Single')
        cbx_single.setChecked(True)
        cbx_single.setEnabled(False)

        lyt2 = layouts.HorizontalLayout()
        cbx_icon1 = buttons.BaseRadioButton('Folder')
        cbx_icon1.setIcon(folder_icon)
        cbx_icon2 = buttons.BaseRadioButton('Play')
        cbx_icon2.setIcon(play_icon)
        cbx_icon3 = buttons.BaseRadioButton('User')
        cbx_icon3.setIcon(user_icon)
        lyt2.addWidget(cbx_icon1)
        lyt2.addWidget(cbx_icon2)
        lyt2.addWidget(cbx_icon3)

        cbx_bind = buttons.BaseRadioButton('Data Bind')
        lbl = label.BaseLabel()
        btn = buttons.BaseButton(text='Change State')
        btn.clicked.connect(lambda: self.set_field('checked', not self.field('checked')))
        self.register_field('checked', True)
        self.register_field('checked_text', lambda: 'Yes!' if self.field('checked') else 'No!')
        self.bind('checked', cbx_bind, 'checked', signal='toggled')
        self.bind('checked_text', lbl, 'text')

        self.main_layout.addWidget(dividers.Divider('Basic'))
        self.main_layout.addLayout(lyt1)
        self.main_layout.addWidget(cbx_single)
        self.main_layout.addWidget(dividers.Divider('Icon'))
        self.main_layout.addLayout(lyt2)
        self.main_layout.addWidget(dividers.Divider('Data Bind'))
        self.main_layout.addWidget(cbx_bind)
        self.main_layout.addWidget(lbl)
        self.main_layout.addWidget(btn)
        self.main_layout.addStretch()


def run():
    return RadioButtonExample()

import tpDcc
from tpDcc.libs.qt.core import base
from tpDcc.libs.qt.widgets import layouts, buttons, dividers


class ToolButtonExample(tpDcc.Window, object):
    def __init__(self):
        super(ToolButtonExample, self).__init__(title='Example for Tool Buttons')

    def ui(self):
        super(ToolButtonExample, self).ui()

        size_lyt = layouts.VerticalLayout()
        sub_lyt1 = layouts.HorizontalLayout()
        size_lyt.addLayout(sub_lyt1)

        sub_lyt1.addWidget(buttons.BaseToolButton().image('back').icon_only())
        sub_lyt1.addWidget(buttons.BaseToolButton().image('next').icon_only())
        sub_lyt1.addWidget(buttons.BaseToolButton().image('collapse').icon_only())
        sub_lyt1.addWidget(buttons.BaseToolButton().image('expand').icon_only())

        state_lyt = layouts.HorizontalLayout()
        btn1 = buttons.BaseToolButton().image('list').icon_only()
        btn1.setEnabled(False)
        btn2 = buttons.BaseToolButton().image('trash').icon_only()
        btn2.setCheckable(True)
        state_lyt.addWidget(btn1)
        state_lyt.addWidget(btn2)
        state_lyt.addStretch()

        btn_trash = buttons.BaseToolButton().image('trash').text_beside_icon()
        btn_trash.setText('Delete')
        btn_login = buttons.BaseToolButton().image('user').text_beside_icon()
        btn_login.setText('Login')
        btn_lyt = layouts.HorizontalLayout()
        btn_lyt.addWidget(btn_trash)
        btn_lyt.addWidget(btn_login)
        btn_lyt.addStretch()

        self.main_layout.addWidget(dividers.Divider('different button size'))
        self.main_layout.addLayout(size_lyt)
        self.main_layout.addWidget(dividers.Divider('disabled & checkable'))
        self.main_layout.addLayout(state_lyt)
        self.main_layout.addWidget(dividers.Divider('type=normal'))
        self.main_layout.addLayout(btn_lyt)


def run():
    return ToolButtonExample()

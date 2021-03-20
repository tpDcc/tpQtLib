import tpDcc
from tpDcc.libs.qt.widgets import layouts, buttons, dividers


class PushButtonExample(tpDcc.Window, object):
    def __init__(self):
        super(PushButtonExample, self).__init__(title='Example for Push Buttons')

    def ui(self):
        super(PushButtonExample, self).ui()

        upload_icon = tpDcc.ResourcesMgr().icon('upload')
        folder_icon = tpDcc.ResourcesMgr().icon('folder')
        ok_icon = tpDcc.ResourcesMgr().icon('ok')
        edit_icon = tpDcc.ResourcesMgr().icon('edit')
        trash_icon = tpDcc.ResourcesMgr().icon('trash')

        sub_layout_1 = layouts.HorizontalLayout()
        sub_layout_1.addWidget(buttons.BaseButton('Default'))
        sub_layout_1.addWidget(buttons.BaseButton('Primary').primary())
        sub_layout_1.addWidget(buttons.BaseButton('Success').success())
        sub_layout_1.addWidget(buttons.BaseButton('Warning').warning())
        sub_layout_1.addWidget(buttons.BaseButton('Danger').danger())

        sub_layout_2 = layouts.HorizontalLayout()
        sub_layout_2.addWidget(buttons.BaseButton('Upload', icon=upload_icon))
        sub_layout_2.addWidget(buttons.BaseButton('Submit', icon=folder_icon).primary())
        sub_layout_2.addWidget(buttons.BaseButton('Submit', icon=ok_icon).success())
        sub_layout_2.addWidget(buttons.BaseButton('Edit', icon=edit_icon).warning())
        sub_layout_2.addWidget(buttons.BaseButton('Delete', icon=trash_icon).danger())

        sub_layout_3 = layouts.HorizontalLayout()
        sub_layout_3.addWidget(buttons.BaseButton('Large').large().primary())
        sub_layout_3.addWidget(buttons.BaseButton('Medium').medium().primary())
        sub_layout_3.addWidget(buttons.BaseButton('Small').small().primary())

        disabled_button = buttons.BaseButton('Disabled')
        disabled_button.setEnabled(False)

        self.main_layout.addWidget(dividers.Divider('different type'))
        self.main_layout.addLayout(sub_layout_1)
        self.main_layout.addLayout(sub_layout_2)
        self.main_layout.addWidget(dividers.Divider('different size'))
        self.main_layout.addLayout(sub_layout_3)
        self.main_layout.addWidget(dividers.Divider('disabled'))
        self.main_layout.addWidget(disabled_button)


def run():
    return PushButtonExample()

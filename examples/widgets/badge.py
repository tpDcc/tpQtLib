import tpDcc
from tpDcc.libs.qt.core import mixin, menu
from tpDcc.libs.qt.widgets import layouts, badge, dividers, spinbox, buttons, avatar, combobox, label


class BadgeExample(tpDcc.Window, mixin.FieldMixin):
    def __init__(self):
        super(BadgeExample, self).__init__(title='Example for Badges')

    def ui(self):
        super(BadgeExample, self).ui()

        avatar_pixmap = tpDcc.ResourcesMgr().pixmap('user')

        standalone_lyt = layouts.HorizontalLayout()
        standalone_lyt.addWidget(badge.Badge.create_count(0, parent=self))
        standalone_lyt.addWidget(badge.Badge.create_count(20, parent=self))
        standalone_lyt.addWidget(badge.Badge.create_count(100, parent=self))
        standalone_lyt.addWidget(badge.Badge.create_dot(True, parent=self))
        standalone_lyt.addWidget(badge.Badge.create_text('new', parent=self))
        standalone_lyt.addStretch()

        btn = buttons.BaseToolButton().image('trash')
        new_avatar = avatar.Avatar.large(avatar_pixmap)
        btn_alert = buttons.BaseToolButton().image('notification').large()
        badge1 = badge.Badge.create_dot(True, widget=btn, parent=self)
        badge2 = badge.Badge.create_dot(True, widget=new_avatar, parent=self)
        self._badge3 = badge.Badge.create_dot(True, widget=btn_alert, parent=self)
        btn.clicked.connect(lambda: badge1._set_dot(False))

        spin_box = spinbox.BaseSpinBox()
        spin_box.setRange(0, 9999)
        spin_box.valueChanged.connect(self._on_set_count)
        spin_box.setValue(1)

        self.register_field('button1_selected', 'A')
        menu1 = menu.BaseMenu()
        menu1.set_data(['A', 'B', 'C', 'D'])
        select1 = combobox.BaseComboBox()
        select1.set_menu(menu1)
        self.bind('button1_selected', select1, 'value', signal='valueChanged')
        badge_hot = badge.Badge.create_text('hot', widget=label.BaseLabel('Hello Badge '), parent=self)

        sub_lyt1 = layouts.HorizontalLayout()
        sub_lyt1.addWidget(badge1)
        sub_lyt1.addWidget(badge2)
        sub_lyt1.addWidget(self._badge3)
        sub_lyt1.addStretch()

        sub_lyt2 = layouts.HorizontalLayout()
        sub_lyt2.addWidget(badge_hot)
        sub_lyt2.addWidget(select1)
        sub_lyt2.addStretch()

        self.main_layout.addWidget(dividers.Divider('use standalone'))
        self.main_layout.addLayout(standalone_lyt)
        self.main_layout.addWidget(dividers.Divider('different type'))
        self.main_layout.addLayout(sub_lyt1)
        self.main_layout.addWidget(spin_box)
        self.main_layout.addWidget(dividers.Divider('different type'))
        self.main_layout.addLayout(sub_lyt2)
        self.main_layout.addStretch()

    def _on_set_count(self, value):
        self._badge3.count = value


def run():
    return BadgeExample()

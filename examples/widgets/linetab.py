from Qt.QtCore import *

import tpDcc
from tpDcc.libs.qt.core import mixin
from tpDcc.libs.qt.widgets import label, dividers, tabs


class LineTabExample(tpDcc.Window, mixin.FieldMixin):
    def __init__(self):
        super(LineTabExample, self).__init__(title='Example for Line Tab')

    def ui(self):
        super(LineTabExample, self).ui()

        tab_center = tabs.MenuLineTabWidget()
        tab_center.add_tab(label.BaseLabel('test 1 ' * 10), {'text': u'Tab 1', 'image': 'user'})
        tab_center.add_tab(label.BaseLabel('test 2 ' * 10), {'image': 'calendar'})
        tab_center.add_tab(label.BaseLabel('test 3 ' * 10), u'Tab 3')
        tab_center.tool_button_group.theme_checked = False

        tab_left = tabs.MenuLineTabWidget(alignment=Qt.AlignLeft)
        tab_left.add_tab(label.BaseLabel('test 1 ' * 10), u'Tab 1')
        tab_left.add_tab(label.BaseLabel('test 2 ' * 10), u'Tab 2')
        tab_left.add_tab(label.BaseLabel('test 3 ' * 10), u'Tab 3')
        tab_left.tool_button_group.theme_checked = False

        tab_right = tabs.MenuLineTabWidget(alignment=Qt.AlignRight)
        tab_right.add_tab(label.BaseLabel('test 1 ' * 10), u'Tab 1')
        tab_right.add_tab(label.BaseLabel('test 2 ' * 10), u'Tab 2')
        tab_right.add_tab(label.BaseLabel('test 3 ' * 10), u'Tab 3')
        tab_right.tool_button_group.theme_checked = False

        self.main_layout.addWidget(dividers.Divider('Center'))
        self.main_layout.addWidget(tab_center)
        self.main_layout.addSpacing(20)
        self.main_layout.addWidget(dividers.Divider('Left'))
        self.main_layout.addWidget(tab_left)
        self.main_layout.addSpacing(20)
        self.main_layout.addWidget(dividers.Divider('Right'))
        self.main_layout.addWidget(tab_right)
        self.main_layout.addStretch()


def run():
    return LineTabExample()

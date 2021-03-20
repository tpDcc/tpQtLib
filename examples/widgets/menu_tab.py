from functools import partial

import tpDcc
from tpDcc.libs.qt.core import mixin
from tpDcc.libs.qt.widgets import tabs, label, message, badge, buttons


class MenuTabWidgetExample(tpDcc.Window, mixin.FieldMixin):
    def __init__(self):
        super(MenuTabWidgetExample, self).__init__(title='Example for Menu Tab Widgets')

    def ui(self):
        super(MenuTabWidgetExample, self).ui()

        item_list = [
            {'text': 'Overview', 'image': 'home', 'clicked': partial(message.PopupMessage.info, 'A', parent=self)},
            {'text': 'B', 'image': 'user', 'clicked': partial(message.PopupMessage.info, 'B', parent=self)},
            {'text': 'Notice', 'image': 'notification', 'clicked': partial(message.PopupMessage.info, 'C', parent=self)}
        ]

        tool_bar = tabs.MenuTabWidget()
        tool_bar.insert_widget(label.BaseLabel('Hello World!').h4().secondary().strong())
        tool_bar.append_widget(
            badge.Badge.create_dot(
                show=True, widget=buttons.BaseToolButton().image('user').icon_only().large(), parent=self))
        self._content_widget = label.BaseLabel()
        for index, data_dict in enumerate(item_list):
            tool_bar.add_menu(data_dict, index)
        tool_bar.tool_btn_grp.checked = False

        self.main_layout.addWidget(tool_bar)
        self.main_layout.addWidget(self._content_widget)


def run():
    return MenuTabWidgetExample()

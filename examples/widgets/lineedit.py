from Qt.QtCore import *

import tpDcc
from tpDcc.libs.qt.core import mixin, menu
from tpDcc.libs.qt.widgets import layouts, label, buttons, lineedit, dividers, message, combobox


class LineEditExample(tpDcc.Window, mixin.FieldMixin):
    def __init__(self):
        super(LineEditExample, self).__init__(title='Example for Line Edits')

    def ui(self):
        super(LineEditExample, self).ui()

        size_lyt = layouts.HorizontalLayout()
        line_edit_small = lineedit.BaseLineEdit().small()
        line_edit_small.setPlaceholderText('small size')
        line_edit_medium = lineedit.BaseLineEdit().medium()
        line_edit_medium.setPlaceholderText('default size')
        line_edit_large = lineedit.BaseLineEdit().large()
        line_edit_large.setPlaceholderText('large size')
        size_lyt.addWidget(line_edit_small)
        size_lyt.addWidget(line_edit_medium)
        size_lyt.addWidget(line_edit_large)

        line_edit_tool_btn = lineedit.BaseLineEdit(text='BaseToolButton')
        line_edit_tool_btn.set_prefix_widget(buttons.BaseToolButton().image('user').icon_only())
        line_edit_label = lineedit.BaseLineEdit(text='BaseLabel')
        line_lbl = label.BaseLabel('User').mark().secondary()
        line_lbl.setAlignment(Qt.AlignCenter)
        line_lbl.setFixedWidth(80)
        line_edit_label.set_prefix_widget(line_lbl)
        line_edit_btn = lineedit.BaseLineEdit('BaseButton')
        push_btn = buttons.BaseButton('Go').primary()
        line_edit_btn.set_suffix_widget(push_btn)
        search_engine_line = lineedit.BaseLineEdit().search_engine().large()
        search_engine_line.returnPressed.connect(self._on_search)
        line_edit_options = lineedit.BaseLineEdit()
        combo_box = combobox.BaseComboBox()
        option_menu = menu.BaseMenu()
        option_menu.set_separator('|')
        option_menu.set_data([r'http://', r'https://'])
        combo_box.set_menu(option_menu)
        combo_box.set_value('http://')
        combo_box.setFixedWidth(90)
        line_edit_options.set_prefix_widget(combo_box)

        self.main_layout.addWidget(dividers.Divider('different size'))
        self.main_layout.addLayout(size_lyt)
        self.main_layout.addWidget(dividers.Divider('custom prefix and suffix widget'))
        self.main_layout.addWidget(line_edit_tool_btn)
        self.main_layout.addWidget(line_edit_label)
        self.main_layout.addWidget(line_edit_btn)
        self.main_layout.addWidget(dividers.Divider('preset'))
        self.main_layout.addWidget(label.BaseLabel('error'))
        self.main_layout.addWidget(lineedit.BaseLineEdit('waring: file d:/ddd/ccc.jpg not exists.').error())
        self.main_layout.addWidget(label.BaseLabel('search'))
        self.main_layout.addWidget(lineedit.BaseLineEdit().search().small())
        self.main_layout.addWidget(label.BaseLabel('search engine'))
        self.main_layout.addWidget(search_engine_line)
        self.main_layout.addWidget(label.BaseLabel('file'))
        self.main_layout.addWidget(lineedit.BaseLineEdit().file().small())
        self.main_layout.addWidget(label.BaseLabel('folder'))
        self.main_layout.addWidget(lineedit.BaseLineEdit().folder().small())
        self.main_layout.addWidget(label.BaseLabel('options'))
        self.main_layout.addWidget(line_edit_options)
        self.main_layout.addStretch()

    def _on_search(self):
        message.PopupMessage.info('Searching ....', parent=self)


def run():
    return LineEditExample()

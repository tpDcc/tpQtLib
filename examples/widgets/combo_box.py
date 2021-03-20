import random

import tpDcc
from tpDcc.libs.qt.core import mixin, theme, menu
from tpDcc.libs.qt.widgets import layouts, combobox, dividers, label


class ComboBoxExample(tpDcc.Window, mixin.FieldMixin):
    def __init__(self):
        super(ComboBoxExample, self).__init__(title='Example for ComboBoxes')

    def ui(self):
        super(ComboBoxExample, self).ui()

        def _get_letters():
            data = ['A', 'B', 'C', 'D', 'E', 'F']
            start = random.randint(0, len(data))
            end = random.randint(start, len(data))
            return data[start:end]

        a = [{'children': [{'value': '\u6545\u5bab', 'label': '\u6545\u5bab'},
                           {'value': '\u5929\u575b', 'label': '\u5929\u575b'},
                           {'value': '\u738b\u5e9c\u4e95', 'label': '\u738b\u5e9c\u4e95'}],
              'value': u'\u5317\u4eac',
              'label': u'\u5317\u4eac'},
             {'children': [{'children': [{'value': '\u592b\u5b50\u5e99', 'label': '\u592b\u5b50\u5e99'}],
                            'value': '\u5357\u4eac',
                            'label': '\u5357\u4eac'},
                           {'children': [{'value': '\u62d9\u653f\u56ed', 'label': '\u62d9\u653f\u56ed'},
                                         {'value': '\u72ee\u5b50\u6797', 'label': '\u72ee\u5b50\u6797'}],
                            'value': '\u82cf\u5dde',
                            'label': '\u82cf\u5dde'}],
              'value': '\u6c5f\u82cf',
              'label': '\u6c5f\u82cf'}]

        current_theme = self.theme()

        self.register_field('button1_selected', 'A')
        self.register_field('button2_selected', 'A')
        self.register_field('button3_selected', '')
        self.register_field('button4_selected', '')
        self.register_field('button5_selected', '')

        menu1 = menu.BaseMenu(parent=self)
        menu1.set_data(['A', 'B', 'C', 'D'])
        menu2 = menu.BaseMenu(exclusive=False, parent=self)
        menu2.set_data(['A', 'B', 'C', 'D'])
        menu3 = menu.BaseMenu(parent=self)
        menu3.set_load_callback(_get_letters)
        menu4 = menu.BaseMenu(parent=self, cascader=True)
        menu4.set_data(a)
        menu5 = menu.BaseMenu(exclusive=False, parent=self)
        menu5.set_data(['A', 'B', 'C', 'D'])

        size_list = [
            ('Small', current_theme.small if current_theme else theme.Theme.Sizes.SMALL),
            ('Medium', current_theme.small if current_theme else theme.Theme.Sizes.MEDIUM),
            ('Large', current_theme.small if current_theme else theme.Theme.Sizes.LARGE)
        ]

        size_lyt = layouts.HorizontalLayout()
        for lbl, size in size_list:
            combo_box = combobox.BaseComboBox()
            combo_box.theme_size = size
            combo_box.set_menu(menu1)
            size_lyt.addWidget(combo_box)
            self.bind('button1_selected', combo_box, 'value', signal='valueChanged')

        select2 = combobox.BaseComboBox()
        select2.set_menu(menu2)
        self.bind('button2_selected', select2, 'value', signal='valueChanged')

        select3 = combobox.BaseComboBox()
        select3.set_menu(menu3)
        self.bind('button3_selected', select3, 'value', signal='valueChanged')

        select4 = combobox.BaseComboBox()
        select4.set_menu(menu4)
        select4.set_formatter(lambda x: ' / '.join(x))
        self.bind('button4_selected', select4, 'value', signal='valueChanged')

        select5 = combobox.BaseComboBox()
        select5.set_menu(menu5)
        select5.set_formatter(lambda x: ' & '.join(x))
        self.bind('button5_selected', select5, 'value', signal='valueChanged')

        sub_lyt1 = layouts.HorizontalLayout()
        sub_lyt1.addWidget(label.BaseLabel('Normal selection with different sizes'))
        sub_lyt1.addLayout(size_lyt)
        sub_lyt1.addStretch()
        sub_lyt2 = layouts.HorizontalLayout()
        sub_lyt2.addWidget(label.BaseLabel('Mutliple options'))
        sub_lyt2.addWidget(select2)
        sub_lyt2.addStretch()
        sub_lyt3 = layouts.HorizontalLayout()
        sub_lyt3.addWidget(label.BaseLabel('Dynamic options'))
        sub_lyt3.addWidget(select3)
        sub_lyt3.addStretch()
        sub_lyt4 = layouts.HorizontalLayout()
        sub_lyt4.addWidget(label.BaseLabel('Cascader Selection'))
        sub_lyt4.addWidget(select4)
        sub_lyt4.addStretch()
        sub_lyt5 = layouts.HorizontalLayout()
        sub_lyt5.addWidget(label.BaseLabel('Custom Screen'))
        sub_lyt5.addWidget(select5)
        sub_lyt5.addStretch()

        self.main_layout.addWidget(dividers.Divider('Select'))
        self.main_layout.addLayout(sub_lyt1)
        self.main_layout.addLayout(sub_lyt2)
        self.main_layout.addLayout(sub_lyt3)
        self.main_layout.addWidget(dividers.Divider('Custom Format'))
        self.main_layout.addLayout(sub_lyt4)
        self.main_layout.addLayout(sub_lyt5)
        self.main_layout.addStretch()


def run():
    return ComboBoxExample()

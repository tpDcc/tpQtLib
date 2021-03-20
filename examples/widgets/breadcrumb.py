from functools import partial

import tpDcc
from tpDcc.libs.qt.core import mixin
from tpDcc.libs.qt.widgets import breadcrumb, dividers, message


class BreadcrumbExample(tpDcc.Window, mixin.FieldMixin):
    def __init__(self):
        super(BreadcrumbExample, self).__init__(title='Example for Breadcrumbs')

    def ui(self):
        super(BreadcrumbExample, self).ui()

        message.PopupMessage.config(duration=1)

        entity_list = [
            {'clicked': partial(self._on_show_message, message.PopupMessage.info, 'Go to "Home Page"'),
             'image': 'home'},
            {'text': 'pl', 'clicked': partial(self._on_show_message, message.PopupMessage.info, 'Go to "pl"'),
             'image': 'user'},
            {'text': 'pl_0010', 'clicked': partial(self._on_show_message, message.PopupMessage.info, 'Go to "pl_0010')}
        ]

        no_icon_bread = breadcrumb.BreadcrumbWidget(parent=self)
        no_icon_bread.set_items(entity_list)

        separator_eq = breadcrumb.BreadcrumbWidget(separator='=>', parent=self)
        separator_eq.set_items(entity_list)

        path_bread = breadcrumb.BreadcrumbWidget(separator='/', parent=self)
        path_bread.set_from_path('C:/Users/BreadCrumb/Hello/World')

        frame_bread = breadcrumb.BreadcrumbFrame(parent=self)
        frame_bread.set_items(entity_list)

        self.main_layout.addWidget(dividers.Divider('normal'))
        self.main_layout.addWidget(no_icon_bread)
        self.main_layout.addWidget(dividers.Divider('separator =>'))
        self.main_layout.addWidget(separator_eq)
        self.main_layout.addWidget(dividers.Divider('from path'))
        self.main_layout.addWidget(path_bread)
        self.main_layout.addWidget(dividers.Divider('frame'))
        self.main_layout.addWidget(frame_bread)
        self.main_layout.addStretch()

    def _on_show_message(self, fn, config):
        fn(config, parent=self)


def run():
    return BreadcrumbExample()

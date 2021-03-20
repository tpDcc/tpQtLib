from functools import partial

import tpDcc
from tpDcc.libs.qt.core import mixin
from tpDcc.libs.qt.widgets import layouts, toast, buttons, dividers


class ToastExample(tpDcc.Window, mixin.FieldMixin):
    def __init__(self):
        super(ToastExample, self).__init__(title='Example for Toast')

    def ui(self):
        super(ToastExample, self).ui()

        btn1 = buttons.BaseButton('Normal Message').primary()
        btn2 = buttons.BaseButton('Success Message').success()
        btn3 = buttons.BaseButton('Warning Message').warning()
        btn4 = buttons.BaseButton('Error Message').danger()

        btn1.clicked.connect(partial(self._on_show_toast, toast.BaseToast.info, {'text': 'Normal'}))
        btn2.clicked.connect(partial(self._on_show_toast, toast.BaseToast.success, {'text': 'Success'}))
        btn3.clicked.connect(partial(self._on_show_toast, toast.BaseToast.warning, {'text': 'Warning'}))
        btn4.clicked.connect(partial(self._on_show_toast, toast.BaseToast.error, {'text': 'Error'}))

        sub_lyt1 = layouts.HorizontalLayout()
        sub_lyt1.addWidget(btn1)
        sub_lyt1.addWidget(btn2)
        sub_lyt1.addWidget(btn3)
        sub_lyt1.addWidget(btn4)

        loading_btn = buttons.BaseButton('Loading Toast').primary()
        loading_btn.clicked.connect(self._on_show_loading_toast)

        self.main_layout.addWidget(dividers.Divider('different type'))
        self.main_layout.addLayout(sub_lyt1)
        self.main_layout.addWidget(dividers.Divider('loading'))
        self.main_layout.addWidget(loading_btn)
        self.main_layout.addStretch()

    def _on_show_toast(self, fn, config):
        fn(parent=self, **config)

    def _on_show_loading_toast(self):
        msg = toast.BaseToast.loading('Loading', parent=self)
        msg.toastClosed.connect(partial(toast.BaseToast.success, 'Loading completed!', self))


def run():
    return ToastExample()

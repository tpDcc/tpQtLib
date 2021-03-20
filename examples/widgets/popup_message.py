from functools import partial

import tpDcc
from tpDcc.libs.qt.core import mixin
from tpDcc.libs.qt.widgets import layouts, dividers, message, buttons, group


class PopupMessageExample(tpDcc.Window, mixin.FieldMixin):
    def __init__(self):
        super(PopupMessageExample, self).__init__(title='Example for PopupMessages')

    def ui(self):
        super(PopupMessageExample, self).ui()

        btn1 = buttons.BaseButton(text='Normal Message').primary()
        btn2 = buttons.BaseButton(text='Success Message').success()
        btn3 = buttons.BaseButton(text='Warning Message').warning()
        btn4 = buttons.BaseButton(text='Error Message').danger()
        btn1.clicked.connect(partial(self._on_show_message, message.PopupMessage.info, {'text': 'Info Message'}))
        btn2.clicked.connect(partial(self._on_show_message, message.PopupMessage.success, {'text': 'Success Message'}))
        btn3.clicked.connect(partial(self._on_show_message, message.PopupMessage.warning, {'text': 'Warning Message'}))
        btn4.clicked.connect(partial(self._on_show_message, message.PopupMessage.error, {'text': 'Error Message'}))
        sub_lyt1 = layouts.HorizontalLayout()
        sub_lyt1.addWidget(btn1)
        sub_lyt1.addWidget(btn2)
        sub_lyt1.addWidget(btn3)
        sub_lyt1.addWidget(btn4)

        btn_duration = buttons.BaseButton(text='show 5s message')
        btn_duration.clicked.connect(
            partial(self._on_show_message, message.PopupMessage.info, {'text': 'Duration Message', 'duration': 5}))
        btn_closable = buttons.BaseButton(text='closable message')
        btn_closable.clicked.connect(
            partial(self._on_show_message, message.PopupMessage.info, {'text': 'Closable Message', 'closable': True}))

        btn_group = group.PushButtonGroup()
        btn_group.set_button_list([
            {'text': 'set duration to 1s', 'clicked': partial(
                self._on_set_config, message.PopupMessage.config, {'duration': 1})},
            {'text': 'set duration to 10s', 'clicked': partial(
                self._on_set_config, message.PopupMessage.config, {'duration': 10})},
            {'text': 'set top to 5', 'clicked': partial(
                self._on_set_config, message.PopupMessage.config, {'top': 5})},
            {'text': 'set top to 50', 'clicked': partial(
                self._on_set_config, message.PopupMessage.config, {'top': 50})},
        ])

        loading_btn = buttons.BaseButton('Dispaly a loading indicator')
        loading_btn.clicked.connect(self._on_show_loading)

        self.main_layout.addWidget(dividers.Divider('different type'))
        self.main_layout.addLayout(sub_lyt1)
        self.main_layout.addWidget(dividers.Divider('set duration'))
        self.main_layout.addWidget(btn_duration)
        self.main_layout.addWidget(dividers.Divider('set closable'))
        self.main_layout.addWidget(btn_closable)
        self.main_layout.addWidget(dividers.Divider('set global setting'))
        self.main_layout.addWidget(btn_group)
        self.main_layout.addWidget(loading_btn)
        self.main_layout.addStretch()

    def _on_show_message(self, fn, config):
        fn(parent=self, **config)

    def _on_set_config(self, fn, config):
        fn(**config)

    def _on_show_loading(self):
        msg = message.PopupMessage.loading('loading', parent=self)
        msg.closed.connect(partial(message.PopupMessage.success, 'Loading completed!', self))


def run():
    return PopupMessageExample()

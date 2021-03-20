from functools import partial

import tpDcc
from tpDcc.libs.qt.core import mixin
from tpDcc.libs.qt.widgets import dividers, message, group


class MessageExample(tpDcc.Window, mixin.FieldMixin):
    def __init__(self):
        super(MessageExample, self).__init__(title='Example for Messages')

    def ui(self):
        super(MessageExample, self).ui()

        self.main_layout.addWidget(dividers.Divider('different type'))
        self.main_layout.addWidget(message.BaseMessage(text='Information message', parent=self).info())
        self.main_layout.addWidget(message.BaseMessage(text='Success message', parent=self).success())
        self.main_layout.addWidget(message.BaseMessage(text='Warning message', parent=self).warning())
        self.main_layout.addWidget(message.BaseMessage(text='Error message', parent=self).error())
        self.main_layout.addWidget(dividers.Divider('closable'))
        self.main_layout.addWidget(message.BaseMessage(text='Closable message', parent=self).closable())
        self.main_layout.addWidget(dividers.Divider('data bind'))

        data_bind_msg = message.BaseMessage(parent=self)
        data_bind_msg.set_closable(True)

        self.register_field('msg', '')
        self.register_field('msg_type', message.MessageTypes.INFO)
        self.bind('msg', data_bind_msg, 'text')
        self.bind('msg_type', data_bind_msg, 'theme_type')

        button_grp = group.PushButtonGroup()
        button_grp.set_button_list([
            {'text': 'error', 'clicked': partial(self._on_change_msg, 'password is wrong', message.MessageTypes.ERROR)},
            {'text': 'success', 'clicked': partial(self._on_change_msg, 'Login success', message.MessageTypes.SUCCESS)},
            {'text': 'no more error', 'clicked': partial(self._on_change_msg, '', message.MessageTypes.ERROR)},
        ])
        self.main_layout.addWidget(button_grp)
        self.main_layout.addWidget(data_bind_msg)
        self.main_layout.addStretch()

    def _on_change_msg(self, msg_text, msg_type):
        self.set_field('msg_type', msg_type)
        self.set_field('msg', msg_text)


def run():
    return MessageExample()

from Qt.QtWidgets import *

import tpDcc
from tpDcc.libs.qt.core import base, mixin, theme
from tpDcc.libs.qt.widgets import layouts, dividers, label, card, layouts


class CardExample(tpDcc.Window, mixin.FieldMixin):
    def __init__(self):
        super(CardExample, self).__init__(title='Example for Cards')

    def ui(self):
        super(CardExample, self).ui()

        geo = QApplication.desktop().screenGeometry()
        self.setGeometry(geo.width() / 4, geo.height() / 4, geo.width() / 1.5, geo.height() / 2)

        current_theme = self.theme()

        basic_card_lyt = layouts.FlowLayout()
        basic_card_lyt.setSpacing(20)

        user_pixmap = tpDcc.ResourcesMgr().pixmap('user')
        houdini_pixmap = tpDcc.ResourcesMgr().pixmap('app_houdini')
        success_pixmap = tpDcc.ResourcesMgr().pixmap('success', color=current_theme.success_color)
        warning_pixmap = tpDcc.ResourcesMgr().pixmap('warning', color=current_theme.warning_color)
        error_pixmap = tpDcc.ResourcesMgr().pixmap('error', color=current_theme.error_color)

        for setting in [
            {'title': ''},
            {'title': 'Card Title', 'size': theme.Theme.Sizes.SMALL},
            {'title': 'Card Title', 'image': houdini_pixmap},
            {'title': 'Card Title', 'extra': 'More', 'image': houdini_pixmap},
            {'title': 'Card Title', 'extra': 'More'}
        ]:
            card0 = card.BaseCard(**setting)
            content_widget0 = base.BaseWidget()
            content_widget0.main_layout.setContentsMargins(15, 15, 15, 15)
            for i in range(4):
                content_widget0.main_layout.addWidget(label.BaseLabel('Card Content {}'.format(i + 1)))
            card0.set_widget(content_widget0)
            basic_card_lyt.addWidget(card0)

        meta_card_lyt = layouts.FlowLayout()
        meta_card_lyt.setSpacing(20)
        for setting in [
            {'title': 'Houdini', 'description': 'Side Effects Software', 'avatar': user_pixmap,
             'cover': houdini_pixmap},
            {'title': 'Autodesk Maya', 'description': '3D', 'cover': houdini_pixmap}
        ]:
            meta_card = card.MetaCard()
            meta_card.setup_data(setting)
            meta_card_lyt.addWidget(meta_card)

        task_widget = QWidget()
        task_card_lyt = layouts.VerticalLayout()
        task_widget.setLayout(task_card_lyt)
        task_scroll = QScrollArea()
        task_scroll.setWidgetResizable(True)
        task_scroll.setWidget(task_widget)
        for setting in [
            {'title': 'Task A', 'description': 'demo animation \n01/01/2020 - 01/12/2020', 'avatar': success_pixmap},
            {'title': 'Task B', 'description': 'closed task', 'avatar': error_pixmap},
            {'title': 'Task C', 'description': 'closed_task', 'avatar': warning_pixmap}
        ] * 5:
            meta_card = card.MetaCard(extra=True)
            meta_card.setup_data(setting)
            task_card_lyt.addWidget(meta_card)

        left_widget = QWidget()
        left_lyt = layouts.VerticalLayout()
        left_widget.setLayout(left_lyt)
        left_lyt.addWidget(dividers.Divider('Basic'))
        left_lyt.addLayout(basic_card_lyt)
        left_lyt.addWidget(dividers.Divider('Meta Card'))
        left_lyt.addLayout(meta_card_lyt)
        left_lyt.addStretch()

        right_widget = QWidget()
        right_lyt = layouts.VerticalLayout()
        right_widget.setLayout(right_lyt)
        right_lyt.addWidget(dividers.Divider('Meta Card Task'))
        right_lyt.addWidget(task_scroll)

        splitter = QSplitter()
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setStretchFactor(0, 80)
        splitter.setStretchFactor(1, 20)
        self.main_layout.addWidget(splitter)


def run():
    return CardExample()

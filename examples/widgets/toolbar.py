#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains examples of toolbar classes
"""

from __future__ import print_function, division, absolute_import

from Qt.QtWidgets import QWidget, QAction
from Qt.QtGui import QColor

from tpDcc.managers import resources
from tpDcc.libs.qt.core import base, contexts
from tpDcc.libs.qt.widgets import layouts, stack, lineedit, toolbar, buttons


class ToolbarExampleWidget(base.BaseWidget):

    def ui(self):
        super(ToolbarExampleWidget, self).ui()

        self._stack = stack.SlidingOpacityStackedWidget(parent=self)
        self.main_layout.addWidget(self._stack)

        for widget in [self._toolbar_example()]:
            self._stack.addWidget(widget)

    def _toolbar_example(self):

        def _collapse():
            tool_bar.collapse()

        def _set_icon_color():
            tool_bar.set_icon_color(QColor(255, 255, 0))

        toolbar_widget = QWidget(parent=self)
        toolbar_layout = layouts.VerticalLayout()
        toolbar_widget.setLayout(toolbar_layout)

        tool_bar = toolbar.ToolBar(parent=self)
        tool_bar.set_children_height(50)
        toolbar_layout.addWidget(tool_bar)
        line_edit = lineedit.BaseLineEdit(parent=self)
        line_edit.setObjectName('hello')

        collapse_action = tool_bar.addAction('Collapse')
        tool_bar.addWidget(line_edit)
        tool_bar.addAction(resources.icon('add'), 'Plus')
        color_action = QAction('Yellow', None)
        tool_bar.insertAction('Plus', color_action)

        collapse_action.triggered.connect(_collapse)
        color_action.triggered.connect(_set_icon_color)

        self.main_layout.addWidget(buttons.BaseButton('Hello'))
        self.main_layout.addStretch()

        return toolbar_widget


if __name__ == '__main__':
    import tpDcc.loader
    tpDcc.loader.init()

    with contexts.application():
        widget = ToolbarExampleWidget()
        with contexts.show_window(widget):
            pass

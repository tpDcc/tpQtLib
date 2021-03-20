#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains implementation for custom combo boxes
"""

from __future__ import print_function, division, absolute_import

from Qt.QtCore import Signal, Property, QPoint, QEvent
from Qt.QtWidgets import QSizePolicy, QComboBox

from tpDcc.libs.resources.core import theme
from tpDcc.libs.qt.core import formatters


@theme.mixin
# @mixin.cursor_mixin
# @mixin.property_mixin
class BaseComboBox(QComboBox, object):

    valueChanged = Signal(list)

    def __init__(self, parent=None):
        super(BaseComboBox, self).__init__(parent)

        self._root_menu = None
        self._display_formatter = formatters.display_formatter
        self._has_custom_view = False
        self._size = self.theme_default_size()

        self.setEditable(True)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

        line_edit = self.lineEdit()
        line_edit.setReadOnly(True)
        line_edit.setTextMargins(4, 0, 4, 0)
        line_edit.setStyleSheet('background-color: transparent;')
        line_edit.installEventFilter(self)

        self.set_value('')
        self.set_placeholder('Please Select')

    # =================================================================================================================
    # PROPERTIES
    # =================================================================================================================

    def _get_size(self):
        """
        Returns the button height size
        :return: float
        """

        return self._size

    def _set_size(self, value):
        """
        Sets button height size
        :param value: float
        """

        self._size = value
        self.lineEdit().setProperty('theme_size', value)
        self.style().polish(self)

    theme_size = Property(int, _get_size, _set_size)

    # =================================================================================================================
    # OVERRIDES
    # =================================================================================================================

    def eventFilter(self, widget, event):
        """
        Overrides base eventFilter function
        :param widget:
        :param event:
        :return:
        """

        if widget is self.lineEdit():
            if event.type() == QEvent.MouseButtonPress and self.isEnabled():
                self.showPopup()
        return super(BaseComboBox, self).eventFilter(widget, event)

    def setView(self, *args, **kwargs):
        """
        Overrides base setView function
        :param args:
        :param kwargs:
        """

        self._has_custom_view = True
        super(BaseComboBox, self).setView(*args, **kwargs)

    def showPopup(self):
        """
        Overrides base showPopup function.
        If we have a custom menu, we make sure that we show it.
        """

        if self._has_custom_view or self._root_menu is None:
            super(BaseComboBox, self).showPopup()
        else:
            QComboBox.hidePopup(self)
            self._root_menu.popup(self.mapToGlobal(QPoint(0, self.height())))

    # =================================================================================================================
    # BASE
    # =================================================================================================================

    def set_formatter(self, fn):
        """
        Sets the formatter used by combobox
        :param fn:
        :return:
        """

        self._display_formatter = fn

    def set_placeholder(self, text):
        """
        Sets the placeholder text that appears when no item is selected
        :param text: str
        """

        self.lineEdit().setPlaceholderText(text)

    def set_value(self, value):
        """
        Sets combo box value
        :param value:
        """

        self.setProperty('value', value)

    def set_menu(self, menu):
        """
        Sets combo box custom menu
        :param menu: QMenu
        """

        self._root_menu = menu
        self._root_menu.valueChanged.connect(self.valueChanged)
        self._root_menu.valueChanged.connect(self.set_value)

    def tiny(self):
        """
        Sets spin box to tiny size
        """

        widget_theme = self.theme()
        self.theme_size = widget_theme.tiny if widget_theme else theme.Theme.Sizes.TINY

        return self

    def small(self):
        """
        Sets spin box to small size
        """

        widget_theme = self.theme()
        self.theme_size = widget_theme.small if widget_theme else theme.Theme.Sizes.SMALL

        return self

    def medium(self):
        """
        Sets spin box to medium size
        """

        widget_theme = self.theme()
        self.theme_size = widget_theme.medium if widget_theme else theme.Theme.Sizes.MEDIUM

        return self

    def large(self):
        """
        Sets spin box to large size
        """

        widget_theme = self.theme()
        self.theme_size = widget_theme.large if widget_theme else theme.Theme.Sizes.LARGE

        return self

    def huge(self):
        """
        Sets spin box to huge size
        """

        widget_theme = self.theme()
        self.theme_size = widget_theme.huge if widget_theme else theme.Theme.Sizes.HUGE

        return self

    # =================================================================================================================
    # PROPERTY MIXIN SETTERS
    # =================================================================================================================

    def _set_value(self, value):
        self.lineEdit().setProperty('text', self._display_formatter(value))
        if self._root_menu:
            self._root_menu.set_value(value)

#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains base functionality for Qt widgets
"""

from __future__ import print_function, division, absolute_import

from Qt.QtCore import Qt, Property, Signal, Property
from Qt.QtWidgets import QApplication, QSizePolicy, QWidget, QFrame, QScrollArea, QWhatsThis

from tpDcc.libs.resources.core import theme
from tpDcc.libs.qt.core import qtutils, contexts as qt_contexts
from tpDcc.libs.qt.widgets import layouts


@theme.mixin
class BaseWidget(QWidget, object):
    """
    Base class for all QWidgets based items
    """

    def_use_scrollbar = False

    def __init__(self, parent=None, **kwargs):
        super(BaseWidget, self).__init__(parent=parent)

        self._size = self.theme_default_size()

        self._use_scrollbar = kwargs.get('use_scrollbar', self.def_use_scrollbar)

        self.ui()
        self.setup_signals()

    # =================================================================================================================
    # PROPERTIES
    # =================================================================================================================

    def _get_size(self):
        """
        Returns the spin box height size
        :return: float
        """

        return self._size

    def _set_size(self, value):
        """
        Sets spin box height size
        :param value: float
        """

        self._size = value
        self.style().polish(self)

    theme_size = Property(int, _get_size, _set_size)

    # =================================================================================================================
    # OVERRIDES
    # =================================================================================================================

    def keyPressEvent(self, event):
        return

    def mousePressEvent(self, event):
        modifiers = QApplication.keyboardModifiers()
        if modifiers == Qt.AltModifier:
            pos = self.mapToGlobal((self.rect().topLeft()))
            QWhatsThis.showText(pos, self.whatsThis())
        else:
            super(BaseWidget, self).mousePressEvent(event)

    # =================================================================================================================
    # BASE
    # =================================================================================================================

    def get_main_layout(self):
        """
        Function that generates the main layout used by the widget
        Override if necessary on new widgets
        :return: QLayout
        """

        return layouts.VerticalLayout(spacing=2, margins=(2, 2, 2, 2))

    def ui(self):
        """
        Function that sets up the ui of the widget
        Override it on new widgets (but always call super)
        """

        self.main_layout = self.get_main_layout()
        if self._use_scrollbar:
            layout = layouts.VerticalLayout(spacing=0, margins=(0, 0, 0, 0))
            self.setLayout(layout)
            central_widget = QWidget()
            central_widget.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
            scroll = QScrollArea()
            scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            scroll.setWidgetResizable(True)
            scroll.setFocusPolicy(Qt.NoFocus)
            layout.addWidget(scroll)
            scroll.setWidget(central_widget)
            central_widget.setLayout(self.main_layout)
            self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        else:
            self.setLayout(self.main_layout)

    def setup_signals(self):
        """
        Function that set up signals of the widget
        """

        pass

    def set_spacing(self, value):
        """
        Set the spacing used by widget's main layout
        :param value: float
        """

        self.main_layout.setSpacing(value)

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


@theme.mixin
class BaseFrame(QFrame, object):
    mouseReleased = Signal(object)

    def __init__(self, *args, **kwargs):
        super(BaseFrame, self).__init__(*args, **kwargs)

        self.ui()
        self.setup_signals()

    def mouseReleaseEvent(self, event):
        self.mouseReleased.emit(event)
        return super(BaseFrame, self).mouseReleaseEvent(event)

    def get_main_layout(self):
        """
        Function that generates the main layout used by the widget
        Override if necessary on new widgets
        :return: QLayout
        """

        return layouts.VerticalLayout(spacing=2, margins=(2, 2, 2, 2))

    def ui(self):
        """
        Function that sets up the ui of the widget
        Override it on new widgets (but always call super)
        """

        self.main_layout = self.get_main_layout()
        self.setLayout(self.main_layout)

    def setup_signals(self):
        pass


class ContainerWidget(QWidget, object):
    """
    Basic widget used a
    """

    def __init__(self, parent=None):
        super(ContainerWidget, self).__init__(parent)

        layout = layouts.HorizontalLayout(spacing=0, margins=(0, 0, 0, 0))
        self.setLayout(layout)

        self.containedWidget = None

    def set_contained_widget(self, widget):
        """
        Sets the current contained widget for this container
        :param widget: QWidget
        """

        self.containedWidget = widget
        if widget:
            widget.setParent(self)
            self.layout().addWidget(widget)

    def clone_and_pass_contained_widget(self):
        """
        Returns a clone of this ContainerWidget
        :return: ContainerWidget
        """

        cloned = ContainerWidget(self.parent())
        cloned.set_contained_widget(self.containedWidget)
        self.set_contained_widget(None)
        return cloned


class DirectoryWidget(BaseWidget, object):
    """
    Widget that contains variables to store current working directory
    """

    def __init__(self, parent=None, **kwargs):
        self._directory = None
        self._last_directory = None
        super(DirectoryWidget, self).__init__(parent=parent, **kwargs)

    def _get_directory(self):
        return self._directory

    def _set_directory(self, directory):
        with qt_contexts.block_signals(self):
            self.set_directory(directory)

    directory = Property(str, _get_directory, _set_directory)

    def get_directory(self):
        return self._directory

    def set_directory(self, directory):
        """
        Set the directory used by this widget
        :param directory: str, new directory of the widget
        """

        self._last_directory = self._directory
        self._directory = directory


class PlaceholderWidget(QWidget, object):
    """
    Basic widget that loads custom UI
    """

    def __init__(self, *args):
        super(PlaceholderWidget, self).__init__(*args)
        qtutils.load_widget_ui(self)

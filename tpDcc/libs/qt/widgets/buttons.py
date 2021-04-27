#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains different buttons
"""

from __future__ import print_function, division, absolute_import

from functools import partial

from Qt.QtCore import Qt, Signal, Property, QPoint, QSize, QRect, QTimer
from Qt.QtWidgets import QApplication, QSizePolicy, QAbstractButton, QPushButton, QToolButton, QRadioButton
from Qt.QtWidgets import QStyle, QStyleOptionButton, QStylePainter, QStyleOption
from Qt.QtGui import QCursor, QIcon, QFontMetrics, QPainter, QPainterPath, QColor, QBrush, QLinearGradient

from tpDcc import dcc
from tpDcc.managers import resources
from tpDcc.libs.python import python
from tpDcc.libs.resources.core import icon, theme
from tpDcc.libs.qt.core import consts, animation, qtutils, menu
from tpDcc.libs.qt.widgets import tooltips

# ===================================================================

NORMAL, DOWN, DISABLED = 1, 2, 3
INNER, OUTER = 1, 2

# ===================================================================


@theme.mixin
# @mixin.cursor_mixin
class BaseButton(QPushButton, object):

    class Types(object):
        DEFAULT = 'default'
        PRIMARY = 'primary'
        SUCCESS = 'success'
        WARNING = 'warning'
        DANGER = 'danger'

    def __init__(self, text='', icon=None, elided=False, parent=None):

        self._text = text
        self._elided = elided

        if not icon:
            super(BaseButton, self).__init__(text=text, parent=parent)
        else:
            super(BaseButton, self).__init__(text=text, parent=parent, icon=icon)

        self._type = self.Types.DEFAULT
        self._size = self.theme_default_size()

        # NOTE: Without this, button will not call focusIn/out events when pressed
        self.setFocusPolicy(Qt.StrongFocus)

    # =================================================================================================================
    # PROPERTIES
    # =================================================================================================================

    def _get_type(self):
        """
        Returns button type
        :return: float
        """

        return self._type

    def _set_type(self, value):
        """
        Sets button type
        :param value: str
        """

        if value in [self.Types.DEFAULT, self.Types.PRIMARY, self.Types.SUCCESS, self.Types.WARNING, self.Types.DANGER]:
            self._type = value
        else:
            raise ValueError(
                'Given button type: "{}" is not supported. Supported types '
                'are: default, primary, success, warning and danger'.format(value))
        self.style().polish(self)

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
        self.style().polish(self)

    theme_type = Property(str, _get_type, _set_type)
    theme_size = Property(int, _get_size, _set_size)

    # =================================================================================================================
    # BASE
    # =================================================================================================================

    def default(self):
        """
        Sets button to default style
        """

        self.theme_type = self.Types.DEFAULT

        return self

    def primary(self):
        """
        Sets button to primary style
        """

        self.theme_type = self.Types.PRIMARY

        return self

    def success(self):
        """
        Sets button to success style
        """

        self.theme_type = self.Types.SUCCESS

        return self

    def warning(self):
        """
        Sets button to warning style
        """

        self.theme_type = self.Types.WARNING

        return self

    def danger(self):
        """
        Sets button to danger style
        """

        self.theme_type = self.Types.DANGER

        return self

    def tiny(self):
        """
        Sets button to tiny size
        """

        widget_theme = self.theme()
        self.theme_size = widget_theme.tiny if widget_theme else theme.Theme.Sizes.TINY

        return self

    def small(self):
        """
        Sets button to small size
        """

        widget_theme = self.theme()
        self.theme_size = widget_theme.small if widget_theme else theme.Theme.Sizes.SMALL

        return self

    def medium(self):
        """
        Sets button to medium size
        """

        widget_theme = self.theme()
        self.theme_size = widget_theme.medium if widget_theme else theme.Theme.Sizes.MEDIUM

        return self

    def large(self):
        """
        Sets button to large size
        """

        widget_theme = self.theme()
        self.theme_size = widget_theme.large if widget_theme else theme.Theme.Sizes.LARGE

        return self

    def huge(self):
        """
        Sets button to huge size
        """

        widget_theme = self.theme()
        self.theme_size = widget_theme.huge if widget_theme else theme.Theme.Sizes.HUGE

        return self

    def setText(self, text):
        self._text = text
        super(BaseButton, self).setText(text)

    def resizeEvent(self, event):
        if self._elided:
            has_icon = self.icon() and not self.icon().isNull()
            if has_icon:
                font_metrics = QFontMetrics(self.font())
                elided = font_metrics.elidedText(self._text, Qt.ElideMiddle, self.width() - 30)
                super(BaseButton, self).setText(elided)
        super(BaseButton, self).resizeEvent(event)


@theme.mixin
# @mixin.cursor_mixin
class BaseRadioButton(QRadioButton, object):
    def __init__(self, *args, **kwargs):
        super(BaseRadioButton, self).__init__(*args, **kwargs)


@theme.mixin
# @mixin.cursor_mixin
class BaseToolButton(QToolButton, object):
    def __init__(self, parent=None):
        super(BaseToolButton, self).__init__(parent=parent)

        self._image = None
        self._image_theme = None
        self._size = self.theme_default_size()

        self.setAutoExclusive(False)
        self.setAutoRaise(True)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        self._polish_icon()

        self.toggled.connect(self._polish_icon)

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
        self.style().polish(self)
        if self.toolButtonStyle() == Qt.ToolButtonIconOnly:
            self.setFixedSize(self._size, self._size)

    theme_size = Property(int, _get_size, _set_size)

    # =================================================================================================================
    # OVERRIDES
    # =================================================================================================================

    def enterEvent(self, event):
        if self._image:
            theme = self.theme()
            if theme:
                accent_color = theme.accent_color
                if self._image_theme:
                    self.setIcon(resources.icon(self._image, theme=self._image_theme, color=accent_color))
                else:
                    self.setIcon(resources.icon(self._image, color=accent_color))
        return super(BaseToolButton, self).enterEvent(event)

    def leaveEvent(self, event):
        self._polish_icon()
        return super(BaseToolButton, self).leaveEvent(event)

    def _polish_icon(self, checked=None, **kwargs):
        if self._image:
            image_theme = kwargs.get('theme', self._image_theme)
            if image_theme:
                kwargs['theme'] = image_theme
            if self.isCheckable() and self.isChecked():
                self.setIcon(resources.icon(self._image, **kwargs))
            else:
                self.setIcon(resources.icon(self._image, **kwargs))

    # =================================================================================================================
    # BASE
    # =================================================================================================================

    def image(self, name, **kwargs):
        """
        Sets the name of the icon to use by the tool button
        :param str name:
        :return:
        """

        self._image = name
        self._image_theme = kwargs.get('theme', None)
        self._polish_icon(**kwargs)

        return self

    def tiny(self):
        """
        Sets tool button to tiny size
        """

        widget_theme = self.theme()
        self.theme_size = widget_theme.tiny if widget_theme else theme.Theme.Sizes.TINY

        return self

    def small(self):
        """
        Sets tool button to small size
        """

        widget_theme = self.theme()
        self.theme_size = widget_theme.small if widget_theme else theme.Theme.Sizes.SMALL

        return self

    def medium(self):
        """
        Sets tool button to medium size
        """

        widget_theme = self.theme()
        self.theme_size = widget_theme.medium if widget_theme else theme.Theme.Sizes.MEDIUM

        return self

    def large(self):
        """
        Sets tool button to large size
        """

        widget_theme = self.theme()
        self.theme_size = widget_theme.large if widget_theme else theme.Theme.Sizes.LARGE

        return self

    def huge(self):
        """
        Sets tool button to huge size
        """

        widget_theme = self.theme()
        self.theme_size = widget_theme.huge if widget_theme else theme.Theme.Sizes.HUGE

        return self

    def icon_only(self):
        """
        Sets tool button style to icon only
        """

        self.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.setFixedSize(self._size, self._size)

        return self

    def text_only(self):
        """
        Sets tool button style to icon only
        """

        self.setToolButtonStyle(Qt.ToolButtonTextOnly)

        return self

    def text_beside_icon(self):
        """
        Sets tool button style to text beside icon
        """

        self.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        return self

    def text_under_icon(self):
        """
        Sets tool button style to text under icon
        """

        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        return self


class StyleBaseButton(QPushButton, animation.BaseAnimObject):
    def __init__(self, *args, **kwargs):

        self._style = kwargs.pop('button_style', None)
        self._pad = kwargs.pop('icon_padding', 0)
        self._min_size = kwargs.pop('min_size', 8)
        self._radius = kwargs.pop('radius', 5)
        self._icon = kwargs.pop('icon', None)

        QPushButton.__init__(self, *args, **kwargs)
        animation.BaseAnimObject.__init__(self)

        self._font_metrics = QFontMetrics(self.font())
        self._border_width = kwargs.get('border_width')

        if self._icon:
            self.setIcon(self._icon)

    def paintEvent(self, event):
        if not self._style:
            super(StyleBaseButton, self).paintEvent(event)
        else:
            self._style.paintEvent(self, event)


class IconButton(StyleBaseButton, object):
    def __init__(self, icon=None, icon_padding=0, icon_min_size=8, button_style=None, parent=None):
        super(IconButton, self).__init__(button_style=button_style, parent=parent)

        self._pad = icon_padding
        self._minSize = icon_min_size

        if icon:
            self.setIcon(icon)
        self.setStyleSheet('QPushButton { background-color: rgba(255, 255, 255, 0); border:0px; }')
        self.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))

    def paintEvent(self, event):

        # If we call super paintEvent function without an style, the icon will be draw twice
        if self._style:
            super(IconButton, self).paintEvent(event)

        painter = QPainter()
        painter.begin(self)
        opt = QStyleOptionButton()
        self.initStyleOption(opt)
        rect = opt.rect
        icon_size = max(min(rect.height(), rect.width()) - 2 * self._pad, self._minSize)
        opt.iconSize = QSize(icon_size, icon_size)
        self.style().drawControl(QStyle.CE_PushButton, opt, painter, self)
        painter.end()


class CloseButton(StyleBaseButton, object):
    def __init__(self, *args, **kwargs):
        super(CloseButton, self).__init__(*args, **kwargs)

        self._radius = 10
        self._style = CloseButtonStyle()
        self.setFixedHeight(20)
        self.setFixedWidth(20)


class BaseButtonStyle(object):
    _gradient = {NORMAL: {}, DOWN: {}, DISABLED: {}}
    inner_gradient = QLinearGradient(0, 3, 0, 24)
    inner_gradient.setColorAt(0, QColor(53, 57, 60))
    inner_gradient.setColorAt(1, QColor(33, 34, 36))
    _gradient[NORMAL][INNER] = QBrush(inner_gradient)
    outer_gradient = QLinearGradient(0, 2, 0, 25)
    outer_gradient.setColorAt(0, QColor(69, 73, 76))
    outer_gradient.setColorAt(1, QColor(17, 18, 20))
    _gradient[NORMAL][OUTER] = QBrush(outer_gradient)
    inner_gradient_down = QLinearGradient(0, 3, 0, 24)
    inner_gradient_down.setColorAt(0, QColor(20, 21, 23))
    inner_gradient_down.setColorAt(1, QColor(48, 49, 51))
    _gradient[DOWN][INNER] = QBrush(inner_gradient_down)
    outer_gradient_down = QLinearGradient(0, 2, 0, 25)
    outer_gradient_down.setColorAt(0, QColor(36, 37, 39))
    outer_gradient_down.setColorAt(1, QColor(32, 33, 35))
    _gradient[DOWN][OUTER] = QBrush(outer_gradient_down)
    inner_gradient_disabled = QLinearGradient(0, 3, 0, 24)
    inner_gradient_disabled.setColorAt(0, QColor(33, 37, 40))
    inner_gradient_disabled.setColorAt(1, QColor(13, 14, 16))
    _gradient[DISABLED][INNER] = QBrush(inner_gradient_disabled)
    outer_gradient_disabled = QLinearGradient(0, 2, 0, 25)
    outer_gradient_disabled.setColorAt(0, QColor(49, 53, 56))
    outer_gradient_disabled.setColorAt(1, QColor(9, 10, 12))
    _gradient[DISABLED][OUTER] = QBrush(outer_gradient_disabled)

    @staticmethod
    def paintEvent(base_button, event):
        painter = QStylePainter(base_button)
        painter.setRenderHint(QPainter.Antialiasing)

        option = QStyleOption()
        option.initFrom(base_button)
        x = option.rect.x()
        y = option.rect.y()
        height = option.rect.height() - 1
        width = option.rect.width() - 1

        radius = base_button._radius
        gradient = BaseButtonStyle._gradient[NORMAL]
        offset = 0
        if base_button.isDown():
            gradient = BaseButtonStyle._gradient[DOWN]
            offset = 1
        elif not base_button.isEnabled():
            gradient = BaseButtonStyle._gradient[DISABLED]

        painter.setBrush(base_button._brush_border)
        painter.setPen(base_button._pens_border)
        painter.drawRoundedRect(QRect(x + 1, y + 1, width - 1, height - 1), radius, radius)

        painter.setPen(base_button._pens_clear)
        painter.setBrush(gradient[OUTER])
        painter.drawRoundedRect(QRect(x + 2, y + 2, width - 3, height - 3), radius, radius)

        painter.setBrush(gradient[INNER])
        painter.drawRoundedRect(QRect(x + 3, y + 3, width - 5, height - 5), radius - 1, radius - 1)
        painter.setBrush(base_button._brush_clear)

        text = base_button.text()
        font = base_button.font()
        text_width = base_button._font_metrics.width(text)
        text_height = font.pointSize()
        text_path = QPainterPath()
        text_path.addText((width - text_width) / 2, height - ((height - text_height) / 2) - 1 + offset, font, text)

        glow_index = base_button._glow_index
        glow_pens = base_button._glow_pens
        alignment = (Qt.AlignHCenter | Qt.AlignVCenter)
        if base_button.isEnabled():
            painter.setPen(base_button._pens_shadow)
            painter.drawPath(text_path)
            painter.setPen(base_button._pens_text)
            painter.drawText(x, y + offset, width, height, alignment, text)
            if glow_index > 0:
                for index in range(3):
                    painter.setPen(glow_pens[glow_index][index])
                    painter.drawPath(text_path)

                painter.setPen(glow_pens[glow_index][3])
                painter.drawText(x, y + offset, width, height, alignment, text)
        else:
            painter.setPen(base_button._pens_shadow_disabled)
            painter.drawPath(text_path)
            painter.setPen(base_button._pens_text_disabled)
            painter.drawText(x, y + offset, width, height, alignment, text)


class FlatButtonStyle(BaseButtonStyle, object):
    @staticmethod
    def paintEvent(base_button, event):
        painter = QStylePainter(base_button)
        painter.setRenderHint(QPainter.Antialiasing)

        option = QStyleOption()
        option.initFrom(base_button)
        x = option.rect.x()
        y = option.rect.y()
        height = option.rect.height() - 1
        width = option.rect.width() - 1

        radius = base_button._radius
        gradient = BaseButtonStyle._gradient[NORMAL]
        offset = 0
        icon_offset = 3     # TODO: maybe we want set this as a property of the base button

        if base_button.isCheckable():
            if base_button.isChecked():
                gradient = BaseButtonStyle._gradient[DOWN]
                offset = 1
        else:
            if base_button.isDown():
                gradient = BaseButtonStyle._gradient[DOWN]
                offset = 1
            elif not base_button.isEnabled():
                gradient = BaseButtonStyle._gradient[DISABLED]

        painter.setBrush(base_button._brush_border)
        painter.setPen(base_button._pens_border)
        painter.drawRoundedRect(QRect(x + 1, y + 1, width - 1, height - 1), radius, radius)

        painter.setPen(base_button._pens_clear)
        painter.setBrush(gradient[OUTER])
        painter.drawRoundedRect(QRect(x + 1, y + 1, width - 1, height - 1), radius, radius)

        painter.setBrush(gradient[INNER])
        painter.drawRoundedRect(QRect(x + 2, y + 2, width - 2, height - 2), radius - 1, radius - 1)
        painter.setBrush(base_button._brush_clear)

        text = base_button.text()
        font = base_button.font()
        text_width = base_button._font_metrics.width(text)
        text_height = font.pointSize()
        text_path = QPainterPath()

        has_icon = base_button.icon()

        if has_icon:
            if base_button.text() == '' or base_button.text() is None:
                icon_size = max(min(height, width) - 2 * base_button._pad, base_button._min_size)
                painter.drawPixmap(
                    (width - icon_size) / 2, (height - icon_size) / 2, base_button.icon().pixmap(icon_size))
            else:
                icon_size = max(min(height, width) - 2 * base_button._pad, base_button._min_size)
                painter.drawPixmap(
                    (width - icon_size - text_width) / 2, (height - icon_size) / 2,
                    base_button.icon().pixmap(icon_size))

        if has_icon:
            text_path.addText(
                (width - text_width + icon_size + icon_offset) / 2,
                height - ((height - text_height) / 2) - 1 + offset, font, text)
        else:
            text_path.addText(
                (width - text_width) / 2, height - ((height - text_height) / 2) - 1 + offset, font, text)

        glow_index = base_button._glow_index
        glow_pens = base_button._glow_pens
        alignment = (Qt.AlignHCenter | Qt.AlignVCenter)
        if base_button.isEnabled():
            painter.setPen(base_button._pens_shadow)
            painter.drawPath(text_path)
            painter.setPen(base_button._pens_text)

            if has_icon:
                painter.drawText(x + ((icon_size + icon_offset) * 0.5), y + offset, width, height, alignment, text)
            else:
                painter.drawText(x, y + offset, width, height, alignment, text)

            if glow_index > 0:
                for index in range(3):
                    painter.setPen(glow_pens[glow_index][index])
                    painter.drawPath(text_path)

                painter.setPen(glow_pens[glow_index][3])

                if has_icon:
                    painter.drawText(x + ((icon_size + icon_offset) * 0.5), y + offset, width, height, alignment, text)
                else:
                    painter.drawText(x, y + offset, width, height, alignment, text)
        else:
            painter.setPen(base_button._pens_shadow_disabled)
            painter.drawPath(text_path)
            painter.setPen(base_button._pens_text_disabled)

            if has_icon:
                painter.drawText(x + ((icon_size + icon_offset) * 0.5), y + offset, width, height, alignment, text)
            else:
                painter.drawText(x, y + offset, width, height, alignment, text)


class ButtonStyle3D(BaseButtonStyle, object):
    @staticmethod
    def paintEvent(base_button, event):
        painter = QStylePainter(base_button)
        painter.setRenderHint(QPainter.Antialiasing)

        option = QStyleOption()
        option.initFrom(base_button)
        x = option.rect.x()
        y = option.rect.y()
        height = option.rect.height() - 1
        width = option.rect.width() - 1

        radius = base_button._radius
        gradient = BaseButtonStyle._gradient[NORMAL]
        offset = 0

        if base_button.isCheckable():
            if base_button.isChecked():
                gradient = BaseButtonStyle._gradient[DOWN]
                offset = 1
        else:
            if base_button.isDown():
                gradient = BaseButtonStyle._gradient[DOWN]
                offset = 1
            elif not base_button.isEnabled():
                gradient = BaseButtonStyle._gradient[DISABLED]

        painter.setBrush(base_button._brush_border)
        painter.setPen(base_button._pens_border)
        painter.drawRoundedRect(QRect(x + 1, y + 1, width - 1, height - 1), radius, radius)

        if base_button.isCheckable():
            if base_button.isChecked():
                painter.setPen(base_button._pens_clear)
                painter.setBrush(gradient[OUTER])
                painter.drawRoundedRect(QRect(x + 1, y + 1, width - 1, height - 1), radius, radius)
            else:
                painter.setPen(base_button._pens_clear)
                painter.setBrush(gradient[OUTER])
                painter.drawRoundedRect(QRect(x + 2, y + 2, width - 2, height - 2), radius, radius)
        else:
            if base_button.isDown():
                painter.setPen(base_button._pens_clear)
                painter.setBrush(gradient[OUTER])
                painter.drawRoundedRect(QRect(x + 1, y + 1, width - 1, height - 1), radius, radius)
            else:
                painter.setPen(base_button._pens_clear)
                painter.setBrush(gradient[OUTER])
                painter.drawRoundedRect(QRect(x + 2, y + 2, width - 2, height - 2), radius, radius)

        painter.setBrush(gradient[INNER])
        painter.drawRoundedRect(QRect(x + 3, y + 3, width - 3, height - 3), radius - 1, radius - 1)
        painter.setBrush(base_button._brush_clear)

        text = base_button.text()
        font = base_button.font()
        text_width = base_button._font_metrics.width(text)
        text_height = font.pointSize()
        text_path = QPainterPath()
        text_path.addText((width - text_width) / 2, height - ((height - text_height) / 2) - 1 + offset, font, text)

        glow_index = base_button._glow_index
        glow_pens = base_button._glow_pens
        alignment = (Qt.AlignHCenter | Qt.AlignVCenter)
        if base_button.isEnabled():
            painter.setPen(base_button._pens_shadow)
            painter.drawPath(text_path)
            painter.setPen(base_button._pens_text)
            painter.drawText(x, y + offset, width, height, alignment, text)
            if glow_index > 0:
                for index in range(3):
                    painter.setPen(glow_pens[glow_index][index])
                    painter.drawPath(text_path)

                painter.setPen(glow_pens[glow_index][3])
                painter.drawText(x, y + offset, width, height, alignment, text)
        else:
            painter.setPen(base_button._pens_shadow_disabled)
            painter.drawPath(text_path)
            painter.setPen(base_button._pens_text_disabled)
            painter.drawText(x, y + offset, width, height, alignment, text)


class CloseButtonStyle(BaseButtonStyle, object):
    @staticmethod
    def paintEvent(base_button, event):
        painter = QStylePainter(base_button)
        painter.setRenderHint(QPainter.Antialiasing)

        option = QStyleOption()
        option.initFrom(base_button)
        x = option.rect.x()
        y = option.rect.y()
        height = option.rect.height() - 1
        width = option.rect.width() - 1

        gradient = BaseButtonStyle._gradient[NORMAL]
        offset = 0
        if base_button.isDown():
            gradient = BaseButtonStyle._gradient[DOWN]
            offset = 1
        elif not base_button.isEnabled():
            gradient = BaseButtonStyle._gradient[DISABLED]

        painter.setPen(base_button._pens_border)
        painter.drawEllipse(x + 1, y + 1, width - 1, height - 1)

        painter.setPen(base_button._pens_clear)
        painter.setBrush(gradient[OUTER])
        painter.drawEllipse(x + 2, y + 2, width - 3, height - 2)

        painter.setBrush(gradient[INNER])
        painter.drawEllipse(x + 3, y + 3, width - 5, height - 4)

        painter.setBrush(base_button._brush_clear)

        line_path = QPainterPath()
        line_path.moveTo(x + 8, y + 8)
        line_path.lineTo(x + 12, x + 12)
        line_path.moveTo(x + 12, y + 8)
        line_path.lineTo(x + 8, y + 12)

        painter.setPen(base_button._pens_border)
        painter.drawPath(line_path)

        glow_index = base_button._glow_index
        glow_pens = base_button._glow_pens

        if glow_index > 0:
            for index in range(3):
                painter.setPen(glow_pens[glow_index][index])
                painter.drawPath(line_path)

            painter.setPen(glow_pens[glow_index][3])
            painter.drawPath(line_path)


class ButtonStyles(object):
    BaseStyle = BaseButtonStyle()
    FlatStyle = FlatButtonStyle()
    Style3D = ButtonStyle3D()
    CloseStyle = CloseButtonStyle()

# ===================================================================


class ButtonIcons(QAbstractButton):

    highlightOffset = 40
    iconColors = (128, 128, 128)
    iconScaling = list()
    grayscale = False
    tintComposition = None

    icon = None
    idleIcon = None
    pressedIcon = None
    hoverIcon = None

    def enterEvent(self, event):
        if self.hoverIcon is not None:
            self.setIcon(self.hoverIcon)

    def leaveEvent(self, event):
        if self.idleIcon is not None:
            self.setIcon(self.idleIcon)

    def setIconSize(self, size):
        if self.idleIcon is None:
            return

        super(ButtonIcons, self).setIconSize(qtutils.size_by_dpi(size))
        self.update_icons()

    def set_highlight(self, highlight):
        self.highlightOffset = highlight

    def set_icon(self, icon, colors=None, size=None, color_offset=None, icon_scaling=None,
                 tint_composition=QPainter.CompositionMode_Plus, grayscale=False):

        if size is not None:
            self.setIconSize(QSize(size, size))

        if color_offset is not None:
            self.highlightOffset = color_offset

        if icon_scaling is not None:
            self.iconScaling = icon_scaling

        colors = colors or self.iconColors
        self.grayscale = grayscale
        self.tintComposition = tint_composition

        self.icon = icon
        self.set_icon_color(colors, update=False)
        self.update_icons()

    def set_icon_color(self, colors, update=True):
        if any(isinstance(el, list) for el in colors):
            self.iconColors = colors
        else:
            self.iconColors = [python.force_list(colors)]
        if update and self.idleIcon is not None and self.icon is not None:
            self.update_icons()

    def update_icons(self):
        if not self.icon:
            return

        hover_color = (255, 255, 255, self.highlightOffset)

        self.idleIcon = icon.colorize_layered_icon(
            icons=self.icon, size=self.iconSize().width(), icon_scaling=self.iconScaling,
            tint_composition=self.tintComposition, colors=self.iconColors, grayscale=self.grayscale
        )

        self.hoverIcon = icon.colorize_layered_icon(
            icons=self.icon, size=self.iconSize().width(), icon_scaling=self.iconScaling,
            tint_composition=self.tintComposition, tint_color=hover_color, grayscale=self.grayscale
        )

        self.setIcon(self.idleIcon)

    def set_icon_idle(self, idle_icon):
        self.idleIcon = idle_icon
        self.setIcon(idle_icon)

    def set_icon_hover(self, hover_icon):
        self.hoverIcon = hover_icon


class BaseMenuButton(QPushButton, ButtonIcons):

    class SearchMenu(menu.SearchableMenu, object):
        def __init__(self, **kwargs):
            super(BaseMenuButton.SearchMenu, self).__init__(**kwargs)

            self._tt_key_pressed = False
            self._tt_key = Qt.Key_Control

        def keyPressEvent(self, event):
            if event.key() == self._tt_key:
                pos = self.mapFromGlobal(QCursor.pos())
                action = self.actionAt(pos)
                if tooltips.has_expanded_tooltips(action):
                    self._popup_tooltip = tooltips.ExpandedTooltipPopup(
                        widget=action, icon_size=qtutils.dpi_scale(40), popup_release=self._tt_key)
                    self._tt_key_pressed = True
            super(BaseMenuButton.SearchMenu, self).keyPressEvent(event)

        def keyReleaseEvent(self, event):
            if event.key() == Qt.Key_Control:
                self._tt_key_pressed = False

        def index(self, name, exclude_search=True):
            for i, a in enumerate(self.actions()):
                if a.text() == name:
                    ret = i
                    if exclude_search:
                        ret -= 2
                    return ret

    leftClicked = Signal()
    middleClicked = Signal()
    rightClicked = Signal()

    leftDoubleClicked = Signal()
    middleDoubleClicked = Signal()
    rightDoubleClicked = Signal()
    clicked = leftClicked

    menuAboutToShow = Signal()
    middleMenuAboutToShow = Signal()
    rightMenuAboutToShow = Signal()

    menuChanged = Signal()
    middleMenuChanged = Signal()
    rigthMenuChanged = Signal()

    actionTriggered = Signal(object, object)

    SINGLE_CLICK = 1
    DOUBLE_CLICK = 2

    highlightOffset = 4

    def __init__(self, icon=None, icon_hover=None, text=None, parent=None, double_click_enabled=False,
                 menu_padding=5, menu_align=Qt.AlignLeft):
        """

        :param icon:
        :param icon_hover:
        :param text:
        :param parent:
        :param double_click_enabled:
        """

        self.idleIcon = icon or QIcon()
        self.hoverIcon = icon_hover or QIcon()

        super(BaseMenuButton, self).__init__(icon=self.idleIcon, text=text, parent=parent)

        self._menu_active = {
            Qt.LeftButton: True,
            Qt.MidButton: True,
            Qt.RightButton: True
        }

        self._click_menu = {
            Qt.LeftButton: None,
            Qt.MidButton: None,
            Qt.RightButton: None
        }

        self._menu_searchable = {
            Qt.LeftButton: False,
            Qt.MidButton: False,
            Qt.RightButton: False
        }

        self._last_click = None
        self._icon_color = None
        self._menu_padding = menu_padding
        self._menu_align = menu_align

        self.leftClicked.connect(partial(self._on_context_menu, Qt.LeftButton))
        self.middleClicked.connect(partial(self._on_context_menu, Qt.MidButton))
        self.rightClicked.connect(partial(self._on_context_menu, Qt.RightButton))

        app = QApplication.instance()
        if app and hasattr(app, 'doubleClickInterval') and callable(app.doubleClickInterval):
            self._double_click_interval = QApplication.instance().doubleClickInterval()
        else:
            self._double_click_interval = 500
        self._double_click_enabled = double_click_enabled

    @property
    def double_click_interval(self, interval=150):
        return self._double_click_interval

    @double_click_interval.setter
    def double_click_interval(self, interval=150):
        self._double_click_interval = interval

    @property
    def double_click_enabled(self):
        return self._double_click_enabled

    @double_click_enabled.setter
    def double_click_enabled(self, enabled):
        self._double_click_enabled = enabled

    def setWindowTitle(self, window_title, mouse_menu=Qt.LeftButton):
        new_menu = self.menu(mouse_menu, searchable=self.is_searchable(mouse_menu))
        new_menu.setWindowTitle(window_title)

    def setMenu(self, menu, mouse_button=Qt.LeftButton):
        self._click_menu[mouse_button] = menu

    def setFixedHeight(self, height):
        return super(BaseMenuButton, self).setFixedHeight(qtutils.dpi_scale(height))

    def setFixedWidth(self, width):
        return super(BaseMenuButton, self).setFixedWidth(qtutils.dpi_scale(width))

    def setFixedSize(self, size):
        super(BaseMenuButton, self).setFixedSize(qtutils.dpi_scale(size))

    def mousePressEvent(self, event):
        if event.button() == Qt.MidButton:
            self.setDown(True)
        elif event.button() == Qt.RightButton:
            self.setDown(True)

        self._last_click = self.SINGLE_CLICK

    def mouseReleaseEvent(self, event):
        button = event.button()
        self.setDown(False)
        if not self._double_click_enabled:
            self.mouse_single_click_action(button)
            return

        if self._last_click == self.SINGLE_CLICK:
            QTimer.singleShot(self._double_click_interval, lambda: self.mouse_single_click_action(button))
        else:
            self.mouseDoubleClickAction(event.button())

    def mouseDoubleClickEvent(self, event):
        self._last_click = self.DOUBLE_CLICK

    def menu(self, mouse_menu=Qt.LeftButton, searchable=False, auto_create=True, parent=None):
        """
        Overrides base menu function
        Get menu depending on the mouse button pressed
        :param mouse_menu:
        :param searchable:
        :param auto_create:
        :return:
        """

        if not self._click_menu[mouse_menu] and auto_create:
            self._click_menu[mouse_menu] = BaseMenuButton.SearchMenu(
                objectName='searchButton', title='Search Button', parent=parent)
            self._click_menu[mouse_menu].triggered.connect(lambda action: self.actionTriggered.emit(action, mouse_menu))
            self._click_menu[mouse_menu].triggered.connect(partial(self._on_menu_changed, mouse_menu))
            if not searchable:
                self._click_menu[mouse_menu].set_search_visible(False)

        return self._click_menu[mouse_menu]

    def index(self, name, mouse_menu=Qt.LeftButton):
        """
        Returns the index of the menu or action item
        :param name: str
        :param mouse_menu:
        :return: int
        """

        return self.menu(mouse_menu).index(name)

    def mouse_single_click_action(self, button):
        if self._last_click == self.SINGLE_CLICK or self._double_click_enabled is False:
            if button == Qt.LeftButton:
                self.leftClicked.emit()
            elif button == Qt.MidButton:
                self.middleClicked.emit()
            elif button == Qt.RightButton:
                self.rightClicked.emit()

    def mouse_double_click_action(self, button):
        if button == Qt.LeftButton:
            self.leftDoubleClicked.emit()
        elif button == Qt.MidButton:
            self.middleDoubleClicked.emit()
        elif button == Qt.RightButton:
            self.rightDoubleClicked.emit()

    def set_searchable(self, mouse_menu=Qt.LeftButton, searchable=True):
        """
        Sets whether menu with given mouse interaction is searchable or not
        :param mouse_menu:
        :param searchable: bool
        """

        self._menu_searchable[mouse_menu] = searchable
        if self._click_menu[mouse_menu]:
            self._click_menu[mouse_menu].set_search_visible(searchable)

    def is_searchable(self, mouse_menu=Qt.LeftButton):
        """
        Returns whether given button menu is searchable or not
        :param mouse_menu:
        """

        if self._click_menu[mouse_menu] is not None:
            return self._click_menu[mouse_menu].search_visible()

        return self._menu_searchable[mouse_menu]

    def set_tear_off_enabled(self, mouse_menu=Qt.LeftButton, tear_off=True):
        menu = self.menu(mouse_menu, searchable=self.is_searchable(mouse_menu))
        menu.setTearOffEnabled(tear_off)

    def set_menu_align(self, align=Qt.AlignLeft):
        self._menu_align = align

    def clear_menu(self, mouse_menu):
        if self._click_menu[mouse_menu] is not None:
            self._click_menu[mouse_menu].clear()

    def addAction(
            self, name, mouse_menu=Qt.LeftButton, connect=None, checkable=False, checked=True,
            action=None, action_icon=None, data=None, icon_text=None, icon_color=None, icon_size=16):
        """
        Overrides base addAction function
        Adds a new menu item through an action
        :param name: str, name of the menu item
        :param mouse_menu: button that will launch menu (Qt.LeftButton or Qt.MidButton or Qt.RightButton)
        :param connect: fn, function to launch when the item is pressed
        :param checkable: bool, Whether or not this menu is checkable
        :param checked: bool, Whether or not this menu is checked by default
        :param action:
        :param action_icon:
        :param data:
        :param icon_text:
        :param icon_color:
        :param icon_size:
        :return:
        """

        new_menu = self.menu(mouse_menu, searchable=False)
        if action is not None:
            new_menu.addAction(action)
            return

        new_action = menu.SearchableTaggedAction(label=name, parent=new_menu)
        new_action.setCheckable(checkable)
        new_action.setChecked(checked)
        new_action.tags = set(self._string_to_tags(name))
        new_action.setData(data)
        new_menu.addAction(new_action)

        if action_icon is not None:
            if isinstance(action_icon, QIcon):
                new_action.setIcon(action_icon)
                new_action.setIconText(icon_text or '')
            elif python.is_string(action_icon):
                new_action.setIconText(action_icon or icon_text or None)
                action_icon = resources.icon(action_icon)
                new_action.setIcon(
                    icon.colorize_layered_icon(action_icon, colors=[icon_color], size=qtutils.dpi_scale(icon_size)))

        if connect is not None:
            if checkable:
                new_action.triggered.connect(partial(connect, new_action))
            else:
                new_action.triggered.connect(connect)

        return new_action

    def add_separator(self, mouse_menu=Qt.LeftButton):
        new_menu = self.menu(mouse_menu)
        new_menu.addSeparator()

    def launch_context_menu(self, mouse_btn):
        menu = self._click_menu[mouse_btn]

        if menu is not None and self._menu_active[mouse_btn]:
            pos = self.menu_pos(widget=menu, align=self._menu_align)
            menu.exec_(pos)
            # add focuss
            # menu.search_edit.focus()

    def menu_pos(self, widget=None, align=Qt.AlignLeft):
        """
        Returns menu position based on the current widget position and size
        :param widget: QWidget, widget to culculate the width based off
        :param align:  Qt.Alignleft or Qt.AlignRight, whether to align menu left or right
        :return:
        """

        pos = 0

        if align == Qt.AlignLeft:
            point = self.rect().bottomLeft() - QPoint(0, -self._menu_padding)
            pos = self.mapToGlobal(point)
        elif align == Qt.AlignRight:
            point = self.rect().bottomRight() - QPoint(widget.sizeHint().width(), -self._menu_padding)
            pos = self.mapToGlobal(point)

        return pos

    def _string_to_tags(self, string):
        res = list()
        res += string.split(' ')
        res += [s.lower() for s in string.split(' ')]

        return res

    def _on_context_menu(self, mouse_btn):
        self.launch_context_menu(mouse_btn=mouse_btn)

    def _on_menu_changed(self, mouse_button, object):
        if mouse_button == Qt.LeftButton:
            self.menuChanged.emit()
        elif mouse_button == Qt.MiddleButton:
            self.middleMenuChanged.emit()
        elif mouse_button == Qt.RightButton:
            self.rigthMenuChanged.emit()


class IconMenuButton(BaseMenuButton, object):

    itemChanged = Signal()

    def __init__(self, icon=None, icon_hover=None, parent=None, double_click_enabled=False, color=(255, 255, 255),
                 icon_menu_state_str='', icon_menu_state_int=0):
        super(IconMenuButton, self).__init__(
            icon=icon, icon_hover=icon_hover, parent=parent, double_click_enabled=double_click_enabled)

        self._icon_color = color
        self._current_menu_item_str = icon_menu_state_str
        self._current_menu_index_int = icon_menu_state_int
        self._menu_name_list = list()
        self._menu_icon_list = list()

        for m in self._click_menu.values():
            if m is not None:
                m.setToolTipsVisible(True)

            self.set_menu_align(Qt.AlignRight)

    @property
    def current_menu_item(self):
        return self._current_menu_item_str

    @property
    def current_menu_index(self):
        return self._current_menu_index_int

    def set_menu_name(self, menu_item_name):
        self._current_menu_item_str = menu_item_name
        self._current_menu_index_int = self._menu_name_list.index(menu_item_name)
        icon_name = self._menu_icon_list[self._current_menu_index_int]

    def icon_and_menu_name_lists(self, mode_list):
        self._menu_name_list = list()
        self._menu_icon_list = list()
        for i, m in enumerate(mode_list):
            self._menu_name_list.append(m[1])
            self._menu_icon_list.append(m[0])


class HoverButton(QPushButton, object):
    """
    Button widget that allows to setup different icons during mouse interaction
    """

    def __init__(self, icon=None, hover_icon=None, pressed_icon=None, parent=None):
        super(HoverButton, self).__init__(parent)

        self._idle_icon = icon
        self._hover_icon = hover_icon
        self._pressed_icon = pressed_icon
        self._mouse_pressed = False
        self._higlight_offset = 40

        self.setIcon(self._idle_icon)

    def enterEvent(self, event):
        if self._hover_icon is not None:
            self.setIcon(self._hover_icon)
        super(HoverButton, self).enterEvent(event)

    def leaveEvent(self, event):
        if self._idle_icon is not None:
            self.setIcon(self._idle_icon)
        super(HoverButton, self).leaveEvent(event)

    def mousePressEvent(self, event):
        if self.rect().contains(event.pos()):
            if self._pressed_icon:
                self.setIcon(self._pressed_icon)
            self._mouse_pressed = True
        super(HoverButton, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if not self.rect().contains(event.pos()):
            self.setIcon(self._idle_icon)
        else:
            if self._mouse_pressed:
                if self._pressed_icon:
                    self.setIcon(self._pressed_icon)

        super(HoverButton, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.rect().contains(event.pos()):
            self.setIcon(self._hover_icon)
        else:
            self.setIcon(self._idle_icon)
        self._mouse_pressed = False
        super(HoverButton, self).mouseReleaseEvent(event)


class ColorButton(QPushButton, object):

    colorChanged = Signal()

    def __init__(self, color_r=1.0, color_g=0.0, color_b=0.0, parent=None, **kwargs):
        super(ColorButton, self).__init__(parent=parent, **kwargs)
        self._color = QColor.fromRgbF(color_r, color_g, color_b)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
        self._update_color()

        self.clicked.connect(self.show_color_editor)

    def get_color(self):
        return self._color

    def set_color(self, color):
        self._color = color
        self._update_color()

    def show_color_editor(self):
        if dcc.is_maya():
            import maya.cmds as cmds
            cmds.colorEditor(rgbValue=(self._color.redF(), self._color.greenF(), self._color.blueF()))
            if not cmds.colorEditor(query=True, result=True):
                return
            new_color = cmds.colorEditor(query=True, rgbValue=True)
            self.color = QColor.fromRgbF(new_color[0], new_color[1], new_color[2])
            self.colorChanged.emit()
        else:
            raise RuntimeError('Code Editor is not available for DCC: {}'.format(dcc.get_name()))

    def _update_color(self):
        self.setStyleSheet(
            'background-color:rgb({0},{1},{2});'.format(
                self._color.redF() * 255, self._color.greenF() * 255, self._color.blueF() * 255))

    color = property(get_color, set_color)


def get_axis_button(axis_type='x', parent=None, as_tool_button=True):
    axis = axis_type.lower() if axis_type else 'x'
    axis = axis if axis in consts.AXISES else 'x'
    if as_tool_button:
        axis_btn = BaseToolButton(parent=parent)
    else:
        axis_btn = BaseButton(parent=parent)
    axis_icon = resources.icon('{}_axis'.format(axis), color=QColor(*consts.AXISES[axis]))
    axis_btn.setIcon(axis_icon)

    return axis_btn

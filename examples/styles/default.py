from Qt.QtCore import Qt
from Qt.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QCheckBox, QDockWidget, QGroupBox


class BaseWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super(BaseWidget, self).__init__(*args, **kwargs)

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Label
        label_tooltip = QLabel('I have a tooltip', self)
        label_tooltip.setToolTip('Hello ToolTip!')

        # Button
        normal_button = QPushButton('Normal', self)
        disabled_button = QPushButton('Disabled', self)
        disabled_button.setEnabled(False)

        # CheckBox
        checkboxes_layout = QHBoxLayout()
        checkbox_on = QCheckBox('On', self)
        checkbox_on.setChecked(True)
        checkbox_off = QCheckBox('Off', self)
        checkbox_on_disabled = QCheckBox('On', self)
        checkbox_on_disabled.setChecked(True)
        checkbox_on_disabled.setEnabled(False)
        checkbox_off_disabled = QCheckBox('Off', self)
        checkbox_off_disabled.setEnabled(False)
        checkbox_tri_state = QCheckBox('TriState', self)
        checkbox_tri_state.setTristate(True)
        checkboxes_layout.addWidget(checkbox_on)
        checkboxes_layout.addWidget(checkbox_off)
        checkboxes_layout.addWidget(checkbox_on_disabled)
        checkboxes_layout.addWidget(checkbox_off_disabled)
        checkboxes_layout.addWidget(checkbox_tri_state)

        # GroupBox
        group_box = QGroupBox(self)
        group_box_layout = QVBoxLayout()
        group_box.setLayout(group_box_layout)
        group_button = QPushButton('GrupBox Button')
        group_box_layout.addWidget(group_button)

        # Dock Widget
        dock_label = QLabel('Hello Dock!', self)
        dock_widget = QDockWidget(self)
        dock_widget.setWidget(dock_label)
        self.parent().addDockWidget(Qt.BottomDockWidgetArea, dock_widget)

        self.main_layout.addWidget(label_tooltip)
        self.main_layout.addWidget(normal_button)
        self.main_layout.addWidget(disabled_button)
        self.main_layout.addLayout(checkboxes_layout)
        self.main_layout.addWidget(group_box)
        self.main_layout.addStretch()


if __name__ == '__main__':

    from Qt.QtWidgets import QMainWindow

    import tpDcc.loader
    from tpDcc.managers import resources
    from tpDcc.libs.qt.core import contexts

    tpDcc.loader.init()

    with contexts.application():
        default_theme = resources.theme('default')
        window = QMainWindow()
        widget = BaseWidget(window)
        window.setCentralWidget(widget)
        window.statusBar().showMessage('Status Bar')
        window.setStyleSheet(default_theme.stylesheet())
        window.show()

import tpDcc
from tpDcc.libs.qt.core import base, mixin
from tpDcc.libs.qt.widgets import layouts, dividers, spinbox, datetime


class SpinBoxExample(tpDcc.Window, mixin.FieldMixin):
    def __init__(self):
        super(SpinBoxExample, self).__init__(title='Example for SpinBoxes')

    def ui(self):
        super(SpinBoxExample, self).ui()

        class_list = [
            spinbox.BaseSpinBox, spinbox.BaseDoubleSpinBox,
            datetime.BaseDateTimeEdit, datetime.BaseDateEdit, datetime.BaseTimeEdit
        ]

        for cls in class_list:
            self.main_layout.addWidget(dividers.Divider(cls.__name__))
            lyt = layouts.HorizontalLayout()
            lyt.addWidget(cls().small())
            lyt.addWidget(cls().medium())
            lyt.addWidget(cls().large())
            self.main_layout.addLayout(lyt)

        extra_spinners_lyt1 = layouts.HorizontalLayout()
        spn1 = spinbox.BaseSpinBoxNumber(parent=self)
        spn2 = spinbox.BaseDoubleNumberSpinBox(parent=self)

        extra_spinners_lyt2 = layouts.HorizontalLayout()
        spn3 = spinbox.DragDoubleSpinBox(parent=self)
        spn4 = spinbox.DragDoubleSpinBoxLine(parent=self)

        extra_spinners_lyt1.addWidget(spn1)
        extra_spinners_lyt1.addWidget(spn2)
        extra_spinners_lyt2.addWidget(spn3)
        extra_spinners_lyt2.addWidget(spn4)

        self.main_layout.addWidget(dividers.Divider('Extra Base'))
        self.main_layout.addLayout(extra_spinners_lyt1)

        self.main_layout.addWidget(dividers.Divider('Draggable'))
        self.main_layout.addLayout(extra_spinners_lyt2)

        self.main_layout.addWidget(dividers.Divider('Pop calendar widget'))
        date_time_edit = datetime.BaseDateTimeEdit()
        date_time_edit.setCalendarPopup(True)
        date_edit = datetime.BaseDateEdit()
        date_edit.setCalendarPopup(True)
        time_edit = datetime.BaseTimeEdit()
        time_edit.setCalendarPopup(True)
        date_lyt = layouts.HorizontalLayout()
        date_lyt.addWidget(date_time_edit)
        date_lyt.addWidget(time_edit)
        date_lyt.addWidget(date_edit)
        self.main_layout.addLayout(date_lyt)
        self.main_layout.addStretch()


def run():
    return SpinBoxExample()

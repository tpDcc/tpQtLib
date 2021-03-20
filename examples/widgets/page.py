import tpDcc
from tpDcc.libs.qt.widgets import page, dividers


class PageExample(tpDcc.Window):
    def __init__(self):
        super(PageExample, self).__init__(title='Example for Pages')

    def ui(self):
        super(PageExample, self).ui()

        page1 = page.Page()
        page1.set_total(255)

        page2 = page.Page()
        page2.set_total(100)

        self.main_layout.addWidget(dividers.Divider())
        self.main_layout.addWidget(page1)
        self.main_layout.addWidget(dividers.Divider())
        self.main_layout.addWidget(page2)
        self.main_layout.addStretch()


def run():
    return PageExample()

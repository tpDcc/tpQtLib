from Qt.QtCore import *

import tpDcc
from tpDcc.libs.qt.core import mixin
from tpDcc.libs.qt.widgets import layouts, label, browser, dividers


class BrowserExample(tpDcc.Window, mixin.FieldMixin):
    def __init__(self):
        super(BrowserExample, self).__init__(title='Example for Browsers')

    def ui(self):
        super(BrowserExample, self).ui()

        browser1 = browser.ClickBrowserFileButton('Browse File PushButton', parent=self).primary()
        browser2 = browser.ClickBrowserFolderButton('Browse Folder PushButton', parent=self)
        browser2.setIcon(tpDcc.ResourcesMgr().icon('upload'))
        browser3 = browser.ClickBrowserFileButton('Browse Multi Files', multiple=True, parent=self).primary()
        browser4 = browser.ClickBrowserFileToolButton().huge()
        lbl4 = label.BaseLabel()
        lbl4._set_elide_mode(Qt.ElideMiddle)
        browser4.fileChanged.connect(lbl4.setText)
        browser5 = browser.ClickBrowserFolderToolButton().huge()
        lbl5 = label.BaseLabel()
        lbl5._set_elide_mode(Qt.ElideMiddle)
        browser5.folderChanged.connect(lbl5.setText)
        browser6 = browser.DragFileButton('Click or drag file here')
        browser6.image = 'attachment'
        lbl6 = label.BaseLabel()
        lbl6._set_elide_mode(Qt.ElideMiddle)
        browser6.fileChanged.connect(lbl6.setText)
        browser7 = browser.DragFolderButton()
        lbl7 = label.BaseLabel()
        lbl7._set_elide_mode(Qt.ElideMiddle)
        browser7.folderChanged.connect(lbl7.setText)
        browser8 = browser.DragFileButton('Click or drag media file here')
        browser8.image('video_file')
        browser8.filters = ['.mov', '.mp4']
        lbl8 = label.BaseLabel()
        lbl8._set_elide_mode(Qt.ElideRight)
        self.register_field('current_file', '')
        self.bind('current_file', browser8, 'path', signal='fileChanged')
        self.bind('current_file', lbl8, 'text')

        lyt1 = layouts.HorizontalLayout()
        lyt1.addWidget(browser1)
        lyt1.addWidget(browser2)
        lyt1.addWidget(browser3)

        lyt2 = layouts.HorizontalLayout()
        lyt2.addWidget(lbl4)
        lyt2.addWidget(browser4)
        lyt2.addWidget(lbl5)
        lyt2.addWidget(browser5)

        lyt3 = layouts.GridLayout()
        lyt3.addWidget(browser6, 2, 0)
        lyt3.addWidget(lbl6, 3, 0)
        lyt3.addWidget(browser7, 2, 1)
        lyt3.addWidget(lbl7, 3, 1)

        self.main_layout.addWidget(dividers.Divider('ClickBrowserFileButton'))
        self.main_layout.addLayout(lyt1)
        self.main_layout.addWidget(dividers.Divider('ClickBrowserToolButton'))
        self.main_layout.addLayout(lyt2)
        self.main_layout.addWidget(dividers.Divider('DragBrowserToolButton'))
        self.main_layout.addLayout(lyt3)
        self.main_layout.addWidget(dividers.Divider('data bind'))
        self.main_layout.addWidget(browser8)
        self.main_layout.addWidget(lbl8)
        self.main_layout.addStretch()


def run():
    return BrowserExample()

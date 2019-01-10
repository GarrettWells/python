import praw
import sys
import threading
from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import pyqtSignal as signal
from PyQt5.QtCore import pyqtSlot as slot
from PyQt5.QtCore import QEvent
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QApplication

from MyQStackedWidget import MyQStackedWidget

class GUI(QtWidgets.QMainWindow):
    _CLIENT_ID = '_xDtKsMYoPzvVA'
    _CLIENT_SECRET = 'ycpN023w7z7jhBGlr120UfUCYps'
    _USER_AGENT = 'Python:Sale Finder:1.0.0 (by /u/sugartits1122)'
    _USERNAME = 'sugartits1122'
    _PASSWORD = 'dominguez1*'

    def __init__(self):
        super(GUI, self).__init__()
        uic.loadUi('Deal Finder.ui', self)

        reddit = praw.Reddit(client_id=GUI._CLIENT_ID, client_secret=GUI._CLIENT_SECRET, user_agent=GUI._USER_AGENT,
                             username=GUI._USERNAME, password=GUI._PASSWORD)
        self.edit_window = MyQStackedWidget(self.editWindow.parent(), self.editWindow)
        self.edit_window.setHidden(True)

        ###############
        # CONNECTIONS #
        ###############
        self.EditSearchTerms.clicked.connect(self.edit_window.show)
        self.EditSubreddits.clicked.connect(self.edit_window.show)
        self.EditSearchTerms.clicked.connect(self.edit_window.setCurrentIndex, 0)
        self.EditSubreddits.clicked.connect(self.edit_window.setCurrentIndex, 1)
        self.newSubmission.connect(self.print_to_stream_of_deals)
        QApplication.instance().focusChanged.connect(self.edit_window_lost_focus)

        self.show()
        self._run(reddit)

    ###########
    # SIGNALS #
    ###########
    newSubmission = signal(praw.models.Submission)

    @slot(praw.models.Submission)
    def print_to_stream_of_deals(self, submission):
        self.StreamOfDeals.moveCursor(QTextCursor.Start, mode=QTextCursor.MoveAnchor)
        self.StreamOfDeals.insertPlainText(submission.title + '\n')
        self.StreamOfDeals.insertPlainText(submission.selftext + '\n')
        self.StreamOfDeals.insertHtml('<a href="' + submission.url + '">' + submission.url + '</a>' + '\n')
        self.StreamOfDeals.insertPlainText('\n\n\n\n\n\n')
        self.StreamOfDeals.update()

    def keyPressEvent(self, event: QEvent):
        key_pressed = event.key()
        if key_pressed == Qt.Key_Escape:
            QApplication.focusWidget().clearFocus()

    def edit_window_lost_focus(self, old: QtWidgets.QWidget, new: QtWidgets.QWidget):
        if old is not None:
            if self.edit_window.isAncestorOf(old):
                if new != self.edit_window:
                    self.lose_edit_window_focus()

    def lose_edit_window_focus(self):
        self.edit_window.hide()

    def listen_for_submissions(self, multi):
        for submission in multi.stream.submissions(pause_after=0,
                                                   skip_existing=True):  # defaults to outputting new posts
            if submission is not None:
                self.newSubmission.emit(submission)

    def _run(self, reddit: praw.Reddit):
        multi = reddit.subreddit('all')

        # for multi in reddit.user.multireddits():
        #     multi_name = multi.display_name
        #     if multi_name == "deals":
                #####################
                # SPAWN NEW THREADS #
                #####################
        threading.Thread(target=self.listen_for_submissions, kwargs={'multi': multi}).start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GUI()
    sys.exit(app.exec_())

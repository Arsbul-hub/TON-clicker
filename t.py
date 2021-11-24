class MainWnd(QMainWindow, mainGui.Ui_RecistMainWindow):
   def __init__(self, parent=None):
        super(MainWnd, self).__init__(parent)
        self.setupUi(self)

        self.actionExit.triggered.connect(self.exitApp)
        self.actionNew_subject.triggered.connect(self.newsubj_clicked)
        self.baseline_btn.clicked.connect(self.baseline_clicked)

    def newsubj_clicked(self, parent=None):
        dialog = NewSubject()
        dialog.exec_()
        self.id_label.setText(dialog.createid_lineedit.text())
        self.baseline_btn.setEnabled(True)

    def baseline_clicked(self):
        dialogbs = BaseLine(self.id_label.text())
        dialogbs.exec_()

    def exitApp(self):
        sys.exit(0)


class NewSubject(QDialog, newidGui.Ui_newSubjId):
    def __init__(self, parent=None, idparam=None):
        super(NewSubject, self).__init__(parent)
        self.setupUi(self)
        self.createid_lineedit.setFocus()


class BaseLine(QDialog, baselineGui.Ui_BaseLine):
    def __init__(self, id_value, parent=None):
        super(BaseLine, self).__init__(parent)
        self.setupUi(self)

        print(id_value)


def main():
    app = QApplication(sys.argv)
    form = MainWnd()
    form.show()
    app.exec_()


if __name__ == "__main__":
    main()

from PySide import QtGui

from medtechcore.pelvisdemo.view.pelvis import PelvisView
from medtechcore.pelvisdemo.ui_mainwindow import Ui_MainWindow


class MainWindow(QtGui.QMainWindow):


    def __init__(self, model):
        super(MainWindow, self).__init__()
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)

        self._view = PelvisView(model)
        self._view.register_visible_gender_options([self._ui.radioButtonMale.text(), self._ui.radioButtonFemale.text()])

        self._model = model
        self._visibleGender = self._ui.radioButtonMale.text()

        self._ui.widgetScene.setContext(model.context())

        self._model.set_time(self._ui.spinBoxHipWidth.value())
        self._view.set_visible_gender(self._visibleGender)

        self._makeConnections()

    def _makeConnections(self):
        self._ui.dockWidget.visibilityChanged.connect(self._dockWidgetVisibilityChanged)
        self._ui.actionDemographicOptions.activated.connect(self._demographicOptionsClicked)
        self._ui.spinBoxHipWidth.valueChanged.connect(self._hipWidthValueChanged)
        self._ui.radioButtonFemale.clicked.connect(self._genderClicked)
        self._ui.radioButtonMale.clicked.connect(self._genderClicked)
        self._ui.actionIMeasureU.activated.connect(self._iMeasureUClicked)
        self._model.imuInputReceived.connect(self._ui.widgetScene.updateFromIMU)
        self._model.resetInitialParameters.connect(self._ui.widgetScene.resetInitial)
        self._ui.pushButtonResetView.clicked.connect(self._resetView)

    def _iMeasureUClicked(self):
        self._model.listen(self._ui.actionIMeasureU.isChecked())

    def _hipWidthValueChanged(self, value):
        self._model.set_time(value)

    def _genderClicked(self):
        visibleGender = self.sender().text()
        if visibleGender != self._visibleGender:
            self._visibleGender = visibleGender
            self._view.set_visible_gender(self._visibleGender)
            self._resetView()

    def _resetView(self):
        self._ui.widgetScene.setInitialView()
        # self._ui.widgetScene.resetView(self._visibleGender)
            # self._ui.widgetScene.viewAll()

    def _demographicOptionsClicked(self):
        state = self._ui.actionDemographicOptions.isChecked()
        self._ui.dockWidget.setVisible(state)

    def _dockWidgetVisibilityChanged(self, state):
        self._ui.actionDemographicOptions.setChecked(state)


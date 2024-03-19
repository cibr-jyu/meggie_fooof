# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer_ui_files/createReportDialogUi.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets


class Ui_CreateReportDialog(object):
    def setupUi(self, CreateReportDialog):
        CreateReportDialog.setObjectName("CreateReportDialog")
        CreateReportDialog.resize(386, 530)
        self.gridLayout = QtWidgets.QGridLayout(CreateReportDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayoutButtons = QtWidgets.QHBoxLayout()
        self.horizontalLayoutButtons.setObjectName("horizontalLayoutButtons")
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayoutButtons.addItem(spacerItem)
        self.pushButtonCancel = QtWidgets.QPushButton(CreateReportDialog)
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.horizontalLayoutButtons.addWidget(self.pushButtonCancel)
        self.pushButtonBatch = QtWidgets.QPushButton(CreateReportDialog)
        self.pushButtonBatch.setObjectName("pushButtonBatch")
        self.horizontalLayoutButtons.addWidget(self.pushButtonBatch)
        self.pushButtonApply = QtWidgets.QPushButton(CreateReportDialog)
        self.pushButtonApply.setObjectName("pushButtonApply")
        self.horizontalLayoutButtons.addWidget(self.pushButtonApply)
        self.gridLayout.addLayout(self.horizontalLayoutButtons, 2, 0, 1, 1)
        self.scrollArea = QtWidgets.QScrollArea(CreateReportDialog)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 352, 700))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBoxBatching = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBoxBatching.setObjectName("groupBoxBatching")
        self.gridLayoutBatching = QtWidgets.QGridLayout(self.groupBoxBatching)
        self.gridLayoutBatching.setContentsMargins(9, 9, 9, 9)
        self.gridLayoutBatching.setObjectName("gridLayoutBatching")
        self.batchingWidgetPlaceholder = QtWidgets.QWidget(self.groupBoxBatching)
        self.batchingWidgetPlaceholder.setMinimumSize(QtCore.QSize(300, 300))
        self.batchingWidgetPlaceholder.setObjectName("batchingWidgetPlaceholder")
        self.gridLayoutBatching.addWidget(self.batchingWidgetPlaceholder, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBoxBatching, 2, 0, 1, 1)
        self.groupBoxInfo = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBoxInfo.setObjectName("groupBoxInfo")
        self.formLayout = QtWidgets.QFormLayout(self.groupBoxInfo)
        self.formLayout.setObjectName("formLayout")
        self.labelName = QtWidgets.QLabel(self.groupBoxInfo)
        self.labelName.setObjectName("labelName")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.labelName)
        self.lineEditName = QtWidgets.QLineEdit(self.groupBoxInfo)
        self.lineEditName.setObjectName("lineEditName")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEditName)
        self.gridLayout_2.addWidget(self.groupBoxInfo, 0, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.gridLayout_2.addItem(spacerItem1, 3, 0, 1, 1)
        self.groupBoxParameters = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBoxParameters.setObjectName("groupBoxParameters")
        self.formLayout_2 = QtWidgets.QFormLayout(self.groupBoxParameters)
        self.formLayout_2.setObjectName("formLayout_2")
        self.labelPeakWidthLow = QtWidgets.QLabel(self.groupBoxParameters)
        self.labelPeakWidthLow.setObjectName("labelPeakWidthLow")
        self.formLayout_2.setWidget(
            0, QtWidgets.QFormLayout.LabelRole, self.labelPeakWidthLow
        )
        self.doubleSpinBoxPeakWidthLow = QtWidgets.QDoubleSpinBox(
            self.groupBoxParameters
        )
        self.doubleSpinBoxPeakWidthLow.setMinimum(0.5)
        self.doubleSpinBoxPeakWidthLow.setMaximum(999.99)
        self.doubleSpinBoxPeakWidthLow.setSingleStep(0.1)
        self.doubleSpinBoxPeakWidthLow.setObjectName("doubleSpinBoxPeakWidthLow")
        self.formLayout_2.setWidget(
            0, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBoxPeakWidthLow
        )
        self.labelPeakWidthHigh = QtWidgets.QLabel(self.groupBoxParameters)
        self.labelPeakWidthHigh.setObjectName("labelPeakWidthHigh")
        self.formLayout_2.setWidget(
            1, QtWidgets.QFormLayout.LabelRole, self.labelPeakWidthHigh
        )
        self.doubleSpinBoxPeakWidthHigh = QtWidgets.QDoubleSpinBox(
            self.groupBoxParameters
        )
        self.doubleSpinBoxPeakWidthHigh.setMaximum(999.99)
        self.doubleSpinBoxPeakWidthHigh.setSingleStep(0.1)
        self.doubleSpinBoxPeakWidthHigh.setProperty("value", 12.0)
        self.doubleSpinBoxPeakWidthHigh.setObjectName("doubleSpinBoxPeakWidthHigh")
        self.formLayout_2.setWidget(
            1, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBoxPeakWidthHigh
        )
        self.labelPeakThreshold = QtWidgets.QLabel(self.groupBoxParameters)
        self.labelPeakThreshold.setObjectName("labelPeakThreshold")
        self.formLayout_2.setWidget(
            2, QtWidgets.QFormLayout.LabelRole, self.labelPeakThreshold
        )
        self.doubleSpinBoxPeakThreshold = QtWidgets.QDoubleSpinBox(
            self.groupBoxParameters
        )
        self.doubleSpinBoxPeakThreshold.setMaximum(9999.99)
        self.doubleSpinBoxPeakThreshold.setSingleStep(0.1)
        self.doubleSpinBoxPeakThreshold.setProperty("value", 2.0)
        self.doubleSpinBoxPeakThreshold.setObjectName("doubleSpinBoxPeakThreshold")
        self.formLayout_2.setWidget(
            2, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBoxPeakThreshold
        )
        self.labelFreqMin = QtWidgets.QLabel(self.groupBoxParameters)
        self.labelFreqMin.setObjectName("labelFreqMin")
        self.formLayout_2.setWidget(
            3, QtWidgets.QFormLayout.LabelRole, self.labelFreqMin
        )
        self.doubleSpinBoxFreqMin = QtWidgets.QDoubleSpinBox(self.groupBoxParameters)
        self.doubleSpinBoxFreqMin.setMaximum(999.99)
        self.doubleSpinBoxFreqMin.setObjectName("doubleSpinBoxFreqMin")
        self.formLayout_2.setWidget(
            3, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBoxFreqMin
        )
        self.labelFreqMax = QtWidgets.QLabel(self.groupBoxParameters)
        self.labelFreqMax.setObjectName("labelFreqMax")
        self.formLayout_2.setWidget(
            4, QtWidgets.QFormLayout.LabelRole, self.labelFreqMax
        )
        self.doubleSpinBoxFreqMax = QtWidgets.QDoubleSpinBox(self.groupBoxParameters)
        self.doubleSpinBoxFreqMax.setMaximum(999.99)
        self.doubleSpinBoxFreqMax.setProperty("value", 30.0)
        self.doubleSpinBoxFreqMax.setObjectName("doubleSpinBoxFreqMax")
        self.formLayout_2.setWidget(
            4, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBoxFreqMax
        )
        self.labelMaxNPeaks = QtWidgets.QLabel(self.groupBoxParameters)
        self.labelMaxNPeaks.setObjectName("labelMaxNPeaks")
        self.formLayout_2.setWidget(
            5, QtWidgets.QFormLayout.LabelRole, self.labelMaxNPeaks
        )
        self.spinBoxMaxNPeaks = QtWidgets.QSpinBox(self.groupBoxParameters)
        self.spinBoxMaxNPeaks.setProperty("value", 6)
        self.spinBoxMaxNPeaks.setObjectName("spinBoxMaxNPeaks")
        self.formLayout_2.setWidget(
            5, QtWidgets.QFormLayout.FieldRole, self.spinBoxMaxNPeaks
        )
        self.labelAperiodicMode = QtWidgets.QLabel(self.groupBoxParameters)
        self.labelAperiodicMode.setObjectName("labelAperiodicMode")
        self.formLayout_2.setWidget(
            6, QtWidgets.QFormLayout.LabelRole, self.labelAperiodicMode
        )
        self.comboBoxAperiodicMode = QtWidgets.QComboBox(self.groupBoxParameters)
        self.comboBoxAperiodicMode.setObjectName("comboBoxAperiodicMode")
        self.comboBoxAperiodicMode.addItem("")
        self.comboBoxAperiodicMode.addItem("")
        self.formLayout_2.setWidget(
            6, QtWidgets.QFormLayout.FieldRole, self.comboBoxAperiodicMode
        )
        self.gridLayout_2.addWidget(self.groupBoxParameters, 1, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)

        self.retranslateUi(CreateReportDialog)
        self.pushButtonCancel.clicked.connect(CreateReportDialog.close)
        self.pushButtonApply.clicked.connect(CreateReportDialog.accept)
        self.pushButtonBatch.clicked.connect(CreateReportDialog.acceptBatch)
        QtCore.QMetaObject.connectSlotsByName(CreateReportDialog)
        CreateReportDialog.setTabOrder(self.scrollArea, self.lineEditName)
        CreateReportDialog.setTabOrder(
            self.lineEditName, self.doubleSpinBoxPeakWidthLow
        )
        CreateReportDialog.setTabOrder(
            self.doubleSpinBoxPeakWidthLow, self.doubleSpinBoxPeakWidthHigh
        )
        CreateReportDialog.setTabOrder(
            self.doubleSpinBoxPeakWidthHigh, self.doubleSpinBoxPeakThreshold
        )
        CreateReportDialog.setTabOrder(
            self.doubleSpinBoxPeakThreshold, self.doubleSpinBoxFreqMin
        )
        CreateReportDialog.setTabOrder(
            self.doubleSpinBoxFreqMin, self.doubleSpinBoxFreqMax
        )
        CreateReportDialog.setTabOrder(self.doubleSpinBoxFreqMax, self.spinBoxMaxNPeaks)
        CreateReportDialog.setTabOrder(
            self.spinBoxMaxNPeaks, self.comboBoxAperiodicMode
        )
        CreateReportDialog.setTabOrder(
            self.comboBoxAperiodicMode, self.pushButtonCancel
        )
        CreateReportDialog.setTabOrder(self.pushButtonCancel, self.pushButtonBatch)
        CreateReportDialog.setTabOrder(self.pushButtonBatch, self.pushButtonApply)

    def retranslateUi(self, CreateReportDialog):
        _translate = QtCore.QCoreApplication.translate
        CreateReportDialog.setWindowTitle(
            _translate("CreateReportDialog", "Meggie - Create report")
        )
        self.pushButtonCancel.setText(_translate("CreateReportDialog", "Cancel"))
        self.pushButtonBatch.setText(_translate("CreateReportDialog", "Batch"))
        self.pushButtonApply.setText(_translate("CreateReportDialog", "Apply"))
        self.groupBoxBatching.setTitle(_translate("CreateReportDialog", "Batching"))
        self.groupBoxInfo.setTitle(_translate("CreateReportDialog", "Info"))
        self.labelName.setText(_translate("CreateReportDialog", "Name:"))
        self.groupBoxParameters.setTitle(_translate("CreateReportDialog", "Parameters"))
        self.labelPeakWidthLow.setText(
            _translate("CreateReportDialog", "Peak width low:")
        )
        self.doubleSpinBoxPeakWidthLow.setSuffix(_translate("CreateReportDialog", "Hz"))
        self.labelPeakWidthHigh.setText(
            _translate("CreateReportDialog", "Peak width high:")
        )
        self.doubleSpinBoxPeakWidthHigh.setSuffix(
            _translate("CreateReportDialog", "Hz")
        )
        self.labelPeakThreshold.setText(
            _translate("CreateReportDialog", "Peak threshold (relative):")
        )
        self.labelFreqMin.setText(_translate("CreateReportDialog", "Min frequency:"))
        self.labelFreqMax.setText(_translate("CreateReportDialog", "Max frequency:"))
        self.labelMaxNPeaks.setText(
            _translate("CreateReportDialog", "Max number of peaks:")
        )
        self.labelAperiodicMode.setText(
            _translate("CreateReportDialog", "Aperiodic mode:")
        )
        self.comboBoxAperiodicMode.setItemText(
            0, _translate("CreateReportDialog", "fixed")
        )
        self.comboBoxAperiodicMode.setItemText(
            1, _translate("CreateReportDialog", "knee")
        )

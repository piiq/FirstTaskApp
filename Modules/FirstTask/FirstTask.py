import os
from __main__ import vtk, qt, ctk, slicer

from slicer.ScriptedLoadableModule import *
from slicer.util import VTKObservationMixin
import logging

#------------------------------------------------------------------------------
#
# FirstTask
#
#------------------------------------------------------------------------------
class FirstTask(ScriptedLoadableModule):

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "FirstTask"
    self.parent.categories = ["First Task"]
    self.parent.dependencies = ["Data", "Models", "Markups"]
    self.parent.contributors = ["Csaba Pinter"]
    self.parent.helpText = """  """
    self.parent.acknowledgementText = """ Developed by Ebatinca S.L. """

#------------------------------------------------------------------------------
#
# FirstTaskWidget
#
#------------------------------------------------------------------------------
class FirstTaskWidget(ScriptedLoadableModuleWidget):

  def __init__(self, parent = None):
    ScriptedLoadableModuleWidget.__init__(self, parent)

    # Add slicer variable for debugging
    slicer.firstTaskWidget = self

    # Define variables used

    # Create logic
    self.logic = FirstTaskLogic()

  #------------------------------------------------------------------------------
  # Clean up when application is closed
  def cleanup(self):
    logging.debug('FirstTask.cleanup')

    self.disconnect()

  #------------------------------------------------------------------------------
  def setup(self):
    ScriptedLoadableModuleWidget.setup(self)

    # Launcher panel
    launcherCollapsibleButton = ctk.ctkCollapsibleButton()
    launcherCollapsibleButton.text = "Slicelet launcher"
    self.layout.addWidget(launcherCollapsibleButton)
    self.launcherFormLayout = qt.QFormLayout(launcherCollapsibleButton)

    # Show slicelet button
    self.launchSliceletButton = qt.QPushButton("Switch to First Task slicelet")
    self.launchSliceletButton.toolTip = "Switch to the First Task customized slicelet"
    self.launcherFormLayout.addWidget(self.launchSliceletButton)
    self.launchSliceletButton.connect('clicked()', self.showSlicelet)

    # Add vertical spacer
    self.layout.addStretch(1)

    # Load style sheet
    self.styleSheet = self.loadStyleSheet()
    slicer.app.setStyleSheet(self.styleSheet)

    # Setup user interface
    self.createMainMenuDockWidget()
    self.setupConnections()

    # Reset views
    self.resetViews()

  #------------------------------------------------------------------------------
  def setupConnections(self):
    logging.debug('FirstTask.setupConnections')

    # Startup
    slicer.app.connect("startupCompleted()", self.onStartupCompleted)

    # Settings panel
    self.showSlicerInterfaceButton.connect('clicked()', self.showSlicerInterface)
    self.showSliceletButton.connect('clicked()', self.showSlicelet)
    self.togglePythonInteractorButton.connect('clicked()', self.onTogglePythonInteractorButton)
    self.exitButton.connect('clicked()', self.onExitButtonClicked)

  #------------------------------------------------------------------------------
  def disconnect(self):
    logging.debug('FirstTask.disconnect')

    # Remove observer to old parameter node
    self.removeParameterNodeObserver()

    # Settings panel
    self.showSlicerInterfaceButton.clicked.disconnect()
    self.showSliceletButton.clicked.disconnect()
    self.togglePythonInteractorButton.clicked.disconnect()
    self.exitButton.clicked.disconnect()

  #------------------------------------------------------------------------------
  def loadStyleSheet(self):
    styleFilePath = os.path.join(self.logic.fileDir, 'Resources', 'StyleSheets', 'FirstTaskStyle.qss')
    f = qt.QFile(styleFilePath)
    if not f.exists():
      logging.error("Unable to load stylesheet, file not found")
      return ""

    f.open(qt.QFile.ReadOnly | qt.QFile.Text)
    ts = qt.QTextStream(f)
    stylesheet = ts.readAll()
    return stylesheet

  #------------------------------------------------------------------------------
  def onStartupCompleted(self):
    qt.QTimer.singleShot(100, self.showSlicelet)

    # Setup python customizations
    self.logic.setupPythonCustomizations()

  #------------------------------------------------------------------------------
  def resetViews(self):
    self.logic.setAxisBoxAndLabelsVisibility(0)
    self.logic.setBackgroundColorToBlack()
    self.logic.setupOrientationMarker()
    # self.logic.setupViewControllers()

  #------------------------------------------------------------------------------
  def createMainMenuDockWidget(self):
    # Set up main frame
    self.mainMenuDockWidget = qt.QDockWidget(self.parent)
    self.mainMenuDockWidget.setTitleBarWidget(qt.QWidget()) # hide title bar
    self.mainMenuDockWidget.setObjectName('FirstTaskPanel')
    self.mainMenuDockWidget.setWindowTitle('First Task')

    # self.mainMenuDockWidget.setStyleSheet(self.styleSheet)
    self.mainMenuDockWidget.setFeatures(qt.QDockWidget.DockWidgetMovable | qt.QDockWidget.DockWidgetFloatable) # not closable

    mainWindow = slicer.util.mainWindow()
    self.mainMenuDockWidget.setParent(mainWindow)

    # Setup scroll area
    self.mainFrame = qt.QFrame(self.mainMenuDockWidget)
    self.mainLayout = qt.QVBoxLayout(self.mainFrame)
    self.mainLayout.setContentsMargins(0,0,0,0)
    self.mainLayout.spacing = 0

    self.mainScrollArea = qt.QScrollArea(self.mainFrame)
    self.mainScrollArea.widgetResizable = True
    self.mainScrollArea.sizeAdjustPolicy = qt.QAbstractScrollArea.AdjustToContentsOnFirstShow
    self.mainScrollArea.horizontalScrollBarPolicy = qt.Qt.ScrollBarAlwaysOff
    self.mainScrollArea.setSizePolicy(qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Expanding))
    self.mainScrollArea.frameShape = qt.QFrame.NoFrame

    # Slicelet panel
    self.sliceletPanel = qt.QFrame(self.mainFrame)
    self.sliceletPanelLayout = qt.QVBoxLayout(self.sliceletPanel)
    self.sliceletPanelLayout.spacing = 0
    self.mainScrollArea.setWidget(self.sliceletPanel)

    self.mainLayout.addWidget(self.mainScrollArea)
    self.mainMenuDockWidget.setWidget(self.mainFrame)

    # Setup feature panel
    self.setupUi()

    self.sliceletPanelLayout.addStretch(1)

    self.setupSettingsPanel()

    self.mainScrollArea.minimumWidth = self.sliceletPanel.sizeHint.width()

  #------------------------------------------------------------------------------
  def setupUi(self):
    logging.debug('FirstTask.setupUi')

    # Load widget from .ui file (created by Qt Designer).
    # Additional widgets can be instantiated manually and added to self.layout.
    uiFilePath = os.path.join(self.logic.fileDir, 'Resources', 'UI', 'FirstTask.ui')
    uiWidget = slicer.util.loadUI(uiFilePath)
    self.ui = slicer.util.childWidgetVariables(uiWidget)

    self.sliceletPanelLayout.addWidget(uiWidget)

  #------------------------------------------------------------------------------
  def showSlicelet(self, maximizeViews=False, maximizeMainWindow=False, hideStatusBar=True):
    settings = qt.QSettings()
    settings.setValue('MainWindow/RestoreGeometry', False)

    self.showToolbars(False)
    self.showModulePanel(False)
    self.showMenuBar(False)
    # self.showPinButtonInViewers(False)

    mainWindow = slicer.util.mainWindow()

    self.mainMenuDockWidget.show()
    mainWindow.setTabPosition(qt.Qt.LeftDockWidgetArea, qt.QTabWidget.North)
    mainWindow.addDockWidget(qt.Qt.LeftDockWidgetArea, self.mainMenuDockWidget)

    if hideStatusBar:
      mainWindow.statusBar().hide()
    else:
      mainWindow.statusBar().show()

    if maximizeMainWindow:
      # mainWindow.showSlicelet()
      mainWindow.showMaximized()

  #------------------------------------------------------------------------------
  def showSlicerInterface(self):
    self.showToolbars(True)
    self.showModulePanel(True)
    self.showMenuBar(True)
    self.showPinButtonInViewers(True)

  #------------------------------------------------------------------------------
  def showToolbars(self, show):
    for toolbar in slicer.util.mainWindow().findChildren('QToolBar'):
      toolbar.setVisible(show)

  #------------------------------------------------------------------------------
  def showModulePanel(self, show):
    modulePanelDockWidget = slicer.util.mainWindow().findChildren('QDockWidget','PanelDockWidget')[0]
    modulePanelDockWidget.setVisible(show)
    if show:
      mainWindow = slicer.util.mainWindow()
      mainWindow.tabifyDockWidget(self.mainMenuDockWidget, modulePanelDockWidget)

  #------------------------------------------------------------------------------
  def showMenuBar(self, show):
    for menubar in slicer.util.mainWindow().findChildren('QMenuBar'):
      menubar.setVisible(show)

  #------------------------------------------------------------------------------
  def showPinButtonInViewers(self, show):
    redSlice = slicer.app.layoutManager().sliceWidget("Red")
    self.showViewerPinButton(redSlice, show)
    yellowSlice = slicer.app.layoutManager().sliceWidget("Yellow")
    self.showViewerPinButton(yellowSlice, show)
    greenSlice = slicer.app.layoutManager().sliceWidget("Green")
    self.showViewerPinButton(greenSlice, show)
    threeDWidget = slicer.app.layoutManager().threeDWidget(0)
    self.showViewerPinButton(threeDWidget, show)

  #------------------------------------------------------------------------------
  def showViewerPinButton(self, sliceWidget, show):
    try:
      sliceControlWidget = sliceWidget.children()[1]
      pinButton = sliceControlWidget.children()[1].children()[1]
      if show:
        pinButton.show()
      else:
        pinButton.hide()
    except:
      pass

  #------------------------------------------------------------------------------
  def onTogglePythonInteractorButton(show):
    visible = slicer.util.mainWindow().pythonConsole().parent().visible
    slicer.util.mainWindow().pythonConsole().parent().setVisible(not visible)

  #------------------------------------------------------------------------------
  # Settings
  #------------------------------------------------------------------------------
  def setupSettingsPanel(self):
    logging.debug('FirstTask.setupSettingsPanel')

    self.settingsCollapsibleButton = ctk.ctkCollapsibleButton()
    self.settingsCollapsibleButton.setProperty('collapsedHeight', 20)
    self.settingsCollapsibleButton.text = "Settings"
    if self.developerMode:
      self.sliceletPanelLayout.addWidget(self.settingsCollapsibleButton)

    self.settingsLayout = qt.QFormLayout(self.settingsCollapsibleButton)
    self.settingsLayout.setContentsMargins(12, 8, 4, 4)
    self.settingsLayout.setSpacing(8)

    # Empty row
    if self.developerMode:
      self.settingsLayout.addRow(' ', None)

    self.togglePythonInteractorButton = qt.QPushButton()
    self.togglePythonInteractorButton.setText("Toggle python console")
    if self.developerMode:
      self.settingsLayout.addRow(self.togglePythonInteractorButton)

    self.showSlicerInterfaceButton = qt.QPushButton()
    self.showSlicerInterfaceButton.setText("Switch to 3D Slicer view")
    if self.developerMode:
      self.settingsLayout.addRow(self.showSlicerInterfaceButton)

    self.showSliceletButton = qt.QPushButton()
    self.showSliceletButton.setText("Show slicelet")
    self.settingsLayout.addRow(self.showSliceletButton)

    # Empty row
    if self.developerMode:
      self.settingsLayout.addRow(' ', None)

    # Empty row
    self.settingsLayout.addRow(' ', None)

    self.exitButton = qt.QPushButton()
    self.exitButton.setText("Exit")
    self.settingsLayout.addRow(self.exitButton)

    # Collapse it by default
    self.settingsCollapsibleButton.collapsed = True

  #------------------------------------------------------------------------------
  def onExitButtonClicked(self):
    mainwindow = slicer.util.mainWindow()
    mainwindow.close()


#------------------------------------------------------------------------------
#
# FirstTaskLogic
#
#------------------------------------------------------------------------------
class FirstTaskLogic(ScriptedLoadableModuleLogic, VTKObservationMixin):

  def __init__(self, parent = None):
    ScriptedLoadableModuleLogic.__init__(self, parent)
    VTKObservationMixin.__init__(self)

    # Define member variables
    self.defaultSceneSavePath = os.path.join(qt.QDir.toNativeSeparators(qt.QDir.home().absolutePath()), 'FirstTask', 'Snapshots')
    self.fileDir = os.path.dirname(__file__)

    # Setup scene
    self.setupScene()

    # Setup keyboard shortcuts
    self.setupKeyboardShortcuts()

  #------------------------------------------------------------------------------
  # Setup scene
  #------------------------------------------------------------------------------
  def setupScene(self):
    logging.debug('FirstTask.setupScene')

    # Register custom layouts
    self.registerCustomLayouts()

  #------------------------------------------------------------------------------
  def registerCustomLayouts(self):
    layoutLogic = slicer.app.layoutManager().layoutLogic()
    customLayout = (
      "<layout type=\"horizontal\">"
      " <item>"
      "  <view class=\"vtkMRMLViewNode\" singletontag=\"OneThreeD\">"
      "   <property name=\"viewlabel\" action=\"default\">3rd</property>"
      "   <property name=\"viewcolor\" action=\"default\">#c17137</property>"
      "  </view>"
      " </item>"
      "</layout>")
    self.thirdPersonOnlyCustomLayoutId=509
    layoutLogic.GetLayoutNode().AddLayoutDescription(self.thirdPersonOnlyCustomLayoutId, customLayout)

  #------------------------------------------------------------------------------
  def setAxisBoxAndLabelsVisibility(self, visible):
    for viewIndex in range(slicer.app.layoutManager().threeDViewCount):
      threeDView = slicer.app.layoutManager().threeDWidget(viewIndex).threeDView()
      threeDView.mrmlViewNode().SetAxisLabelsVisible(visible)
      threeDView.mrmlViewNode().SetBoxVisible(visible)

  #------------------------------------------------------------------------------
  def setBackgroundColorToBlack(self):
    for viewIndex in range(slicer.app.layoutManager().threeDViewCount):
      threeDViewNode = slicer.app.layoutManager().threeDWidget(viewIndex).mrmlViewNode()
      threeDViewNode.SetBackgroundColor(0.0,0.0,0.0)
      threeDViewNode.SetBackgroundColor2(0.0,0.0,0.0)

  #------------------------------------------------------------------------------
  def setupViewControllers(self):
    # Customize 3D view
    layoutManager = slicer.app.layoutManager()
    for viewIndex in range(layoutManager.threeDViewCount):
      viewController = layoutManager.threeDWidget(viewIndex).threeDController()
      self.customizeViewControllerStyle(viewController)

    # Customize slice views
    for sliceViewName in layoutManager.sliceViewNames():
      sliceViewController = layoutManager.sliceWidget(sliceViewName).sliceController()
      self.customizeViewControllerStyle(sliceViewController)

  #------------------------------------------------------------------------------
  def setupOrientationMarker(self):
    # Set human orientation marker to all 3D views
    layoutManager = slicer.app.layoutManager()
    for viewIndex in range(layoutManager.threeDViewCount):
      threeDView = layoutManager.threeDWidget(viewIndex).threeDView()
      threeDViewNode = threeDView.mrmlViewNode()

    # Customize slice views
    for sliceViewName in layoutManager.sliceViewNames():
      sliceView = layoutManager.sliceWidget(sliceViewName).sliceView()
      sliceViewNode = sliceView.mrmlSliceNode()
      if sliceViewNode.GetLayoutLabel() == 'R':
        sliceViewNode.SetLayoutLabel('Axial')
      elif sliceViewNode.GetLayoutLabel() == 'Y':
        sliceViewNode.SetLayoutLabel('Sagittal')
      elif sliceViewNode.GetLayoutLabel() == 'G':
        sliceViewNode.SetLayoutLabel('Coronal')

  #------------------------------------------------------------------------------
  def customizeViewControllerStyle(self, viewController):
    barWidget = viewController.barWidget()
    barWidget.setStyleSheet(' \
      QWidget { background-color: black; color: white; padding: 0px; border-width: 0px; } \
      QSlider::handle:horizontal { background-color: black; } \
      QSlider::add-page:horizontal { background-color: rgba(0, 0, 0, 0.75); } \
      QSlider::add-page:horizontal:hover { background-color: rgba(0, 0, 0, 0.75); } \
      ')

  #------------------------------------------------------------------------------
  def setupKeyboardShortcuts(self):
    shortcuts = [
        ('Ctrl+3', lambda: slicer.util.mainWindow().pythonConsole().parent().setVisible(not slicer.util.mainWindow().pythonConsole().parent().visible))
        ]

    for (shortcutKey, callback) in shortcuts:
        shortcut = qt.QShortcut(slicer.util.mainWindow())
        shortcut.setKey(qt.QKeySequence(shortcutKey))
        shortcut.connect('activated()', callback)

  #------------------------------------------------------------------------------
  def setupPythonCustomizations(self):
    # Override function so that geometry warning popup is never shown
    def newWarnUserIfLoadableWarningsAndProceed(self):
      logging.debug('DICOM loadable warnings suppressed by newWarnUserIfLoadableWarningsAndProceed')
      return True
    dicomWidget = slicer.modules.dicom.widgetRepresentation()
    dicomWidgetSelf = dicomWidget.self()
    import types
    dicomWidgetSelf.browserWidget.warnUserIfLoadableWarningsAndProceed = types.MethodType(newWarnUserIfLoadableWarningsAndProceed, dicomWidgetSelf.browserWidget)

    # Hide advanced checkbox in DICOM browser
    dicomWidgetSelf.browserWidget.advancedViewButton.visible = False


#------------------------------------------------------------------------------
#
# FirstTaskTest
#
#------------------------------------------------------------------------------
class FirstTaskTest(ScriptedLoadableModuleTest):
  """This is the test case for your scripted module.
  """

  def runTest(self):
    """Run as few or as many tests as needed here.
    """
    ScriptedLoadableModuleTest.runTest(self)
    #self.test_FirstTask1() #add applet specific tests here

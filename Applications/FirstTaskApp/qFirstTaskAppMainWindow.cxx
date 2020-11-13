/*==============================================================================

  Copyright (c) Ebatinca, S.L.

==============================================================================*/

// FirstTask includes
#include "qFirstTaskAppMainWindow.h"
#include "qFirstTaskAppMainWindow_p.h"

// Qt includes
#include <QDesktopWidget>

// Slicer includes
#include "qSlicerApplication.h"
#include "qSlicerAboutDialog.h"
#include "qSlicerMainWindow_p.h"
#include "qSlicerModuleSelectorToolBar.h"

//-----------------------------------------------------------------------------
// qFirstTaskAppMainWindowPrivate methods

qFirstTaskAppMainWindowPrivate::qFirstTaskAppMainWindowPrivate(qFirstTaskAppMainWindow& object)
  : Superclass(object)
{
}

//-----------------------------------------------------------------------------
qFirstTaskAppMainWindowPrivate::~qFirstTaskAppMainWindowPrivate()
{
}

//-----------------------------------------------------------------------------
void qFirstTaskAppMainWindowPrivate::init()
{
  Q_Q(qFirstTaskAppMainWindow);
  this->Superclass::init();
}

//-----------------------------------------------------------------------------
void qFirstTaskAppMainWindowPrivate::setupUi(QMainWindow * mainWindow)
{
  qSlicerApplication * app = qSlicerApplication::application();

  //----------------------------------------------------------------------------
  // Add actions
  //----------------------------------------------------------------------------
  QAction* helpAboutSlicerAppAction = new QAction(mainWindow);
  helpAboutSlicerAppAction->setObjectName("HelpAboutFirstTaskAppAction");
  helpAboutSlicerAppAction->setText("About " + app->applicationName());

  //----------------------------------------------------------------------------
  // Calling "setupUi()" after adding the actions above allows the call
  // to "QMetaObject::connectSlotsByName()" done in "setupUi()" to
  // successfully connect each slot with its corresponding action.
  this->Superclass::setupUi(mainWindow);

  //----------------------------------------------------------------------------
  // Configure
  //----------------------------------------------------------------------------
  mainWindow->setWindowIcon(QIcon(":/Icons/Medium/DesktopIcon.png"));

  QPixmap logo(":/LogoFull.png");
#if (QT_VERSION >= QT_VERSION_CHECK(5, 0, 0))
  qreal dpr = sqrt(qApp->desktop()->logicalDpiX()*qreal(qApp->desktop()->logicalDpiY()) / (qApp->desktop()->physicalDpiX()*qApp->desktop()->physicalDpiY()));
  logo.setDevicePixelRatio(dpr);
#endif
  this->LogoLabel->setPixmap(logo);

  // Hide the toolbars
  this->MainToolBar->setVisible(false);
  //this->ModuleSelectorToolBar->setVisible(false);
  this->ModuleToolBar->setVisible(false);
  this->ViewToolBar->setVisible(false);
  this->MouseModeToolBar->setVisible(false);
  this->CaptureToolBar->setVisible(false);
  this->ViewersToolBar->setVisible(false);
  this->DialogToolBar->setVisible(false);

  // Hide the menus
  //this->menubar->setVisible(false);
  //this->FileMenu->setVisible(false);
  //this->EditMenu->setVisible(false);
  //this->ViewMenu->setVisible(false);
  //this->LayoutMenu->setVisible(false);
  //this->HelpMenu->setVisible(false);

  // Hide the modules panel
  //this->PanelDockWidget->setVisible(false);
  this->DataProbeCollapsibleWidget->setCollapsed(true);
  this->DataProbeCollapsibleWidget->setVisible(false);
  this->StatusBar->setVisible(false);
}

//-----------------------------------------------------------------------------
// qFirstTaskAppMainWindow methods

//-----------------------------------------------------------------------------
qFirstTaskAppMainWindow::qFirstTaskAppMainWindow(QWidget* windowParent)
  : Superclass(new qFirstTaskAppMainWindowPrivate(*this), windowParent)
{
  Q_D(qFirstTaskAppMainWindow);
  d->init();
}

//-----------------------------------------------------------------------------
qFirstTaskAppMainWindow::qFirstTaskAppMainWindow(
  qFirstTaskAppMainWindowPrivate* pimpl, QWidget* windowParent)
  : Superclass(pimpl, windowParent)
{
  // init() is called by derived class.
}

//-----------------------------------------------------------------------------
qFirstTaskAppMainWindow::~qFirstTaskAppMainWindow()
{
}

//-----------------------------------------------------------------------------
void qFirstTaskAppMainWindow::on_HelpAboutFirstTaskAppAction_triggered()
{
  qSlicerAboutDialog about(this);
  about.setLogo(QPixmap(":/Logo.png"));
  about.exec();
}

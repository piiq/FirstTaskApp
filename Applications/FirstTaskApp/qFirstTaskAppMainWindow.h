/*==============================================================================

  Copyright (c) Ebatinca, S.L.

==============================================================================*/

#ifndef __qFirstTaskAppMainWindow_h
#define __qFirstTaskAppMainWindow_h

// FirstTask includes
#include "qFirstTaskAppExport.h"
class qFirstTaskAppMainWindowPrivate;

// Slicer includes
#include "qSlicerMainWindow.h"

class Q_FIRSTTASK_APP_EXPORT qFirstTaskAppMainWindow : public qSlicerMainWindow
{
  Q_OBJECT
public:
  typedef qSlicerMainWindow Superclass;

  qFirstTaskAppMainWindow(QWidget *parent=0);
  virtual ~qFirstTaskAppMainWindow();

public slots:
  void on_HelpAboutFirstTaskAppAction_triggered();

protected:
  qFirstTaskAppMainWindow(qFirstTaskAppMainWindowPrivate* pimpl, QWidget* parent);

private:
  Q_DECLARE_PRIVATE(qFirstTaskAppMainWindow);
  Q_DISABLE_COPY(qFirstTaskAppMainWindow);
};

#endif

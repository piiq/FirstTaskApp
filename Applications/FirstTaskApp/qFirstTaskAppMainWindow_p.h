/*==============================================================================

  Copyright (c) Ebatinca, S.L.

==============================================================================*/

#ifndef __qFirstTaskAppMainWindow_p_h
#define __qFirstTaskAppMainWindow_p_h

// FirstTask includes
#include "qFirstTaskAppMainWindow.h"

// Slicer includes
#include "qSlicerMainWindow_p.h"

//-----------------------------------------------------------------------------
class Q_FIRSTTASK_APP_EXPORT qFirstTaskAppMainWindowPrivate
  : public qSlicerMainWindowPrivate
{
  Q_DECLARE_PUBLIC(qFirstTaskAppMainWindow);
public:
  typedef qSlicerMainWindowPrivate Superclass;
  qFirstTaskAppMainWindowPrivate(qFirstTaskAppMainWindow& object);
  virtual ~qFirstTaskAppMainWindowPrivate();

  virtual void init();
  /// Reimplemented for custom behavior
  virtual void setupUi(QMainWindow * mainWindow);
};

#endif

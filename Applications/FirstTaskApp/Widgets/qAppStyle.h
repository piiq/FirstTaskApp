/*==============================================================================

  Copyright (c) Ebatinca, S.L.

==============================================================================*/

#ifndef __qAppStyle_h
#define __qAppStyle_h

// FirstTask includes
#include "qFirstTaskAppExport.h"

// Slicer includes
#include "qSlicerStyle.h"

class Q_FIRSTTASK_APP_EXPORT qAppStyle
  : public qSlicerStyle
{
  Q_OBJECT
public:
  /// Superclass typedef
  typedef qSlicerStyle Superclass;

  /// Constructors
  qAppStyle();
  virtual ~qAppStyle();

  /// Reimplemented to customize colors.
  /// \sa QStyle::standardPalette()
  virtual QPalette standardPalette() const;

  /// Reimplemented to apply custom palette to widgets
  /// \sa QStyle::drawComplexControl()
  void drawComplexControl(ComplexControl control,
                          const QStyleOptionComplex* option,
                          QPainter* painter,
                          const QWidget* widget = 0)const;
  /// Reimplemented to apply custom palette to widgets
  /// \sa QStyle::drawControl()
  virtual void drawControl(ControlElement element,
                           const QStyleOption* option,
                           QPainter* painter,
                           const QWidget* widget = 0 )const;

  /// Reimplemented to apply custom palette to widgets
  /// \sa QStyle::drawPrimitive()
  virtual void drawPrimitive(PrimitiveElement element,
                             const QStyleOption* option,
                             QPainter* painter,
                             const QWidget* widget = 0 )const;

  /// Tweak the colors of some widgets.
  virtual QPalette tweakWidgetPalette(QPalette palette,
                                      const QWidget* widget)const;

  /// Reimplemented to apply styling to widgets.
  /// \sa QStyle::polish()
  virtual void polish(QWidget* widget);
  using Superclass::polish;
};

#endif

#!/bin/sh

. ./CommonVars.sh

BIN_DIR=$FIRSTTASK_SUPERBUILD_BIN_DIR_DBG_X64

echo "Build started ($BIN_DIR)"

mkdir $BIN_DIR
cd $BIN_DIR
cmake $FIRSTTASK_SOURCE_DIR -DQt5_DIR:PATH=$QT5_DIR -DSlicer_USE_VTK_DEBUG_LEAKS:BOOL=ON
ctest -D Experimental -C Debug

date

echo "Build finished ($BIN_DIR")

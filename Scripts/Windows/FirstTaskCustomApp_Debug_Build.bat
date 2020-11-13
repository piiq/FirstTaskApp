@call CommonVars.bat
time /t

set BIN_DIR=%FIRSTTASKCUSTOMAPP_SUPERBUILD_BIN_DIR_DBG_X64%

echo Build started (%BIN_DIR%)
taskkill /IM TGitCache.exe /F
mkdir %BIN_DIR%
cd /d %BIN_DIR%
%CMAKE_EXE% %FIRSTTASKCUSTOMAPP_SOURCE_DIR% -G %CMAKE_GENERATOR_X64% -DQt5_DIR:PATH=%QT5_DIR_X64% -DSlicer_USE_VTK_DEBUG_LEAKS:BOOL=ON
%CTEST_EXE% -D Experimental -C Debug

time /t
echo Build finished (%BIN_DIR%)
pause

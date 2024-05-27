@echo off
set "file_path=%~1"
echo %file_path%
echo.
set png=extract
echo.
echo.
REM pyinstaller.exe -F %file_path% -i .\pyinstaller\%png%.png --upx-dir .\pyinstaller\upx
pyinstaller.exe -F %file_path% -i .\pyinstaller\%png%.png
TIMEOUT /T 1 /NOBREAK
del /Q /S %~dp0\*.spec
rmdir /S /Q %~dp0\build\
move /Y %~dp0\dist\*.exe %~dp0\
rmdir /S /Q %~dp0\dist
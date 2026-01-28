@echo off
echo PyInstaller로 exe 파일 빌드 중...
pyinstaller --onedir ^
    --windowed ^
    --name CareNote ^
    --hidden-import PyQt6.QtCore ^
    --hidden-import PyQt6.QtWidgets ^
    --hidden-import PyQt6.QtGui ^
    --hidden-import PyQt6.QtPrintSupport ^
    --hidden-import carenote.database ^
    --hidden-import carenote.models ^
    --hidden-import carenote.crud ^
    --hidden-import carenote.gui ^
    --hidden-import carenote.config ^
    --collect-all qt_material ^
    --collect-all PyQt6 ^
    --clean ^
    main_gui.py
echo.
echo 빌드 완료! dist\CareNote 폴더를 확인하세요.
pause
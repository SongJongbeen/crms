@echo off
echo PyInstaller로 exe 파일 빌드 중...
pyinstaller --onedir ^
    --windowed ^
    --name CareNote ^
    --hidden-import PyQt6 ^
    --hidden-import qt_material ^
    --collect-all qt_material ^
    --collect-all PyQt6 ^
    --clean ^
    main_gui.py
echo.
echo 빌드 완료! dist\CareNote 폴더를 확인하세요.
pause
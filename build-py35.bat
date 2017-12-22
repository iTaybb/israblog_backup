@echo off

rmdir /s /q build
rmdir /s /q __pycache__
c:\python35\python.exe c:\python35\scripts\pyinstaller IsrablogScrapper.spec

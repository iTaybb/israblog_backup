@echo off

rmdir /s /q build
rmdir /s /q __pycache__
c:\python36\python.exe c:\python36\scripts\pyinstaller IsrablogScrapper.spec

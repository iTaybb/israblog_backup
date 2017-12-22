@echo off

rmdir /s /q build
rmdir /s /q dist
rmdir /s /q __pycache__
pyinstaller IsrablogScrapper.spec

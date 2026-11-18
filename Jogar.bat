@echo off
rem Clique duas vezes neste arquivo para abrir o jogo.
cd /d "%~dp0"
"%LOCALAPPDATA%\Programs\Python\Python312\python.exe" main.py
if errorlevel 1 pause

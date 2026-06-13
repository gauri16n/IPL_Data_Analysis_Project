@echo off
setlocal

REM Run Streamlit dashboard
cd /d "%~dp0"

REM If you have a venv, uncomment and use it:
REM call venv\Scripts\activate

REM Force Dark Theme via CLI to guarantee it applies
python -m streamlit run ipl_dashboard.py --server.port 8501 --theme.base "dark" --theme.primaryColor "#3b82f6" --theme.backgroundColor "#0e1117" --theme.secondaryBackgroundColor "#161b22" --theme.textColor "#f9fafb"

endlocal
pause

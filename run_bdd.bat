@echo off
setlocal enabledelayedexpansion

REM
for /f "usebackq tokens=1,* delims==" %%A in (".env") do (
    set "%%A=%%B"
)

echo === Starting BDD ===
mysql -hlocalhost -u %DB_USER% -p%DB_PASSWORD% < database/schema.sql


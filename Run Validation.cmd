@echo off
setlocal
title Yokai Dominion - Validation
set "YOKAI_TOOLS=E:\Source\YokaiTools"
set "DOTNET_ROOT=%YOKAI_TOOLS%\dotnet"
set "PATH=%DOTNET_ROOT%;%PATH%"
set "DOTNET_CLI_HOME=%YOKAI_TOOLS%\dotnet-cli"
set "NUGET_PACKAGES=%YOKAI_TOOLS%\nuget\packages"
set "NUGET_HTTP_CACHE_PATH=%YOKAI_TOOLS%\nuget\http-cache"
if not exist "%DOTNET_ROOT%\dotnet.exe" (
    echo The .NET SDK was not found at "%DOTNET_ROOT%".
    goto failed
)
set "YOKAI_SOURCE_REVISION="
set /p "YOKAI_SOURCE_REVISION=" < "%~dp0production.ref"
if not defined YOKAI_SOURCE_REVISION (
    echo Could not read production.ref.
    goto failed
)
set "YOKAI_CHECKOUT="
for /f %%I in ('git -C "%~dp0production" rev-parse HEAD 2^>nul') do set "YOKAI_CHECKOUT=%%I"
if /i not "%YOKAI_CHECKOUT%"=="%YOKAI_SOURCE_REVISION%" (
    echo The production folder must be checked out at %YOKAI_SOURCE_REVISION%.
    goto failed
)
pushd "%~dp0production" || goto failed
echo Running the 18 core checks...
"%DOTNET_ROOT%\dotnet.exe" run --project "tests\Yokai.Tissue.Checks" -c Release
if errorlevel 1 goto failed_in_repo

echo.
echo Running the 9 advanced checks...
"%DOTNET_ROOT%\dotnet.exe" run --project "tests\Yokai.Tissue.AdvancedChecks" -c Release
if errorlevel 1 goto failed_in_repo

cd ..
echo.
echo Running the material sweep...
"%DOTNET_ROOT%\dotnet.exe" run --project "scenarios\MaterialSweep" -c Release
if errorlevel 1 goto failed_in_repo
popd

echo.
echo All checks passed and the material sweep completed.
echo Numerical reports: "%~dp0production\artifacts"
echo Material sweep report: "%~dp0artifacts\material-sweep.json"
pause
exit /b 0

:failed_in_repo
popd
:failed
echo.
echo Validation stopped. See the output above.
pause
exit /b 1

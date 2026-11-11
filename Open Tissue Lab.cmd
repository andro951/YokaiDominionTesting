@echo off
setlocal
title Yokai Dominion - Tissue Laboratory
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
set "GODOT=%YOKAI_TOOLS%\godot\Godot_v4.7.2-stable_mono_win64\Godot_v4.7.2-stable_mono_win64.exe"
if not exist "%GODOT%" (
    echo Godot was not found at "%GODOT%".
    goto failed
)
if not exist "%~dp0..\YokaiDominion\game\project.godot" (
    echo The YokaiDominion repo must be next to YokaiDominionTesting.
    goto failed
)
pushd "%~dp0..\YokaiDominion" || goto failed
echo Building the tissue laboratory...
"%DOTNET_ROOT%\dotnet.exe" build "game\YokaiDominion.csproj" -c Debug
if errorlevel 1 (
    popd
    goto failed
)
start "" "%GODOT%" --path "%CD%\game" --log-file "%YOKAI_TOOLS%\lab.log"
if errorlevel 1 (
    popd
    goto failed
)
popd
exit /b 0

:failed
echo.
echo The tissue laboratory could not start.
pause
exit /b 1

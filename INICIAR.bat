@echo off
setlocal
cd /d "%~dp0"

rem Confere se o Python 3.11 esta instalado.
py -3.11 --version >nul 2>&1
if errorlevel 1 goto PYTHON_NAO_ENCONTRADO

rem Remove somente um ambiente virtual incompleto, sem o executavel do Python.
if exist ".venv" (
    if not exist ".venv\Scripts\python.exe" (
        echo Removendo ambiente virtual incompleto...
        rmdir /s /q ".venv"
    )
)

rem Cria o ambiente virtual caso ainda nao exista.
if not exist ".venv\Scripts\python.exe" (
    echo Criando o ambiente virtual...
    py -3.11 -m venv .venv
    if errorlevel 1 goto ERRO_AMBIENTE
)

rem Confere a existencia do interpretador antes de continuar.
if not exist ".venv\Scripts\python.exe" goto ERRO_AMBIENTE
set "PYTHON=%CD%\.venv\Scripts\python.exe"

rem Usa diretamente o Python do ambiente virtual, sem depender de activate.bat.
echo.
echo Instalando as bibliotecas do projeto...
"%PYTHON%" -m pip install -r requirements.txt
if errorlevel 1 goto ERRO_BIBLIOTECAS

rem Prepara o framework Py3D.
echo.
echo Preparando o framework Py3D...
"%PYTHON%" instalar_framework.py
if errorlevel 1 goto ERRO_FRAMEWORK

rem Inicia a aplicacao grafica.
echo.
echo Iniciando o trabalho de Computacao Grafica...
"%PYTHON%" main.py
if errorlevel 1 goto ERRO_EXECUCAO

goto FIM

:PYTHON_NAO_ENCONTRADO
echo.
echo ERRO: Python 3.11 nao foi encontrado.
echo Abra o Prompt de Comando e execute:
echo     py install 3.11
echo Depois confirme com:
echo     py -3.11 --version
echo Em seguida, execute este arquivo novamente.
goto FALHA

:ERRO_AMBIENTE
echo.
echo ERRO: nao foi possivel criar o ambiente virtual.
echo Confira se o Python 3.11 foi instalado corretamente.
goto FALHA

:ERRO_BIBLIOTECAS
echo.
echo ERRO: falha ao instalar as bibliotecas.
echo Confira a conexao com a internet e tente novamente.
goto FALHA

:ERRO_FRAMEWORK
echo.
echo ERRO: nao foi possivel preparar o framework Py3D.
echo Confira a conexao com a internet e tente novamente.
goto FALHA

:ERRO_EXECUCAO
echo.
echo ERRO: a aplicacao foi encerrada com falha.
echo Confira a mensagem exibida acima.
goto FALHA

:FALHA
echo.
pause
exit /b 1

:FIM
endlocal

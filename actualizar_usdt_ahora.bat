@echo off
echo ========================================
echo Actualizando USDT a 241.76 VES
echo ========================================
cd C:\web2py
python web2py.py -S sistema_divisas -M -R C:\web2py\applications\divisas2os\actualizar_usdt_241.py
pause

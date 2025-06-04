@echo off
echo 正在安装前端项目依赖...
echo.

cd /d "%~dp0"

echo 检查Node.js是否已安装...
node --version >nul 2>&1
if errorlevel 1 (
    echo 错误：Node.js未安装，请先安装Node.js
    pause
    exit /b 1
)

echo Node.js版本:
node --version

echo.
echo 正在安装依赖包...
npm install

if errorlevel 1 (
    echo.
    echo 安装失败，请检查网络连接或尝试使用淘宝镜像：
    echo npm config set registry https://registry.npmmirror.com
    pause
    exit /b 1
)

echo.
echo 依赖安装完成！
echo.
echo 要启动开发服务器，请运行：
echo npm run dev
echo.
pause 
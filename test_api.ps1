# API测试脚本
$baseUrl = "http://127.0.0.1:8000/api/v1"
$headers = @{ "Content-Type" = "application/json" }

Write-Host "开始测试API接口..." -ForegroundColor Green

# 测试用户登录
Write-Host "`n1. 测试用户登录接口" -ForegroundColor Yellow
$loginBody = @{
    username = "testuser"
    password = "testpass123"
} | ConvertTo-Json

try {
    $loginResponse = Invoke-WebRequest -Uri "$baseUrl/users/login/" -Method Post -Headers $headers -Body $loginBody
    Write-Host "登录成功! 状态码: $($loginResponse.StatusCode)" -ForegroundColor Green
    
    # 解析响应以获取token
    $loginData = $loginResponse.Content | ConvertFrom-Json
    $accessToken = $loginData.access
    $refreshToken = $loginData.refresh
    
    Write-Host "Access Token 前20个字符: $($accessToken.Substring(0, 20))..." -ForegroundColor Cyan
    Write-Host "Refresh Token 前20个字符: $($refreshToken.Substring(0, 20))..." -ForegroundColor Cyan
    
    # 测试获取当前用户信息
    Write-Host "`n2. 测试获取当前用户信息接口" -ForegroundColor Yellow
    $authHeaders = @{
        "Content-Type" = "application/json"
        "Authorization" = "Bearer $accessToken"
    }
    
    $userInfoResponse = Invoke-WebRequest -Uri "$baseUrl/users/me/" -Method Get -Headers $authHeaders
    Write-Host "获取用户信息成功! 状态码: $($userInfoResponse.StatusCode)" -ForegroundColor Green
    Write-Host "用户信息:" -ForegroundColor Cyan
    $userInfo = $userInfoResponse.Content | ConvertFrom-Json
    $userInfo | ConvertTo-Json -Depth 3
    
    # 测试Token刷新
    Write-Host "`n3. 测试Token刷新接口" -ForegroundColor Yellow
    $refreshBody = @{
        refresh = $refreshToken
    } | ConvertTo-Json
    
    $refreshResponse = Invoke-WebRequest -Uri "$baseUrl/users/token/refresh/" -Method Post -Headers $headers -Body $refreshBody
    Write-Host "Token刷新成功! 状态码: $($refreshResponse.StatusCode)" -ForegroundColor Green
    
    $refreshData = $refreshResponse.Content | ConvertFrom-Json
    Write-Host "新的Access Token 前20个字符: $($refreshData.access.Substring(0, 20))..." -ForegroundColor Cyan
    
} catch {
    Write-Host "请求失败: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.Exception.Response) {
        $errorResponse = $_.Exception.Response.GetResponseStream()
        $reader = New-Object System.IO.StreamReader($errorResponse)
        $errorContent = $reader.ReadToEnd()
        Write-Host "错误详情: $errorContent" -ForegroundColor Red
    }
}

Write-Host "`n测试完成!" -ForegroundColor Green 
#!/usr/bin/env python3
import requests
import json

# API基础URL
BASE_URL = "http://127.0.0.1:8000/api/v1"

def test_api():
    print("开始测试API接口...")
    
    # 1. 测试用户登录
    print("\n1. 测试用户登录接口")
    login_data = {
        "username": "testuser",
        "password": "testpass123"
    }
    
    try:
        login_response = requests.post(
            f"{BASE_URL}/users/login/",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        if login_response.status_code == 200:
            print(f"✅ 登录成功! 状态码: {login_response.status_code}")
            login_result = login_response.json()
            
            # 获取token
            access_token = login_result.get('access')
            refresh_token = login_result.get('refresh')
            
            print(f"Access Token 前20个字符: {access_token[:20]}...")
            print(f"Refresh Token 前20个字符: {refresh_token[:20]}...")
            
            # 显示用户信息
            if 'user' in login_result:
                print("用户信息:")
                print(json.dumps(login_result['user'], indent=2, ensure_ascii=False))
            
            # 2. 测试获取当前用户信息
            print("\n2. 测试获取当前用户信息接口")
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}"
            }
            
            user_info_response = requests.get(
                f"{BASE_URL}/users/me/",
                headers=headers
            )
            
            if user_info_response.status_code == 200:
                print(f"✅ 获取用户信息成功! 状态码: {user_info_response.status_code}")
                user_info = user_info_response.json()
                print("当前用户详细信息:")
                print(json.dumps(user_info, indent=2, ensure_ascii=False))
            else:
                print(f"❌ 获取用户信息失败! 状态码: {user_info_response.status_code}")
                print(f"错误信息: {user_info_response.text}")
            
            # 3. 测试Token刷新
            print("\n3. 测试Token刷新接口")
            refresh_data = {
                "refresh": refresh_token
            }
            
            refresh_response = requests.post(
                f"{BASE_URL}/users/token/refresh/",
                json=refresh_data,
                headers={"Content-Type": "application/json"}
            )
            
            if refresh_response.status_code == 200:
                print(f"✅ Token刷新成功! 状态码: {refresh_response.status_code}")
                refresh_result = refresh_response.json()
                new_access_token = refresh_result.get('access')
                print(f"新的Access Token 前20个字符: {new_access_token[:20]}...")
            else:
                print(f"❌ Token刷新失败! 状态码: {refresh_response.status_code}")
                print(f"错误信息: {refresh_response.text}")
                
        else:
            print(f"❌ 登录失败! 状态码: {login_response.status_code}")
            print(f"错误信息: {login_response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求异常: {e}")
    except Exception as e:
        print(f"❌ 其他错误: {e}")
    
    print("\n测试完成!")

if __name__ == "__main__":
    test_api() 
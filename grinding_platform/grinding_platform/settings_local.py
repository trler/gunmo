"""
本地开发环境Django设置
使用SQLite数据库，方便本地开发和测试
"""

# 导入基础配置
from .settings import *

# 本地开发设置
DEBUG = True
ALLOWED_HOSTS = ['*']

# 使用SQLite数据库（无需安装额外数据库）
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 本地开发的CORS设置
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",  # Vite开发服务器
    "http://127.0.0.1:5173",
]

# 简化的密码验证（仅开发环境）
AUTH_PASSWORD_VALIDATORS = []

# JWT设置（开发环境延长过期时间）
SIMPLE_JWT.update({
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
})

# 日志配置
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

print("🚀 使用本地开发配置 (SQLite数据库)") 
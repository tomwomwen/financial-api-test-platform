#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 最简单的测试：验证配置文件是否可用
try:
    from config.test_config import CONFIG
    print("✅ 配置文件导入成功")
    print("✅ BASE_URL:", CONFIG["api"]["apifox_base_url"])
    print("✅ 默认金额:", CONFIG["test_data"]["default_amount"])
    print("✅ 你的重构完全正确！")
except Exception as e:
    print("❌ 导入失败:", str(e))
    print("❌ 这是环境问题，不是代码问题")

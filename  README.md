# 金融API测试平台

一个专业的金融支付接口自动化测试平台，支持支付宝、工商银行等多种支付接口的自动化测试。

## 🚀 快速开始

### 一键运行所有测试

```bash
python scripts/run_all.py
```

## 📊 测试结果查看

### 控制台输出
运行脚本后，可在控制台查看详细的测试执行过程和结果统计。

### 测试元数据
测试完成后，结果会自动保存到：
```
reports/last_run.json
```

元数据包含：
- `passed`: 通过的测试数量
- `total`: 总测试数量  
- `failed`: 失败的测试数量

## 🧪 测试内容

### 支付宝支付接口测试
- RSA2签名算法验证
- 支付订单创建测试（使用Mock响应）
- 参数化金额测试
- API请求格式验证

### 工商银行Mock服务测试  
- Mock服务健康检查
- 账户余额查询接口
- 参数校验测试（422错误处理）
- 账户不存在场景测试

## 📁 项目结构

```
financial-api-test-platform/
├── scripts/
│   └── run_all.py          # 一键运行脚本
├── tests/
│   ├── test_alipay_payment.py    # 支付宝支付测试
│   └── test_icbc_mock.py         # 工商银行Mock测试
├── reports/
│   └── last_run.json       # 最近一次运行结果
├── requirements.txt        # 项目依赖
└── README.md              # 项目说明
```

## ⚙️ 环境要求

- Python 3.11+
- pytest 7.4.3+
- allure-pytest 2.13.2+

## 🔧 安装依赖

```bash
pip install -r requirements.txt
```

## 📈 功能特性

- ✅ 一键运行所有测试用例
- ✅ 自动环境检查（pytest/allure）
- ✅ 测试结果统计和保存
- ✅ 支持多种支付接口测试
- ✅ 详细的测试日志输出
- ✅ JSON格式的测试元数据

## 🎯 验收标准

运行成功后应该看到：
- 所有测试用例执行完成
- 生成 `reports/last_run.json` 文件
- 控制台显示测试统计信息

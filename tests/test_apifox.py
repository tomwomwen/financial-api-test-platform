import requests
import time
import random
from config.test_config import CONFIG
BASE_URL = CONFIG["api"]["apifox_base_url"]

def test_connection():
    response = requests.get(BASE_URL);

def test_refund():
    result = generate_test_order()
    trade_no = result["out_trade_no"]
    amount = result["amount"]
    url = BASE_URL + "/refund"
    data= {
        "refund_amount": amount,
        "refund_reason": CONFIG["test_data"]["refund_reason"],
        "out_trade_no": trade_no
    }
    response = requests.post(url,json=data)
    validate_common_response(response)
    assert response.json()["data"]["refund_amount"] == amount
    assert response.json()["data"]["refund_reason"] == CONFIG["test_data"]["refund_reason"]
    print(f"状态码：{response.status_code}")
def test_query():
    result = generate_test_order()
    trade_no = result["out_trade_no"]
    amount = result["amount"]
    url = BASE_URL + "/query"
    params = {
        "out_trade_no": trade_no
    }
    response = requests.get(url,params=params)
    validate_common_response(response)
    assert response.json()["data"]["total_amount"] == CONFIG["test_data"]["default_amount"]
def test_idempotent():
    # 步骤1：固定订单号和请求数据
    result = generate_test_order()
    trade_no = CONFIG["test_data"]["idempotent_order"]
    amount = result["amount"]
    url = BASE_URL + "/pay"  # 支付接口URL
    # 固定的支付请求数据
    data = {
        "amount": amount,
        "subject": "幂等测试订单",
        "out_trade_no": trade_no
    }
    first_response = requests.post(url, json=data)
    second_response = requests.post(url,json=data)
    # 步骤4：验证两次调用都成功
    validate_common_response(first_response)
    validate_common_response(second_response)
    # 步骤5：获取响应内容进行比较
    first_result = first_response.json()
    second_result = second_response.json()

def generate_test_order(amount=None):
    if amount is None:
        amount = CONFIG["test_data"]["default_amount"]
    random1 = random.randint(1000,9999)
    trade_no = f"{CONFIG['test_data']['order_prefix']}{int(time.time())}_{random1}"
    return{
        "out_trade_no": trade_no,
        "amount": amount
    }
def validate_common_response(response):
    json_data = response.json()  # 只解析一次
    print(f"实际返回的数据: {json_data}")
    assert response.status_code == 200
    assert json_data["code"] == "0000"      # 使用变量
    assert json_data["message"] == "success"
    assert json_data["data"] is not None

def test_refund_missing_field():
    """测试退款接口缺少必填字段"""
    url = BASE_URL + "/refund"
    data = {
        # 故意不包含 out_trade_no
        "refund_amount": CONFIG["test_data"]["default_amount"],
        "refund_reason": "测试缺少字段"
    }
    response = requests.post(url, json=data)
    validate_common_response(response)
def test_refund_empty_field():
    """测试退款接口空字段"""
    result = generate_test_order()
    trade_no = result["out_trade_no"]
    url = BASE_URL + "/refund"
    data = {
        "refund_amount": "",  # 空字符串
        "refund_reason": "",  # 空字符串
        "out_trade_no": trade_no
    }
    response = requests.post(url, json=data)
    validate_common_response(response)
def test_query_invalid_order():
    """测试查询不存在的订单"""
    url = BASE_URL + "/query"
    params = {
        "out_trade_no": "INVALID_ORDER_123456789"  # 不存在的订单号
    }
    response = requests.get(url, params=params)
    validate_common_response(response)
def validate_error_response(response, expected_code, expected_message):
    body = response.json()
    assert response.status_code == 200
    print(body)
    assert body["code"] == expected_code
    assert body["message"] == expected_message
    assert body["data"] is None
def test_pay_zero_amount():
    result = generate_test_order(amount="0")
    trade_no = result["out_trade_no"]
    amount = result["amount"]
    url = BASE_URL + "/pay"
    data= {
        "amount": amount,
        "subject": "0元支付测试",
        "out_trade_no": trade_no
    }
    response = requests.post(url, json=data)
    validate_error_response(response, "40001", "支付金额不能为0")

def test_pay_min_amount():
    result = generate_test_order()
    trade_no = result["out_trade_no"]
    amount = result["amount"]
    url = BASE_URL + "/pay"
    data= {
        "amount": amount,
        "subject": "0.01元支付测试",
        "out_trade_no": trade_no
    }
    response = requests.post(url, json=data)
    validate_common_response(response)

def test_pay_max_amount():
    result = generate_test_order(amount="50000")
    trade_no = result["out_trade_no"]
    amount = result["amount"]
    url = BASE_URL + "/pay"
    data= {
        "amount": amount,
        "subject": "50000元支付测试",
        "out_trade_no": trade_no
    }
    response = requests.post(url, json=data)
    validate_common_response(response)


def test_pay_over_limit():
    result = generate_test_order(amount="50001")
    trade_no = result["out_trade_no"]
    amount = result["amount"]
    url = BASE_URL + "/pay"
    data= {
        "amount": amount,
        "subject": "50001元支付测试",
        "out_trade_no": trade_no
    }
    response = requests.post(url, json=data)
    validate_error_response(response, "40002", "支付金额超过限额")
def test_insufficient_balance():
    timestamp = int(time.time())
    trade_no = f"TEST_INSUFFICIENT_BALANCE_{timestamp}"
    url = BASE_URL + "/pay"
    data = {
        "amount": "100",
        "subject": "金额不足测试",
        "out_trade_no": trade_no
    }
    response = requests.post(url, json=data)
    validate_error_response(response, "10001", "账户余额不足")
def test_account_frozen():
    timestamp = int(time.time())
    trade_no = f"TEST_ACCOUNT_FROZEN_{timestamp}"
    url = BASE_URL + "/pay"
    data = {
        "amount": "100",
        "subject": "账户冻结测试",
        "out_trade_no": trade_no
    }
    response = requests.post(url, json=data)
    validate_error_response(response, "10002", "账户已被冻结")
import pytest
import requests

BASE_URL = "http://127.0.0.1:8000"

def test_mock_server_health():
    r = requests.get(f"{BASE_URL}/")
    assert r.status_code == 200
    body = r.json()
    assert body.get("message") == "Hello World"
    assert r.headers.get("content-type", "").startswith("application/json")

def test_account_balance_success():
    r = requests.get(f"{BASE_URL}/account/balance", params={"account_no": "123456789"})
    assert r.status_code == 200
    body = r.json()
    assert body["code"] == "0000"
    assert body["message"] == "success"
    assert "data" in body and isinstance(body["data"], dict)
    data = body["data"]
    assert data["account_no"] == "123456789"
    assert data["balance"] == "10000.00"
    assert data["currency"] == "CNY"

def test_account_balance_not_found():
    r = requests.get(f"{BASE_URL}/account/balance", params={"account_no": "999999999"})
    assert r.status_code == 200
    body = r.json()
    assert body["code"] == "1001"
    assert body["message"] == "error"
    assert body["data"] == {}

def test_account_balance_missing_param_returns_422():
    # 少传参数应返回 422（FastAPI 校验错误）
    r = requests.get(f"{BASE_URL}/account/balance")
    assert r.status_code == 422


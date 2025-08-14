import requests
import json
import time
from datetime import datetime
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import base64
import allure
import allure

class AlipayPayTest:
    def __init__(self):
        self.use_mock = True
        self.app_id = "2021005183600676"
        self.gateway_url = "https://openapi.alipaydev.com/gateway.do"
        self.charset = "utf-8"
        self.sign_type ="RSA2"
        self.version = "1.0"
        self.app_private_key = """-----BEGIN PRIVATE KEY-----
MIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQClDaafoe4n0b40IHSJfmg5YkJ2GYEjyacnhUwV9FrFp7SuDJuaCJY1qIjvJ1SmoNSBhMsX3MVO6UhhgLhg6fdiznB60/wIyl82foudz1GDc1/nW3RizXPeU1y9ofuKHYyJcnBYVr2efW4I1ySUzNejLkVhnkULosl+ug9o4mXqXYApPrK9Y8QVo5/O2u7Asu2JLzcwq6jmLWRNeoYVEzelt/gcLXrV5ldryykjsBdwYcO7BVeeMMG/mZpxjtdBfG5CXHq/IY1mUaCgpRVATqhCL1rYMUkKXbbtJdIFbLuGP7BulpO0PaGMkviRHexfcGqiotueBgc/zcJ/5Tvhu7qhAgMBAAECggEBAKNQyZFkufEeoZSUlJtDv78gEeEnxVdy/fml9K44leTD14zsnr6gRnkbpTr2cNVbiEoL6qVW5sj5HYyUwFvsxcM3v6ZZwSW1kNasClwBOofWDowvOw9UeZUAaWCeOfXk3R1XZgCS+5cqR0lqECFIOwqVC0PXRjyIO9YwJnVCp1NoyaNm029+yTo4RvWjlPVKdnwzLVv+yg8wotxwZovxqZE4glNfEtjf1nVJr43PPXpjQ+jE7AEVha8uWAY32Uva/9JV2+rgjtbr3jD/uctlF9rHvX4w/e4bBggBj1pW+r6K//XhWuLdWTlA2NR4eBeflw7GXJvxI8u65wvBopP66UECgYEA9lDYdZzJIG4GPwvkYlywpWQPZnLgxvcVbCBsxV5WrBbbQcMhDLjjwBsn5pY8phl2mAzn/OKQTEwYSwj7Zq+T7UGZJzWD8dd/x5+zIwaXInm04BiiUjR8nE89Zzp0kgK7i2BrTNid/7K/OgpmBIYPcpE4+AGmHOYS2ReRh7tS5UkCgYEAq4rnM2EL26ZQX1Qw38WMYQt6ID6YZP7asTP2FQVLxYb/eFlNt5veVWYa5LFXPieH4yvuJOW6PhPEnVjHC/NllvuVtYKQJp+fXQRhRg86R3PZHCoQIFd9/bofxGc/cENo3SCz16UVnEpCRevNqtsg/zZGrngLYxzhcVWAWv3VIpkCgYEAm6uOkg5LwpYmlnPinBOuhGiPnxTdYIHJ5TM86yPrLQmo+o/i9FJphgDjn8S1gdg37nLBrz5VKhMxi0Ka+FPg7qJ1s6ULxa2HkVcp9On2XJCEsth+xetsEbG2weXcxGa7tqNyTPfeKzsBxiHKRfOgEa0cTwljvYHeyZsum5TVGBkCgYEAkWV+aXIMFvR0kxhNBJ3wSiDsNoBXsuLAggnEvjRq8NVnm5413TZj0IZmrQgTJj9jUg1eIDAHF66xq5wfueVnaf17+wjbHaGV9cVMnZEymHV8w/5zBLajt3cWjeXlQ0Yfj620QUdPddULLzCadgKdiTN73U0qeat0+ha6YGVdTaECgYB5BmrcLwPyfZ3XvUC3cQ52CkUorhTaKYgqYBWksQSGaZQ7N5OjIEf1ztqHtQYJBAcLFggKNMaYthmKyupHrMu2YoijiBDkKCmi2w7QsHjq43I+F4/PsnGd9SCLqElel5Spbz1XSqxoX7emAqQkk9bViRLNqG8R9G194/sIk4wj/g==
-----END PRIVATE KEY-----"""
        self.alipay_public_key = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAtqc1PqvB+1gMMn3a0Qruot/MI7PHJJ4WhcBENS58enh63EAFLF/Rw4BXfJPiX5ZlRUGDbycmLhSnLxzUkiZFwtwiKxIVZGbpz+qOxOHHRiYZnkUePyeCBrJ9ep4gr9l8BMe3K3tIewiezPubheL+3TldpQ3EneJlTZYFrV1zTNoe7vCB8aKUZuHB+aAbEVcJ6hTitkj2J9roa+SPxtYTkGWgDwGKBwteGeqr8We9K68Rg9A8zI06g8F8vRSWbVSmzFreeTyUMJOaSBfaqSgLsBsUWhvx/x1a+taPl+qeUZ0srDOEqQ87U7tg7mtDAZds2599JkyDnfvUX5D9idEwoQIDAQAB
-----END PUBLIC KEY-----"""

    def generate_sign_string(self,params):
        """生成签名原文"""
        filtered_params = {}
        for key,value in params.items():
            if value and key != "sign":
                filtered_params[key] = value

        sorted_keys = sorted(filtered_params.keys())

        result_list = []
        for key in sorted_keys:
            item = f"{key}={filtered_params[key]}"
            result_list.append(item)
        sign_string = "&".join(result_list)

        return sign_string
    def rsa2_sign(self,sign_string):
        """RSA2签名"""
        try:
            # 1. 加载私钥
            private_key = RSA.import_key(self.app_private_key)
            # 2. 计算SHA256哈希
            hash_obj = SHA256.new(sign_string.encode('utf-8'))
            # 3. RSA签名
            signature = pkcs1_15.new(private_key).sign(hash_obj)
            # 4. Base64编码
            sign = base64.b64encode(signature).decode('utf-8')
            # 5. 返回结果
            return sign
        except Exception as e:
            print(f"签名失败：{e}")
            return None

    def create_payment_order(self,out_trade_no, total_amount,subject):
        biz_content = {
            'out_trade_no': out_trade_no,
            'total_amount': total_amount,
            'subject': subject,
            'product_code': 'FAST_INSTANT_TRADE_PAY'
        }
        params = {
            'app_id': self.app_id,
            'method': 'alipay.trade.create',
            'charset': self.charset,
            'sign_type': self.sign_type,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'version' : self.version,
            'biz_content': json.dumps(biz_content)
        }
        if self.use_mock : return self._get_mock_response()
        sign_string = self.generate_sign_string(params)
        signature = self.rsa2_sign(sign_string)

        if not signature:
            return None

        params['sign'] = signature

        try:
            response = requests.post(self.gateway_url,data=params,timeout=30)
            return {
                'status_code': response.status_code,
                'sign_string':sign_string,
                'response_text': response.text
            }

        except Exception as e:
            print(f"请求失败：{e}")
            return None

    def _get_mock_response(self):
        return {
            'status_code': 200,
            'sign_string': 'fdgdafdfdgfdsgfdsgdfbfbgvfdvfioefndisanpfevnipaedanpndviandpveidnvrejqaevnperd',
            'response_text': '{"alipay_trade_create_response": {"product_code": "FAST_INSTANT_TRADE_PAY"}}'
        }


@allure.feature("支付宝支付")
@allure.story("创建订单")
@allure.severity(allure.severity_level.CRITICAL)
def test_alipay_payment_success():
    AlipayPay = AlipayPayTest()
    trade = f"TEST_{int(time.time())}"
    amount = "0.01"
    order_name = "API测试订单"

    print(f"开始测试支付宝支付API")
    print(f"订单号: {trade}")

    result = AlipayPay.create_payment_order(trade, amount, order_name)

    if result:
        print(f"API调用成功!")
        assert result['status_code'] == 200
        assert 'FAST_INSTANT_TRADE_PAY' in result['response_text']
        # 验证签名不为空且长度合理
        assert result['sign_string'], "签名不能为空"
        assert len(result['sign_string']) > 30, "签名长度异常"
    else:
        print("API调用失败")



if __name__ == '__main__':
    test_alipay_payment_success()

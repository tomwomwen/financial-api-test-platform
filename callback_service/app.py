from flask import Flask, request, jsonify
import json
import logging
from datetime import datetime


app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format ='%(asctime)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger()

def validate_callback_data(data):
    """
    验证回调数据的完整性和有效性

    Args:
        data (dict): HTTP请求的JSON数据

    Returns:
        dict: 验证结果，包含success、message和data字段
    """
    if not data:
        return {"success": False, "message": "请求数据为空"}

    required_fields = ['order_id', 'amount', 'signature']
    for field in required_fields:
        if field not in data:
            return {"success": False, "message": f"{field}为空"}
        if data[field] == "":
            return {"success": False, "message": f"{field}为空字符串"}
    return {"success": True, "message": "请求数据成功", "data": data}
@app.route('/')
def index():
    return "Hello world"
@app.route('/callback', methods=['POST'])
def callback():
    try:
        data = request.get_json()
        validation_result = validate_callback_data(data)
        if not validation_result["success"]:
            logger.error(f"请求数据失败：{validation_result['message']}")
            return jsonify({"status": "error", "message": validation_result['message']}), 400
        order_id = data.get('order_id', '未知')
        amount = data.get('amount', '未知')
        signature = data.get('signature', '未知')

        logger.info("收到回调数据")
        logger.info(f"订单号: {order_id}")
        logger.info(f"金额 ： {amount}")
        logger.info(f"签名 ： {signature}")
        logger.info("回调处理状态: SUCCESS")

        return jsonify({
            "status": "success",
            "message": "回调处理成功"
        })
    except Exception as e:
        logger.error(f"处理回调时发生错误: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "回调处理失败"
        }),500

if __name__ == '__main__':
    app.run()
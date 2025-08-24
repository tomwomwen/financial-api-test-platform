from operator import truediv

import pandas as pd
import time
import random
import datetime
import os

def generate_reconciliation_data():
    """
    生成对账测试数据，包括支付系统和银行流水数据

    Returns:
        bool: 生成成功返回True，失败返回False
    """
    try:
        # 创建订单号列表
        order_ids = ["ORDER_001", "ORDER_002", "ORDER_003", "ORDER_004", "ORDER_005"]
        # 创建用户ID列表
        user_ids = ["USER_001", "USER_002", "USER_003", "USER_004", "USER_005"]
        # 创建支付方式列表
        payment_methods = ["支付宝", "微信支付", "银行卡", "支付宝", "微信支付"]
        # 创建状态列表
        statuses = ["成功", "成功", "成功", "处理中", "成功"]
        # 创建金额列表
        amounts = [100.00, 50.50, 200.00, 75.25, 150.00]
        # 创建交易时间列表（今天的不同时间）
        transaction_times = ["2025-01-17 10:00:00", "2025-01-17 10:30:00", "2025-01-17 11:00:00", "2025-01-17 11:30:00", "2025-01-17 12:00:00"]
        # 创建支付系统数据
        payment_data = {
            '订单号': order_ids,
            '金额': amounts,
            '状态': statuses,
            '交易时间': transaction_times,
            '用户ID': user_ids,
            '支付方式': payment_methods
        }
        payment_df = pd.DataFrame(payment_data)

        # 创建银行流水数据（故意制造一些差异）
        bank_data = {
            '订单号': ["ORDER_001", "ORDER_002", "ORDER_003", "ORDER_004", "ORDER_005"],
            '金额': [100.00, 49.50, 200.00, 75.25, 150.00],  # 第二条金额不同
            '状态': ["成功", "成功", "成功", "成功", "成功"],    # 第四条状态不同
            '交易时间': ["2025-01-17 10:00:00", "2025-01-17 10:30:00", "2025-01-17 11:00:00", "2025-01-17 11:30:00", "2025-01-17 12:00:00"],
            '用户ID': ["USER_001", "USER_002", "USER_003", "USER_004", "USER_005"],
            '支付方式': ["支付宝", "微信支付", "银行卡", "支付宝", "微信支付"]
        }

        # 转换为DataFrame
        bank_df = pd.DataFrame(bank_data)

        os.makedirs("../reports", exist_ok=True)
        payment_df.to_csv("../reports/payment_system.csv", index=False,encoding='gbk')
        bank_df.to_csv("../reports/bank_records.csv", index=False,encoding='gbk')

        print("CSV文件生成完成！")
        print(f"支付系统数据：{len(payment_df)}条")
        print(f"银行流水数据：{len(bank_df)}条")
        return True
    except Exception as e:
        print(f"生成数据失败：{str(e)}")
        return False
if __name__ == "__main__":
    success = generate_reconciliation_data()
    if success:
        print("数据报告生成成功")
    else:
        print("数据报告生成失败")
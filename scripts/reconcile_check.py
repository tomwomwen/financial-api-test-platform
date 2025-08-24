import pandas as pd

def perform_reconciliation():
    """
    执行对账操作，对比支付系统和银行流水数据

    Returns:
        dict: 对账结果统计信息
    """
    try:
            payment_df = pd.read_csv('../reports/payment_system.csv',encoding='gbk')
            bank_df = pd.read_csv('../reports/bank_records.csv',encoding='gbk')

            print(f"支付系统数据：{len(payment_df)}条")
            print(f"银行流水数据：{len(bank_df)}条")

            payment_counts= payment_df['状态'].value_counts()
            bank_counts = bank_df['状态'].value_counts()

            print(f"支付系统数据状态分布：{payment_counts}")
            print(f"银行系统数据状态分布：{bank_counts}")

            payment_sum = payment_df['金额'].sum()
            bank_sum = bank_df['金额'].sum()

            print(f"支付系统数据总金额：{payment_sum}")
            print(f"银行系统数据总金额：{bank_sum}")

            merged_df = pd.merge(payment_df, bank_df, how='inner', on='订单号')

            print(f"合并后数据：{len(merged_df)}条")
            print("合并后的列名：", merged_df.columns.tolist())
            print("前几行数据预览：")
            print(merged_df.head())

            amount_diff = merged_df[merged_df['金额_x'] != merged_df['金额_y']]
            status_diff = merged_df[merged_df['状态_x'] != merged_df['状态_y']]

            print(f"金额差异记录：{len(amount_diff)}条")
            print(amount_diff)
            print(f"状态差异记录：{len(status_diff)}条")
            print(status_diff)

            all_diff = pd.concat([amount_diff, status_diff]).drop_duplicates()
            print(f"总差异记录：{len(all_diff)}条")

            all_diff.to_csv('../reports/reconcile_diff.csv',index=False,encoding='gbk')
            print("\n=== 对账结果汇总 ===")
            print(f"金额差异：{len(amount_diff)}条")
            print(f"状态差异：{len(status_diff)}条")
            print(f"总差异：{len(all_diff)}条")
            return {
                "success": True,
                "total_diff": len(all_diff),
                "amount_diff": len(amount_diff),
                "status_diff": len(status_diff)
            }
    except Exception as e:
        print(f"对账失败：{str(e)}")
        return {"success": False, "error": str(e)}


import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from reconcile_check import perform_reconciliation

def test_reconciliation_success():
    """测试对账功能执行成功"""
    result = perform_reconciliation()
    assert result['success'] == True
    assert result['total_diff'] == 2
    assert result['amount_diff'] == 1
    assert result['status_diff'] == 1

def test_csv_file_generate():
    perform_reconciliation()
    assert os.path.exists('../reports/reconcile_diff.csv')

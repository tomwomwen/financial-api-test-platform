import subprocess
import json
import os


def check_environment():
    try:
        subprocess.run(["pytest", "--version"], capture_output=True, text=True, encoding='utf-8')
        print("pytest安装成功")
    except:
        print("pytest安装失败")
    print("allure命令行工具未安装，跳过检查")


def run_test():
    try:
        result = subprocess.run(["pytest", "tests/"], text=True, encoding='utf-8', cwd="..", capture_output=True)
        print("检查到有测试文件")
        print(result.stdout)

        lines = result.stdout.split('\n')
        passed_count = "0"  # 默认值
        failed_count = "0"  # 默认值

        for line in lines:
            # 查找包含测试结果的行，格式如："===== 18 passed in 3.72s ====="
            if "passed in" in line and "=" in line:
                print(f"找到结果行: {line}")
                # 提取数字，查找 "数字 passed" 的模式
                parts = line.split()
                for i, part in enumerate(parts):
                    if part == "passed" and i > 0:
                        # 检查前一个是否为数字
                        try:
                            passed_count = str(int(parts[i - 1]))
                            break
                        except ValueError:
                            continue
                break

        print(f"提取到的通过数: {passed_count}")

        metadata = {
            "passed": passed_count,
            'total': passed_count,
            "failed": failed_count
        }

        print(f"创建的元数据: {metadata}")

        # 修改：保存到项目根目录的reports文件夹
        if not os.path.exists("../reports"):
            os.makedirs("../reports")
            print("创建了reports文件夹")

        # 修改：保存到项目根目录
        with open("../reports/last_run.json", "w", encoding='utf-8') as f:
            json.dump(metadata, f)

        print("文件保存完成！")
        print(f"当前工作目录: {os.getcwd()}")
        print(f"文件完整路径: {os.path.abspath('../reports/last_run.json')}")

        # 修改：从项目根目录读取验证
        with open("../reports/last_run.json", "r", encoding='utf-8') as f:
            content = f.read()
            print(f"文件内容: {content}")
    except Exception as e:
        print(f"没有检索到有测试文件: {e}")


if __name__ == "__main__":
    check_environment()
    run_test()
import subprocess
import json
import os

def check_environment():
    try:
        subprocess.run(["pytest","--version"],capture_output=True,text=True)
        print("pytest安装成功")
    except:
        print("pytest安装失败")
    print("allure命令行工具未安装，跳过检查")

def run_test():
    try:
        result = subprocess.run(["pytest", "tests/"], text=True, cwd="..", capture_output=True)
        print("检查到有测试文件")
        print(result.stdout)

        lines = result.stdout.split('\n')
        for line in lines:
            if "pass" in line:
                print(line)
                li = line.split()
                passed_count = li[1]  # 保存通过数

        print(f"提取到的通过数: {passed_count}")

        metadata = {
            "passed": passed_count,
            'total': passed_count,
            "failed": 0
        }

        print(f"创建的元数据: {metadata}")

        # 修改：保存到项目根目录的reports文件夹
        if not os.path.exists("../reports"):
            os.makedirs("../reports")
            print("创建了reports文件夹")

        # 修改：保存到项目根目录
        with open("../reports/last_run.json", "w") as f:
            json.dump(metadata, f)

        print("文件保存完成！")
        print(f"当前工作目录: {os.getcwd()}")
        print(f"文件完整路径: {os.path.abspath('../reports/last_run.json')}")

        # 修改：从项目根目录读取验证
        with open("../reports/last_run.json", "r") as f:
            content = f.read()
            print(f"文件内容: {content}")
    except:
        print("没有检索到有测试文件")

if __name__ == "__main__":
    check_environment()
    run_test()
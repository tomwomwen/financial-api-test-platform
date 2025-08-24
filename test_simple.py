
import os
import re
from pathlib import Path
from typing import Dict, List, Tuple


class CodeLineCounter:
    """代码行数统计器"""

    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.file_extensions = {'.py', '.md', '.txt', '.yml', '.yaml', '.json'}
        self.exclude_dirs = {'__pycache__', '.git', '.pytest_cache', 'allure-results', 'node_modules'}

    def is_comment_line(self, line: str, file_ext: str) -> bool:
        """判断是否为注释行"""
        stripped = line.strip()
        if not stripped:
            return False

        if file_ext == '.py':
            return stripped.startswith('#') or (stripped.startswith('"""') or stripped.startswith("'''"))
        elif file_ext == '.md':
            return stripped.startswith('<!--') or stripped.endswith('-->')
        elif file_ext in {'.yml', '.yaml'}:
            return stripped.startswith('#')
        return False

    def is_empty_line(self, line: str) -> bool:
        """判断是否为空行"""
        return len(line.strip()) == 0

    def count_file_lines(self, file_path: Path) -> Dict[str, int]:
        """统计单个文件的行数"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
        except Exception as e:
            print(f"警告：无法读取文件 {file_path}: {e}")
            return {'total': 0, 'code': 0, 'comment': 0, 'empty': 0}

        total_lines = len(lines)
        code_lines = 0
        comment_lines = 0
        empty_lines = 0

        file_ext = file_path.suffix.lower()
        in_multiline_comment = False

        for line in lines:
            if self.is_empty_line(line):
                empty_lines += 1
            elif file_ext == '.py' and ('"""' in line or "'''" in line):
                # Python多行注释处理
                if line.strip().startswith('"""') or line.strip().startswith("'''"):
                    comment_lines += 1
                    if not (line.count('"""') >= 2 or line.count("'''") >= 2):
                        in_multiline_comment = not in_multiline_comment
                else:
                    if in_multiline_comment:
                        comment_lines += 1
                        if '"""' in line or "'''" in line:
                            in_multiline_comment = False
                    else:
                        code_lines += 1
            elif in_multiline_comment:
                comment_lines += 1
            elif self.is_comment_line(line, file_ext):
                comment_lines += 1
            else:
                code_lines += 1

        return {
            'total': total_lines,
            'code': code_lines,
            'comment': comment_lines,
            'empty': empty_lines
        }

    def should_exclude_dir(self, dir_path: Path) -> bool:
        """判断是否应该排除某个目录"""
        return any(exclude in str(dir_path) for exclude in self.exclude_dirs)

    def get_all_files(self) -> List[Path]:
        """获取所有需要统计的文件"""
        files = []
        for root, dirs, filenames in os.walk(self.project_root):
            root_path = Path(root)

            # 排除特定目录
            if self.should_exclude_dir(root_path):
                continue

            for filename in filenames:
                file_path = root_path / filename
                if file_path.suffix.lower() in self.file_extensions:
                    files.append(file_path)

        return sorted(files)

    def count_project_lines(self) -> Dict:
        """统计整个项目的行数"""
        all_files = self.get_all_files()

        total_stats = {'total': 0, 'code': 0, 'comment': 0, 'empty': 0}
        file_stats = {}
        ext_stats = {}

        print(f"开始统计项目：{self.project_root.name}")
        print(f"项目路径：{self.project_root}")
        print("-" * 80)

        for file_path in all_files:
            relative_path = file_path.relative_to(self.project_root)
            file_stat = self.count_file_lines(file_path)

            # 累计总数
            for key in total_stats:
                total_stats[key] += file_stat[key]

            # 记录文件统计
            file_stats[str(relative_path)] = file_stat

            # 按扩展名统计
            ext = file_path.suffix.lower()
            if ext not in ext_stats:
                ext_stats[ext] = {'total': 0, 'code': 0, 'comment': 0, 'empty': 0, 'files': 0}

            for key in ext_stats[ext]:
                if key == 'files':
                    ext_stats[ext][key] += 1
                elif key in file_stat:
                    ext_stats[ext][key] += file_stat[key]

        return {
            'total_stats': total_stats,
            'file_stats': file_stats,
            'ext_stats': ext_stats,
            'file_count': len(all_files)
        }

    def print_results(self, results: Dict):
        """打印统计结果"""
        total_stats = results['total_stats']
        file_stats = results['file_stats']
        ext_stats = results['ext_stats']
        file_count = results['file_count']

        print(f"统计完成！共分析了 {file_count} 个文件")
        print("=" * 80)

        # 总体统计
        print("总体统计：")
        print(f"   总行数：{total_stats['total']:,}")
        print(f"   代码行：{total_stats['code']:,}")
        print(f"   注释行：{total_stats['comment']:,}")
        print(f"   空白行：{total_stats['empty']:,}")
        print()

        # 按文件类型统计
        print("按文件类型统计：")
        for ext, stats in sorted(ext_stats.items()):
            print(f"   {ext} 文件 ({stats['files']} 个):")
            print(f"     总行数：{stats['total']:,}")
            print(f"     代码行：{stats['code']:,}")
            print(f"     注释行：{stats['comment']:,}")
            print(f"     空白行：{stats['empty']:,}")
        print()

        # 详细文件统计（只显示有实际内容的文件）
        print("详细文件统计（按代码行数排序）：")
        sorted_files = sorted(file_stats.items(), key=lambda x: x[1]['code'], reverse=True)

        for file_path, stats in sorted_files:
            if stats['total'] > 0:  # 只显示非空文件
                print(f"   {file_path}")
                print \
                    (f"     总行数：{stats['total']:,} | 代码：{stats['code']:,} | 注释：{stats['comment']:,} | 空白：{stats['empty']:,}")


def main():
    """主函数"""
    # 获取当前脚本所在目录作为项目根目录
    current_dir = Path(__file__).parent

    print("代码行数统计工具")
    print("=" * 80)

    counter = CodeLineCounter(current_dir)
    results = counter.count_project_lines()
    counter.print_results(results)

    print("\n" + "=" * 80)
    print("统计完成！")


if __name__ == "__main__":
    main()

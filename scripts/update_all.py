#!/usr/bin/env python3
"""
一键更新所有数据
统一入口，执行完整的数据更新流程
"""
import subprocess
import sys
from pathlib import Path

# 添加脚本目录到路径
SCRIPTS_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS_DIR))

from utils import colorize


def run_script(script_name: str, args: list = None, description: str = '') -> bool:
    """运行脚本"""
    script_path = SCRIPTS_DIR / script_name
    if not script_path.exists():
        print(f"   {colorize('❌', 'red')} 脚本不存在: {script_name}")
        return False

    cmd = [sys.executable, str(script_path)]
    if args:
        cmd.extend(args)

    print(f"\n{'=' * 50}")
    print(f"🔧 {description or script_name}")
    print(f"{'=' * 50}")

    try:
        result = subprocess.run(cmd, cwd=SCRIPTS_DIR)
        return result.returncode == 0
    except Exception as e:
        print(f"   {colorize('❌', 'red')} 执行失败: {e}")
        return False


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(
        description='一键更新 AWS GPU 数据',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  python3 update_all.py --all          # 完整更新（下载 + 转换 + 生成）
  python3 update_all.py --convert      # 只转换数据（不下载）
  python3 update_all.py --pages        # 只生成 HTML 页面
  python3 update_all.py --gpu-md       # 只更新 gpu.md
'''
    )

    parser.add_argument('--download', '-d', action='store_true',
                        help='下载最新数据')
    parser.add_argument('--convert', '-c', action='store_true',
                        help='转换数据格式')
    parser.add_argument('--pages', '-p', action='store_true',
                        help='生成 HTML 页面')
    parser.add_argument('--gpu-md', '-g', action='store_true',
                        help='生成 gpu.md 文档')
    parser.add_argument('--all', '-a', action='store_true',
                        help='执行所有步骤')
    parser.add_argument('--skip-download', action='store_true',
                        help='跳过下载步骤（与 --all 一起使用）')

    args = parser.parse_args()

    # 如果没有指定任何参数，显示帮助
    if not any([args.download, args.convert, args.pages, args.gpu_md, args.all]):
        parser.print_help()
        print(f"\n{colorize('提示:', 'yellow')} 请指定要执行的步骤，或使用 --all 执行完整更新")
        return 0

    print("=" * 60)
    print("🚀 AWS GPU 数据一键更新工具")
    print("=" * 60)

    steps_run = 0
    steps_success = 0

    # 步骤 1: 下载数据
    if args.download or (args.all and not args.skip_download):
        steps_run += 1
        if run_script('download_data.py', ['--all'], '步骤 1/4: 下载最新数据'):
            steps_success += 1
        else:
            print(f"\n{colorize('⚠️', 'yellow')} 下载失败，尝试继续后续步骤...")

    # 步骤 2: 转换数据
    if args.convert or args.all:
        steps_run += 1
        if run_script('convert_data.py', ['--all'], '步骤 2/4: 转换数据格式'):
            steps_success += 1
        else:
            print(f"\n{colorize('❌', 'red')} 数据转换失败")
            if args.all:
                print("后续步骤依赖数据转换，终止执行")
                return 1

    # 步骤 3: 生成页面
    if args.pages or args.all:
        steps_run += 1
        if run_script('generate_pages.py', [], '步骤 3/4: 生成 HTML 页面'):
            steps_success += 1

    # 步骤 4: 生成 gpu.md
    if args.gpu_md or args.all:
        steps_run += 1
        if run_script('generate_gpu_md.py', [], '步骤 4/4: 生成 gpu.md 文档'):
            steps_success += 1

    # 总结
    print("\n" + "=" * 60)
    print("📊 更新总结")
    print("=" * 60)
    print(f"执行步骤: {steps_run}")
    print(f"成功: {colorize(str(steps_success), 'green')}")
    print(f"失败: {colorize(str(steps_run - steps_success), 'red') if steps_run > steps_success else '0'}")

    if steps_success == steps_run:
        print(f"\n{colorize('🎉 所有更新完成！', 'green')}")
        return 0
    else:
        print(f"\n{colorize('⚠️ 部分步骤失败', 'yellow')}")
        return 1


if __name__ == '__main__':
    sys.exit(main())

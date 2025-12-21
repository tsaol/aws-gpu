#!/usr/bin/env python3
"""
下载 AWS 实例数据
从 instances.vantage.sh 下载最新的实例数据
"""
import sys
import urllib.request
import urllib.error
from pathlib import Path

# 添加脚本目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from config import DATA_SOURCES, RAW_DATA_FILES, DATA_DIR
from utils import print_progress, colorize


def download_file(url: str, output_path: Path, description: str = '') -> bool:
    """下载文件并显示进度"""
    print(f"\n📥 下载 {description or output_path.name}...")
    print(f"   URL: {url}")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        # 创建请求
        request = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (compatible; aws-gpu-updater/1.0)'}
        )

        # 打开连接
        with urllib.request.urlopen(request, timeout=60) as response:
            total_size = response.headers.get('Content-Length')
            total_size = int(total_size) if total_size else 0

            # 下载数据
            downloaded = 0
            chunk_size = 1024 * 1024  # 1MB

            with open(output_path, 'wb') as f:
                while True:
                    chunk = response.read(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)

                    if total_size > 0:
                        print_progress(
                            downloaded, total_size,
                            prefix='   ',
                            suffix=f'{downloaded / 1024 / 1024:.1f} MB'
                        )
                    else:
                        print(f'\r   已下载: {downloaded / 1024 / 1024:.1f} MB', end='', flush=True)

            print()

        # 验证文件
        file_size = output_path.stat().st_size
        print(f"   {colorize('✅', 'green')} 下载完成: {file_size / 1024 / 1024:.1f} MB")
        return True

    except urllib.error.HTTPError as e:
        print(f"   {colorize('❌', 'red')} HTTP 错误: {e.code} {e.reason}")
        return False
    except urllib.error.URLError as e:
        print(f"   {colorize('❌', 'red')} 连接错误: {e.reason}")
        return False
    except Exception as e:
        print(f"   {colorize('❌', 'red')} 下载失败: {e}")
        return False


def download_global_data() -> bool:
    """下载全球数据"""
    return download_file(
        DATA_SOURCES['global'],
        RAW_DATA_FILES['global'],
        '全球实例数据'
    )


def download_china_data() -> bool:
    """下载中国区数据"""
    return download_file(
        DATA_SOURCES['china'],
        RAW_DATA_FILES['china'],
        '中国区实例数据'
    )


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description='下载 AWS 实例数据')
    parser.add_argument('--global', '-g', dest='download_global', action='store_true',
                        help='下载全球数据')
    parser.add_argument('--china', '-c', dest='download_china', action='store_true',
                        help='下载中国区数据')
    parser.add_argument('--all', '-a', action='store_true',
                        help='下载所有数据')

    args = parser.parse_args()

    # 如果没有指定参数，默认下载全部
    if not (args.download_global or args.download_china or args.all):
        args.all = True

    print("=" * 50)
    print("📦 AWS 实例数据下载工具")
    print("=" * 50)
    print(f"数据目录: {DATA_DIR}")

    success_count = 0
    total_count = 0

    # 下载全球数据
    if args.download_global or args.all:
        total_count += 1
        if download_global_data():
            success_count += 1

    # 下载中国区数据
    if args.download_china or args.all:
        total_count += 1
        if download_china_data():
            success_count += 1

    # 总结
    print("\n" + "=" * 50)
    print("📊 下载总结")
    print("=" * 50)
    print(f"成功: {colorize(str(success_count), 'green')} / {total_count}")

    if success_count == total_count:
        print(f"\n{colorize('🎉 所有数据下载完成！', 'green')}")
        print("\n下一步: 运行 convert_data.py 转换数据")
        return 0
    else:
        print(f"\n{colorize('⚠️  部分数据下载失败', 'yellow')}")
        return 1


if __name__ == '__main__':
    sys.exit(main())

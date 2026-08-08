from pathlib import Path
import csv
from datetime import datetime
from time import perf_counter


def get_csv_files(input_dir: Path) -> list[Path]:
    """inputフォルダ内のCSVファイルを取得する。"""
    return sorted(input_dir.glob("*.csv"))


def create_output_path(output_dir: Path) -> Path:
    """日時付きの出力ファイルパスを作成する。"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return output_dir / f"売上結合_{timestamp}.csv"


def merge_csv_files(csv_files: list[Path], output_path: Path) -> int:
    """複数のCSVを1つに結合し、書き込んだデータ件数を返す。"""

    header = None
    total_rows = 0

    with output_path.open(
        "w",
        encoding="utf-8-sig",
        newline=""
    ) as output_file:

        writer = csv.writer(output_file)

        for csv_file in csv_files:
            print(f"読み込み中: {csv_file.name}")

            with csv_file.open(
                "r",
                encoding="utf-8-sig",
                newline=""
            ) as input_file:

                reader = csv.reader(input_file)

                try:
                    current_header = next(reader)
                except StopIteration:
                    print(f"空のCSVをスキップしました: {csv_file.name}")
                    continue

                if header is None:
                    header = current_header
                    writer.writerow(header)

                elif current_header != header:
                    raise ValueError(
                        f"列構成が異なります: {csv_file.name}"
                    )

                for row in reader:
                    if not row:
                        continue

                    writer.writerow(row)
                    total_rows += 1

    return total_rows


def main():
    print("=" * 40)
    print("CSV Merge Tool")
    print("=" * 40)

    start_time = perf_counter()

    base_dir = Path(__file__).resolve().parent
    input_dir = base_dir / "input"
    output_dir = base_dir / "output"

    output_dir.mkdir(exist_ok=True)

    csv_files = get_csv_files(input_dir)

    if not csv_files:
        print("CSVファイルが見つかりません。")
        return

    output_path = create_output_path(output_dir)

    try:
        total_rows = merge_csv_files(csv_files, output_path)

    except ValueError as error:
        if output_path.exists():
            output_path.unlink()

        print()
        print("処理を中止しました。")
        print(error)
        return

    except Exception as error:
        if output_path.exists():
            output_path.unlink()

        print()
        print("予期しないエラーが発生しました。")
        print(error)
        print(error)
        return


    elapsed_time = perf_counter() - start_time

    print()
    print("=" * 40)
    print("CSVの結合が完了しました。")
    print(f"対象ファイル数 : {len(csv_files)}")
    print(f"データ件数     : {total_rows}")
    print(f"処理時間       : {elapsed_time:.3f}秒")
    print(f"保存先         : {output_path}")
    print("=" * 40, flush=True)

if __name__ == "__main__":
    main()
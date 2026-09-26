#!/usr/bin/env python
"""二维码批量生成工具。"""

import argparse
import csv
import re
from pathlib import Path

import qrcode
from qrcode.constants import ERROR_CORRECT_H


def make_qr(data: str, size: int, fill: str, back: str, logo: str | None) -> "qrcode.image.pil.PilImage":
    qr = qrcode.QRCode(error_correction=ERROR_CORRECT_H, box_size=10, border=2)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill, back_color=back).convert("RGB")
    img = img.resize((size, size))

    if logo:
        from PIL import Image
        icon = Image.open(logo).convert("RGBA")
        side = size // 4
        icon = icon.resize((side, side))
        pos = ((size - side) // 2, (size - side) // 2)
        img.paste(icon, pos, icon)
    return img


def safe_name(text: str) -> str:
    name = re.sub(r"[^\w\u4e00-\u9fa5-]+", "_", text).strip("_")
    return (name[:50] or "qr") + ".png"


def main() -> int:
    parser = argparse.ArgumentParser(description="二维码批量生成")
    parser.add_argument("content", nargs="?", help="二维码内容")
    parser.add_argument("-o", "--output", help="输出文件")
    parser.add_argument("--size", type=int, default=400)
    parser.add_argument("--fill", default="black")
    parser.add_argument("--back", default="white")
    parser.add_argument("--batch", help="内容列表文件")
    parser.add_argument("--csv", help="CSV 文件（内容,文件名）")
    parser.add_argument("--out-dir", default="qrcodes")
    parser.add_argument("--wifi", help="WiFi 名称")
    parser.add_argument("--password", help="WiFi 密码")
    parser.add_argument("--logo", help="logo 图片")
    args = parser.parse_args()

    # WiFi 模式
    if args.wifi:
        pw = args.password or ""
        data = f"WIFI:T:WPA;S:{args.wifi};P:{pw};;"
        out = Path(args.output or "wifi.png")
        make_qr(data, args.size, args.fill, args.back, args.logo).save(out)
        print(f"已生成 WiFi 二维码 -> {out}")
        return 0

    # CSV 批量
    if args.csv:
        out_dir = Path(args.out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        count = 0
        with open(args.csv, newline="", encoding="utf-8-sig") as fh:
            for row in csv.reader(fh):
                if not row or not row[0].strip():
                    continue
                name = row[1].strip() if len(row) > 1 and row[1].strip() else safe_name(row[0])
                if not name.endswith(".png"):
                    name += ".png"
                make_qr(row[0].strip(), args.size, args.fill, args.back, args.logo).save(out_dir / name)
                count += 1
        print(f"已生成 {count} 个二维码 -> {out_dir}")
        return 0

    # 文本列表批量
    if args.batch:
        out_dir = Path(args.out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        lines = [l.strip() for l in Path(args.batch).read_text(encoding="utf-8").splitlines() if l.strip()]
        for line in lines:
            make_qr(line, args.size, args.fill, args.back, args.logo).save(out_dir / safe_name(line))
        print(f"已生成 {len(lines)} 个二维码 -> {out_dir}")
        return 0

    # 单个
    if not args.content:
        parser.print_help()
        return 1
    out = Path(args.output or "qr.png")
    make_qr(args.content, args.size, args.fill, args.back, args.logo).save(out)
    print(f"已生成 -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
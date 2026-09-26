# qr-generator

二维码批量生成工具。把链接、文本、WiFi 信息、联系人批量转成二维码图片。

## 安装

```bash
pip install -r requirements.txt
```

## 用法

```bash
# 生成单个二维码
python qrgen.py "https://example.com" -o qr.png

# 批量：从文件读取内容（每行一个）
python qrgen.py --batch links.txt --out-dir ./qrcodes

# 自定义大小和颜色
python qrgen.py "hello" -o hello.png --size 500 --fill "#1a1a1a"

# 生成 WiFi 二维码
python qrgen.py --wifi "MyWiFi" --password "12345678" -o wifi.png

# CSV 批量（第一列内容，第二列文件名）
python qrgen.py --csv data.csv --out-dir ./out
```

## 参数

- `-o/--output`：输出文件
- `--size`：图片边长（默认 400）
- `--fill` / `--back`：前景/背景色
- `--batch`：内容列表文件
- `--csv`：CSV 批量（内容,文件名）
- `--out-dir`：批量输出目录
- `--wifi`：生成 WiFi 二维码（配 --password）
- `--logo`：中间叠加 logo 图片
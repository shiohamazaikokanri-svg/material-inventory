# 材料在庫管理システム

Django + SQLite で作成した材料在庫管理アプリです。Excel取込、材料一覧、検索、材質・板厚フィルター、同一材料の集計、合計枚数・合計重量の確認ができます。

データの流れ:

```text
Excel → SQLite → App
```

Excelファイルは取込時だけ読み込みます。画面表示、検索、フィルター、集計はSQLiteデータベースを使用します。

## 起動方法

```bash
cd "/Users/bhimjoshi/Documents/New project/material_inventory"
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python manage.py migrate
.venv/bin/python manage.py runserver
```

ブラウザで http://127.0.0.1:8000/ を開きます。

## Excel列

必須列:

- キー
- 材質
- 板厚
- 巾
- 長さ
- 枚数
- 重量

任意列:

- メーカー
- 場所
- 番地

英語列名や `Qty` などの一般的な別名にも対応しています。

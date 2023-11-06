# LabelmeToYOLO Converter

このスクリプトは、Labelmeによって生成されたJSON形式のアノテーションをYOLOフォーマットに変換するツールです。これにより、オブジェクト検出モデルのトレーニングデータとして使用するために、アノテーションを簡単に準備することができます。

## 機能

- Labelme JSONファイルからYOLOフォーマットへの変換
- セグメンテーションデータセットへの対応 (YOLOv5 v7.0)

## 前提条件

- Python 3
- PIL
- NumPy
- labelme (画像データのデコード用)

## セットアップ

リポジトリをクローンし、必要な依存関係をインストールしてください。

```
git clone [リポジトリURL]
cd [クローンしたリポジトリディレクトリ]
pip install -r requirements.txt
```

## 使用方法

コマンドラインからスクリプトを実行してください。以下はその実行例です。


```
python labelme_to_yolo.py --json_dir=/path/to/labelme/jsons --output_dir=/path/to/yolo/labels
```

### 引数
- --json_dir : Labelme JSONファイルが格納されているディレクトリのパス。
- --output_dir : YOLO形式のアノテーションファイルを保存するディレクトリのパス。
- --seg : オプション。セグメンテーションデータセットに変換する場合に使用します。


## 出力形式
出力される .txt ファイルには、YOLOフォーマットのアノテーションが含まれます。各行は以下の形式を取ります。

```
<class_id> <x_center> <y_center> <width> <height>
```

## 注意事項
- このスクリプトは、Labelmeによって作成された特定のJSONフォーマットを想定しています。入力ファイルがこのフォーマットと異なる場合は、適宜スクリプトを調整してください。
- 出力ディレクトリはスクリプトによって自動的に作成されますが、--json_dir で指定されるディレクトリは事前に存在している必要があります。
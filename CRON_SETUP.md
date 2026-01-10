# 自動実行の設定方法（cron）

このスクリプトを毎朝8時に自動実行するための設定手順です。

## macOS / Linuxの場合

### 1. crontabを編集

```bash
crontab -e
```

### 2. 以下の行を追加

```
0 8 * * * /Users/yoshida_antlerspirits/projects/ai-news-slack-notifier/run_news_notifier.sh
```

**重要:** パスは絶対パスで指定してください。上記のパスを実際のプロジェクトパスに置き換えてください。

現在のパスを確認するには：
```bash
cd /Users/yoshida_antlerspirits/projects/ai-news-slack-notifier
pwd
```

### 3. crontabの記法

```
分 時 日 月 曜日 コマンド
```

#### 例

- `0 8 * * *` - 毎日午前8時
- `0 8 * * 1-5` - 平日（月〜金）の午前8時
- `0 8,20 * * *` - 毎日午前8時と午後8時
- `*/30 * * * *` - 30分ごと

### 4. cronの設定を確認

```bash
crontab -l
```

### 5. macOSの場合：Full Disk Accessの許可

macOS Catalina以降では、cronにFull Disk Accessを許可する必要がある場合があります。

1. システム環境設定 → セキュリティとプライバシー → プライバシー
2. 左側のメニューから「フルディスクアクセス」を選択
3. 鍵アイコンをクリックして変更を許可
4. 「+」ボタンをクリック
5. `/usr/sbin/cron` を追加

### 6. ログの確認

実行ログは以下に記録されます：

```bash
tail -f logs/cron.log
```

## Windowsの場合

### タスクスケジューラを使用

1. 「タスクスケジューラ」を開く
2. 「基本タスクの作成」を選択
3. タスク名: "AI News Notifier"
4. トリガー: 毎日
5. 時刻: 8:00
6. 操作: プログラムの開始
7. プログラム/スクリプト:
   ```
   C:\Python3X\python.exe
   ```
8. 引数の追加:
   ```
   main.py
   ```
9. 開始: プロジェクトのフルパス

## トラブルシューティング

### cronが実行されない場合

1. **パスを絶対パスで指定**
   ```bash
   # NG（相対パス）
   0 8 * * * ./run_news_notifier.sh

   # OK（絶対パス）
   0 8 * * * /Users/yoshida_antlerspirits/projects/ai-news-slack-notifier/run_news_notifier.sh
   ```

2. **実行権限を確認**
   ```bash
   chmod +x run_news_notifier.sh
   ```

3. **ログを確認**
   ```bash
   cat logs/cron.log
   ```

4. **手動でスクリプトを実行してテスト**
   ```bash
   ./run_news_notifier.sh
   ```

5. **cronのログを確認（macOS）**
   ```bash
   log show --predicate 'process == "cron"' --last 1h
   ```

### 環境変数が読み込まれない場合

cronは通常のシェル環境とは異なる環境で実行されるため、`.env`ファイルが正しく読み込まれることを確認してください。

`run_news_notifier.sh`が正しいディレクトリに移動してから実行していることを確認してください。

## テスト実行

まずは手動で実行して動作を確認することをおすすめします：

```bash
cd /Users/yoshida_antlerspirits/projects/ai-news-slack-notifier
./run_news_notifier.sh
```

正常に動作したら、cron設定を行ってください。

## 一時的にcronを無効化

```bash
crontab -e
```

該当行の先頭に `#` を付けてコメントアウト：

```
# 0 8 * * * /Users/yoshida_antlerspirits/projects/ai-news-slack-notifier/run_news_notifier.sh
```

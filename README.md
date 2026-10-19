# Discord.py NukeBot

## 必要要件
- Python 3.8以降
- Discord BotのToken
  - Privileged Gateway Intents:
    - Message Content Intent
    - Server Members Intent
- 使用ライブラリ
  - discord.py
  - python-dotenv 
# ディレクトリ構造
```
.
├─ .env ------------- 設定ファイル(Bot Tokenの保存用)
├─ .gitignore ------- .envを公開しないためのファイル
├─ nuke.py ---------- 本体
├─ README.md -------- 本ドキュメント
├─ requirements.txt - ライブラリ一覧
└─ setup.gif -------- BOT追加時に一緒に送るgifファイル(任意で置き換えてね)
```
## 使い方
1. ディレクトリに、`.env`を新規作成し、以下を記述してください
    ```ini
    TOKEN = あなたのbotトークン
    ```
    **注意：** `.env` ファイルには機密情報が含まれるため、GitHub などの公開リポジトリにアップロードしないでください。
2. ディレクトリ内でコンソールを開いて以下を実行します
    1. `pip install -r requirements.txt`
    2. `python nuke.py`
3. コンソールに出力された招待リンク(`https://discord.com/oauth2/...`)をCtrl+クリックで開いてサーバーに追加します。
    - 任意ですが、ロール位置を一番上にすることをおすすめします
## 機能
| コマンド | 説明 |
| --- | --- |
| `ubm!setup` | 全チャンネル削除＆大量作成+全ロール名称変更・指定されたユーザーidに管理者付与+全チャンネルでスパム→自動退出 |
| `/idinvite` | 参加しているサーバーのguildidから招待リンクを生成

## 免責事項
**本ツールは教育・検証目的であり、許可されていないサーバーでの実行や利用規約に違反する使い方をした場合はすべて自己責任となります。**


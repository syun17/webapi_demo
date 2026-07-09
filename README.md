# 開発実務演習WebAPIデモアプリ

WebAPIをまとめて試せるFlaskアプリです。

## できること

- 気象庁 天気予報API
- PokeAPI
- JSONPlaceholder
- Icanhazdadjoke API
- REST Countries API
- Random User API
- Lorem Picsum

## 1.Pythonをインストール

    https://www.python.org/downloads/
    ↑の「Download Python 3.14.6」をクリック

    ダウンロードした.exeを実行
    ※「Add Python 3.x to PATH」にチェックを入れる

## 2.pytonコマンドが実行できない場合
    スタートメニューから設定を開き、
    アプリ⇒アプリの詳細設定⇒アプリ実行エイリアス
    アプリインストーラー(python.exe)とアプリインストーラー(python3.exe)をオフにする

## 3.仮想環境構築

    ターミナルでコマンドプロンプトを開く

    初回のみ
    ```cmd
    python - m venv venv
    ```
    
    起動時
    ```cmd
    venv\Scripts\Activate
    ```

    終了時
    ```cmd
    deactivate
    ```

## 3.ライブラリをダウンロード 

    ```cmd
    pip install -r requirements.txt
    ```

## 4.実行

    python run.py

ブラウザで http://127.0.0.1:5000/ を開いてください。








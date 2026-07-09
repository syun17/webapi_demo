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

## APIを新規で追加する手順

新しいAPIを追加するときは、次の流れで作業します。

1. 取得処理を追加する

    `api_client.py` の共通 `fetch_json` を使い、必要に応じて `xxx_api.py` を新規作成します。
    既存APIと同じように、APIごとの取得ロジックを1ファイルにまとめます。

2. `wether.py` に公開関数を追加する

    `run.py` から呼べるように、追加したAPIのクラスや関数を `wether.py` で import して再公開します。

3. `run.py` にルートを追加する

    `@app.get("/your-path")` の形式でエンドポイントを追加し、入力値の取得、API呼び出し、例外処理を実装します。
    既存ルートと同じように、`page_key`、`page_title`、`summary`、`result` を返す形に揃えます。

4. テンプレートを追加する

    `templates/your_page.html` を新規作成し、`base.html` を継承して表示を作ります。
    入力フォームや結果表示が必要なら、既存の `weather.html` や `country.html` を参考にします。

5. ホーム画面のカードを増やす

    `run.py` の `API_CARDS` に新しいカードを追加すると、トップページから開けるようになります。

6. 必要なら依存関係を更新する

    新しいライブラリを使う場合は `requirements.txt` を更新し、README に使い方を追記します。

## 1.Pythonをインストール

    https://www.python.org/downloads/
    ↑の「Download Python 3.14.6」をクリック

    ダウンロードした.exeを実行
    ※「Add Python 3.x to PATH」にチェックを入れる

## 2.pythonコマンドが実行できない場合
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








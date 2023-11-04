# 東京都スポーツ施設キャンセル待ちツール

[東京都スポーツ施設サービス](https://yoyaku.sports.metro.tokyo.lg.jp/user/view/user/homeIndex.html) のキャンセル待ちをするツール。

## 使い方

1. ローカルで [docker](https://www.docker.com/) を使えるようにしておく
2. 本リポジトリをローカルにクローンする

    ```
    git clone https://github.com/IwataYasuaki/tmgbc-cancel-list.git
    ```

3. コンテナを起動する

    ```
    docker-compose up -d
    ```

4. コンテナに入る

    ```
    docker-compose exec python bash
    ```

5. アプリケーションを実行する

    ```
    python /tmgbc-cancel-list/main.py
    ```

6. 現時点では以下のメッセージがコンソール出力されるはず（将来的には予約できたかどうかを出力する予定）

    ```
    都立公園スポーツ施設予約｜東京都
    ```

7. コンテナから抜ける

    ```
    exit
    ```

8. コンテナを停止させる

    ```
    docker-compose down
    ```

## 注意点

Apple Silicon搭載のMacの場合、事前にRosetta 2をインストールしておく必要がある。
以下のページが参考になった。

https://www.sria.co.jp/blog/2023/06/7308/


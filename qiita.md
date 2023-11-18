
## 概要

curlを使ってchomedriver（以下、WebDriver）に命令を出し、ブラウザを動かす記事です。
なお、タイトルにはないですが、SessionIdを取り出す時はjqを使ってます。

## 動作環境

- MacBook
  - Apple Sillicon M1
  - Sonoma 14.0
- brew install
  - curl
  - jq
- WebDriver
  - chromedirver:119

## curlの基本

まずはhelpを見てみよう。

```bash
~ $ curl --help
Usage: curl [options...] <url>
 -d, --data <data>          HTTP POST data
 -f, --fail                 Fail fast with no output on HTTP errors
 -h, --help <category>      Get help for commands
 -i, --include              Include protocol response headers in the output
 -o, --output <file>        Write to file instead of stdout
 -O, --remote-name          Write output to a file named as the remote file
 -s, --silent               Silent mode
 -T, --upload-file <file>   Transfer local FILE to destination
 -u, --user <user:password> Server user and password
 -A, --user-agent <name>    Send User-Agent <name> to server
 -v, --verbose              Make the operation more talkative
 -V, --version              Show version number and quit

This is not the full help, this menu is stripped into categories.
Use "--help category" to get an overview of all categories.
For all options use the manual or "--help all".
```

どうやら全部のヘルプを見る場合は`--help all`とつけないといけないようです。
下記のコマンドを実行します。

```bash
curl --help all
```

さまざまなオプションが表示されますが、今回は個人的によく使う`-X`と`-H`、`-d`を使ってWebDriverを動かしていきたいと思います。

### `-X`とは

リクエストの種類を指定します。
リクエストの種類：GET,POST,PUT,DELETE

### `-H`とは

ヘッダを指定します。今回は`Content-Type: application/json`をヘッダとして送信します。

```text
Content-Type: application/json
```

### `-d`とは

リクエスト時に送信するデータです。今回はWebDriverの仕様に沿ってデータを渡します。

## WebDriverのセットアップ

まずはWebDriverを実行するブラウザとWebDriverのバージョンを同じバージョンにする必要があります。
ブラウザからバージョンを確認しましょう。

`Settings`の`About Chrome`から参照できます。

![VersionCheck.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/527543/c8f226a4-a65f-cc01-bd03-5ae6129951e1.png)

次にブラウザと同じバージョンのWebDriverをダウンロードします。

バージョン番号が114までのブラウザの場合は以下のリンクからダウンロードできます。
[ダウンロードリンク](https://chromedriver.chromium.org/downloads)

115以降の方は以下のリンクです。`Stable`版を選択しましょう。
[ダウンロードリンク](https://googlechromelabs.github.io/chrome-for-testing/)

ダウンロードすると`exe`が圧縮されたファイルに入っていますのでコマンドとして実行したい人は
環境変数の`PATH`にWebDriverのパスを入力しておきましょう。

PATHが通っているかの確認コマンドとして以下のコマンドを実行します。

```bash
chromedriver --version
```

実行結果

```text
ChromeDriver 119.0.6045.105 (38c72552c5e15ba9b3117c0967a0fd105072d7c6-refs/branch-heads/6045@{#1103})
```

## WebDriverの仕様

WebDriverは実行時、ローカルホストで9515のポートを占有します。
実行時に生成されたローカルホストへのURLがエンドポイントになります。

つまりはデフォルトのエンドポイントは下記の通りです。

```text
http://localhost:9515
```

## WebDriverの操作方法

WebDriverのエンドポイントURLにさまざまなリクエストを送ることで
WebDriverはリクエスト内容に応じてブラウザに命令します。

命令を実行するにあたり、WebDriverは`sessionId`を発行します。
発行したsessionIdを用いることでどのブラウザへ命令できるかを認識します。

### WebDriverを起動

今回はGoogle Chromeを動かすため`chromedriver`を実行します。
下記のコマンドを実行してください。

```bash
chromedriver
```

### sessionIdを発行

起動ができたところでsessionIdを発行します。
下記のコマンドを実行します。

```bash
res=$(curl -X POST -H "Content-Type: application/json" -d '{"capabilities":"alwaysMatch": {"browserName": "chrome"}}' http://localhost:9515/session)
```

実行に成功するとブラウザが立ち上がりますが、ここではいったん無視で大丈夫です。
次に`jq`を使って`res`変数内にある`sessionId`を取得します。

```bash
sessionId=$(echo $res | jq -r '.value.sessionId')
```

### 特定のページを開く

`sessionId`が取得できましたら、`sessionId`を使ってChromeを操作していきましょう。
下記のコマンドを実行すると`https://www.google.co.jp/`をブラウザで開きます。

```bash
curl -X POST -H "Content-Type: application/json" -d '{"url":"https://www.google.co.jp/"}' "http://localhost:9515/session/$sessionId/url"
```

### 開いたページのタイトルを取得

Webページを開くことに成功しましたらcurlからブラウザまでの通信経路については問題がないと思うので
今度は逆パターン、つまりはブラウザの情報を`WebDriver`で取得しましょう。

下記のコマンドを実行します。

```bash
curl -X GET -H "Content-Type: application/json" "http://localhost:9515/session/$sessionId/title"
```

Webページのタイトルが返ってくれば、成功です。

### ブラウザを閉じる

最後にブラウザを閉じましょう。

```bash
curl -X DELETE -H "Content-Type: application/json" "http://localhost:9515/session/$sessionId"
```

## まとめ

今回はcurlを使ってWebDriverに命令を出し、ブラウザを操作しました。
他にもいろんな操作ができます。詳しくは以前のzenn記事に書いていますので
興味のある方は読んでいただけますと幸いです。

なお、実際にはSeleniumを利用してブラウザテストをやるものなのでアプリのテストでは
フレームワークなどを活用しましょう。

## 参考

以前のzenn記事について

- [SeleniumなしでWebDriverを操作するには - Part1](https://zenn.dev/ymd65536/articles/e13f278a5d9803)
- [SeleniumなしでWebDriverを操作するには - Part2](https://zenn.dev/ymd65536/articles/0ab63cd4a41411)

## コマンド集

```bash
curl -X POST -H "Content-Type: application/json" -d '{"capabilities":{"browserName": "chrome","goog:chromeOptions": {"args": ["--headless"]}}}' http://localhost:9515/session
```

```json
"browserOptions": {"args": ["--headless"]}
```

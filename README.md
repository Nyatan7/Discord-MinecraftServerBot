# Discord-MinecraftServerBot

Minecraftプラグインサーバー向けに開発したDiscordBOT。
サーバー運営者の手を使わず、Discordサーバー上で誰もが簡単にMinecraftサーバーの起動、停止、再起動の動作をさせることが可能です。

## BOT運用の前提条件

* 空のDiscordBOTの用意
* Python3系のインストール
* SpigotやPaperなどのプラグインサーバーの構築
* サーバー構築に伴うポートの開放

※外部プラグイン「DiscordSRV」と相性が良くなるように設計していますので、こちらの導入もしておくと、なお良いです！

## BOT使用までの流れ

* BOTのクローン
* 同ディレクトリにてターミナルで「pip install -r requirements.txt」を実行
* 「.env.sample」ファイルを「.env」にリネームして必要情報を入力。
* 「main.py」ファイルと「.env」ファイルをそのままご自身のプラグインサーバーディレクトリに配置。
* 「main.py」ファイルの実行

BOTが起動したら、Discordで「/mcstart」コマンドを打ちます。
「.env」ファイルの記述にミスが無ければ、BOTを起動したターミナル上でMinecraftサーバーのログが流れます。
記述ミスがある場合、ターミナルにエラーが出力されます。記述を訂正し、BOTの再起動を行ってください。

GUIはデフォルトで無効にしているため、使用したい場合は、「main.py」内の「# .jar関連の処理」中に記述されている「"-nogui",」を削除してください。最後の「,」も忘れずに！
あとは常時ターミナルを起動させておくだけで、Minecraftサーバーの操作はDiscord上で完結します。

## 注意点

本来のMinecraftサーバーでは、サーバーを停止させる場合に管理者がターミナルで「stop」コマンドを打つことが基本です。
しかし、現状、BOTは独自でサーバーの起動回数、状態を記憶しているため、外部のコマンドを打ってしまうと認識が異なってしまうために動作しなくなります。

やむを得ず、BOT以外で停止操作を行った場合は、Minecraftサーバーが停止している状態で本BOTの再起動を行ってください。
※「DiscordSRV」の機能である、テキストチャンネルからの「stop」コマンド送信に関しては、起動状況を同期させる解決策はありますので、必要な場合はアップデートいたします。

なにか質問があれば、Discord「1L.」までお知らせください。
今後さらに機能の大きいBOTやその他システムなども作りたいですし、近いうちにDiscordコミュニティサーバーの開設を考えています。


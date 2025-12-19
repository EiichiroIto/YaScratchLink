# scratchlink-mqtt.py
この Python スクリプトは、Scratchのmicrobit 拡張をMQTTに受け渡す ScratchLink です。

# 用意するもの
## PC側
- Scratch
- Python3 環境
- Python モジュール（pyserial, websocket_server, paho-mqtt）
- MQTTブローカー
- scratchlink-mqtt.py

## デバイス側
- MQTTクライアント

# 準備
PCにPython3環境を構築し、必要なモジュールをインストールする。

MQTTブローカーをインストールしておく。

# 使い方
1. MQTTブローカーを起動する。
2. scratchlink-mqtt.py を起動する。パラメータは、ブローカーのIPアドレス、MQTTのトピック名を順に指定する。
3. Scratch を起動し、microbit拡張を追加する。
4. microbitの接続でmqttを選ぶ。

# 通信プロトコル
## PCからデバイス
- 文字列を表示する：/トピック名/say に文字列が送られる
- シンボルを表示する：/トピック名/led に文字列が送られる

## デバイスからPC
- Aボタン：/トピック名/button/a に0または1を指定する。
- Bボタン：/トピック名/button/b に0または1を指定する。
- タッチ0：/トピック名/touch/0 に0または1を指定する。
- タッチ1：/トピック名/touch/1 に0または1を指定する。
- タッチ2：/トピック名/touch/2 に0または1を指定する。
- 加速度センサ(X軸)：/トピック名/accel/x に-32768〜32767の値を指定する。
- 加速度センサ(Y軸)：/トピック名/accel/y に-32768〜32767の値を指定する。



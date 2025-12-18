# scratchlink-serial.py
この Python スクリプトは、USBで接続した micro:bit とUSBシリアルで通信します。
（シリアル通信できるデバイスであればmicro:bit でなくとも構いません）

# 用意するもの
## PC側
- Scratch
- Python3 環境
- Python モジュール（pyserial, websocket_server）
- scratchlink-serial.py

## デバイス側
- micro:bit
- USBケーブル（micro B --- Type A）
- BBC micro:bit MicroPython
- MicroPython にファイルを転送するアプリ（muエディタなど？）
- main.py

デバイス側はシリアル通信できるものであれば何でも構わない。

# 準備
PCにPython3環境を構築し、必要なモジュールをインストールする。

micro:bitに MicroPython をインストールし、micro:bit側のスクリプト（main.py）を転送する。

# 使い方
USBケーブルで PCとmicro:bit を接続する。

PCでPC側スクリプト（python-scratchlink-serial.py）を起動する。

PCでScratchを起動し、「作る」をクリックする。

micro:bit 拡張を追加する。

microbit を選んで接続する。

# 通信プロトコル
## シリアル通信設定
- 115200bps
- 8 Bit
- 1 Stopbit
- No Parity

## PCからデバイス
- 文字列を表示する：指定した文字列+CRLF
- シンボルを表示する：未実装

## デバイスからPC
- Aボタン：A
- Bボタン：B
- 加速度センサ：未実装

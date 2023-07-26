# Thums-up_Recognize
* 環境構築
  * 使用するハード(PCに繋ぐだけで良い)
    * webカメラ
    * 音声を再生するもの(スピーカー等)
  * 使用するソフト
    * Windows 11 (Windows 10 でも可？)
    * Python 3.9.13 (Python 3.9.Xなら可？)
  * 仮想環境に必要なモジュールをインストール
    * python -m venv env
    * env\Scripts\activate.bat
    * pip install -r requirements.txt
  * プログラム実行
    * python main.py
* 動作
  * Thums-up を検出すると音声ファイルが再生されます
  * "camera" ウィンドウに検出した手の目印(landmark)が表示されます

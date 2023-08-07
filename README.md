# Gesture_Recognizer

## For Windows
* 環境構築
  * 使用するハード(PCに繋ぐだけで良い)
    * webカメラ
    * 音声を再生するもの(スピーカー等)
  * 使用するソフト
    * Windows 11 (Windows 10 でも可？)
    * Python 3.9.13 (Python 3.9.Xなら可？)
  * プログラム実行(pyproject.toml が存在するフォルダで以下のコマンドを実行する)
    * poetry run my-script
* 動作
  * Thumbs-up を検出すると音声ファイルが再生されます
  * "camera" ウィンドウに検出した手の目印(landmark)が表示されます
  * プログラムを終了するには "ESC"キーを押します

## For Raspberry Pi

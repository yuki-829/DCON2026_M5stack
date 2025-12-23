from serial import Serial  # type: ignore
import time
import os
import subprocess
import psutil  # type: ignore
import sys
import json

ALIVE_SIGNAL="ALIVE_DONGLE_CONNECTED"
SERIAL_PORT="COM3"
BAUD_RATE=115200
APP_PATH=r"C:\APP\test.exe" #集中度のアプリの実行パス
APP_EXE_NAME="test.exe" #アプリの状態を監視する
TIMEOUT_SECONDS =3

def is_app_running(exe_name):
  return exe_name in (p.name() for p in psutil.process_iter())

def start_aap(path):
  if not is_app_running(APP_EXE_NAME):
    print(f"ソフトウェアを起動します:{path}")
    try:
      subprocess.Popen(path , creationflags=subprocess.CREATE_NO_WINDOW)
    except FileNotFoundError:
      print(f"ソフトウェアが見つかりません。パスを確認してください:{path}")
      print("システムを終了します。")
      sys.exit(1)

def stop_app():
  for proc in psutil.process_iter("name"):
    if proc.info["name"] == APP_EXE_NAME:
      print(f"物理キーが取り外されました。ソフトウェア({APP_EXE_NAME})を終了します。")
      proc.terminate()
      return True
  return False


def monitor_key():
  print(f"集中度測定を開始します。")
  print(f"使用中のポート:{SERIAL_PORT}")

ser = None
last_signal_time = time.time()

while True:
  try:
    if ser is None:
      print(f"{SERIAL_PORT}に接続中...")
      ser = Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT_SECONDS)
      print(f"{SERIAL_PORT}に接続しました。")
      last_signal_time = time.time()

    line = ser.readline().decode("utf-8",errors="ignore").strip()
    
    if ALIVE_SIGNAL == line:
      last_signal_time = time.time()
      start_aap(APP_PATH)

    time_since_last_signal = time.time() - last_signal_time

    if time_since_last_signal > TIMEOUT_SECONDS:
      print("接続が切断されました。")
      stop_app()
      ser.close()
      ser = None
      time.sleep(6)
      continue

  except OSError as e:
    if ser:
      ser.close()
      ser = None
    print(f"シリアル接続エラー:{e}")
    print(f"10秒後に再接続します。")
    time.sleep(10)
  except Exception as e:
    print(f"予期せぬエラーが発生しました。:{e}")
    print(f"システムを終了します。")
    time.sleep(5)

if __name__ == "__main__":
  monitor_key()
import subprocess
import psutil
import time
import os

# -----------------------------------------------------------------
# !!! ユーザー設定: 必ず本番のアプリのパスに合わせてください !!!
# -----------------------------------------------------------------
# 集中度測定アプリの実行ファイルパス
APP_PATH = r"C:\Concentration_App\ConcentrationMeter.exe" 
# アプリケーションの実行ファイル名
APP_EXE_NAME = "ConcentrationMeter.exe"  
# -----------------------------------------------------------------


# --- 監視スクリプトから抜粋した重要な関数 ---

def is_app_running(exe_name):
  """アプリケーションが実行中かチェックする"""
  # psutilを使って、exe_nameを持つプロセスが実行中か確認
  return exe_name in (p.name() for p in psutil.process_iter())

def start_app(path):
  """アプリケーションを起動する"""
  print("--- 1. 起動チェック ---")
  if not is_app_running(APP_EXE_NAME):
    print(f"[ACTION] アプリケーションを起動します: {path}")
    try:
      # 新しいプロセスとしてアプリを起動
      # CREATE_NO_WINDOWで余計な黒い画面が出ないようにする
      subprocess.Popen(path, creationflags=subprocess.CREATE_NO_WINDOW) 
      print(f"[SUCCESS] アプリケーションの起動に成功しました。")
    except FileNotFoundError:
      print(f"[FATAL] アプリケーションが見つかりません。パスを確認してください: {path}")
      
  else:
    print(f"[INFO] アプリケーション ({APP_EXE_NAME}) は既に実行中です。二重起動をスキップします。")


def stop_app():
  """アプリケーションを終了する"""
  print("--- 2. 終了処理 ---")
  terminated = False
  for proc in psutil.process_iter(['name']):
    if proc.info['name'] == APP_EXE_NAME:
      print(f"[ACTION] アプリケーション ({APP_EXE_NAME}) を終了します。")
      proc.terminate() # プロセスを終了 (強制終了)
      terminated = True
      
  if terminated:
    print(f"[SUCCESS] アプリケーションの終了に成功しました。")
  else:
    print(f"[INFO] アプリケーション ({APP_EXE_NAME}) は実行されていませんでした。")
  
  return terminated


# --- テスト実行ロジック ---

def run_test_scenario():
  """
  起動と終了の動作を確認するためのシナリオを実行します。
  """
  print("\n" + "="*50)
  print(f"テストシナリオ開始: アプリ名 ({APP_EXE_NAME})")
  print("="*50 + "\n")

  # 1. 起動テスト (アプリが動いていない状態から)
  print("--- シナリオ1: アプリを起動する ---")
  stop_app() # 念のため停止してから開始
  start_app(APP_PATH)

  time.sleep(2) # 起動を待つ

  print("\n--- 2. 起動確認 ---")
  if is_app_running(APP_EXE_NAME):
    print(f"[SUCCESS] アプリケーション ({APP_EXE_NAME}) が実行中です。")
  else:
    print(f"[FAILURE] アプリケーションの起動に失敗しました。")


  # 3. 二重起動テスト
  print("\n--- シナリオ3: 二重起動を試みる (スキップされるべき) ---")
  start_app(APP_PATH)


  # 4. 終了テスト (アプリが動いている状態から)
  print("\n--- シナリオ4: アプリを終了させる ---")
  stop_app()
  
  time.sleep(2) # 終了を待つ

  print("\n--- 5. 終了確認 ---")
  if not is_app_running(APP_EXE_NAME):
    print(f"[SUCCESS] アプリケーション ({APP_EXE_NAME}) が正常に終了しました。")
  else:
    print(f"[FAILURE] アプリケーションが終了できていません。")

  print("\n" + "="*50)
  print("テストシナリオ終了")
  print("="*50)


if __name__ == "__main__":
  # Pythonファイルを単独で実行したときに run_test_scenario() が実行される
  run_test_scenario()
# pod_status_notRunning
プログラムを置く VM に作成されている Pod のステータスが Running 以外の Pod を対象とする．

kubectl get pod の内容と kubectl describe pod の Evens を取得し，同ディレクトリ内にあるテキストファイルに書き込むプログラム．

## 内容
各Pod のステータスを取得し，Running ではない Pod を選別する．

Podごとに kubectl get pod でターミナル表示される情報を取得し，書き込む．

同様に kubectl describe pod でターミナル表示される情報にあるEvents を取得し，書き込む．

最後に，書き込んだテキストファイル名をターミナル表示する

## 使い方
そのままダウンロードして使えます．

同ディレクトリ内に名前が "pod-data.txt" というテキストファイルを配置してください．

＊ "# ターミナルに出力" の下にあるprint文のコメントアウトを外すと，ターミナルにテキストファイルに書き込んだ内容が出力されます．

＊ kubectl describe pod の内容が無い場合，"None" と書き込まれます．

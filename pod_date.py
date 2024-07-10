from kubernetes import client, config
import subprocess
import re



def pod_evens(pod_name, namespace):
    try:
        # PodのEventsを取得
        events = v1.list_namespaced_event(namespace, field_selector=f"involvedObject.name={pod_name}")
        txt = ""
        for event in events.items:
            event_time = event.first_timestamp or event.last_timestamp
            event_message = event.message
            event_type = event.type
            # フォーマットされた文字列を生成
            txt += f"{event_time}\t{event_type}\t{event_message}\n"
        if txt == "":
            txt = "None"

        return txt

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while describing the pod: {e}")



if __name__ == "__main__":
    # Kubernetesクラスターへの接続
    # Configs can be set in Configuration class directly or using helper utility
    config.load_kube_config()

    # CoreV1Apiの初期化
    v1 = client.CoreV1Api()
    #print("Listing pods with their IPs:")

    # 全ての名前空間のPodのリストを取得
    pod_list = v1.list_pod_for_all_namespaces(watch=False)
    #print(pod_list)

    # Podの要素の抽出，表示，ファイルに書き込み
    file_path = "pod-date.txt"
    with open(file_path, "w") as file:
        # Podの数，繰り返し
        for i in pod_list.items:
            pod_ip = i.status.pod_ip
            pod_namespace = i.metadata.namespace
            pod_name = i.metadata.name
            pod_status = i.status.phase
            # READY
            if i.status.container_statuses is not None:
                ready_containers = sum(1 for c in i.status.container_statuses if c.ready)
                total_containers = len(i.status.container_statuses)
            else:
                ready_containers = 0
                total_containers = 0
            ready_field = f"{ready_containers}/{total_containers}"

            # PodのSTATUSがRunning以外のとき
            if pod_status != "Running" or ready_containers != total_containers:# or state == Waiting:
                # podのIP，namespace，名前，ステータス
                # フォーマットされた文字列を生成（IP，namespace，名前，ステータス）
                txt = "%s\t%s\t%s\t%s\t%s\n" % (pod_ip, pod_namespace, pod_name, ready_field, pod_status)
                # ターミナルに出力
                # print("IP Address   Namespace   Name    Ready   Status")
                # print(txt)
                # ファイルに書き込み
                file.write("IP Address\tNamespace\tName\tReady\tStatus\n")
                file.write(txt+ "\n")

                # describeのエラー文
                # events文生成
                describe = pod_evens(pod_name, pod_namespace)
                # ターミナルに出力
                # print("Events for Pod:")
                # print(describe)
                # ファイルに書き込み
                file.write(f"Events for Pod: \n")
                file.write(describe + "\n")
                
                # 各podの区切り線
                # ターミナルに出力
                # print("--------------------")
                # ファイルに書き込み
                file.write("--------------------" + "\n")


    # 書き込んだファイル名を表示
    print(f"Pod information written to {file_path}")

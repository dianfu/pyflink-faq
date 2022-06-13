# Run PyFlink jobs on Kubernetes

In this example, we'd like to give a simple example to show how to run PyFlink jobs on Kubernetes in application mode.
It has been documented clearly in Flink's [official documentation](https://nightlies.apache.org/flink/flink-docs-stable/docs/deployment/resource-providers/native_kubernetes/) about how to work with Kubernetes.
All the documentation there also applies for PyFlink jobs. It's strongly advised to read that documentation carefully before going through the following example.

## Preparation

### Setup Kubernetes cluster

If there is no kubernetes cluster available for use, you need firstly set up it. You can take a look at [how to set up a Kubernetes cluster](https://kubernetes.io/docs/setup/) for more details.

You can verify the permissions by running `kubectl auth can-i <list|create|edit|delete> pods`, e.g.
```shell
kubectl auth can-i create pods
```

Then, you could run the following command:
```shell
kubectl get pods -A
```
If the outputs are something like the following, it means that the Kubernetes cluster is running, and the kubectl is configured correctly,
you could proceed to the next section:
```shell
kube-system   coredns-f9fd979d6-96xql                  1/1     Running   0          7m41s
kube-system   coredns-f9fd979d6-h9q5v                  1/1     Running   0          7m41s
kube-system   etcd-docker-desktop                      1/1     Running   0          6m44s
kube-system   kube-apiserver-docker-desktop            1/1     Running   0          6m47s
kube-system   kube-controller-manager-docker-desktop   1/1     Running   0          6m42s
kube-system   kube-proxy-94f22                         1/1     Running   0          7m41s
kube-system   kube-scheduler-docker-desktop            1/1     Running   0          6m39s
kube-system   storage-provisioner                      1/1     Running   0          7m6s
kube-system   vpnkit-controller                        1/1     Running   0          7m5s
```

### Build docker image with PyFlink installed

It requires PyFlink installed on all the cluster nodes. Currently, it has still not provided official Flink docker images with PyFlink installed.
You need to build it yourself as following.

```shell
docker build -t pyflink:1.14.4 -f docker/Dockerfile .
```

## Execute PyFlink jobs

### Creating a custom image containing the PyFlink job you want to execute and also the dependencies if needed

In application mode, it requires that the user code is bundled together with the Flink image. See [Application Mode](https://nightlies.apache.org/flink/flink-docs-stable/docs/deployment/resource-providers/native_kubernetes/#application-mode) for more details.
So you need to build a custom image with PyFlink job code bundled in the image.

```shell
docker build -t pyflink_wc -f docker/Dockerfile.job .
```

Note: Make sure to publish the Docker image to a repository which is accessible for the Kubernetes cluster if the Kubernetes cluster is not a local test cluster.

### Submit PyFlink jobs

1) Download Flink distribution, e.g. for Flink 1.14.4, it's available in https://www.apache.org/dyn/closer.lua/flink/flink-1.14.4/flink-1.14.4-bin-scala_2.11.tgz

2) Extract it
```shell
tar zxvf flink-1.14.4-bin-scala_2.11.tgz
```

3) Submit PyFlink jobs:
```shell
cd flink-1.14.4
./bin/flink run-application \
      --target kubernetes-application \
      --parallelism 2 \
      -Dkubernetes.cluster-id=word-count \
      -Djobmanager.memory.process.size=1024m \
      -Dtaskmanager.memory.process.size=1024m \
      -Dkubernetes.taskmanager.cpu=2 \
      -Dtaskmanager.numberOfTaskSlots=2 \
      -Dkubernetes.container.image=pyflink_wc:latest \
      -Dkubernetes.rest-service.exposed.type=ClusterIP \
      -py /opt/flink/usrlib/word_count.py
```

Note:
- More Kubernetes specific configurations could be found [here](https://nightlies.apache.org/flink/flink-docs-stable/docs/deployment/config/#kubernetes)
- You could override configurations set in `conf/flink-conf.yaml` via `-Dkey=value`
- Clusterrolebinding for `edit` needs to be configured with `kubectl create clusterrolebinding flink-role-binding-default --clusterrole=edit --serviceaccount=default:default`. If you already have defined clusterrolebinding for a different namespace, edit the yaml to add service account `default:default`

If you see outputs as following, the job should have been submitted successfully:
```shell
2022-04-24 17:08:32,603 INFO  org.apache.flink.kubernetes.utils.KubernetesUtils            [] - Kubernetes deployment requires a fixed port. Configuration blob.server.port will be set to 6124
2022-04-24 17:08:32,603 INFO  org.apache.flink.kubernetes.utils.KubernetesUtils            [] - Kubernetes deployment requires a fixed port. Configuration taskmanager.rpc.port will be set to 6122
2022-04-24 17:08:33,289 WARN  org.apache.flink.kubernetes.KubernetesClusterDescriptor      [] - Please note that Flink client operations(e.g. cancel, list, stop, savepoint, etc.) won't work from outside the Kubernetes cluster since 'kubernetes.rest-service.exposed.type' has been set to ClusterIP.
2022-04-24 17:08:33,302 INFO  org.apache.flink.kubernetes.KubernetesClusterDescriptor      [] - Create flink application cluster word-count successfully, JobManager Web Interface: http://word-count-rest.default:8081
```

You could verify the pod status as following:
```shell
kubectl get pods -A | grep word-count
```

If everything runs normally, you should see outputs like the following:
```shell
NAMESPACE     NAME                                     READY   STATUS    RESTARTS   AGE
default       word-count-5f5d44b598-zg5z8              1/1     Running   0          90s
default       word-count-taskmanager-1-1               0/1     Pending   0          59s
```
Among them, the JobManager runs in the pod `word-count-5f5d44b598-zg5z8 ` and the TaskManager runs in the pod `word-count-taskmanager-1-1`.

If the pods are not running normally, you could check the logs of the pods, e.g. checking the log of the JM as following:
```shell
kubectl logs word-count-5f5d44b598-zg5z8
```

See [Flink documentation](https://nightlies.apache.org/flink/flink-docs-stable/docs/deployment/cli/#submitting-pyflink-jobs) for more details on how to submit PyFlink jobs.

### Accessing Flink’s Web UI

Flink’s Web UI and REST endpoint can be exposed in several ways via the `kubernetes.rest-service.exposed.type` configuration option.
Since it's set to `ClusterIP` in this example, the Flink’s Web UI could be accessed in the following way:
```shell
kubectl port-forward service/word-count-rest 8081
```
Then you could access Flink's Web UI of the job via `http://127.0.0.1:8081`.

You could refer to Flink's [official documentation](https://nightlies.apache.org/flink/flink-docs-stable/docs/deployment/resource-providers/native_kubernetes/#accessing-flinks-web-ui) for more details.

### Cancel the jobs

You could either cancel the job through Flink's Web UI or REST API.

## FAQ

### 0/1 nodes are available: 1 Insufficient memory

If the pods of the TaskManagers are always running in `PENDING` status after a long while, you could use the following command to see what happens:
```shell
kubectl describe pod word-count-taskmanager-1-1
```

If see outputs like the following, it means that the memory of the kubernetes cluster is insufficient:
```shell
Events:
  Type     Reason            Age                From               Message
  ----     ------            ----               ----               -------
  Warning  FailedScheduling  16s (x2 over 16s)  default-scheduler  0/1 nodes are available: 1 Insufficient memory.
```

You need to configure the kubernetes cluster with more memory.

---
id: operational_faq.md
summary: Find answers to commonly asked questions about operations in Milvus.
title: Operational FAQ
---

# Operational FAQ

<!-- TOC -->


<!-- /TOC -->

#### What if I failed to pull the Milvus Docker image from Docker Hub?

If you failed to pull the Milvus Docker image from Docker Hub, try adding other registry mirrors. 

Users from Mainland China can add the URL "https://registry.docker-cn.com" to the registry-mirrors array in **/etc.docker/daemon.json**.

```
{
  "registry-mirrors": ["https://registry.docker-cn.com"]
}
```

#### Is Docker the only way to install and run Milvus?

Docker is an efficient way to deploy Milvus, but not the only way. You can also deploy Milvus from source code. This requires Ubuntu (18.04 or higher) or CentOS (7 or higher). See [Building Milvus from Source Code](https://github.com/milvus-io/milvus#build-milvus-from-source-code) for more information.

#### What are the main factors affecting recall?

Recall is affected mainly by index type and search parameters.

For FLAT index, Milvus takes an exhaustive scan within a collection, with a 100% return.

For IVF indexes, the nprobe parameter determines the scope of a search within the collection. Increasing nprobe increases the proportion of vectors searched and recall, but diminishes query performance.

For HNSW index, the ef parameter determines the breadth of the graph search. Increasing ef increases the number of points searched on the graph and recall, but diminishes query performance.

For more information, see [Vector Indexing](https://www.zilliz.com/blog/Accelerating-Similarity-Search-on-Really-Big-Data-with-Vector-Indexing).

#### Why did my changes to the configuration files not take effect?

Milvus does not support modification to configuration files during runtime. You must restart Milvus Docker for configuration file changes to take effect.

#### How do I know if Milvus has started successfully?

If Milvus is started using Docker Compose, run `docker ps` to observe how many Docker containers are running and check if Milvus services started correctly.

For Milvus standalone, you should be able to observe at least three running Docker containers, one being the Milvus service and the other two being etcd management and storage service. For more information, see [Installing Milvus Standalone](install_standalone-docker.md).

#### Why is the time in the log files different from the system time?

The time difference is usually due to the fact that the host machine does not use Coordinated Universal Time (UTC).

The log files inside the Docker image use UTC by default. If your host machine does not use UTC, this issue may occur.


#### How do I know if my CPU supports Milvus?

{{fragments/cpu_support.md}}

#### Why does Milvus return `illegal instruction` during startup?

Milvus requires your CPU to support a SIMD instruction set: SSE4.2, AVX, AVX2, or AVX512. CPU must support at least one of these to ensure that Milvus operates normally. An `illegal instruction` error returned during startup suggests that your CPU does not support any of the above four instruction sets.

See [CPU’s support for SIMD Instruction Set](prerequisite-docker.md).

#### Can I install Milvus on Windows?

Yes. You can install Milvus on Windows either by compiling from source code or from a binary package. 

See [Run Milvus on Windows](https://milvus.io/blog/2021-11-19-run-milvus-2.0-on-windows.md) to learn how to install Milvus on Windows.

#### I got an error when installing pymilvus on Windows. What shall I do?

It is not recommended to install PyMilvus on Windows. But if you have to install PyMilvus on Windows but got an error, try installing it in a [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) environment. See [Install Milvus SDK](install-pymilvus.md) for more information about how to install PyMilvus in the Conda environment.

#### Can I deploy Milvus when disconnected from the Internet?

Yes. You can install Milvus in an offline environment. See [Install Milvus Offline](install_offline-helm.md) for more information.

#### Where can I find the logs generated by Milvus?

The Milvus log is printed to stout (standard output) and stderr (standard error) by default, however we highly recommend redirecting your log to a persistent volume in production. To do so, update `log.file.rootPath` in **milvus.yaml**. And if you deploy Milvus with `milvus-helm` chart, you also need to enable log persistence first via `--set log.persistence.enabled=true`. 

If you didn't change the config, using kubectl logs <pod-name> or docker logs CONTAINER can also help you to find the log.


#### Can I create index for a segment before inserting data into it?

Yes, you can. But we recommend inserting data in batches, each of which should not exceed 256 MB, before indexing each segment.

#### Can I share an etcd instance among multiple Milvus instances?

Yes, you can share an etcd instance among multiple Milvus instances. To do so, you need to change `etcd.rootPath` to a separate value for each Milvus instance in the configuration files of each before starting them.

#### Can I share a Pulsar instance among multiple Milvus instances?

Yes, you can share a Pulsar instance among multiple Milvus instances. To do so, you can

- If multi-tenancy is enabled on your Pulsar instance, consider allocating a separate tenant or namespace for each Milvus instance. To do so, you need to change `pulsar.tenant` or `pulsar.namespace` in the configuration files of your Milvus instances to a unique value for each before starting them.
- If you do not plan on enabling multi-tenancy on your Pulsar instance, consider changing `msgChannel.chanNamePrefix.cluster` in the configuration files of your Milvus instances to a unique value for each before starting them.

#### Can I share a MinIO instance among multiple Milvus instances?

Yes, you can share a MinIO instance among multiple Milvus instances. To do so, you need to change `minio.rootPath` to a unique value for each Milvus instance in the configuration files of each before starting them.

#### Still have questions?

You can:

- Check out [Milvus](https://github.com/milvus-io/milvus/issues) on GitHub. Feel free to ask questions, share ideas, and help others.
- Join our [Milvus Forum](https://discuss.milvus.io/) or [Slack Channel](https://join.slack.com/t/milvusio/shared_invite/enQtNzY1OTQ0NDI3NjMzLWNmYmM1NmNjOTQ5MGI5NDhhYmRhMGU5M2NhNzhhMDMzY2MzNDdlYjM5ODQ5MmE3ODFlYzU3YjJkNmVlNDQ2ZTk) to find support and engage with our open-source community.
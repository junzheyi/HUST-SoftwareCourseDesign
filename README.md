# HUST-SoftwareCourseDesign
这是华中科技大学电信学院大三上学期的软件课设项目所用的仓库
# 选题内容：
## 项目名称
AI智能客服机器人系统设计与开发
# 森海塞尔耳机售后机器人——使用说明书

源码链接 :point_down:

<https://github.com/junzheyi/HUST-SoftwareCourseDesign>

## 源代码使用说明

因为本项目是基于端侧设备数据库实现的RAG系统，如需在不同边缘端运行本项目，每一个边缘端都需要做载入数据的前期准备工作，如果使用的是Milvus Cloud则直接可以使用前端页面交互。

**载入数据准备工作**：

:one: 首先确保本机的Milvus在docker中运行

* docker图形化管理界面启动milvus
* 或者命令行启动`docker compose up -d`

:two: 运行`create_collection_and_index.py`

* 如果本地没有启动Milvus，会有如下报错信息：

  ```python
  Problem in connecting to Milvus
  <MilvusException: (code=2, message=Fail connecting to server on localhost:19530. Timeout)>
  ```

  很明显，这是第一步没有做好，请返回 :one:。

* 运行成功并打印调试信息：

  ```python
  Connected to Milvus!
  Database Version:  v2.5.0
  Collections:  ['PythonQA', 'PythonBooks']
  Indexes:  ['question_vec'] ['book_chunk_vec']
  Disconnected from Milvus!
  ```

:three: 运行`load_docs.py`

* 此步骤请严格按照help_text中的指示通过命令行传参。
* 传参成功后会打印调试信息和载入结果，如果看到调试信息和载入结果则说明此步骤执行无误。

:four: 更新`config.ini`文件

* 更换为你自己的信息。

**至此，数据载入工作全部完成**:smile:

接下来运行前端代码就可以

* 命令行输入

  ```cmd
  streamlit run robot_login_with_backend.py
  ```

* 出现以下信息代表运行成功

   ```cmd
   You can now view your Streamlit app in your browser.
   ```

* 直接点击local URL或者记住端口名前往浏览器输入本机IP+端口即可访问。

## 前端交互使用说明

打开端口后会看到如下界面：

![image-20250113200709023](https://cdn.jsdelivr.net/gh/junzheyi/typorabed@master/img/image-20250113200709023.png)

:one:首先需要注册你的账号，然后再登录

如果登录管理员账号，可以看到所有用户的信息，便于管理。

> 管理员：
>
> username：admin
>
> pw：123456789

:two:在左侧输入用户画像信息，点击submit。

![image-20250113201124979](https://cdn.jsdelivr.net/gh/junzheyi/typorabed@master/img/image-20250113201124979.png)

:three: 选择你想要使用的LLM

​	本项目提供了三个LLM，分别是：

* local Llama2：首先要确保你的本地已经部署了Llama，这个模型返回结果**质量高**，但是CPU跑起来很**慢**，需要约4min返回结果。
* OpenAI：需要你在config文件中提供API Key，**注意：OpenAI的模型API需付费才有使用额度**。
* zephyr：这是Huggingface上的在线模型，免费且返回结果速度快，需要约10s（0.2min）返回结果。

下面是我提问 *“如何对Momentum 4这款耳机进行充电，大约需要多久充满”*

售后机器人返回

* LLM生成的文本；
* 索引所用的时间（我选择了zephyr模型，可以从下图看到用时0.09min）；
* 数据库中与问题向量余弦相似度最高的三个文本块作为source document返回给用户。

![image-20250113202545140](https://cdn.jsdelivr.net/gh/junzheyi/typorabed@master/img/image-20250113202545140.png)


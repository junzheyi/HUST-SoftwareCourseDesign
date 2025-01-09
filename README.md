# HUST-SoftwareCourseDesign
这是华中科技大学电信学院大三上学期的软件课设项目所用的仓库
# 选题内容：
## 项目名称
AI智能客服机器人系统设计与开发
## 基本要求：
* 设计并实现一个Web界面，包括对话区、用户信息显示区；
* 实现基于大规模语言模型（e.g. 通义千问）的对话生成功能
* 构建本地知识库，实现与大模型的综合使用
* 实现基于用户画像的个性化回答生成
* 设计并实现一个垂直领域（e.g. 产品咨询、技术支持、售后服务）的专业问答能力
* 系统能够通过数据库实现信息的存储和交互
## 选做要求：
* 设计管理员后台，支持知识库的在线更新和系统性能监控
* 能够使用自己本地部署的开源大模型进行调用回答用户问题

# 项目计划
中期报告所计划的是做一个法律咨询客服机器人，但是在之后我发现milvus对中文的索引效果很不好，甚至可以说是很差
所以整个项目只做到支持英文，最后做的是关于森海塞尔无线耳机的专业售后问答机器人，RAG效果非常好
机器人支持三种LLM，分别是本地LLM（我用的是LLama2），OpenAI（没有提供key），hf的在线大模型（在config中我隐藏了我的api key）
成果展示
![show.png](images%2Fshow.png)
![show2.png](images%2Fshow2.png)



---

# 使用说明

AI 软件测试平台是一个本地运行的智能测试辅助工具。

支持输入：

```text
产品需求
需求文档
接口信息
历史 Bug
测试规范
```

自动完成：

- 需求评审
- 测试点分析
- 测试用例生成
- 测试用例优化
- 测试质量评分
- RTM 需求追踪
- 测试质量 Dashboard
- Bug 智能分析
- 历史 Bug 知识沉淀
- 接口测试用例生成
- Boundary Skill 边界值测试
- Equivalence Skill 等价类测试
- API Skill 接口测试规则
- AI 输出结构校验
- Pytest + Requests 自动化脚本生成
- Excel 测试结果导出

项目同时加入了 RAG 测试知识库，可以将测试规范、历史 Bug 等资料作为测试经验，在后续需求分析和测试设计中进行检索参考。

---

# 1. 推荐运行环境

推荐使用：

```text
Python 3.11
```

Windows 可以在终端执行：

```bash
python --version
```

或者：

```bash
py --version
```

如果输出类似：

```text
Python 3.11.x
```

说明 Python 环境正常。

当前项目也可以尝试运行在更高版本 Python，但：

```text
LangChain
Embedding
Torch
HuggingFace
```

等 AI 相关依赖通常在 Python 3.11 下兼容性更稳定。

---

# 2. 下载项目

## 方法一：Git Clone

打开终端执行：

```bash
git clone https://github.com/zzb131012-cpu/Repository-name-ai-software-testing-platform.git
```

进入项目目录：

```bash
cd Repository-name-ai-software-testing-platform
```

---

## 方法二：下载 ZIP

进入 GitHub 仓库页面：

```text
Code
→ Download ZIP
```

下载完成后解压项目。

---

# 3. 创建虚拟环境

Windows：

```bash
python -m venv .venv
```

激活虚拟环境：

```bash
.venv\Scripts\activate
```

激活成功后终端前面一般会出现：

```text
(.venv)
```

例如：

```text
(.venv) PS D:\ai-software-testing-platform>
```

macOS / Linux：

```bash
python3 -m venv .venv
```

激活：

```bash
source .venv/bin/activate
```

---

# 4. 安装项目依赖

项目已经提供：

```text
requirements.txt
```

执行：

```bash
python -m pip install -r requirements.txt
```

首次运行时可能需要下载：

```text
HuggingFace Embedding 模型
```

如果下载速度较慢，需要等待模型下载完成。

---

# 5. 配置环境变量

项目不会上传真实 API Key。

仓库中提供：

```text
.env.example
```

复制一份并改名为：

```text
.env
```

例如 DeepSeek：

```env
DEEPSEEK_API_KEY=你的API_KEY
```

示例：

```env
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxx
```

项目中的：

```text
.env
```

已经通过：

```text
.gitignore
```

忽略。

请不要把真实 API Key 上传到 GitHub。

---

# 6. 启动功能测试平台

功能测试主页面：

```text
app.py
```

执行：

```bash
python -m streamlit run app.py
```

启动成功后终端会显示：

```text
Local URL: http://localhost:8501
```

浏览器打开：

```text
http://localhost:8501
```

即可进入：

```text
AI 软件测试平台
```

---

# 7. 功能测试使用流程

## 第一步：输入需求

支持两种方式：

```text
手动输入
上传需求文档
```

支持上传：

- TXT
- Markdown
- PDF
- Word

例如：

```text
用户通过手机号和密码登录。

手机号不能为空。
密码不能为空。

手机号必须为11位数字。

密码连续输错5次后，
账号锁定30分钟。

账号锁定期间，即使输入正确密码，
也不能登录。

登录成功后进入首页。
```

输入完成后点击：

```text
开始生成测试方案
```

---

# 8. 需求评审

系统会自动分析：

- 需求理解
- 已明确业务规则
- 需求风险
- 需求待确认
- 测试建议

对于需求中没有明确说明的内容，不直接编造业务规则，而是标记：

```text
【需求待确认】
```

例如：

```text
密码最大长度未明确
```

---

# 9. 测试点分析

系统会从多个维度进行分析：

- 正常场景
- 异常场景
- 边界值
- 等价类
- 业务规则
- 数据校验
- 状态流转
- 权限与安全
- 兼容性
- 历史 Bug 回归
- 需求待确认

---

# 10. 自动生成测试用例

测试用例包含：

| 字段 | 说明 |
|---|---|
| 用例编号 | TC001、TC002... |
| 测试模块 | 当前测试功能模块 |
| 测试标题 | 用例验证目标 |
| 前置条件 | 执行前准备 |
| 操作步骤 | 实际测试步骤 |
| 测试数据 | 输入数据 |
| 预期结果 | 正确业务结果 |
| 优先级 | P0 / P1 / P2 |

例如：

```text
TC001
登录
正确手机号和正确密码登录成功
P0
```

生成后的测试用例支持直接在页面中：

- 修改
- 新增
- 删除

---

# 11. 智能用例优化

目前支持：

```text
AI 补充遗漏用例
AI 删除重复用例
AI 全面优化
```

## 补充遗漏用例

系统检查是否遗漏：

- 正常场景
- 异常场景
- 边界场景
- 关键业务规则
- 历史 Bug 回归场景

## 删除重复用例

识别：

```text
完全重复
高度重复
验证目标基本一致
```

的测试用例。

## 全面优化

可以同时完成：

- 补遗漏
- 去重复
- 优化标题
- 优化步骤
- 优化测试数据
- 优化预期结果
- 调整优先级

---

# 12. 测试质量评分

点击：

```text
开始质量评分
```

系统从多个维度进行评分：

```text
需求覆盖度
正常场景覆盖
异常场景覆盖
边界值覆盖
业务规则覆盖
可执行性
非重复质量
```

例如：

```text
总体质量评分：88 / 100

需求覆盖：92
正常场景：95
异常场景：88
边界覆盖：80
业务规则：92
可执行性：90
非重复：95
```

同时输出：

- 测试设计优势
- 遗漏场景
- 高风险遗漏
- 优化建议

---

# 13. RTM 需求追踪矩阵

RTM：

```text
Requirement Traceability Matrix
```

用于建立：

```text
需求
↓
测试用例
```

之间的对应关系。

点击：

```text
生成 RTM
```

系统会先拆分需求：

```text
R001 手机号不能为空
R002 密码不能为空
R003 手机号必须11位
R004 密码连续错误5次锁定30分钟
```

然后分析每条需求由哪些测试用例覆盖。

例如：

| 需求编号 | 需求内容 | 覆盖用例 | 状态 |
|---|---|---|---|
| R001 | 手机号不能为空 | TC003 | 已覆盖 |
| R002 | 密码不能为空 | TC004 | 已覆盖 |
| R003 | 手机号必须11位 | TC005、TC006 | 已覆盖 |
| R004 | 错误5次锁定 | TC010 | 部分覆盖 |

覆盖状态包括：

```text
已覆盖
部分覆盖
未覆盖
```

可以用于快速检查是否存在漏测。

---

# 14. 测试质量 Dashboard

Dashboard 用于汇总当前测试设计数据。

包括：

```text
测试用例总数
总体质量评分
需求覆盖率
未覆盖需求数
P0 核心用例
部分覆盖需求
高风险遗漏
重复风险
```

帮助快速判断当前测试设计质量。

---

# 15. Excel 导出

测试完成后可以下载：

```text
AI测试结果.xlsx
```

Excel 包含：

```text
Sheet1：测试用例
Sheet2：RTM需求追踪矩阵
```

方便继续进行：

- 测试执行
- 测试评审
- 用例维护
- 回归测试

---

# 16. RAG 测试知识库

项目支持维护自己的软件测试知识库。

知识库中可以保存：

```text
测试规范
历史 Bug
测试经验
业务注意事项
```

项目使用：

```text
Embedding
+
Chroma
+
RAG
```

将文档转换为向量知识。

当输入新的需求时：

```text
当前需求
↓
向量检索
↓
找到相关测试规范 / 历史 Bug
↓
作为测试经验传递给测试分析流程
```

---

# 17. 历史 Bug 经验复用

例如历史上发现：

```text
密码连续输错5次后，
账号没有进入锁定状态。
```

将 Bug 保存到知识库以后，下次出现类似登录需求时，系统可以检索相关经验，并辅助关注：

```text
第4次 → 第5次状态转换
第5次错误
锁定状态
锁定期间输入正确密码
29分59秒
30分钟
30分01秒
登录成功后的计数重置
```

形成：

```text
发现 Bug
↓
沉淀历史经验
↓
进入知识库
↓
RAG 检索
↓
反哺下一次测试设计
```

---

# 18. Bug 智能分析

主页面支持输入实际测试 Bug。

输入：

- Bug 标题
- Bug 描述
- 复现步骤
- 预期结果
- 实际结果
- 测试环境

系统辅助分析：

- 严重程度
- Bug 优先级
- Bug 类型
- 可能原因
- 定位建议
- 测试遗漏
- 回归测试点

注意：

项目只根据 Bug 现象提供：

```text
可能原因
定位方向
```

不会假设已经知道真实代码根因。

确认后可以保存到：

```text
knowledge/历史Bug.txt
```

并重新构建 RAG 知识库。

---

# 19. 启动接口测试平台

项目还提供独立接口测试页面：

```text
api_test.py
```

启动：

```bash
python -m streamlit run api_test.py
```

如果主页面已经占用：

```text
8501
```

Streamlit 可能自动使用：

```text
8502
```

---

# 20. 接口测试使用流程

## 第一步：输入接口信息

支持填写：

```text
接口名称
请求方法
接口 URL
接口需求
Headers
Request Body
成功响应
异常响应
```

例如：

```text
接口名称：
用户登录接口

请求方法：
POST

URL：
https://api.example.com/login
```

Headers：

```json
{
  "Content-Type": "application/json"
}
```

Request Body：

```json
{
  "phone": "13800138000",
  "password": "123456"
}
```

成功响应：

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "token": "example_token"
  }
}
```

异常响应：

```json
{
  "code": 1001,
  "message": "手机号或密码错误"
}
```

---

# 21. AI + Skill 接口分析

点击：

```text
开始接口测试分析
```

现在系统不再只是让大模型自由生成测试点。

当前流程已经升级为：

```text
接口需求
↓
接口分析
↓
字段规则提取
↓
Testing Skill
↓
测试点生成
↓
测试用例生成
↓
AI 输出校验
```

---

# 22. Boundary Skill 边界值测试

项目新增：

```text
skills/boundary_skill.py
```

用于程序化生成边界值。

例如：

```text
password 长度 6~20 位
```

生成：

```text
5  → 下边界外
6  → 下边界
7  → 下边界内

19 → 上边界内
20 → 上边界
21 → 上边界外
```

例如：

```text
phone 必须11位
```

生成：

```text
10位
11位
12位
```

这样边界测试不再完全依赖大模型自由推理。

---

# 23. Equivalence Skill 等价类测试

项目新增：

```text
skills/equivalence_skill.py
```

用于生成有效等价类和无效等价类。

例如手机号：

```text
有效：
合法手机号

无效：
字段缺失
空字符串
null
长度不足
长度超出
包含字母
包含特殊字符
非1开头
全角数字
错误数据类型
```

对于邮箱也支持：

```text
合法邮箱
缺少@
缺少域名
缺少用户名
格式错误
```

---

# 24. API Skill 接口测试规则

项目新增：

```text
skills/api_skill.py
```

用于组合：

```text
Boundary Skill
+
Equivalence Skill
+
接口通用测试规则
```

当前覆盖：

### HTTP Method

例如 POST 接口：

```text
POST 正常请求
GET 错误请求
PUT 错误请求
PATCH 错误请求
DELETE 错误请求
```

### Headers

```text
Content-Type正确
Content-Type缺失
Content-Type=text/plain
Content-Type=application/xml
```

### Request Body

```text
正常JSON
空Body
非法JSON
JSON数组
额外字段
```

### Response

```text
HTTP状态码
业务code
message
响应字段类型
必返回字段
```

### Exception

```text
请求超时
服务异常
网络中断
重复提交
```

### Security

```text
SQL特殊字符
异常脚本字符
敏感数据传输
高频请求风险
```

---

# 25. Skill 使用原则

Skill 不是新的业务需求。

项目遵循：

```text
当前需求
>
测试 Skill
>
AI 自由推理
```

也就是说：

```text
需求明确
→ 按需求生成

需求未明确
→ 标记【需求待确认】

Skill 与需求冲突
→ 以需求为准
```

同时禁止 AI 为不存在的请求字段编造确定性测试场景。

---

# 26. AI 输出结构校验

项目新增：

```text
utils/validation_utils.py
```

AI 生成用例后，不会直接完全信任模型输出。

现在流程：

```text
AI生成
↓
JSON容错解析
↓
字段标准化
↓
结构校验
↓
异常提示
↓
测试人员复核
```

当前可检查：

```text
case_id
module
title
method
url
expected_http_status
expected_business_result
priority
```

并识别：

```text
字段缺失
非法 priority
非法 HTTP Method
HTTP 状态码异常
重复 case_id
重复标题
```

priority 目前只允许：

```text
P0
P1
P2
```

如果 AI 输出：

```text
高
中
低
P3
P0级
空值
```

平台会将其识别为异常。

---

# 27. 接口用例原子化生成

为了避免 AI 把多个场景合并成一条用例，当前 Prompt 已加入：

```text
一个独立测试条件
=
一条独立测试用例
```

例如：

```text
password 5位
password 6位
password 7位
password 19位
password 20位
password 21位
```

需要分别生成。

而不是只生成：

```text
验证password长度边界
```

同样：

```text
phone缺失
phone=""
phone=null
```

也必须尽量拆成独立测试用例。

这有利于：

```text
测试执行
问题定位
自动化参数化
后续评测
```

---

# 28. Pytest 自动化脚本生成

接口测试页面支持根据当前接口测试用例生成：

```text
Pytest + Requests
```

自动化测试脚本。

生成内容包括：

- pytest
- requests
- parametrize
- timeout
- HTTP 状态码断言
- 业务结果断言
- 请求参数数据
- 异常处理

生成后支持下载：

```text
test_api_generated.py
```

---

# 29. 当前项目结构

当前项目结构已经逐步拆分为：

```text
ai-software-testing-platform/
│
├── app.py
│   └── 功能测试主平台
│
├── api_test.py
│   └── 接口测试平台
│
├── rag.py
│   └── RAG 知识库
│
├── main.py
│
├── prompts/
│   ├── __init__.py
│   ├── functional_prompts.py
│   └── api_prompts.py
│
├── services/
│   ├── __init__.py
│   └── model_factory.py
│
├── utils/
│   ├── __init__.py
│   ├── json_utils.py
│   ├── file_utils.py
│   ├── case_utils.py
│   ├── excel_utils.py
│   └── validation_utils.py
│
├── skills/
│   ├── __init__.py
│   ├── boundary_skill.py
│   ├── equivalence_skill.py
│   └── api_skill.py
│
├── knowledge/
│   ├── 测试规范.txt
│   └── 历史Bug.txt
│
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

本地运行过程中还会生成：

```text
chroma_db/
knowledge_hash.json
.env
.venv/
```

其中：

```text
.env
.venv/
chroma_db/
```

不建议提交到 GitHub。

---

# 30. 技术栈

项目主要使用：

```text
Python
Streamlit
LangChain
DeepSeek
Chroma
HuggingFace Embeddings
RAG
Pandas
OpenPyXL
PyPDF
python-docx
json-repair
Pytest
Requests
```

---

# 31. 当前核心流程

## 功能测试

```text
需求
↓
RAG测试经验检索
↓
需求评审
↓
测试点设计
↓
测试用例生成
↓
人工编辑
↓
智能优化
↓
质量评分
↓
RTM
↓
Dashboard
↓
Excel
```

## 接口测试

现在已经升级为：

```text
接口信息
↓
接口分析
↓
字段规则提取
↓
Boundary Skill
+
Equivalence Skill
+
API Skill
↓
接口测试点
↓
接口测试用例
↓
AI输出结构校验
↓
Pytest 自动化脚本
```

## 测试经验

```text
Bug
↓
Bug分析
↓
测试遗漏
↓
回归测试点
↓
历史Bug知识库
↓
RAG
↓
后续需求检索复用
```

---

# 32. 当前已经完成的工程化优化

当前项目已经完成：

- Prompt 独立模块
- 模型调用统一封装
- Utils 公共工具层
- JSON 容错解析
- 文件读取工具层
- 测试用例转换工具层
- Excel 工具层
- AI 输出 Validation 校验层
- Boundary Skill
- Equivalence Skill
- API Skill
- Skill 与接口 Prompt 集成
- Skill 状态页面展示
- 接口测试用例细粒度约束
- 非标准 AI 输出识别

项目已经从最早：

```text
Prompt
↓
AI
↓
测试用例
```

升级到：

```text
需求
↓
测试知识
+
Testing Skill
↓
Prompt
↓
AI
↓
JSON解析
↓
Validation
↓
测试用例
```

---

# 33. 后续开发计划

接下来项目会继续扩展以下能力。

## 第一阶段：通用字段规则自动提取

目前接口 Skill 已经可以处理：

```text
phone
password
```

下一步会升级为自动识别任意接口字段，例如：

```text
username
email
age
amount
price
page
page_size
order_id
address
status
```

目标：

```text
接口需求
↓
自动提取字段
↓
提取类型
↓
提取必填规则
↓
提取长度
↓
提取范围
↓
自动进入 Skill
```

---

## 第二阶段：固定 AI 评测集

计划建立标准测试需求，例如：

```text
登录
注册
订单
搜索
分页
文件上传
权限
支付
```

每个需求人工维护标准测试点。

例如：

```text
标准测试点：30
AI实际覆盖：26
遗漏：4
```

用于真正衡量 AI 测试设计质量。

---

## 第三阶段：自动测试质量评测

计划增加自动指标：

```text
需求覆盖率
Skill覆盖率
边界覆盖率
等价类覆盖率
异常覆盖率
重复率
非法输出率
需求一致性
```

形成：

```text
AI测试用例
↓
自动评测
↓
质量评分
↓
遗漏分析
```

而不是完全依赖另一个大模型进行主观评分。

---

## 第四阶段：Pytest 自动执行

当前已经可以：

```text
生成 Pytest 脚本
```

后续增加：

```text
生成
↓
执行
↓
获取结果
```

页面直接显示：

```text
通过
失败
跳过
异常
执行耗时
```

---

## 第五阶段：Allure 测试报告

Pytest 执行完成后计划接入：

```text
Allure
```

生成：

```text
测试执行结果
测试步骤
失败详情
历史趋势
失败截图/日志
```

---

## 第六阶段：AI 自动分析失败用例

对执行失败的测试：

```text
失败用例
↓
请求
↓
响应
↓
异常日志
↓
AI分析
```

输出：

```text
可能原因
接口问题
数据问题
脚本问题
环境问题
断言问题
建议定位方向
```

---

## 第七阶段：任务与历史记录

增加：

```text
任务ID
需求名称
创建时间
测试用例
质量评分
执行结果
```

支持查看历史任务。

后续可以实现：

```text
第一次生成
↓
需求修改
↓
第二次生成
↓
版本差异
```

---

## 第八阶段：接口文档自动解析

计划支持：

```text
Swagger
OpenAPI
```

直接导入接口文档。

流程：

```text
Swagger / OpenAPI
↓
解析接口
↓
识别参数
↓
识别类型
↓
识别必填字段
↓
识别响应
↓
Skill
↓
自动生成用例
```

---

## 第九阶段：持续集成

后续计划接入：

```text
Jenkins
GitHub Actions
```

实现：

```text
代码提交
↓
自动执行接口测试
↓
生成报告
↓
失败分析
```

---

## 第十阶段：Web UI 自动化

后续可以扩展：

```text
页面元素识别
UI测试点生成
Playwright / Selenium
UI自动化脚本生成
```

形成：

```text
功能测试
+
接口测试
+
UI自动化
```

统一测试平台。

---

# 34. 项目定位

这个项目不是为了完全替代测试工程师。

项目的核心思路是：

```text
AI
负责提效

Testing Skill
负责确定性测试方法

RAG
负责经验复用

Validation
负责检查AI输出

测试人员
负责最终判断
```

最终目标是：

```text
减少重复测试设计工作
↓
复用历史测试经验
↓
降低AI随机性
↓
减少测试场景遗漏
↓
提升测试设计效率和质量
```

目前项目还会继续完善，重点方向是：

```text
规则自动提取
固定评测集
自动评分
Pytest真实执行
Allure报告
失败分析
任务历史
Swagger/OpenAPI
CI/CD
UI自动化
```

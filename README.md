AI 软件测试平台是一个本地运行的智能测试辅助工具。
支持输入产品需求、需求文档和接口信息，自动完成：
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
- Pytest + Requests 自动化脚本生成
- Excel 测试结果导出
项目同时加入了 RAG 测试知识库，可以将测试规范、历史 Bug 等资料作为测试经验，在后续需求分析和测试设计中进行检索参考。
推荐使用：
```text
Python 3.11
Windows 可以在终端执行：
python --version
或者：
py --version
如果输出类似：
Python 3.11.x
说明 Python 环境正常。
当前项目也可以尝试运行在更高版本 Python，但 LangChain、Embedding、Torch 等 AI 相关依赖通常在 Python 3.11 下兼容性更稳定。

2. 下载项目
方法一：Git Clone
打开终端执行：
git clone https://github.com/zzb131012-cpu/Repository-name-ai-software-testing-platform.git
进入项目目录：
cd Repository-name-ai-software-testing-platform
方法二：下载 ZIP
在 GitHub 仓库页面点击：
Code
→ Download ZIP
下载后解压项目。
3. 创建虚拟环境
Windows：
python -m venv .venv
激活虚拟环境：
.venv\Scripts\activate
激活成功后，终端前面通常会出现：
(.venv)
例如：
(.venv) PS D:\ai-software-testing-platform>
macOS / Linux：
python3 -m venv .venv
激活：
source .venv/bin/activate
4. 安装项目依赖
项目已经提供：
requirements.txt
执行：
python -m pip install -r requirements.txt
安装时间根据网络情况有所不同。
如果下载 HuggingFace Embedding 模型较慢，需要等待模型首次下载完成。
5. 配置环境变量
项目不会上传真实 API Key。
仓库中提供：
.env.example
复制一份并改名为：
.env
Windows 可以直接在项目根目录创建 .env 文件。
内容：
DEEPSEEK_API_KEY=你的API_KEY
例如：
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxx
注意：
.env
已经加入：
.gitignore
不要把真实 API Key 上传到 GitHub。
6. 启动功能测试平台
项目主页面：
app.py
执行：
python -m streamlit run app.py
启动成功后终端会显示：
Local URL: http://localhost:8501
浏览器打开：
http://localhost:8501
即可进入：
AI 软件测试平台
功能测试使用流程
1. 输入需求
支持两种方式：
手动输入
上传需求文档
支持上传：
- TXT
- Markdown
- PDF
- Word
示例需求：
用户通过手机号和密码登录。

手机号不能为空。
密码不能为空。

手机号必须为11位数字。

密码连续输错5次后，
账号锁定30分钟。

账号锁定期间，即使输入正确密码，
也不能登录。

登录成功后进入首页。
点击：
开始智能测试分析
2. 需求评审
系统会自动分析：
- 需求理解
- 已明确需求规则
- 需求风险
- 需求待确认
- 测试建议
对于需求中没有明确说明的内容，不直接编造业务规则，而是标记：
【需求待确认】
例如：
密码最大长度未明确
3. 测试点分析
系统会从多个测试维度进行分析：
- 正常场景
- 异常场景
- 边界值
- 业务规则
- 数据校验
- 状态流转
- 权限与安全
- 兼容性
- 历史 Bug 回归
- 需求待确认
4. 自动生成测试用例
生成的测试用例包含：
字段	说明
用例编号	TC001、TC002...
测试模块	当前测试功能模块
测试标题	用例验证目标
前置条件	执行前准备
操作步骤	实际测试步骤
测试数据	输入数据
预期结果	正确业务结果
优先级	P0 / P1 / P2


例如：
TC001
登录
正确手机号和正确密码登录成功
P0
生成后的测试用例可以直接在网页表格中进行：
- 修改
- 新增
- 删除
修改完成后点击：
保存修改
5. 智能用例优化
支持三个操作：
补充遗漏用例
删除重复用例
全面优化用例
补充遗漏用例
系统检查当前测试设计是否漏掉：
- 正常场景
- 异常场景
- 边界场景
- 关键业务规则
- 历史 Bug 回归场景
删除重复用例
识别：
重复
高度重复
验证目标基本一致
的测试用例。
全面优化
同时完成：
- 补遗漏
- 去重复
- 优化标题
- 优化步骤
- 优化测试数据
- 优化预期结果
- 调整优先级
6. 测试质量评分
点击：
开始质量评估
系统从多个维度进行评分：
需求覆盖度
正常场景覆盖
异常场景覆盖
边界值覆盖
业务规则覆盖
可执行性
非重复质量
例如：
总体质量评分：88 / 100

需求覆盖：92
正常场景：95
异常场景：88
边界覆盖：80
业务规则：92
可执行性：90
非重复：95
同时输出：
- 测试设计优势
- 遗漏场景
- 高风险遗漏
- 优化建议
7. RTM 需求追踪矩阵
RTM：
Requirement Traceability Matrix
用于建立：
需求
↓
测试用例
之间的对应关系。
点击：
生成需求追踪矩阵
系统首先自动拆分需求：
R001 手机号不能为空
R002 密码不能为空
R003 手机号必须11位
R004 密码连续错误5次锁定30分钟
...
然后分析每条需求由哪些测试用例覆盖。
例如：
需求编号	需求内容	覆盖用例	状态
R001	手机号不能为空	TC003	已覆盖
R002	密码不能为空	TC004	已覆盖
R003	手机号必须11位	TC005、TC006	已覆盖
R004	错误5次锁定	TC010	部分覆盖


覆盖状态包括：
已覆盖
部分覆盖
未覆盖
可以用于快速检查是否存在漏测。
8. 测试质量 Dashboard
Dashboard 汇总当前测试设计数据。
包括：
测试用例总数
总体质量评分
需求覆盖率
未覆盖需求数
P0 核心用例
部分覆盖需求
高风险遗漏
重复风险
用于快速判断当前测试设计质量。
9. Excel 导出
测试完成后点击：
下载测试结果
系统生成：
AI测试结果.xlsx
Excel 可以包含：
Sheet1：测试用例
Sheet2：需求追踪矩阵
方便继续进行：
- 测试执行
- 测试评审
- 用例维护
- 回归测试
RAG 测试知识库
项目支持维护自己的软件测试知识库。
左侧：
测试知识库
支持上传：
- TXT
- Markdown
- PDF
- Word
例如：
测试规范.txt
历史Bug.txt
项目使用：
Embedding
+
Chroma
+
RAG
将文档转换为向量知识。
当用户输入需求时：
当前需求
↓
向量检索
↓
找到相关测试规范 / 历史 Bug
↓
作为测试经验传递给测试分析流程
历史 Bug 经验复用
例如曾经发现：
密码连续输错5次后，
账号没有进入锁定状态。
将 Bug 保存到知识库以后，下次出现类似登录需求时，系统可以检索这条历史测试经验，并提示重点检查：
第4次 → 第5次失败状态转换
锁定状态
锁定期间输入正确密码
29分59秒
30分钟
30分01秒
登录成功后失败次数清零
形成：
发现 Bug
↓
沉淀历史经验
↓
进入知识库
↓
RAG 检索
↓
反哺下一次测试设计
Bug 智能分析
主页面支持输入实际测试 Bug。
输入：
- Bug 标题
- Bug 描述
- 复现步骤
- 预期结果
- 实际结果
- 测试环境
系统会辅助分析：
- 严重程度
- Bug 优先级
- Bug 类型
- 可能原因
- 定位建议
- 测试遗漏
- 回归测试点
注意：
项目只根据 Bug 现象提供：
可能原因
定位方向
不会假设已经知道真实代码根因。
分析确认后，可以保存到：
knowledge/历史Bug.txt
并自动更新测试知识库。
接口测试平台
项目还提供单独的接口测试页面：
api_test.py
启动：
python -m streamlit run api_test.py
如果 8501 已被主页面使用，Streamlit 会自动使用新的端口，例如：
http://localhost:8502
接口测试使用流程
1. 输入接口信息
支持填写：
接口名称
请求方法
接口 URL
接口需求
Headers
Request Body
成功响应
异常响应
例如：
接口名称：
用户登录接口
请求方法：
POST
URL：
https://api.example.com/login
Headers：
{
  "Content-Type": "application/json"
}
请求：
{
  "phone": "13800138000",
  "password": "123456"
}
成功响应：
{
  "code": 0,
  "message": "success",
  "data": {
    "token": "example_token"
  }
}
异常响应：
{
  "code": 1001,
  "message": "手机号或密码错误"
}
2. 接口分析
点击：
开始 AI 接口分析
自动分析：
- 请求参数
- 响应结构
- 参数校验
- Header
- 鉴权
- Token
- 权限
- 重复提交
- HTTP 状态码
- 业务状态码
- 服务异常
- 超时
- 并发风险
3. 接口测试用例
自动生成：
API001
API002
API003
...
测试维度包括：
- 正常请求
- 缺少参数
- 参数为空
- 参数类型错误
- 参数格式错误
- 参数边界
- Header 异常
- Token 异常
- 权限不足
- 重复提交
- HTTP 状态码
- 业务返回
- 服务异常
- 超时
4. Pytest 自动化脚本
接口测试页面可以根据测试用例进一步生成：
Pytest + Requests
自动化测试模板。
点击：
生成 Pytest 脚本
生成脚本包含：
- pytest
- requests
- parametrize 参数化
- timeout
- HTTP 状态码断言
- 业务结果断言
- 请求异常处理
生成后支持直接下载：
test_api.py
项目结构
ai-software-testing-platform/
│
├── app.py
│   └── 功能测试主平台
│
├── api_test.py
│   └── 接口测试平台
│
├── rag.py
│   └── RAG 知识库处理
│
├── main.py
│   └── 命令行测试用例生成示例
│
├── knowledge/
│   ├── 测试规范.txt
│   └── 历史Bug.txt
│
├── requirements.txt
│
├── .env.example
│
├── .gitignore
│
└── README.md
本地运行过程中还会生成：
chroma_db/
knowledge_hash.json
.env
.venv/
其中：
.env
.venv/
chroma_db/
不建议提交到 GitHub。
技术栈
项目主要使用：
Python
Streamlit
LangChain
Chroma
HuggingFace Embeddings
RAG
Pandas
OpenPyXL
PyPDF
python-docx
Pytest
Requests
项目核心流程
功能测试：
需求
↓
测试经验检索
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
接口测试：
接口信息
↓
接口分析
↓
接口测试点
↓
接口测试用例
↓
Pytest 自动化脚本
测试经验：
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
后续需求检索复用
安全说明
请勿将真实 API Key 上传到 GitHub。
项目中的：
.env
已通过：
.gitignore
忽略。
GitHub 中只保留：
.env.example
示例：
DEEPSEEK_API_KEY=your_api_key_here
后续计划
后续可以继续扩展：
- Pytest 自动执行
- Allure 测试报告
- AI 自动分析失败用例
- Jenkins 持续集成
- 接口文档自动解析
- Swagger / OpenAPI 导入
- 测试报告自动生成
- 多项目知识库管理
- 测试用例版本管理
- Web UI 自动化测试生成
项目定位
这个项目不是为了完全替代测试工程师。
主要目标是：
AI 负责提效
+
知识库负责经验复用
+
测试人员负责最终判断
帮助测试人员减少重复工作，提高需求分析和测试设计效率，同时降低测试场景遗漏风险。
```

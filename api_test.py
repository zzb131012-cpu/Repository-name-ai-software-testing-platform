import os
import json

import pandas as pd
import streamlit as st

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from json_repair import repair_json


# =========================================================
# 1. 页面配置
# =========================================================

st.set_page_config(
    page_title="AI 接口测试平台",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# 2. 页面 CSS
# =========================================================

st.markdown(
    """
<style>

/* 页面背景 */
.stApp {
    background:
        linear-gradient(
            180deg,
            #f7f9fc 0%,
            #ffffff 300px
        );
}

/* 主内容最大宽度 */
.block-container {
    max-width: 1500px;
    padding-top: 1.4rem;
    padding-bottom: 4rem;
}

/* 隐藏 Streamlit footer */
footer {
    visibility: hidden;
}

/* 标题 */
.main-title {
    font-size: 32px;
    font-weight: 800;
    margin-bottom: 6px;
    letter-spacing: -0.5px;
}

.main-description {
    color: #667085;
    font-size: 15px;
    margin-bottom: 22px;
}

/* Hero */
.hero-card {
    padding: 24px 28px;
    background: linear-gradient(
        135deg,
        #ffffff,
        #f5f8ff
    );
    border: 1px solid #e7ecf3;
    border-radius: 18px;
    margin-bottom: 20px;
    box-shadow:
        0 6px 22px rgba(15, 23, 42, 0.05);
}

/* 通用卡片 */
.panel-card {
    background: white;
    border: 1px solid #e7ecf3;
    border-radius: 16px;
    padding: 18px 20px;
    margin-bottom: 16px;
    box-shadow:
        0 4px 16px rgba(15, 23, 42, 0.035);
}

/* 小标签 */
.status-chip {
    display: inline-block;
    padding: 5px 10px;
    border-radius: 20px;
    background: #eef4ff;
    color: #175cd3;
    font-size: 12px;
    font-weight: 600;
    margin-right: 6px;
}

/* Section 标题 */
.section-title {
    font-size: 21px;
    font-weight: 750;
    margin-top: 14px;
    margin-bottom: 12px;
}

/* 辅助说明 */
.section-description {
    color: #667085;
    margin-bottom: 14px;
    font-size: 14px;
}

/* Metric */
[data-testid="stMetric"] {
    background: white;
    border: 1px solid #e7ecf3;
    padding: 14px 16px;
    border-radius: 14px;
    box-shadow:
        0 3px 12px rgba(15, 23, 42, 0.03);
}

[data-testid="stMetricValue"] {
    font-size: 27px;
    font-weight: 750;
}

/* 输入框 */
div[data-baseweb="input"] > div {
    border-radius: 10px;
}

textarea {
    border-radius: 10px !important;
}

/* 按钮 */
.stButton > button {
    border-radius: 10px;
    min-height: 42px;
    font-weight: 650;
}

/* 下载按钮 */
.stDownloadButton > button {
    border-radius: 10px;
    min-height: 42px;
    font-weight: 650;
}

/* tabs */
button[data-baseweb="tab"] {
    font-weight: 650;
}

/* sidebar */
[data-testid="stSidebar"] {
    background: #f8fafc;
    border-right: 1px solid #e7ecf3;
}

/* dataframe */
[data-testid="stDataFrame"] {
    border: 1px solid #e7ecf3;
    border-radius: 12px;
    overflow: hidden;
}

/* success/warning/error */
[data-testid="stAlert"] {
    border-radius: 12px;
}

</style>
""",
    unsafe_allow_html=True
)


# =========================================================
# 3. 环境变量
# =========================================================

load_dotenv()

api_key = os.getenv(
    "DEEPSEEK_API_KEY"
)

if not api_key:

    st.error(
        "没有读取到 DEEPSEEK_API_KEY，请检查 .env 文件。"
    )

    st.stop()


# =========================================================
# 4. DeepSeek
# =========================================================

model = ChatOpenAI(
    model="deepseek-chat",
    api_key=api_key,
    base_url="https://api.deepseek.com",
    temperature=0
)


# =========================================================
# 5. Session State
# =========================================================

default_states = {
    "api_analysis": "",
    "api_test_points": "",
    "api_cases": [],
    "pytest_script": ""
}


for key, value in default_states.items():

    if key not in st.session_state:

        st.session_state[key] = value


# =========================================================
# 6. JSON 工具
# =========================================================

def clean_json_text(content):

    if not content:

        return ""

    content = content.strip()

    if content.startswith("```json"):

        content = content[
            len("```json"):
        ].strip()

    elif content.startswith("```"):

        content = content[
            3:
        ].strip()

    if content.endswith("```"):

        content = content[
            :-3
        ].strip()

    return content


def parse_json_list(content):

    if not content:

        return None

    cleaned = clean_json_text(
        content
    )

    # 第一次：直接解析
    try:

        result = json.loads(
            cleaned
        )

        if isinstance(
            result,
            list
        ):

            return result

    except json.JSONDecodeError:

        pass


    # 第二次：提取数组
    start = cleaned.find("[")

    end = cleaned.rfind("]")

    if (
        start != -1
        and end != -1
        and end > start
    ):

        cleaned = cleaned[
            start:end + 1
        ]

        try:

            result = json.loads(
                cleaned
            )

            if isinstance(
                result,
                list
            ):

                return result

        except json.JSONDecodeError:

            pass


    # 第三次：JSON Repair
    try:

        repaired = repair_json(
            cleaned
        )

        result = json.loads(
            repaired
        )

        if isinstance(
            result,
            list
        ):

            return result

    except Exception:

        pass


    return None


def clean_python_code(content):

    if not content:

        return ""

    content = content.strip()

    if content.startswith(
        "```python"
    ):

        content = content[
            len("```python"):
        ].strip()

    elif content.startswith(
        "```"
    ):

        content = content[
            3:
        ].strip()

    if content.endswith(
        "```"
    ):

        content = content[
            :-3
        ].strip()

    return content


# =========================================================
# 7. Sidebar
# =========================================================

with st.sidebar:

    st.markdown(
        "## 🧪 AI Test Platform"
    )

    st.caption(
        "接口测试智能生成平台"
    )

    st.divider()

    st.markdown(
        "### 当前能力"
    )

    st.write(
        "✅ 接口需求分析"
    )

    st.write(
        "✅ 接口测试点"
    )

    st.write(
        "✅ 测试用例生成"
    )

    st.write(
        "✅ JSON 自动修复"
    )

    st.write(
        "✅ Pytest 自动化"
    )

    st.divider()

    st.markdown(
        "### 模型"
    )

    st.info(
        "DeepSeek Chat"
    )

    st.divider()

    api_count = len(
        st.session_state[
            "api_cases"
        ]
    )

    st.metric(
        "当前接口用例",
        api_count
    )

    if st.session_state[
        "pytest_script"
    ]:

        st.success(
            "自动化脚本已生成"
        )

    else:

        st.caption(
            "尚未生成自动化脚本"
        )


# =========================================================
# 8. 顶部 Hero
# =========================================================

st.markdown(
    """
<div class="hero-card">

<div class="main-title">
🧪 AI 接口测试平台
</div>

<div class="main-description">
基于 DeepSeek 自动完成接口分析、测试点设计、
测试用例生成以及 Pytest + Requests 自动化脚本生成。
</div>

<span class="status-chip">DeepSeek</span>
<span class="status-chip">Pytest</span>
<span class="status-chip">Requests</span>
<span class="status-chip">JSON Repair</span>

</div>
""",
    unsafe_allow_html=True
)


# =========================================================
# 9. 接口配置
# =========================================================

st.markdown(
    '<div class="section-title">① 接口配置</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    '填写接口基本信息、请求参数和响应示例。'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# 基础配置
# =========================================================

with st.container(
    border=True
):

    st.markdown(
        "#### 基础信息"
    )

    base_col1, base_col2, base_col3 = (
        st.columns(
            [
                2,
                1,
                3
            ]
        )
    )

    with base_col1:

        api_name = st.text_input(
            "接口名称",
            placeholder="用户登录接口"
        )

    with base_col2:

        request_method = st.selectbox(
            "请求方法",
            [
                "GET",
                "POST",
                "PUT",
                "DELETE",
                "PATCH"
            ]
        )

    with base_col3:

        api_url = st.text_input(
            "接口 URL",
            placeholder=(
                "https://api.example.com/login"
            )
        )


    api_description = st.text_area(
        "接口需求",
        height=150,
        placeholder="""
用户通过手机号和密码登录。

手机号不能为空。
密码不能为空。
手机号必须为11位数字。

正确手机号和正确密码登录成功并返回 token。

密码错误时返回手机号或密码错误。
"""
    )


# =========================================================
# 请求与响应 Tabs
# =========================================================

request_tab, response_tab = st.tabs(
    [
        "📤 请求配置",
        "📥 响应配置"
    ]
)


with request_tab:

    request_col1, request_col2 = (
        st.columns(2)
    )

    with request_col1:

        headers_text = st.text_area(
            "Headers",
            height=190,
            placeholder="""
{
  "Content-Type": "application/json"
}
"""
        )

    with request_col2:

        request_body = st.text_area(
            "Request Body",
            height=190,
            placeholder="""
{
  "phone": "13800138000",
  "password": "123456"
}
"""
        )


with response_tab:

    response_col1, response_col2 = (
        st.columns(2)
    )

    with response_col1:

        success_response = (
            st.text_area(
                "成功响应",
                height=190,
                placeholder="""
{
  "code": 0,
  "message": "success",
  "data": {
    "token": "example_token"
  }
}
"""
            )
        )

    with response_col2:

        error_response = (
            st.text_area(
                "异常响应",
                height=190,
                placeholder="""
{
  "code": 1001,
  "message": "手机号或密码错误"
}
"""
            )
        )


# =========================================================
# 10. AI 分析按钮
# =========================================================

st.write("")

button_col1, button_col2 = st.columns(
    [
        1,
        4
    ]
)


with button_col1:

    start_analysis = st.button(
        "🚀 开始 AI 接口分析",
        type="primary",
        use_container_width=True
    )


with button_col2:

    st.caption(
        "AI 会依次生成：接口分析 → 测试点 → 测试用例"
    )


# =========================================================
# 11. AI 分析
# =========================================================

if start_analysis:

    if not api_url.strip():

        st.warning(
            "请先填写接口 URL。"
        )

        st.stop()


    # =====================================================
    # 接口分析
    # =====================================================

    analysis_prompt = f"""
你是一名高级接口测试工程师。

分析下面接口。

请输出：

## 接口用途
## 请求参数分析
## 响应分析
## 业务规则
## 异常风险
## 测试重点
## 需求待确认

规则：

1. 不创造不存在的业务规则。
2. 不明确内容标记【需求待确认】。

接口名称：

{api_name}

请求方法：

{request_method}

URL：

{api_url}

接口需求：

{api_description}

Header：

{headers_text}

请求参数：

{request_body}

成功响应：

{success_response}

异常响应：

{error_response}
"""


    try:

        with st.spinner(
            "① 正在分析接口..."
        ):

            response = model.invoke(
                analysis_prompt
            )

            st.session_state[
                "api_analysis"
            ] = response.content

    except Exception as e:

        st.error(
            f"接口分析失败：{e}"
        )

        st.stop()


    # =====================================================
    # 测试点
    # =====================================================

    point_prompt = f"""
你是一名高级接口测试工程师。

根据接口需求生成完整测试点。

覆盖：

正常请求
参数缺失
参数为空
参数类型
参数长度
参数格式
非法参数
Header
鉴权
Token
权限
重复提交
幂等性
HTTP状态码
业务码
响应字段
超时
服务异常
安全
并发
需求待确认

未明确内容必须标记【需求待确认】。

接口：

{api_name}

方法：

{request_method}

URL：

{api_url}

需求：

{api_description}

接口分析：

{st.session_state["api_analysis"]}
"""


    try:

        with st.spinner(
            "② 正在生成接口测试点..."
        ):

            response = model.invoke(
                point_prompt
            )

            st.session_state[
                "api_test_points"
            ] = response.content

    except Exception as e:

        st.error(
            f"测试点生成失败：{e}"
        )

        st.stop()


    # =====================================================
    # 测试用例
    # =====================================================

    case_prompt = f"""
你是一名高级接口测试工程师。

生成接口测试用例。

只输出 JSON 数组。

字段：

case_id
module
title
method
url
headers
request_data
expected_http_status
expected_business_result
priority

要求：

1. case_id 从 API001 开始。
2. priority 只能 P0/P1/P2。
3. 覆盖正常、异常、边界。
4. 覆盖参数缺失、为空、类型、格式。
5. 覆盖 Header、鉴权、Token、权限。
6. 覆盖重复提交、状态码、业务响应。
7. 覆盖超时、服务异常。
8. 不创造业务规则。
9. 未明确预期使用【需求待确认】。
10. headers 与 request_data 使用字符串。
11. 不输出 Markdown。

接口：

{api_name}

请求方法：

{request_method}

URL：

{api_url}

需求：

{api_description}

Headers：

{headers_text}

Request：

{request_body}

成功响应：

{success_response}

异常响应：

{error_response}

测试点：

{st.session_state["api_test_points"]}
"""


    try:

        with st.spinner(
            "③ 正在生成接口测试用例..."
        ):

            case_response = model.invoke(
                case_prompt
            )

    except Exception as e:

        st.error(
            f"测试用例生成失败：{e}"
        )

        st.stop()


    cases = parse_json_list(
        case_response.content
    )


    if cases is None:

        st.error(
            "接口测试用例 JSON 解析失败。"
        )

        with st.expander(
            "查看 AI 原始返回",
            expanded=True
        ):

            st.code(
                case_response.content
            )

        st.stop()


    for index, case in enumerate(
        cases,
        start=1
    ):

        case[
            "case_id"
        ] = f"API{index:03d}"


    st.session_state[
        "api_cases"
    ] = cases

    st.session_state[
        "pytest_script"
    ] = ""


    st.success(
        f"AI 分析完成，共生成 {len(cases)} 条接口测试用例。"
    )


# =========================================================
# 12. 分析结果
# =========================================================

if (
    st.session_state[
        "api_analysis"
    ]
    or st.session_state[
        "api_test_points"
    ]
):

    st.divider()

    st.markdown(
        '<div class="section-title">'
        '② AI 分析结果'
        '</div>',
        unsafe_allow_html=True
    )


    analysis_tab, point_tab = st.tabs(
        [
            "🧠 接口分析",
            "🎯 测试点"
        ]
    )


    with analysis_tab:

        if st.session_state[
            "api_analysis"
        ]:

            st.markdown(
                st.session_state[
                    "api_analysis"
                ]
            )

        else:

            st.info(
                "暂无接口分析结果。"
            )


    with point_tab:

        if st.session_state[
            "api_test_points"
        ]:

            st.markdown(
                st.session_state[
                    "api_test_points"
                ]
            )

        else:

            st.info(
                "暂无测试点。"
            )


# =========================================================
# 13. 测试用例
# =========================================================

if st.session_state[
    "api_cases"
]:

    st.divider()

    st.markdown(
        '<div class="section-title">'
        '③ 接口测试用例'
        '</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "支持直接编辑、新增和删除测试用例。"
    )


    rows = []


    for case in st.session_state[
        "api_cases"
    ]:

        rows.append(
            {
                "用例编号":
                    case.get(
                        "case_id",
                        ""
                    ),

                "模块":
                    case.get(
                        "module",
                        ""
                    ),

                "标题":
                    case.get(
                        "title",
                        ""
                    ),

                "Method":
                    case.get(
                        "method",
                        ""
                    ),

                "URL":
                    case.get(
                        "url",
                        ""
                    ),

                "Headers":
                    case.get(
                        "headers",
                        ""
                    ),

                "请求数据":
                    case.get(
                        "request_data",
                        ""
                    ),

                "HTTP状态":
                    case.get(
                        "expected_http_status",
                        ""
                    ),

                "业务预期":
                    case.get(
                        "expected_business_result",
                        ""
                    ),

                "优先级":
                    case.get(
                        "priority",
                        ""
                    )
            }
        )


    api_df = pd.DataFrame(
        rows
    )


    edited_api_df = st.data_editor(
        api_df,
        use_container_width=True,
        hide_index=True,
        num_rows="dynamic",
        height=430,
        key="api_case_editor",
        column_config={
            "Method":
                st.column_config.SelectboxColumn(
                    "Method",
                    options=[
                        "GET",
                        "POST",
                        "PUT",
                        "DELETE",
                        "PATCH"
                    ],
                    width="small"
                ),

            "优先级":
                st.column_config.SelectboxColumn(
                    "优先级",
                    options=[
                        "P0",
                        "P1",
                        "P2"
                    ],
                    width="small"
                ),

            "用例编号":
                st.column_config.TextColumn(
                    "用例编号",
                    width="small"
                ),

            "标题":
                st.column_config.TextColumn(
                    "标题",
                    width="large"
                )
        }
    )


    # =====================================================
    # 保存按钮
    # =====================================================

    save_col1, save_col2 = st.columns(
        [
            1,
            4
        ]
    )


    with save_col1:

        save_cases = st.button(
            "💾 保存修改",
            use_container_width=True
        )


    if save_cases:

        updated_cases = []

        for _, row in (
            edited_api_df.iterrows()
        ):

            updated_cases.append(
                {
                    "case_id":
                        str(
                            row.get(
                                "用例编号",
                                ""
                            )
                        ),

                    "module":
                        str(
                            row.get(
                                "模块",
                                ""
                            )
                        ),

                    "title":
                        str(
                            row.get(
                                "标题",
                                ""
                            )
                        ),

                    "method":
                        str(
                            row.get(
                                "Method",
                                ""
                            )
                        ),

                    "url":
                        str(
                            row.get(
                                "URL",
                                ""
                            )
                        ),

                    "headers":
                        str(
                            row.get(
                                "Headers",
                                ""
                            )
                        ),

                    "request_data":
                        str(
                            row.get(
                                "请求数据",
                                ""
                            )
                        ),

                    "expected_http_status":
                        row.get(
                            "HTTP状态",
                            ""
                        ),

                    "expected_business_result":
                        str(
                            row.get(
                                "业务预期",
                                ""
                            )
                        ),

                    "priority":
                        str(
                            row.get(
                                "优先级",
                                ""
                            )
                        )
                }
            )


        for index, case in enumerate(
            updated_cases,
            start=1
        ):

            case[
                "case_id"
            ] = f"API{index:03d}"


        st.session_state[
            "api_cases"
        ] = updated_cases

        st.session_state[
            "pytest_script"
        ] = ""

        st.success(
            "测试用例修改已保存。"
        )

        st.rerun()


    # =====================================================
    # 14. Dashboard
    # =====================================================

    st.markdown(
        '<div class="section-title">'
        '④ 接口测试 Dashboard'
        '</div>',
        unsafe_allow_html=True
    )


    current_rows = (
        edited_api_df.to_dict(
            orient="records"
        )
    )


    total_count = len(
        current_rows
    )


    p0_count = sum(
        1
        for row in current_rows
        if str(
            row.get(
                "优先级",
                ""
            )
        ) == "P0"
    )


    p1_count = sum(
        1
        for row in current_rows
        if str(
            row.get(
                "优先级",
                ""
            )
        ) == "P1"
    )


    p2_count = sum(
        1
        for row in current_rows
        if str(
            row.get(
                "优先级",
                ""
            )
        ) == "P2"
    )


    dashboard1, dashboard2, dashboard3, dashboard4 = (
        st.columns(4)
    )


    dashboard1.metric(
        "测试用例总数",
        total_count
    )

    dashboard2.metric(
        "P0 核心用例",
        p0_count
    )

    dashboard3.metric(
        "P1 重要用例",
        p1_count
    )

    dashboard4.metric(
        "P2 普通用例",
        p2_count
    )


    # =====================================================
    # 15. Pytest
    # =====================================================

    st.divider()

    st.markdown(
        '<div class="section-title">'
        '⑤ Pytest 接口自动化'
        '</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "根据当前编辑后的接口测试用例生成 pytest + requests 自动化脚本。"
    )


    script_col1, script_col2 = (
        st.columns(
            [
                1,
                4
            ]
        )
    )


    with script_col1:

        generate_script = st.button(
            "⚙️ 生成 Pytest 脚本",
            type="primary",
            use_container_width=True
        )


    if generate_script:

        current_cases = (
            edited_api_df.to_dict(
                orient="records"
            )
        )


        script_prompt = f"""
你是一名高级 Python 接口自动化测试工程师。

根据接口信息和测试用例生成完整
pytest + requests 自动化脚本。

要求：

1. 使用 pytest。
2. 使用 requests。
3. 使用 @pytest.mark.parametrize。
4. timeout=10。
5. 校验 HTTP 状态码。
6. 需求明确时校验业务 code/message。
7. 需求不明确使用 TODO 注释。
8. 不允许写 API Key。
9. 不允许写真实 Token。
10. 使用：
<VALID_PHONE>
<VALID_PASSWORD>
<VALID_TOKEN>
11. JSON 字符串使用 json.loads。
12. GET 使用 params。
13. POST/PUT/PATCH 使用 json。
14. 捕获 requests 异常。
15. 最后加入：

if __name__ == "__main__":
    pytest.main(["-v", __file__])

16. 只输出 Python 代码。
17. 不输出 Markdown。

接口：

{api_name}

方法：

{request_method}

URL：

{api_url}

Headers：

{headers_text}

需求：

{api_description}

测试用例：

{json.dumps(
    current_cases,
    ensure_ascii=False
)}
"""


        try:

            with st.spinner(
                "正在生成 Pytest 自动化脚本..."
            ):

                response = model.invoke(
                    script_prompt
                )

                st.session_state[
                    "pytest_script"
                ] = clean_python_code(
                    response.content
                )

        except Exception as e:

            st.error(
                f"自动化脚本生成失败：{e}"
            )


# =========================================================
# 16. 自动化脚本预览
# =========================================================

if st.session_state[
    "pytest_script"
]:

    script_tab, json_tab = st.tabs(
        [
            "🐍 自动化脚本",
            "🔍 测试数据 JSON"
        ]
    )


    with script_tab:

        st.code(
            st.session_state[
                "pytest_script"
            ],
            language="python"
        )

        st.download_button(
            "⬇️ 下载 test_api.py",
            data=st.session_state[
                "pytest_script"
            ],
            file_name="test_api.py",
            mime="text/x-python",
            type="primary"
        )


    with json_tab:

        st.json(
            st.session_state[
                "api_cases"
            ]
        )


# =========================================================
# 17. 底部操作
# =========================================================

if (
    st.session_state[
        "api_analysis"
    ]
    or st.session_state[
        "api_cases"
    ]
):

    st.divider()

    bottom_col1, bottom_col2 = (
        st.columns(
            [
                1,
                4
            ]
        )
    )


    with bottom_col1:

        if st.button(
            "🗑 清空当前结果",
            use_container_width=True
        ):

            st.session_state[
                "api_analysis"
            ] = ""

            st.session_state[
                "api_test_points"
            ] = ""

            st.session_state[
                "api_cases"
            ] = []

            st.session_state[
                "pytest_script"
            ] = ""

            st.rerun()
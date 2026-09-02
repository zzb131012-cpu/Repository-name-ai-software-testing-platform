import json

import pandas as pd
import streamlit as st

try:
    from json_repair import repair_json
except ImportError:
    repair_json = None

from services.model_factory import get_model

from prompts.api_prompts import (
    build_api_analysis_prompt,
    build_api_test_point_prompt,
    build_api_case_prompt,
    build_pytest_script_prompt
)


# =========================================================
# 1. 页面配置
# =========================================================

st.set_page_config(
    page_title="AI 接口测试助手",
    page_icon="🔌",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# 2. 页面样式
# =========================================================

st.markdown(
    """
<style>

.stApp {
    background:
        linear-gradient(
            180deg,
            #f7f9fc 0%,
            #ffffff 300px
        );
}

.block-container {
    max-width: 1500px;
    padding-top: 1.4rem;
    padding-bottom: 4rem;
}

footer {
    visibility: hidden;
}

.hero-card {
    padding: 26px 30px;
    border-radius: 18px;
    border: 1px solid #e6eaf0;
    background:
        linear-gradient(
            135deg,
            #ffffff,
            #f4f7ff
        );
    box-shadow:
        0 6px 24px rgba(15, 23, 42, 0.05);
    margin-bottom: 20px;
}

.hero-title {
    font-size: 32px;
    font-weight: 800;
    margin-bottom: 6px;
}

.hero-description {
    color: #667085;
    font-size: 15px;
    line-height: 1.7;
}

.feature-chip {
    display: inline-block;
    padding: 5px 11px;
    border-radius: 20px;
    background: #eef4ff;
    color: #175cd3;
    font-size: 12px;
    font-weight: 650;
    margin-right: 6px;
    margin-top: 8px;
}

.section-title {
    font-size: 22px;
    font-weight: 760;
    margin-top: 16px;
    margin-bottom: 6px;
}

.section-desc {
    color: #667085;
    font-size: 14px;
    margin-bottom: 14px;
}

[data-testid="stMetric"] {
    background: white;
    border: 1px solid #e6eaf0;
    border-radius: 14px;
    padding: 14px 16px;
}

.stButton > button {
    border-radius: 10px;
    min-height: 42px;
    font-weight: 650;
}

.stDownloadButton > button {
    border-radius: 10px;
    min-height: 42px;
    font-weight: 650;
}

[data-testid="stDataFrame"] {
    border: 1px solid #e6eaf0;
    border-radius: 12px;
    overflow: hidden;
}

[data-testid="stSidebar"] {
    background: #f8fafc;
    border-right: 1px solid #e6eaf0;
}

textarea {
    border-radius: 10px !important;
}

</style>
""",
    unsafe_allow_html=True
)


# =========================================================
# 3. AI 模型
# =========================================================

try:
    model = get_model()

except Exception as e:

    st.error(
        f"AI 服务初始化失败：{e}"
    )

    st.stop()


# =========================================================
# 4. Session State
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
# 5. JSON 工具
# =========================================================

def clean_json_text(content):

    if not content:
        return ""

    content = content.strip()

    if content.startswith("```json"):
        content = content[len("```json"):].strip()

    elif content.startswith("```"):
        content = content[3:].strip()

    if content.endswith("```"):
        content = content[:-3].strip()

    return content


def parse_json_list(content):

    cleaned = clean_json_text(
        content
    )

    # =====================================================
    # 第一次：直接解析
    # =====================================================

    try:

        result = json.loads(
            cleaned
        )

        if isinstance(
            result,
            list
        ):
            return result

    except Exception:
        pass

    # =====================================================
    # 第二次：提取 [...]
    # =====================================================

    start = cleaned.find(
        "["
    )

    end = cleaned.rfind(
        "]"
    )

    if (
        start != -1
        and end != -1
        and end > start
    ):

        json_part = cleaned[
            start:end + 1
        ]

        try:

            result = json.loads(
                json_part
            )

            if isinstance(
                result,
                list
            ):
                return result

        except Exception:
            pass

    # =====================================================
    # 第三次：json-repair
    # =====================================================

    if repair_json:

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

    if content.startswith("```python"):

        content = content[
            len("```python"):
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


# =========================================================
# 6. 接口用例编号
# =========================================================

def normalize_api_case_ids(
    api_cases
):

    for index, case in enumerate(
        api_cases,
        start=1
    ):

        case[
            "case_id"
        ] = f"API{index:03d}"

    return api_cases


# =========================================================
# 7. DataFrame 转换
# =========================================================

def api_cases_to_dataframe(
    api_cases
):

    rows = []

    for case in api_cases:

        rows.append(
            {
                "用例编号":
                    case.get(
                        "case_id",
                        ""
                    ),

                "测试模块":
                    case.get(
                        "module",
                        ""
                    ),

                "测试标题":
                    case.get(
                        "title",
                        ""
                    ),

                "请求方式":
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

                "预期HTTP状态码":
                    case.get(
                        "expected_http_status",
                        ""
                    ),

                "预期业务结果":
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

    return pd.DataFrame(
        rows
    )


def dataframe_to_api_cases(
    dataframe
):

    cases = []

    for _, row in dataframe.iterrows():

        cases.append(
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
                            "测试模块",
                            ""
                        )
                    ),

                "title":
                    str(
                        row.get(
                            "测试标题",
                            ""
                        )
                    ),

                "method":
                    str(
                        row.get(
                            "请求方式",
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
                    str(
                        row.get(
                            "预期HTTP状态码",
                            ""
                        )
                    ),

                "expected_business_result":
                    str(
                        row.get(
                            "预期业务结果",
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

    return cases


# =========================================================
# 8. Sidebar
# =========================================================

with st.sidebar:

    st.markdown(
        "## 🔌 接口测试助手"
    )

    st.caption(
        "接口分析 · 测试设计 · 自动化脚本"
    )

    st.divider()

    st.markdown(
        "### 📊 当前状态"
    )

    current_api_cases = (
        st.session_state[
            "api_cases"
        ]
    )

    total_count = len(
        current_api_cases
    )

    p0_count = sum(
        case.get(
            "priority"
        ) == "P0"
        for case in current_api_cases
    )

    p1_count = sum(
        case.get(
            "priority"
        ) == "P1"
        for case in current_api_cases
    )

    p2_count = sum(
        case.get(
            "priority"
        ) == "P2"
        for case in current_api_cases
    )

    side1, side2 = st.columns(
        2
    )

    side1.metric(
        "用例",
        total_count
    )

    side2.metric(
        "P0",
        p0_count
    )

    side3, side4 = st.columns(
        2
    )

    side3.metric(
        "P1",
        p1_count
    )

    side4.metric(
        "P2",
        p2_count
    )

    st.divider()

    if st.button(
        "🗑 清空当前接口分析",
        width="stretch"
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


# =========================================================
# 9. Hero
# =========================================================

st.markdown(
    """
<div class="hero-card">

<div class="hero-title">
🔌 AI 接口测试助手
</div>

<div class="hero-description">
输入接口信息后，自动完成接口分析、测试点设计、
接口测试用例生成以及 Pytest + Requests 自动化脚本生成。
</div>

<span class="feature-chip">接口分析</span>
<span class="feature-chip">参数校验</span>
<span class="feature-chip">异常场景</span>
<span class="feature-chip">接口用例</span>
<span class="feature-chip">Pytest</span>

</div>
""",
    unsafe_allow_html=True
)


# =========================================================
# 10. 接口输入
# =========================================================

st.markdown(
    '<div class="section-title">'
    '① 接口信息'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-desc">'
    '填写接口基本信息和请求响应示例。'
    '</div>',
    unsafe_allow_html=True
)


with st.container(
    border=True
):

    base_col1, base_col2 = (
        st.columns(2)
    )

    with base_col1:

        api_name = st.text_input(
            "接口名称",
            placeholder="例如：用户登录接口"
        )

        request_method = st.selectbox(
            "请求方式",
            [
                "GET",
                "POST",
                "PUT",
                "PATCH",
                "DELETE"
            ]
        )

    with base_col2:

        api_url = st.text_input(
            "接口 URL",
            placeholder="https://api.example.com/login"
        )

        api_description = st.text_area(
            "接口需求",
            height=110,
            placeholder="""
例如：

用户通过手机号和密码进行登录。
手机号不能为空。
密码不能为空。
登录成功返回 token。
"""
        )


    st.markdown(
        "#### 请求信息"
    )

    request_col1, request_col2 = (
        st.columns(2)
    )

    with request_col1:

        headers_text = st.text_area(
            "Headers",
            height=160,
            value="""{
    "Content-Type": "application/json"
}"""
        )

    with request_col2:

        request_body = st.text_area(
            "Request Body / Params",
            height=160,
            value="""{
    "phone": "13800138000",
    "password": "123456"
}"""
        )


    st.markdown(
        "#### 响应示例"
    )

    response_col1, response_col2 = (
        st.columns(2)
    )

    with response_col1:

        success_response = (
            st.text_area(
                "成功响应示例",
                height=180,
                value="""{
    "code": 0,
    "message": "success",
    "data": {
        "token": "example_token"
    }
}"""
            )
        )

    with response_col2:

        error_response = (
            st.text_area(
                "异常响应示例",
                height=180,
                value="""{
    "code": 1001,
    "message": "手机号或密码错误"
}"""
            )
        )


    start_col1, start_col2 = (
        st.columns(
            [
                1,
                4
            ]
        )
    )

    with start_col1:

        start_analysis = st.button(
            "🚀 开始接口测试分析",
            type="primary",
            width="stretch"
        )

    with start_col2:

        st.caption(
            "系统将执行：接口分析 → 测试点 → 接口测试用例"
        )


# =========================================================
# 11. 主分析流程
# =========================================================

if start_analysis:

    if not api_name.strip():

        st.warning(
            "请填写接口名称。"
        )

        st.stop()

    if not api_url.strip():

        st.warning(
            "请填写接口 URL。"
        )

        st.stop()

    # =====================================================
    # 接口分析
    # =====================================================

    analysis_prompt = (
        build_api_analysis_prompt(
            api_name,
            request_method,
            api_url,
            api_description,
            headers_text,
            request_body,
            success_response,
            error_response
        )
    )

    try:

        with st.spinner(
            "正在分析接口..."
        ):

            analysis_response = (
                model.invoke(
                    analysis_prompt
                )
            )

    except Exception as e:

        st.error(
            f"接口分析失败：{e}"
        )

        st.stop()

    api_analysis = (
        analysis_response.content
    )

    st.session_state[
        "api_analysis"
    ] = api_analysis


    # =====================================================
    # 测试点
    # =====================================================

    point_prompt = (
        build_api_test_point_prompt(
            api_name,
            request_method,
            api_url,
            api_description,
            api_analysis
        )
    )

    try:

        with st.spinner(
            "正在生成接口测试点..."
        ):

            point_response = (
                model.invoke(
                    point_prompt
                )
            )

    except Exception as e:

        st.error(
            f"接口测试点生成失败：{e}"
        )

        st.stop()

    api_test_points = (
        point_response.content
    )

    st.session_state[
        "api_test_points"
    ] = api_test_points


    # =====================================================
    # 接口测试用例
    # =====================================================

    case_prompt = (
        build_api_case_prompt(
            api_name,
            request_method,
            api_url,
            api_description,
            headers_text,
            request_body,
            success_response,
            error_response,
            api_test_points
        )
    )

    try:

        with st.spinner(
            "正在生成接口测试用例..."
        ):

            case_response = (
                model.invoke(
                    case_prompt
                )
            )

    except Exception as e:

        st.error(
            f"接口测试用例生成失败：{e}"
        )

        st.stop()

    api_cases = (
        parse_json_list(
            case_response.content
        )
    )

    if api_cases is None:

        st.error(
            "接口测试用例 JSON 解析失败。"
        )

        with st.expander(
            "查看 AI 原始返回"
        ):

            st.code(
                case_response.content
            )

        st.stop()

    api_cases = (
        normalize_api_case_ids(
            api_cases
        )
    )

    st.session_state[
        "api_cases"
    ] = api_cases

    st.session_state[
        "pytest_script"
    ] = ""

    st.success(
        f"分析完成，共生成 {len(api_cases)} 条接口测试用例。"
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
        '② 接口分析结果'
        '</div>',
        unsafe_allow_html=True
    )

    analysis_tab, point_tab = (
        st.tabs(
            [
                "📋 接口分析",
                "🎯 接口测试点"
            ]
        )
    )

    with analysis_tab:

        st.markdown(
            st.session_state[
                "api_analysis"
            ]
        )

    with point_tab:

        st.markdown(
            st.session_state[
                "api_test_points"
            ]
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
        "支持在表格中直接修改、新增或删除接口用例。"
    )

    dataframe = (
        api_cases_to_dataframe(
            st.session_state[
                "api_cases"
            ]
        )
    )

    edited_df = st.data_editor(
        dataframe,
        width="stretch",
        hide_index=True,
        num_rows="dynamic",
        height=500,
        key="api_case_editor",
        column_config={
            "用例编号":
                st.column_config.TextColumn(
                    "用例编号",
                    width="small"
                ),

            "测试标题":
                st.column_config.TextColumn(
                    "测试标题",
                    width="large"
                ),

            "请求方式":
                st.column_config.SelectboxColumn(
                    "请求方式",
                    options=[
                        "GET",
                        "POST",
                        "PUT",
                        "PATCH",
                        "DELETE"
                    ]
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
                )
        }
    )

    current_cases = (
        dataframe_to_api_cases(
            edited_df
        )
    )


    save_col1, save_col2 = (
        st.columns(
            [
                1,
                4
            ]
        )
    )

    with save_col1:

        save_cases = st.button(
            "💾 保存接口用例修改",
            width="stretch"
        )

    if save_cases:

        current_cases = (
            normalize_api_case_ids(
                current_cases
            )
        )

        st.session_state[
            "api_cases"
        ] = current_cases

        st.session_state[
            "pytest_script"
        ] = ""

        st.success(
            "接口测试用例修改已保存。"
        )

        st.rerun()


    # =====================================================
    # 用例统计
    # =====================================================

    st.markdown(
        '<div class="section-title">'
        '④ 用例统计'
        '</div>',
        unsafe_allow_html=True
    )

    total_count = len(
        current_cases
    )

    p0_count = sum(
        case.get(
            "priority"
        ) == "P0"
        for case in current_cases
    )

    p1_count = sum(
        case.get(
            "priority"
        ) == "P1"
        for case in current_cases
    )

    p2_count = sum(
        case.get(
            "priority"
        ) == "P2"
        for case in current_cases
    )

    metric1, metric2, metric3, metric4 = (
        st.columns(4)
    )

    metric1.metric(
        "总用例",
        total_count
    )

    metric2.metric(
        "P0",
        p0_count
    )

    metric3.metric(
        "P1",
        p1_count
    )

    metric4.metric(
        "P2",
        p2_count
    )


    # =====================================================
    # 14. Pytest 自动化
    # =====================================================

    st.markdown(
        '<div class="section-title">'
        '⑤ Pytest 自动化脚本'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-desc">'
        '根据当前接口测试用例生成 Pytest + Requests 自动化脚本。'
        '</div>',
        unsafe_allow_html=True
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
            width="stretch"
        )


    if generate_script:

        script_prompt = (
            build_pytest_script_prompt(
                api_name,
                request_method,
                api_url,
                headers_text,
                api_description,
                json.dumps(
                    current_cases,
                    ensure_ascii=False
                )
            )
        )

        try:

            with st.spinner(
                "正在生成自动化测试脚本..."
            ):

                script_response = (
                    model.invoke(
                        script_prompt
                    )
                )

        except Exception as e:

            st.error(
                f"Pytest 脚本生成失败：{e}"
            )

            st.stop()

        pytest_script = (
            clean_python_code(
                script_response.content
            )
        )

        st.session_state[
            "pytest_script"
        ] = pytest_script


    pytest_script = (
        st.session_state[
            "pytest_script"
        ]
    )

    if pytest_script:

        st.code(
            pytest_script,
            language="python"
        )

        st.download_button(
            "⬇️ 下载 Pytest 自动化脚本",
            data=pytest_script,
            file_name="test_api.py",
            mime="text/x-python",
            type="primary"
        )
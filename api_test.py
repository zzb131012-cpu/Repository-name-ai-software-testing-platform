import json

import pandas as pd
import streamlit as st

from services.model_factory import get_model

from prompts.api_prompts import (
    build_api_analysis_prompt,
    build_api_test_point_prompt,
    build_api_case_prompt,
    build_pytest_script_prompt,
)

from skills.api_skill import (
    build_api_skill_context,
)

from utils.json_utils import (
    parse_json_list,
    clean_python_code,
)

from utils.case_utils import (
    normalize_case_ids,
    api_cases_to_dataframe,
    dataframe_to_api_cases,
)

from utils.validation_utils import (
    normalize_api_cases,
    validate_api_cases,
)


# =========================================================
# 1. 页面配置
# =========================================================

st.set_page_config(
    page_title="AI 接口测试助手",
    page_icon="🔌",
    layout="wide",
    initial_sidebar_state="expanded",
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
    unsafe_allow_html=True,
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

DEFAULT_STATES = {
    "api_analysis": "",
    "api_test_points": "",
    "api_cases": [],
    "pytest_script": "",
    "api_validation_result": None,
    "api_skill_context": "",
}

for key, value in DEFAULT_STATES.items():

    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# 5. 通用方法
# =========================================================

def invoke_model(prompt):

    response = model.invoke(
        prompt
    )

    content = getattr(
        response,
        "content",
        response,
    )

    return str(content)


def reset_api_state():

    st.session_state.api_analysis = ""
    st.session_state.api_test_points = ""
    st.session_state.api_cases = []
    st.session_state.pytest_script = ""
    st.session_state.api_validation_result = None
    st.session_state.api_skill_context = ""


def refresh_validation():

    st.session_state[
        "api_validation_result"
    ] = validate_api_cases(
        st.session_state.api_cases
    )


def build_field_rules_from_requirement(
    api_description
):
    """
    当前阶段先使用轻量规则提取。

    后续会升级成：
    AI结构化规则提取 + Skill。
    """

    text = str(
        api_description
        or ""
    )

    rules = []

    lower_text = text.lower()

    if "phone" in lower_text:

        phone_parts = []

        if (
            "必填" in text
            or "不能为空" in text
        ):
            phone_parts.append(
                "必填"
            )

        if "11位" in text:
            phone_parts.append(
                "11位数字"
            )

        if (
            "以1开头" in text
            or "1开头" in text
        ):
            phone_parts.append(
                "以1开头"
            )

        rules.append(
            {
                "field": "phone",
                "rule": "，".join(
                    phone_parts
                )
                or "按照当前需求校验",
            }
        )

    if "password" in lower_text:

        password_parts = []

        if (
            "必填" in text
            or "不能为空" in text
        ):
            password_parts.append(
                "必填"
            )

        if (
            "6~20" in text
            or "6～20" in text
            or "6-20" in text
            or "6至20" in text
            or "6到20" in text
        ):
            password_parts.append(
                "长度6~20位"
            )

        rules.append(
            {
                "field":
                    "password",

                "rule":
                    "，".join(
                        password_parts
                    )
                    or "按照当前需求校验",
            }
        )

    return rules


# =========================================================
# 6. Sidebar
# =========================================================

with st.sidebar:

    st.markdown(
        "## 🔌 接口测试助手"
    )

    st.caption(
        "接口分析 · Skill测试设计 · 自动化脚本"
    )

    st.divider()

    current_api_cases = (
        st.session_state.api_cases
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

    st.markdown(
        "### 📊 当前状态"
    )

    side1, side2 = st.columns(2)

    side1.metric(
        "用例",
        total_count,
    )

    side2.metric(
        "P0",
        p0_count,
    )

    side3, side4 = st.columns(2)

    side3.metric(
        "P1",
        p1_count,
    )

    side4.metric(
        "P2",
        p2_count,
    )

    validation = (
        st.session_state.api_validation_result
    )

    if validation:

        st.divider()

        st.markdown(
            "### 🛡 输出校验"
        )

        col_valid, col_invalid = (
            st.columns(2)
        )

        col_valid.metric(
            "有效",
            validation.get(
                "valid",
                0,
            ),
        )

        col_invalid.metric(
            "异常",
            validation.get(
                "invalid",
                0,
            ),
        )

        if (
            validation.get(
                "error_count",
                0,
            )
            > 0
        ):

            st.error(
                f"发现 "
                f"{validation['error_count']} "
                f"个输出错误"
            )

        elif (
            validation.get(
                "warning_count",
                0,
            )
            > 0
        ):

            st.warning(
                f"发现 "
                f"{validation['warning_count']} "
                f"个风险提示"
            )

        else:

            st.success(
                "AI 输出结构校验通过"
            )

    if st.session_state.api_skill_context:

        st.divider()

        st.markdown(
            "### 🧠 Skill 状态"
        )

        st.success(
            "API Skill 已启用"
        )

    st.divider()

    if st.button(
        "🗑 清空当前接口分析",
        width="stretch",
    ):

        reset_api_state()

        st.rerun()


# =========================================================
# 7. Hero
# =========================================================

st.markdown(
    """
<div class="hero-card">

<div class="hero-title">
🔌 AI 接口测试助手
</div>

<div class="hero-description">
通过接口需求 + 测试 Skill + AI，
完成接口分析、测试点、测试用例、
输出校验以及 Pytest 自动化脚本生成。
</div>

<span class="feature-chip">接口分析</span>
<span class="feature-chip">Boundary Skill</span>
<span class="feature-chip">Equivalence Skill</span>
<span class="feature-chip">API Skill</span>
<span class="feature-chip">输出校验</span>
<span class="feature-chip">Pytest</span>

</div>
""",
    unsafe_allow_html=True,
)


# =========================================================
# 8. 接口输入
# =========================================================

st.markdown(
    '<div class="section-title">'
    '① 接口信息'
    '</div>',
    unsafe_allow_html=True,
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
            placeholder="例如：用户登录接口",
        )

        request_method = st.selectbox(
            "请求方式",
            [
                "GET",
                "POST",
                "PUT",
                "PATCH",
                "DELETE",
            ],
        )

    with base_col2:

        api_url = st.text_input(
            "接口 URL",
            placeholder=(
                "https://api.example.com/v1/login"
            ),
        )

        api_description = st.text_area(
            "接口需求",
            height=180,
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
}""",
        )

    with request_col2:

        request_body = st.text_area(
            "Request Body / Params",
            height=160,
            value="""{
    "phone": "13800138000",
    "password": "123456"
}""",
        )

    response_col1, response_col2 = (
        st.columns(2)
    )

    with response_col1:

        success_response = (
            st.text_area(
                "成功响应示例",
                height=180,
            )
        )

    with response_col2:

        error_response = (
            st.text_area(
                "异常响应示例",
                height=180,
            )
        )


# =========================================================
# 9. AI接口测试分析
# =========================================================

st.markdown(
    '<div class="section-title">'
    '② AI + Skill 接口测试分析'
    '</div>',
    unsafe_allow_html=True,
)

if st.button(
    "🚀 开始接口测试分析",
    type="primary",
    width="stretch",
):

    if not api_name.strip():

        st.warning(
            "请填写接口名称"
        )

    elif not api_url.strip():

        st.warning(
            "请填写接口 URL"
        )

    else:

        reset_api_state()

        try:

            with st.status(
                "正在执行 AI + Skill 接口测试分析...",
                expanded=True,
            ) as status:

                # =========================================
                # 1. 接口分析
                # =========================================

                st.write(
                    "① 正在分析接口..."
                )

                analysis_prompt = (
                    build_api_analysis_prompt(
                        api_name,
                        request_method,
                        api_url,
                        api_description,
                        headers_text,
                        request_body,
                        success_response,
                        error_response,
                    )
                )

                api_analysis = invoke_model(
                    analysis_prompt
                )

                st.session_state.api_analysis = (
                    api_analysis
                )

                # =========================================
                # 2. 生成 Skill
                # =========================================

                st.write(
                    "② 正在生成测试 Skill..."
                )

                field_rules = (
                    build_field_rules_from_requirement(
                        api_description
                    )
                )

                skill_context = (
                    build_api_skill_context(
                        request_method,
                        headers_text,
                        field_rules,
                    )
                )

                st.session_state[
                    "api_skill_context"
                ] = skill_context

                # =========================================
                # 3. 测试点
                # =========================================

                st.write(
                    "③ 正在生成接口测试点..."
                )

                point_prompt = (
                    build_api_test_point_prompt(
                        api_name,
                        request_method,
                        api_url,
                        api_description,
                        api_analysis,
                        skill_context,
                    )
                )

                points = invoke_model(
                    point_prompt
                )

                st.session_state.api_test_points = (
                    points
                )

                # =========================================
                # 4. 测试用例
                # =========================================

                st.write(
                    "④ 正在生成接口测试用例..."
                )

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
                        points,
                        skill_context,
                    )
                )

                case_content = invoke_model(
                    case_prompt
                )

                api_cases = parse_json_list(
                    case_content
                )

                if not api_cases:

                    raise ValueError(
                        "AI 返回的接口测试用例无法解析为 JSON"
                    )

                api_cases = (
                    normalize_api_cases(
                        api_cases
                    )
                )

                api_cases = (
                    normalize_case_ids(
                        api_cases,
                        prefix="API",
                    )
                )

                st.session_state.api_cases = (
                    api_cases
                )

                refresh_validation()

                status.update(
                    label=(
                        "AI + Skill 接口测试分析完成"
                    ),
                    state="complete",
                    expanded=False,
                )

            st.rerun()

        except Exception as e:

            st.error(
                f"接口测试分析失败：{e}"
            )


# =========================================================
# 10. AI分析结果
# =========================================================

if (
    st.session_state.api_analysis
    or st.session_state.api_test_points
    or st.session_state.api_skill_context
):

    st.markdown(
        '<div class="section-title">'
        '③ AI + Skill 分析结果'
        '</div>',
        unsafe_allow_html=True,
    )

    tab1, tab2, tab3 = st.tabs(
        [
            "接口分析",
            "测试点",
            "Skill规则",
        ]
    )

    with tab1:

        st.markdown(
            st.session_state.api_analysis
        )

    with tab2:

        st.markdown(
            st.session_state.api_test_points
        )

    with tab3:

        st.code(
            st.session_state.api_skill_context,
            language="text",
        )


# =========================================================
# 11. 接口测试用例
# =========================================================

if st.session_state.api_cases:

    st.markdown(
        '<div class="section-title">'
        '④ 接口测试用例'
        '</div>',
        unsafe_allow_html=True,
    )

    current_cases = (
        normalize_case_ids(
            st.session_state.api_cases,
            prefix="API",
        )
    )

    case_dataframe = (
        api_cases_to_dataframe(
            current_cases
        )
    )

    edited_dataframe = st.data_editor(
        case_dataframe,
        width="stretch",
        hide_index=True,
        num_rows="dynamic",
        key="api_case_editor",
    )

    edited_cases = (
        dataframe_to_api_cases(
            edited_dataframe
        )
    )

    edited_cases = (
        normalize_api_cases(
            edited_cases
        )
    )

    edited_cases = (
        normalize_case_ids(
            edited_cases,
            prefix="API",
        )
    )

    if (
        edited_cases
        != st.session_state.api_cases
    ):

        st.session_state.api_cases = (
            edited_cases
        )

        refresh_validation()

    p0_count = sum(
        case.get("priority") == "P0"
        for case in edited_cases
    )

    p1_count = sum(
        case.get("priority") == "P1"
        for case in edited_cases
    )

    p2_count = sum(
        case.get("priority") == "P2"
        for case in edited_cases
    )

    unknown_priority = (
        len(edited_cases)
        - p0_count
        - p1_count
        - p2_count
    )

    metric1, metric2, metric3, metric4 = (
        st.columns(4)
    )

    metric1.metric(
        "全部用例",
        len(edited_cases),
    )

    metric2.metric(
        "P0",
        p0_count,
    )

    metric3.metric(
        "P1",
        p1_count,
    )

    metric4.metric(
        "P2",
        p2_count,
    )

    if unknown_priority > 0:

        st.warning(
            f"存在 {unknown_priority} 条"
            f"优先级不规范的测试用例"
        )


# =========================================================
# 12. 输出校验
# =========================================================

if st.session_state.api_validation_result:

    validation = (
        st.session_state.api_validation_result
    )

    st.markdown(
        '<div class="section-title">'
        '⑤ AI 输出质量校验'
        '</div>',
        unsafe_allow_html=True,
    )

    validation_columns = (
        st.columns(5)
    )

    validation_columns[0].metric(
        "总用例",
        validation.get(
            "total",
            0,
        ),
    )

    validation_columns[1].metric(
        "有效用例",
        validation.get(
            "valid",
            0,
        ),
    )

    validation_columns[2].metric(
        "异常用例",
        validation.get(
            "invalid",
            0,
        ),
    )

    validation_columns[3].metric(
        "错误",
        validation.get(
            "error_count",
            0,
        ),
    )

    validation_columns[4].metric(
        "警告",
        validation.get(
            "warning_count",
            0,
        ),
    )

    issues = validation.get(
        "issues",
        []
    )

    if issues:

        issue_dataframe = (
            pd.DataFrame(
                issues
            )
        )

        issue_dataframe = (
            issue_dataframe.rename(
                columns={
                    "case_id":
                        "用例编号",

                    "level":
                        "级别",

                    "field":
                        "字段",

                    "message":
                        "问题说明",
                }
            )
        )

        st.dataframe(
            issue_dataframe,
            width="stretch",
            hide_index=True,
        )

    else:

        st.success(
            "AI 输出结构校验全部通过"
        )


# =========================================================
# 13. Pytest自动化
# =========================================================

if st.session_state.api_cases:

    st.markdown(
        '<div class="section-title">'
        '⑥ Pytest 自动化脚本'
        '</div>',
        unsafe_allow_html=True,
    )

    if st.button(
        "🐍 生成 Pytest 自动化脚本",
        width="stretch",
    ):

        try:

            with st.spinner(
                "正在生成 Pytest 脚本..."
            ):

                cases_json = json.dumps(
                    st.session_state.api_cases,
                    ensure_ascii=False,
                    indent=2,
                )

                prompt = (
                    build_pytest_script_prompt(
                        api_name,
                        request_method,
                        api_url,
                        headers_text,
                        api_description,
                        cases_json,
                    )
                )

                script = invoke_model(
                    prompt
                )

                script = (
                    clean_python_code(
                        script
                    )
                )

                if not script:

                    raise ValueError(
                        "AI 没有返回有效 Python 代码"
                    )

                st.session_state.pytest_script = (
                    script
                )

            st.success(
                "Pytest 脚本生成完成"
            )

        except Exception as e:

            st.error(
                f"Pytest 脚本生成失败：{e}"
            )


if st.session_state.pytest_script:

    st.code(
        st.session_state.pytest_script,
        language="python",
    )

    st.download_button(
        label="📥 下载 Pytest 脚本",
        data=st.session_state.pytest_script,
        file_name="test_api_generated.py",
        mime="text/x-python",
        width="stretch",
    )
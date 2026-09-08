import os
import json
from datetime import datetime

import pandas as pd
import streamlit as st

from services.model_factory import get_model

from prompts.functional_prompts import (
    build_review_prompt,
    build_test_point_prompt,
    build_test_case_prompt,
    build_add_missing_prompt,
    build_remove_duplicate_prompt,
    build_optimize_all_prompt,
    build_quality_prompt,
    build_requirement_split_prompt,
    build_rtm_prompt,
    build_bug_analysis_prompt,
)

from rag import (
    get_rag_context,
    rebuild_vector_db,
    get_knowledge_file_list,
    get_knowledge_file_content,
    delete_knowledge_file,
)

from utils.json_utils import (
    parse_json_list,
    parse_json_dict,
)

from utils.file_utils import (
    extract_requirement,
)

from utils.case_utils import (
    normalize_case_ids,
    functional_cases_to_dataframe,
    dataframe_to_functional_cases,
)

from utils.excel_utils import (
    create_test_result_excel,
)


# =========================================================
# 1. 页面配置
# =========================================================

st.set_page_config(
    page_title="AI 软件测试平台",
    page_icon="🧪",
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
            #ffffff 320px
        );
}

.block-container {
    max-width: 1500px;
    padding-top: 1.3rem;
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
    letter-spacing: -0.6px;
    margin-bottom: 6px;
}

.hero-description {
    color: #667085;
    font-size: 15px;
    line-height: 1.7;
    margin-bottom: 14px;
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
    margin-top: 4px;
}

.section-title {
    font-size: 22px;
    font-weight: 760;
    margin-top: 14px;
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
    box-shadow:
        0 3px 12px rgba(15, 23, 42, 0.035);
}

[data-testid="stMetricValue"] {
    font-size: 27px;
    font-weight: 760;
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

div[data-baseweb="input"] > div {
    border-radius: 10px;
}

textarea {
    border-radius: 10px !important;
}

[data-testid="stAlert"] {
    border-radius: 12px;
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

button[data-baseweb="tab"] {
    font-weight: 650;
}

</style>
""",
    unsafe_allow_html=True,
)


# =========================================================
# 3. 项目路径
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

KNOWLEDGE_DIR = os.path.join(
    BASE_DIR,
    "knowledge",
)

HISTORY_BUG_FILE = os.path.join(
    KNOWLEDGE_DIR,
    "历史Bug.txt",
)

os.makedirs(
    KNOWLEDGE_DIR,
    exist_ok=True,
)


# =========================================================
# 4. AI 模型
# =========================================================

try:
    model = get_model()

except Exception as e:
    st.error(
        f"AI 服务初始化失败：{e}"
    )
    st.stop()


# =========================================================
# 5. Session State
# =========================================================

DEFAULT_STATES = {
    "test_cases": [],
    "review_content": "",
    "analysis_content": "",
    "rag_context": "",
    "current_requirement": "",
    "quality_result": None,
    "rtm_result": [],
    "requirement_items": [],
    "bug_analysis": None,
    "knowledge_preview": "",
}

for key, value in DEFAULT_STATES.items():

    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# 6. 通用方法
# =========================================================

def invoke_model(prompt):
    """
    统一调用大模型。
    """

    response = model.invoke(prompt)

    content = getattr(
        response,
        "content",
        response,
    )

    return str(content)


def reset_analysis_state():
    """
    清空当前需求分析产生的数据。
    """

    st.session_state.test_cases = []
    st.session_state.review_content = ""
    st.session_state.analysis_content = ""
    st.session_state.rag_context = ""
    st.session_state.current_requirement = ""
    st.session_state.quality_result = None
    st.session_state.rtm_result = []
    st.session_state.requirement_items = []


def safe_score(value):
    """
    将 AI 返回评分安全转换为整数。
    """

    try:
        return int(float(value))

    except Exception:
        return 0


# =========================================================
# 7. Sidebar
# =========================================================

with st.sidebar:

    st.title("🧪 AI 测试平台")

    st.caption(
        "功能测试 · RAG · RTM · Bug 分析"
    )

    st.divider()

    st.subheader("📚 测试知识库")

    knowledge_files = (
        get_knowledge_file_list()
    )

    st.metric(
        "知识文件",
        len(knowledge_files),
    )

    if st.button(
        "🔄 重建 RAG 知识库",
        width="stretch",
    ):

        try:

            with st.spinner(
                "正在重新构建向量知识库..."
            ):

                rebuild_vector_db()

            st.success(
                "RAG 知识库重建完成"
            )

        except Exception as e:

            st.error(
                f"知识库重建失败：{e}"
            )

    if knowledge_files:

        selected_knowledge_file = st.selectbox(
            "查看知识文件",
            knowledge_files,
        )

        col_preview, col_delete = st.columns(
            2
        )

        with col_preview:

            if st.button(
                "查看",
                width="stretch",
            ):

                try:

                    st.session_state[
                        "knowledge_preview"
                    ] = get_knowledge_file_content(
                        selected_knowledge_file
                    )

                except Exception as e:

                    st.error(
                        f"读取失败：{e}"
                    )

        with col_delete:

            if st.button(
                "删除",
                width="stretch",
            ):

                try:

                    delete_knowledge_file(
                        selected_knowledge_file
                    )

                    rebuild_vector_db()

                    st.success(
                        "文件已删除"
                    )

                    st.rerun()

                except Exception as e:

                    st.error(
                        f"删除失败：{e}"
                    )

        if st.session_state.knowledge_preview:

            with st.expander(
                "知识文件内容",
                expanded=False,
            ):

                st.text(
                    st.session_state.knowledge_preview[
                        :10000
                    ]
                )

    st.divider()

    st.subheader("📊 当前分析")

    st.metric(
        "测试用例",
        len(
            st.session_state.test_cases
        ),
    )

    st.metric(
        "需求条目",
        len(
            st.session_state.requirement_items
        ),
    )

    st.metric(
        "RTM 条目",
        len(
            st.session_state.rtm_result
        ),
    )

    st.divider()

    if st.button(
        "🗑 清空当前结果",
        width="stretch",
    ):

        reset_analysis_state()

        st.session_state.bug_analysis = None

        st.rerun()


# =========================================================
# 8. Hero
# =========================================================

st.markdown(
    """
<div class="hero-card">

<div class="hero-title">
🧪 AI 软件测试用例生成与质量评估平台
</div>

<div class="hero-description">
从需求评审、测试点分析、RAG 历史经验检索，
到测试用例生成、AI 补漏去重、质量评分、
RTM 需求追踪和 Bug 分析。
</div>

<span class="feature-chip">需求评审</span>
<span class="feature-chip">RAG</span>
<span class="feature-chip">测试点</span>
<span class="feature-chip">测试用例</span>
<span class="feature-chip">质量评分</span>
<span class="feature-chip">RTM</span>
<span class="feature-chip">Bug 分析</span>

</div>
""",
    unsafe_allow_html=True,
)


# =========================================================
# 9. 需求输入
# =========================================================

st.markdown(
    '<div class="section-title">① 输入测试需求</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="section-desc">
可以直接输入需求，也可以上传 TXT、MD、PDF、DOCX 文档。
</div>
""",
    unsafe_allow_html=True,
)

input_mode = st.radio(
    "需求输入方式",
    [
        "手动输入",
        "上传需求文档",
    ],
    horizontal=True,
)

requirement = ""

if input_mode == "手动输入":

    requirement = st.text_area(
        "需求内容",
        height=260,
        placeholder=(
            "例如：\n"
            "用户输入手机号和验证码登录系统。\n"
            "手机号必须为 11 位...\n"
        ),
    )

else:

    uploaded_file = st.file_uploader(
        "上传需求文件",
        type=[
            "txt",
            "md",
            "pdf",
            "docx",
        ],
    )

    if uploaded_file is not None:

        try:

            requirement = extract_requirement(
                uploaded_file
            )

            st.success(
                f"文件解析成功，共提取 "
                f"{len(requirement)} 个字符"
            )

            with st.expander(
                "查看解析后的需求",
                expanded=False,
            ):

                st.text_area(
                    "文档内容",
                    requirement,
                    height=300,
                    disabled=True,
                )

        except Exception as e:

            st.error(
                f"需求文件解析失败：{e}"
            )

            requirement = ""


# =========================================================
# 10. 一键分析需求
# =========================================================

st.markdown(
    '<div class="section-title">② AI 测试分析</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="section-desc">
系统将按照：RAG 检索 → 需求评审 → 测试点 → 测试用例 的流程执行。
</div>
""",
    unsafe_allow_html=True,
)

if st.button(
    "🚀 开始生成测试方案",
    type="primary",
    width="stretch",
):

    if not requirement.strip():

        st.warning(
            "请先输入或上传测试需求"
        )

    else:

        reset_analysis_state()

        st.session_state[
            "current_requirement"
        ] = requirement.strip()

        try:

            # =============================================
            # RAG
            # =============================================

            with st.status(
                "正在执行 AI 测试分析...",
                expanded=True,
            ) as status:

                st.write(
                    "① 检索 RAG 测试知识库..."
                )

                try:

                    rag_context = get_rag_context(
                        requirement
                    )

                except Exception as e:

                    rag_context = ""

                    st.warning(
                        f"RAG 检索失败，将继续使用当前需求分析：{e}"
                    )

                st.session_state[
                    "rag_context"
                ] = rag_context or ""

                # =========================================
                # 需求评审
                # =========================================

                st.write(
                    "② AI 需求评审..."
                )

                review_prompt = (
                    build_review_prompt(
                        requirement,
                        rag_context,
                    )
                )

                review_content = invoke_model(
                    review_prompt
                )

                st.session_state[
                    "review_content"
                ] = review_content

                # =========================================
                # 测试点
                # =========================================

                st.write(
                    "③ 生成测试点..."
                )

                test_point_prompt = (
                    build_test_point_prompt(
                        requirement,
                        review_content,
                        rag_context,
                    )
                )

                analysis_content = invoke_model(
                    test_point_prompt
                )

                st.session_state[
                    "analysis_content"
                ] = analysis_content

                # =========================================
                # 测试用例
                # =========================================

                st.write(
                    "④ 生成结构化测试用例..."
                )

                test_case_prompt = (
                    build_test_case_prompt(
                        requirement,
                        review_content,
                        analysis_content,
                        rag_context,
                    )
                )

                case_content = invoke_model(
                    test_case_prompt
                )

                test_cases = parse_json_list(
                    case_content
                )

                if not test_cases:

                    raise ValueError(
                        "AI 返回的测试用例无法解析为 JSON"
                    )

                test_cases = normalize_case_ids(
                    test_cases,
                    prefix="TC",
                )

                st.session_state[
                    "test_cases"
                ] = test_cases

                status.update(
                    label="AI 测试分析完成",
                    state="complete",
                    expanded=False,
                )

            st.success(
                f"生成完成，共生成 "
                f"{len(test_cases)} 条测试用例"
            )

        except Exception as e:

            st.error(
                f"测试方案生成失败：{e}"
            )


# =========================================================
# 11. AI 分析结果
# =========================================================

if (
    st.session_state.review_content
    or st.session_state.analysis_content
):

    st.markdown(
        '<div class="section-title">③ AI 分析结果</div>',
        unsafe_allow_html=True,
    )

    tab_review, tab_points, tab_rag = (
        st.tabs(
            [
                "需求评审",
                "测试点",
                "RAG参考",
            ]
        )
    )

    with tab_review:

        st.markdown(
            st.session_state.review_content
            or "暂无结果"
        )

    with tab_points:

        st.markdown(
            st.session_state.analysis_content
            or "暂无结果"
        )

    with tab_rag:

        if st.session_state.rag_context:

            st.text(
                st.session_state.rag_context
            )

        else:

            st.info(
                "本次没有检索到相关历史知识"
            )


# =========================================================
# 12. 测试用例
# =========================================================

if st.session_state.test_cases:

    st.markdown(
        '<div class="section-title">④ 测试用例</div>',
        unsafe_allow_html=True,
    )

    current_cases = normalize_case_ids(
        st.session_state.test_cases,
        prefix="TC",
    )

    st.session_state.test_cases = (
        current_cases
    )

    case_dataframe = (
        functional_cases_to_dataframe(
            current_cases
        )
    )

    edited_dataframe = st.data_editor(
        case_dataframe,
        width="stretch",
        hide_index=True,
        num_rows="dynamic",
        key="functional_case_editor",
    )

    st.session_state.test_cases = (
        dataframe_to_functional_cases(
            edited_dataframe
        )
    )

    st.session_state.test_cases = (
        normalize_case_ids(
            st.session_state.test_cases,
            prefix="TC",
        )
    )

    # =============================================
    # 用例统计
    # =============================================

    p0_count = sum(
        1
        for case in st.session_state.test_cases
        if case.get("priority") == "P0"
    )

    p1_count = sum(
        1
        for case in st.session_state.test_cases
        if case.get("priority") == "P1"
    )

    p2_count = sum(
        1
        for case in st.session_state.test_cases
        if case.get("priority") == "P2"
    )

    col1, col2, col3, col4 = st.columns(
        4
    )

    col1.metric(
        "全部用例",
        len(st.session_state.test_cases),
    )

    col2.metric(
        "P0",
        p0_count,
    )

    col3.metric(
        "P1",
        p1_count,
    )

    col4.metric(
        "P2",
        p2_count,
    )


# =========================================================
# 13. AI 用例优化
# =========================================================

if st.session_state.test_cases:

    st.markdown(
        '<div class="section-title">⑤ AI 用例优化</div>',
        unsafe_allow_html=True,
    )

    col_add, col_duplicate, col_all = (
        st.columns(3)
    )

    with col_add:

        add_missing = st.button(
            "➕ AI 补充遗漏用例",
            width="stretch",
        )

    with col_duplicate:

        remove_duplicate = st.button(
            "🧹 AI 删除重复用例",
            width="stretch",
        )

    with col_all:

        optimize_all = st.button(
            "✨ AI 全面优化",
            width="stretch",
        )

    current_cases_json = json.dumps(
        st.session_state.test_cases,
        ensure_ascii=False,
        indent=2,
    )

    if add_missing:

        try:

            with st.spinner(
                "AI 正在检查遗漏场景..."
            ):

                prompt = build_add_missing_prompt(
                    st.session_state.current_requirement,
                    st.session_state.analysis_content,
                    st.session_state.rag_context,
                    current_cases_json,
                )

                result_content = invoke_model(
                    prompt
                )

                result = parse_json_list(
                    result_content
                )

                if not result:

                    raise ValueError(
                        "AI 返回结果无法解析"
                    )

                st.session_state.test_cases = (
                    normalize_case_ids(
                        result,
                        prefix="TC",
                    )
                )

            st.success(
                "遗漏用例补充完成"
            )

            st.rerun()

        except Exception as e:

            st.error(
                f"补充失败：{e}"
            )

    if remove_duplicate:

        try:

            with st.spinner(
                "AI 正在检查重复用例..."
            ):

                prompt = (
                    build_remove_duplicate_prompt(
                        current_cases_json
                    )
                )

                result_content = invoke_model(
                    prompt
                )

                result = parse_json_list(
                    result_content
                )

                if not result:

                    raise ValueError(
                        "AI 返回结果无法解析"
                    )

                st.session_state.test_cases = (
                    normalize_case_ids(
                        result,
                        prefix="TC",
                    )
                )

            st.success(
                "重复用例清理完成"
            )

            st.rerun()

        except Exception as e:

            st.error(
                f"去重失败：{e}"
            )

    if optimize_all:

        try:

            with st.spinner(
                "AI 正在全面优化测试用例..."
            ):

                prompt = (
                    build_optimize_all_prompt(
                        st.session_state.current_requirement,
                        st.session_state.analysis_content,
                        st.session_state.rag_context,
                        current_cases_json,
                    )
                )

                result_content = invoke_model(
                    prompt
                )

                result = parse_json_list(
                    result_content
                )

                if not result:

                    raise ValueError(
                        "AI 返回结果无法解析"
                    )

                st.session_state.test_cases = (
                    normalize_case_ids(
                        result,
                        prefix="TC",
                    )
                )

            st.success(
                "测试用例优化完成"
            )

            st.rerun()

        except Exception as e:

            st.error(
                f"优化失败：{e}"
            )


# =========================================================
# 14. AI 用例质量评分
# =========================================================

if st.session_state.test_cases:

    st.markdown(
        '<div class="section-title">⑥ AI 用例质量评估</div>',
        unsafe_allow_html=True,
    )

    if st.button(
        "📊 开始质量评分",
        width="stretch",
    ):

        try:

            with st.spinner(
                "正在评估测试用例质量..."
            ):

                cases_json = json.dumps(
                    st.session_state.test_cases,
                    ensure_ascii=False,
                    indent=2,
                )

                prompt = build_quality_prompt(
                    st.session_state.current_requirement,
                    st.session_state.analysis_content,
                    cases_json,
                )

                quality_content = invoke_model(
                    prompt
                )

                quality_result = (
                    parse_json_dict(
                        quality_content
                    )
                )

                if not quality_result:

                    raise ValueError(
                        "AI 质量评分结果无法解析"
                    )

                st.session_state[
                    "quality_result"
                ] = quality_result

            st.success(
                "质量评估完成"
            )

        except Exception as e:

            st.error(
                f"质量评分失败：{e}"
            )


if st.session_state.quality_result:

    quality = (
        st.session_state.quality_result
    )

    score_columns = st.columns(
        4
    )

    score_columns[0].metric(
        "综合评分",
        safe_score(
            quality.get(
                "overall_score",
                0,
            )
        ),
    )

    score_columns[1].metric(
        "需求覆盖",
        safe_score(
            quality.get(
                "requirement_coverage",
                0,
            )
        ),
    )

    score_columns[2].metric(
        "异常覆盖",
        safe_score(
            quality.get(
                "exception_coverage",
                0,
            )
        ),
    )

    score_columns[3].metric(
        "可执行性",
        safe_score(
            quality.get(
                "executability",
                0,
            )
        ),
    )

    with st.expander(
        "查看完整质量评估",
        expanded=True,
    ):

        st.json(
            quality
        )


# =========================================================
# 15. RTM 需求追踪矩阵
# =========================================================

if st.session_state.test_cases:

    st.markdown(
        '<div class="section-title">⑦ RTM 需求追踪矩阵</div>',
        unsafe_allow_html=True,
    )

    st.caption(
        "将需求拆成最小可验证条目，再检查每条需求是否有测试用例覆盖。"
    )

    if st.button(
        "🔗 生成 RTM",
        width="stretch",
    ):

        try:

            with st.spinner(
                "正在拆解需求并生成 RTM..."
            ):

                # =========================================
                # 需求拆分
                # =========================================

                split_prompt = (
                    build_requirement_split_prompt(
                        st.session_state.current_requirement
                    )
                )

                split_content = invoke_model(
                    split_prompt
                )

                requirement_items = (
                    parse_json_list(
                        split_content
                    )
                )

                if not requirement_items:

                    raise ValueError(
                        "需求拆分结果解析失败"
                    )

                st.session_state[
                    "requirement_items"
                ] = requirement_items

                # =========================================
                # RTM
                # =========================================

                requirement_items_json = (
                    json.dumps(
                        requirement_items,
                        ensure_ascii=False,
                        indent=2,
                    )
                )

                current_cases_json = (
                    json.dumps(
                        st.session_state.test_cases,
                        ensure_ascii=False,
                        indent=2,
                    )
                )

                rtm_prompt = build_rtm_prompt(
                    requirement_items_json,
                    current_cases_json,
                )

                rtm_content = invoke_model(
                    rtm_prompt
                )

                rtm_result = parse_json_list(
                    rtm_content
                )

                if not rtm_result:

                    raise ValueError(
                        "RTM 结果无法解析"
                    )

                st.session_state[
                    "rtm_result"
                ] = rtm_result

            st.success(
                "RTM 生成完成"
            )

        except Exception as e:

            st.error(
                f"RTM 生成失败：{e}"
            )


if st.session_state.rtm_result:

    rtm_dataframe = pd.DataFrame(
        st.session_state.rtm_result
    )

    st.dataframe(
        rtm_dataframe,
        width="stretch",
        hide_index=True,
    )

    covered = sum(
        1
        for item in st.session_state.rtm_result
        if item.get(
            "coverage_status"
        ) == "已覆盖"
    )

    partial = sum(
        1
        for item in st.session_state.rtm_result
        if item.get(
            "coverage_status"
        ) == "部分覆盖"
    )

    uncovered = sum(
        1
        for item in st.session_state.rtm_result
        if item.get(
            "coverage_status"
        ) == "未覆盖"
    )

    rtm_col1, rtm_col2, rtm_col3 = (
        st.columns(3)
    )

    rtm_col1.metric(
        "已覆盖",
        covered,
    )

    rtm_col2.metric(
        "部分覆盖",
        partial,
    )

    rtm_col3.metric(
        "未覆盖",
        uncovered,
    )


# =========================================================
# 16. Excel 导出
# =========================================================

if st.session_state.test_cases:

    st.markdown(
        '<div class="section-title">⑧ 测试结果导出</div>',
        unsafe_allow_html=True,
    )

    try:

        excel_data = (
            create_test_result_excel(
                st.session_state.test_cases,
                st.session_state.rtm_result,
            )
        )

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        st.download_button(
            label="📥 下载测试用例 Excel",
            data=excel_data,
            file_name=(
                f"AI测试用例_{timestamp}.xlsx"
            ),
            mime=(
                "application/vnd.openxmlformats-"
                "officedocument.spreadsheetml.sheet"
            ),
            width="stretch",
        )

    except Exception as e:

        st.error(
            f"Excel 生成失败：{e}"
        )


# =========================================================
# 17. Bug AI 分析
# =========================================================

st.divider()

st.markdown(
    '<div class="section-title">⑨ Bug AI 分析与知识沉淀</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="section-desc">
分析 Bug 可能原因、定位方向、测试遗漏及回归测试点，
并可将确认后的历史 Bug 保存到 RAG 知识库。
</div>
""",
    unsafe_allow_html=True,
)

bug_col1, bug_col2 = st.columns(
    2
)

with bug_col1:

    bug_title = st.text_input(
        "Bug 标题",
        placeholder="例如：登录接口连续输错密码未限制",
    )

    bug_description = st.text_area(
        "Bug 描述",
        height=130,
    )

    bug_steps = st.text_area(
        "复现步骤",
        height=150,
    )

with bug_col2:

    bug_expected = st.text_area(
        "预期结果",
        height=100,
    )

    bug_actual = st.text_area(
        "实际结果",
        height=100,
    )

    bug_environment = st.text_area(
        "测试环境",
        height=100,
        placeholder=(
            "例如：Android 14 / 测试环境 / "
            "APP 版本 1.2.0"
        ),
    )


if st.button(
    "🤖 AI 分析 Bug",
    width="stretch",
):

    if not (
        bug_title.strip()
        or bug_description.strip()
    ):

        st.warning(
            "请至少填写 Bug 标题或 Bug 描述"
        )

    else:

        try:

            with st.spinner(
                "AI 正在分析 Bug..."
            ):

                prompt = (
                    build_bug_analysis_prompt(
                        bug_title,
                        bug_description,
                        bug_steps,
                        bug_expected,
                        bug_actual,
                        bug_environment,
                    )
                )

                bug_content = invoke_model(
                    prompt
                )

                bug_analysis = (
                    parse_json_dict(
                        bug_content
                    )
                )

                if not bug_analysis:

                    raise ValueError(
                        "Bug 分析结果无法解析"
                    )

                st.session_state[
                    "bug_analysis"
                ] = bug_analysis

            st.success(
                "Bug 分析完成"
            )

        except Exception as e:

            st.error(
                f"Bug 分析失败：{e}"
            )


if st.session_state.bug_analysis:

    analysis = (
        st.session_state.bug_analysis
    )

    bug_metric1, bug_metric2, bug_metric3 = (
        st.columns(3)
    )

    bug_metric1.metric(
        "严重程度",
        analysis.get(
            "severity",
            "-",
        ),
    )

    bug_metric2.metric(
        "优先级",
        analysis.get(
            "priority",
            "-",
        ),
    )

    bug_metric3.metric(
        "Bug 类型",
        analysis.get(
            "bug_type",
            "-",
        ),
    )

    with st.expander(
        "查看完整 Bug 分析",
        expanded=True,
    ):

        st.json(
            analysis
        )

    if st.button(
        "💾 保存到历史 Bug 知识库",
        width="stretch",
    ):

        if not bug_title.strip():

            st.warning(
                "保存前请填写 Bug 标题"
            )

        else:

            try:

                os.makedirs(
                    KNOWLEDGE_DIR,
                    exist_ok=True,
                )

                root_causes = analysis.get(
                    "root_causes",
                    [],
                )

                regression_points = (
                    analysis.get(
                        "regression_points",
                        [],
                    )
                )

                knowledge_summary = (
                    analysis.get(
                        "knowledge_summary",
                        "",
                    )
                )

                record = (
                    "\n\n"
                    "====================================\n"
                    f"Bug标题：{bug_title}\n"
                    f"Bug描述：{bug_description}\n"
                    f"复现步骤：{bug_steps}\n"
                    f"预期结果：{bug_expected}\n"
                    f"实际结果：{bug_actual}\n"
                    f"测试环境：{bug_environment}\n"
                    f"严重程度：{analysis.get('severity', '')}\n"
                    f"优先级：{analysis.get('priority', '')}\n"
                    f"Bug类型：{analysis.get('bug_type', '')}\n"
                    f"所属模块：{analysis.get('module', '')}\n"
                    f"可能原因：{json.dumps(root_causes, ensure_ascii=False)}\n"
                    f"回归测试点：{json.dumps(regression_points, ensure_ascii=False)}\n"
                    f"知识摘要：{knowledge_summary}\n"
                    "====================================\n"
                )

                with open(
                    HISTORY_BUG_FILE,
                    "a",
                    encoding="utf-8",
                ) as file:

                    file.write(record)

                with st.spinner(
                    "正在重新构建 RAG..."
                ):

                    rebuild_vector_db()

                st.success(
                    "Bug 已保存到历史知识库，并完成 RAG 重建"
                )

            except Exception as e:

                st.error(
                    f"Bug 保存失败：{e}"
                )
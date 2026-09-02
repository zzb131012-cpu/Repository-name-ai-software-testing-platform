def build_review_prompt(
    requirement,
    rag_context
):
    return f"""
你是一名资深软件测试工程师。

请严格根据当前需求进行需求评审。

规则：

1. 当前需求是唯一业务依据。
2. 历史测试资料只作为经验参考。
3. 不允许自行创造需求规则。
4. 未说明内容必须标记【需求待确认】。

输出：

## 一、需求理解
## 二、已明确需求规则
## 三、需求风险
## 四、需求待确认
## 五、测试建议

当前需求：

{requirement}

历史测试参考：

{rag_context}
"""


def build_test_point_prompt(
    requirement,
    review_content,
    rag_context
):
    return f"""
你是一名专业软件测试工程师。

根据需求和需求评审分析完整测试点。

必须覆盖：

1. 正常场景
2. 异常场景
3. 边界值
4. 业务规则
5. 数据校验
6. 状态流转
7. 权限与安全
8. 兼容性
9. 历史缺陷回归
10. 需求待确认

要求：

不得创造需求中没有的业务规则。

需求：

{requirement}

需求评审：

{review_content}

测试经验：

{rag_context}
"""


def build_test_case_prompt(
    requirement,
    review_content,
    analysis_content,
    rag_context
):
    return f"""
你是一名专业软件测试工程师。

根据需求、需求评审、测试点和历史测试经验
生成完整测试用例。

字段必须包含：

case_id
module
title
precondition
steps
test_data
expected_result
priority

priority 只能：

P0
P1
P2

要求：

1. 覆盖正常场景。
2. 覆盖异常场景。
3. 覆盖边界场景。
4. 覆盖核心业务规则。
5. 历史 Bug 只作为回归经验。
6. 不允许创造需求中不存在的规则。
7. 未明确内容标记【需求待确认】。
8. 避免重复测试用例。
9. 只输出合法 JSON 数组。
10. 不输出 Markdown。

需求：

{requirement}

需求评审：

{review_content}

测试点：

{analysis_content}

历史测试经验：

{rag_context}
"""


def build_add_missing_prompt(
    requirement,
    analysis_content,
    rag_context,
    current_cases_json
):
    return f"""
你是一名高级软件测试工程师。

检查现有测试用例是否存在遗漏。

要求：

1. 保留已有有效用例。
2. 只补充真正遗漏的场景。
3. 不生成重复用例。
4. 不创造需求规则。
5. 返回原用例 + 新增用例的完整 JSON 数组。

字段：

case_id
module
title
precondition
steps
test_data
expected_result
priority

需求：

{requirement}

测试点：

{analysis_content}

历史测试经验：

{rag_context}

现有用例：

{current_cases_json}
"""


def build_remove_duplicate_prompt(
    current_cases_json
):
    return f"""
你是一名高级软件测试工程师。

删除下面测试用例中的重复或高度重复场景。

要求：

1. 不删除具有独立测试价值的用例。
2. 保留边界和异常测试。
3. 不创造新的需求规则。
4. 返回完整 JSON 数组。
5. 不输出 Markdown。

测试用例：

{current_cases_json}
"""


def build_optimize_all_prompt(
    requirement,
    analysis_content,
    rag_context,
    current_cases_json
):
    return f"""
你是一名高级软件测试工程师。

全面优化当前测试用例。

目标：

1. 删除重复用例。
2. 补充遗漏测试场景。
3. 优化标题。
4. 优化前置条件。
5. 优化步骤。
6. 优化测试数据。
7. 优化预期结果。
8. 调整不合理优先级。
9. 不创造需求中不存在的规则。

字段：

case_id
module
title
precondition
steps
test_data
expected_result
priority

只输出 JSON 数组。

需求：

{requirement}

测试点：

{analysis_content}

历史经验：

{rag_context}

当前用例：

{current_cases_json}
"""


def build_quality_prompt(
    requirement,
    analysis_content,
    current_cases_json
):
    return f"""
你是一名高级软件测试负责人。

严格评估当前测试用例质量。

返回合法 JSON 对象：

{{
  "overall_score": 0,
  "requirement_coverage": 0,
  "normal_coverage": 0,
  "exception_coverage": 0,
  "boundary_coverage": 0,
  "business_rule_coverage": 0,
  "executability": 0,
  "non_duplicate_score": 0,
  "strengths": [],
  "missing_scenarios": [],
  "duplicate_risks": [],
  "high_risk_gaps": [],
  "improvement_suggestions": [],
  "summary": ""
}}

所有评分范围 0-100。

不得创造需求中不存在的规则。

需求：

{requirement}

测试点：

{analysis_content}

测试用例：

{current_cases_json}
"""


def build_requirement_split_prompt(
    requirement
):
    return f"""
你是一名软件测试需求分析工程师。

把原始需求拆分成最小可验证需求条目。

字段：

requirement_id
requirement
requirement_type

编号从 R001 开始。

不得创造需求中不存在的规则。

只输出 JSON 数组。

需求：

{requirement}
"""


def build_rtm_prompt(
    requirement_items_json,
    current_cases_json
):
    return f"""
你是一名高级软件测试工程师。

建立需求追踪矩阵。

字段：

requirement_id
requirement
requirement_type
covered_cases
coverage_status
note

coverage_status 只能：

已覆盖
部分覆盖
未覆盖

规则：

1. 不强行建立需求与用例映射。
2. covered_cases 只能使用已有测试用例编号。
3. 没有覆盖返回空数组。
4. 每条需求必须返回。
5. 不允许新增需求。
6. 只输出 JSON 数组。

需求：

{requirement_items_json}

测试用例：

{current_cases_json}
"""


def build_bug_analysis_prompt(
    bug_title,
    bug_description,
    bug_steps,
    bug_expected,
    bug_actual,
    bug_environment
):
    return f"""
你是一名高级软件测试工程师。

分析下面的 Bug。

注意：

1. 不要声称已经确认真实代码根因。
2. root_causes 只能表示可能原因。
3. 给出实际可执行的定位建议。
4. 分析测试遗漏。
5. 给出回归测试点。
6. knowledge_summary 需要适合保存到历史 Bug 知识库。

只输出合法 JSON：

{{
  "severity": "S1/S2/S3/S4",
  "priority": "P0/P1/P2",
  "bug_type": "功能/接口/数据/兼容性/性能/安全/UI/其他",
  "module": "",
  "impact": "",
  "root_causes": [],
  "localization_steps": [],
  "test_gaps": [],
  "regression_points": [],
  "knowledge_summary": ""
}}

Bug标题：

{bug_title}

Bug描述：

{bug_description}

复现步骤：

{bug_steps}

预期结果：

{bug_expected}

实际结果：

{bug_actual}

环境：

{bug_environment}
"""
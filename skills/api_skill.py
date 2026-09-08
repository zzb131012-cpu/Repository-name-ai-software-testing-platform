import json

from skills.boundary_skill import (
    build_boundary_prompt_context,
)

from skills.equivalence_skill import (
    build_equivalence_prompt_context,
)


def safe_text(value):
    """
    安全转换字符串。
    """

    if value is None:
        return ""

    return str(value).strip()


def build_http_method_rules(
    request_method
):
    """
    生成 HTTP Method 测试规则。
    """

    request_method = safe_text(
        request_method
    ).upper()

    methods = [
        "GET",
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
    ]

    rules = []

    if request_method:

        rules.append(
            {
                "category":
                    "HTTP Method",

                "scenario":
                    f"使用正确请求方式 {request_method}",

                "expected":
                    "按业务规则正常处理",
            }
        )

        for method in methods:

            if method == request_method:
                continue

            rules.append(
                {
                    "category":
                        "HTTP Method",

                    "scenario":
                        f"使用错误请求方式 {method}",

                    "expected":
                        "应拒绝请求或返回明确错误",
                }
            )

    return rules


def build_content_type_rules(
    headers_text
):
    """
    Content-Type 测试规则。
    """

    rules = []

    text = safe_text(
        headers_text
    ).lower()

    if "application/json" in text:

        rules.extend(
            [
                {
                    "category":
                        "Headers",

                    "scenario":
                        "Content-Type 为 application/json",

                    "expected":
                        "正常处理 JSON 请求",
                },
                {
                    "category":
                        "Headers",

                    "scenario":
                        "缺失 Content-Type",

                    "expected":
                        "应按接口规范处理或返回明确错误",
                },
                {
                    "category":
                        "Headers",

                    "scenario":
                        "Content-Type 为 text/plain",

                    "expected":
                        "应拒绝错误媒体类型",
                },
                {
                    "category":
                        "Headers",

                    "scenario":
                        "Content-Type 为 application/xml",

                    "expected":
                        "应拒绝非支持格式",
                },
            ]
        )

    return rules


def build_body_rules(
    request_method
):
    """
    请求体异常测试。
    """

    request_method = safe_text(
        request_method
    ).upper()

    rules = []

    if request_method in {
        "POST",
        "PUT",
        "PATCH",
    }:

        rules.extend(
            [
                {
                    "category":
                        "Request Body",

                    "scenario":
                        "请求体为空",

                    "expected":
                        "应根据必填规则返回明确结果",
                },
                {
                    "category":
                        "Request Body",

                    "scenario":
                        "请求体为非法 JSON",

                    "expected":
                        "应拒绝请求并返回格式错误",
                },
                {
                    "category":
                        "Request Body",

                    "scenario":
                        "请求体为 JSON 数组而不是对象",

                    "expected":
                        "应拒绝错误数据类型",
                },
                {
                    "category":
                        "Request Body",

                    "scenario":
                        "请求体增加未定义字段",

                    "expected":
                        "【需求待确认：忽略额外字段或返回错误】",
                },
            ]
        )

    return rules


def build_response_rules():
    """
    通用响应校验规则。
    """

    return [
        {
            "category":
                "Response",

            "scenario":
                "校验 HTTP 状态码",

            "expected":
                "状态码符合接口规范",
        },
        {
            "category":
                "Response",

            "scenario":
                "校验业务 code",

            "expected":
                "业务状态码与场景一致",
        },
        {
            "category":
                "Response",

            "scenario":
                "校验 message",

            "expected":
                "提示信息与业务结果一致",
        },
        {
            "category":
                "Response",

            "scenario":
                "校验响应字段类型",

            "expected":
                "字段类型符合接口契约",
        },
        {
            "category":
                "Response",

            "scenario":
                "校验必返回字段",

            "expected":
                "必填响应字段不能缺失",
        },
    ]


def build_exception_rules():
    """
    通用异常场景。
    """

    return [
        {
            "category":
                "Exception",

            "scenario":
                "请求超时",

            "expected":
                "客户端应得到明确超时结果",
        },
        {
            "category":
                "Exception",

            "scenario":
                "服务内部异常",

            "expected":
                "应返回合理的服务异常响应",
        },
        {
            "category":
                "Exception",

            "scenario":
                "网络中断",

            "expected":
                "请求失败时不应产生错误业务状态",
        },
        {
            "category":
                "Exception",

            "scenario":
                "重复提交",

            "expected":
                "【需求待确认：接口是否需要幂等控制】",
        },
    ]


def build_security_rules():
    """
    通用安全测试规则。

    注意：
    这里只生成风险测试建议，
    不把需求中没有定义的安全机制当成确定业务规则。
    """

    return [
        {
            "category":
                "Security",

            "scenario":
                "输入 SQL 特殊字符",

            "expected":
                "接口不应出现数据库异常或绕过校验",
        },
        {
            "category":
                "Security",

            "scenario":
                "输入脚本/特殊字符",

            "expected":
                "接口应安全处理异常字符",
        },
        {
            "category":
                "Security",

            "scenario":
                "敏感信息传输",

            "expected":
                "敏感字段不应通过明文非加密通道泄露",
        },
        {
            "category":
                "Security",

            "scenario":
                "高频请求",

            "expected":
                "【需求待确认：是否存在限流或风控机制】",
        },
    ]


def build_field_skill_context(
    field_name,
    rule_text
):
    """
    组合字段级 Skill：
    边界值 + 等价类。
    """

    sections = []

    boundary_context = (
        build_boundary_prompt_context(
            field_name,
            rule_text,
        )
    )

    if boundary_context:

        sections.append(
            "【边界值 Skill】\n"
            + boundary_context
        )

    equivalence_context = (
        build_equivalence_prompt_context(
            field_name,
            rule_text,
        )
    )

    if equivalence_context:

        sections.append(
            "【等价类 Skill】\n"
            + equivalence_context
        )

    return "\n\n".join(
        sections
    )


def build_api_generic_rules(
    request_method,
    headers_text
):
    """
    生成接口级通用测试规则。
    """

    rules = []

    rules.extend(
        build_http_method_rules(
            request_method
        )
    )

    rules.extend(
        build_content_type_rules(
            headers_text
        )
    )

    rules.extend(
        build_body_rules(
            request_method
        )
    )

    rules.extend(
        build_response_rules()
    )

    rules.extend(
        build_exception_rules()
    )

    rules.extend(
        build_security_rules()
    )

    return rules


def rules_to_prompt_text(
    rules
):
    """
    将规则列表转成 Prompt 文本。
    """

    lines = []

    for index, item in enumerate(
        rules,
        start=1
    ):

        lines.append(
            f"{index}. "
            f"[{item.get('category', '')}] "
            f"{item.get('scenario', '')} "
            f"→ {item.get('expected', '')}"
        )

    return "\n".join(
        lines
    )


def build_api_skill_context(
    request_method,
    headers_text,
    field_rules=None
):
    """
    构建完整接口 Skill Prompt Context。

    field_rules 示例：

    [
        {
            "field": "phone",
            "rule": "必填，11位数字，以1开头"
        },
        {
            "field": "password",
            "rule": "必填，长度6~20位"
        }
    ]
    """

    if field_rules is None:
        field_rules = []

    sections = []

    # =============================================
    # 1. 字段 Skill
    # =============================================

    field_sections = []

    for item in field_rules:

        if not isinstance(
            item,
            dict
        ):
            continue

        field_name = safe_text(
            item.get(
                "field"
            )
        )

        rule_text = safe_text(
            item.get(
                "rule"
            )
        )

        if not field_name:
            continue

        field_context = (
            build_field_skill_context(
                field_name,
                rule_text,
            )
        )

        if field_context:

            field_sections.append(
                field_context
            )

    if field_sections:

        sections.append(
            "===== 字段测试 Skill =====\n\n"
            + "\n\n".join(
                field_sections
            )
        )

    # =============================================
    # 2. 接口通用 Skill
    # =============================================

    generic_rules = (
        build_api_generic_rules(
            request_method,
            headers_text,
        )
    )

    generic_text = (
        rules_to_prompt_text(
            generic_rules
        )
    )

    if generic_text:

        sections.append(
            "===== 接口通用测试 Skill =====\n"
            + generic_text
        )

    # =============================================
    # 3. 强约束
    # =============================================

    sections.append(
        """
===== Skill 使用原则 =====

1. Skill 是测试设计辅助规则，不是业务需求本身。
2. 当前需求明确规定的业务规则优先级最高。
3. Skill 与需求冲突时，以当前需求为准。
4. 需求未定义的预期结果不得自行编造。
5. 对需求未明确的场景，标记【需求待确认】。
6. 相同测试点需要去重。
7. 边界值和等价类要优先覆盖高风险输入字段。
8. 不允许为接口不存在的请求字段凭空生成确定性用例。
""".strip()
    )

    return "\n\n".join(
        sections
    )


def build_api_skill_json(
    request_method,
    headers_text,
    field_rules=None
):
    """
    返回结构化 Skill 数据，
    后续可以用于页面展示或评测。
    """

    if field_rules is None:
        field_rules = []

    return {
        "request_method":
            safe_text(
                request_method
            ).upper(),

        "field_rules":
            field_rules,

        "generic_rules":
            build_api_generic_rules(
                request_method,
                headers_text,
            ),
    }


def pretty_print_api_skill_json(
    request_method,
    headers_text,
    field_rules=None
):
    """
    调试使用。
    """

    data = build_api_skill_json(
        request_method,
        headers_text,
        field_rules,
    )

    return json.dumps(
        data,
        ensure_ascii=False,
        indent=2,
    )
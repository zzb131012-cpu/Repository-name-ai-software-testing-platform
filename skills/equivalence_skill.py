import re


def safe_text(value):
    """
    安全转换字符串。
    """

    if value is None:
        return ""

    return str(value).strip()


def contains_any(
    text,
    keywords
):
    """
    判断文本中是否包含任意关键词。
    """

    text = safe_text(text).lower()

    return any(
        keyword.lower() in text
        for keyword in keywords
    )


def detect_required(rule_text):
    """
    判断字段是否必填。

    支持：
    必填
    不能为空
    必须填写
    required
    """

    return contains_any(
        rule_text,
        [
            "必填",
            "不能为空",
            "不可为空",
            "必须填写",
            "required",
        ]
    )


def detect_numeric(rule_text):
    """
    判断是否要求数字类型。
    """

    return contains_any(
        rule_text,
        [
            "数字",
            "整数",
            "numeric",
            "number",
            "int",
        ]
    )


def detect_phone(rule_text):
    """
    判断是否是手机号规则。
    """

    return contains_any(
        rule_text,
        [
            "手机号",
            "手机号码",
            "phone",
            "mobile",
        ]
    )


def detect_email(rule_text):
    """
    判断是否是邮箱规则。
    """

    return contains_any(
        rule_text,
        [
            "邮箱",
            "email",
            "电子邮箱",
        ]
    )


def detect_url(rule_text):
    """
    判断是否是 URL。
    """

    return contains_any(
        rule_text,
        [
            "url",
            "链接",
            "网址",
        ]
    )


def detect_fixed_length(
    rule_text
):
    """
    提取固定长度。
    """

    text = safe_text(
        rule_text
    )

    patterns = [
        r"(\d+)\s*位数字",
        r"长度为?\s*(\d+)\s*位",
        r"必须为\s*(\d+)\s*位",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text
        )

        if match:

            return int(
                match.group(1)
            )

    return None


def build_common_invalid_classes(
    required=False
):
    """
    通用无效等价类。
    """

    invalid_classes = []

    if required:

        invalid_classes.extend(
            [
                {
                    "name": "字段缺失",
                    "value": "__MISSING__",
                    "expected": "无效",
                },
                {
                    "name": "空字符串",
                    "value": "",
                    "expected": "无效",
                },
                {
                    "name": "null",
                    "value": None,
                    "expected": "无效",
                },
            ]
        )

    return invalid_classes


def build_phone_equivalence_classes(
    required=True
):
    """
    手机号等价类。
    """

    valid_classes = [
        {
            "name": "合法手机号",
            "value": "13800138000",
            "expected": "有效",
        }
    ]

    invalid_classes = (
        build_common_invalid_classes(
            required
        )
    )

    invalid_classes.extend(
        [
            {
                "name": "长度不足",
                "value": "1380013800",
                "expected": "无效",
            },
            {
                "name": "长度超出",
                "value": "138001380001",
                "expected": "无效",
            },
            {
                "name": "包含字母",
                "value": "1380013800a",
                "expected": "无效",
            },
            {
                "name": "包含特殊字符",
                "value": "1380013800@",
                "expected": "无效",
            },
            {
                "name": "不是1开头",
                "value": "23800138000",
                "expected": "无效",
            },
            {
                "name": "全角数字",
                "value": "１３８００１３８０００",
                "expected": "无效",
            },
            {
                "name": "布尔类型",
                "value": True,
                "expected": "无效",
            },
            {
                "name": "数组类型",
                "value": [],
                "expected": "无效",
            },
            {
                "name": "对象类型",
                "value": {},
                "expected": "无效",
            },
        ]
    )

    return {
        "valid_classes": valid_classes,
        "invalid_classes": invalid_classes,
    }


def build_numeric_equivalence_classes(
    required=False
):
    """
    数字字段等价类。
    """

    valid_classes = [
        {
            "name": "合法数字",
            "value": 1,
            "expected": "有效",
        }
    ]

    invalid_classes = (
        build_common_invalid_classes(
            required
        )
    )

    invalid_classes.extend(
        [
            {
                "name": "字母字符串",
                "value": "abc",
                "expected": "无效",
            },
            {
                "name": "特殊字符",
                "value": "@#$",
                "expected": "无效",
            },
            {
                "name": "对象类型",
                "value": {},
                "expected": "无效",
            },
            {
                "name": "数组类型",
                "value": [],
                "expected": "无效",
            },
        ]
    )

    return {
        "valid_classes": valid_classes,
        "invalid_classes": invalid_classes,
    }


def build_string_equivalence_classes(
    required=False
):
    """
    普通字符串字段等价类。
    """

    valid_classes = [
        {
            "name": "正常字符串",
            "value": "test",
            "expected": "有效",
        }
    ]

    invalid_classes = (
        build_common_invalid_classes(
            required
        )
    )

    invalid_classes.extend(
        [
            {
                "name": "数组类型",
                "value": [],
                "expected": "无效",
            },
            {
                "name": "对象类型",
                "value": {},
                "expected": "无效",
            },
        ]
    )

    return {
        "valid_classes": valid_classes,
        "invalid_classes": invalid_classes,
    }


def build_email_equivalence_classes(
    required=False
):
    """
    邮箱等价类。
    """

    valid_classes = [
        {
            "name": "合法邮箱",
            "value": "test@example.com",
            "expected": "有效",
        }
    ]

    invalid_classes = (
        build_common_invalid_classes(
            required
        )
    )

    invalid_classes.extend(
        [
            {
                "name": "缺少@",
                "value": "testexample.com",
                "expected": "无效",
            },
            {
                "name": "缺少域名",
                "value": "test@",
                "expected": "无效",
            },
            {
                "name": "缺少用户名",
                "value": "@example.com",
                "expected": "无效",
            },
            {
                "name": "格式错误",
                "value": "test@@example.com",
                "expected": "无效",
            },
        ]
    )

    return {
        "valid_classes": valid_classes,
        "invalid_classes": invalid_classes,
    }


def build_url_equivalence_classes(
    required=False
):
    """
    URL 等价类。
    """

    valid_classes = [
        {
            "name": "合法HTTPS地址",
            "value": "https://example.com",
            "expected": "有效",
        }
    ]

    invalid_classes = (
        build_common_invalid_classes(
            required
        )
    )

    invalid_classes.extend(
        [
            {
                "name": "缺少协议",
                "value": "example.com",
                "expected": "无效",
            },
            {
                "name": "非法协议",
                "value": "abc://example.com",
                "expected": "无效",
            },
            {
                "name": "普通字符串",
                "value": "test",
                "expected": "无效",
            },
        ]
    )

    return {
        "valid_classes": valid_classes,
        "invalid_classes": invalid_classes,
    }


def analyze_equivalence_classes(
    field_name,
    rule_text
):
    """
    根据字段名称和规则分析等价类。

    返回：
    {
        field,
        rule,
        valid_classes,
        invalid_classes
    }
    """

    field_name = safe_text(
        field_name
    )

    rule_text = safe_text(
        rule_text
    )

    combined_text = (
        f"{field_name} {rule_text}"
    )

    required = detect_required(
        rule_text
    )

    if detect_phone(
        combined_text
    ):

        result = (
            build_phone_equivalence_classes(
                required=True
            )
        )

    elif detect_email(
        combined_text
    ):

        result = (
            build_email_equivalence_classes(
                required=required
            )
        )

    elif detect_url(
        combined_text
    ):

        result = (
            build_url_equivalence_classes(
                required=required
            )
        )

    elif detect_numeric(
        rule_text
    ):

        result = (
            build_numeric_equivalence_classes(
                required=required
            )
        )

    else:

        result = (
            build_string_equivalence_classes(
                required=required
            )
        )

    return {
        "field": field_name,
        "rule": rule_text,
        "valid_classes":
            result[
                "valid_classes"
            ],
        "invalid_classes":
            result[
                "invalid_classes"
            ],
    }


def build_equivalence_prompt_context(
    field_name,
    rule_text
):
    """
    将等价类转换为 Prompt 文本。
    """

    result = (
        analyze_equivalence_classes(
            field_name,
            rule_text
        )
    )

    lines = [
        f"字段：{result['field']}",
        f"规则：{result['rule']}",
        "",
        "有效等价类：",
    ]

    for item in result[
        "valid_classes"
    ]:

        lines.append(
            f"- {item['name']}："
            f"{repr(item['value'])}，"
            f"预期：{item['expected']}"
        )

    lines.append(
        ""
    )

    lines.append(
        "无效等价类："
    )

    for item in result[
        "invalid_classes"
    ]:

        lines.append(
            f"- {item['name']}："
            f"{repr(item['value'])}，"
            f"预期：{item['expected']}"
        )

    return "\n".join(
        lines
    )
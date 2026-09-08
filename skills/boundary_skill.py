import re


def safe_text(value):
    """
    安全转换字符串。
    """

    if value is None:
        return ""

    return str(value).strip()


def build_length_boundary_values(
    min_length=None,
    max_length=None
):
    """
    根据最小长度、最大长度生成边界值。

    例如：
    min=6
    max=20

    返回：
    5,6,7,19,20,21
    """

    values = []

    if min_length is not None:

        try:
            min_length = int(
                min_length
            )

            if min_length > 0:
                values.extend(
                    [
                        min_length - 1,
                        min_length,
                        min_length + 1,
                    ]
                )

        except Exception:
            pass

    if max_length is not None:

        try:
            max_length = int(
                max_length
            )

            if max_length > 0:
                values.extend(
                    [
                        max_length - 1,
                        max_length,
                        max_length + 1,
                    ]
                )

        except Exception:
            pass

    # 去重并排序
    values = sorted(
        set(
            value
            for value in values
            if value >= 0
        )
    )

    return values


def build_numeric_boundary_values(
    min_value=None,
    max_value=None
):
    """
    数值边界值。

    例如：
    min=1
    max=100

    返回：
    0,1,2,99,100,101
    """

    values = []

    if min_value is not None:

        try:
            min_value = float(
                min_value
            )

            values.extend(
                [
                    min_value - 1,
                    min_value,
                    min_value + 1,
                ]
            )

        except Exception:
            pass

    if max_value is not None:

        try:
            max_value = float(
                max_value
            )

            values.extend(
                [
                    max_value - 1,
                    max_value,
                    max_value + 1,
                ]
            )

        except Exception:
            pass

    # 去重
    unique_values = []

    for value in values:

        if value not in unique_values:
            unique_values.append(
                value
            )

    return unique_values


def extract_length_range(text):
    """
    从自然语言中提取长度范围。

    支持：
    长度6~20位
    长度6-20位
    6~20位
    6至20位
    6到20位

    返回：
    {
        "min_length": 6,
        "max_length": 20
    }
    """

    text = safe_text(
        text
    )

    patterns = [
        r"(\d+)\s*[~～\-]\s*(\d+)\s*位",
        r"(\d+)\s*至\s*(\d+)\s*位",
        r"(\d+)\s*到\s*(\d+)\s*位",
        r"长度\s*(\d+)\s*[~～\-]\s*(\d+)",
        r"长度\s*(\d+)\s*至\s*(\d+)",
        r"长度\s*(\d+)\s*到\s*(\d+)",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text
        )

        if match:

            return {
                "min_length": int(
                    match.group(1)
                ),
                "max_length": int(
                    match.group(2)
                ),
            }

    return None


def extract_fixed_length(text):
    """
    提取固定长度。

    例如：
    11位数字
    长度为11位

    返回：
    11
    """

    text = safe_text(
        text
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


def build_fixed_length_boundaries(
    length
):
    """
    固定长度边界。

    11位：
    10,11,12
    """

    try:
        length = int(
            length
        )

    except Exception:
        return []

    values = [
        max(
            0,
            length - 1
        ),
        length,
        length + 1,
    ]

    return sorted(
        set(values)
    )


def analyze_boundary_rules(
    field_name,
    rule_text
):
    """
    对单个字段规则进行边界分析。

    示例：

    field_name = password
    rule_text = 长度6~20位

    输出结构化测试规则。
    """

    field_name = safe_text(
        field_name
    )

    rule_text = safe_text(
        rule_text
    )

    result = {
        "field": field_name,
        "rule": rule_text,
        "boundary_type": "",
        "boundary_values": [],
        "test_points": [],
    }

    # =============================================
    # 长度区间
    # =============================================

    length_range = extract_length_range(
        rule_text
    )

    if length_range:

        min_length = (
            length_range[
                "min_length"
            ]
        )

        max_length = (
            length_range[
                "max_length"
            ]
        )

        values = (
            build_length_boundary_values(
                min_length,
                max_length,
            )
        )

        result[
            "boundary_type"
        ] = "length_range"

        result[
            "boundary_values"
        ] = values

        result[
            "test_points"
        ] = [
            {
                "value":
                    min_length - 1,

                "type":
                    "下边界外",

                "expected":
                    "无效",
            },

            {
                "value":
                    min_length,

                "type":
                    "下边界",

                "expected":
                    "有效",
            },

            {
                "value":
                    min_length + 1,

                "type":
                    "下边界内",

                "expected":
                    "有效",
            },

            {
                "value":
                    max_length - 1,

                "type":
                    "上边界内",

                "expected":
                    "有效",
            },

            {
                "value":
                    max_length,

                "type":
                    "上边界",

                "expected":
                    "有效",
            },

            {
                "value":
                    max_length + 1,

                "type":
                    "上边界外",

                "expected":
                    "无效",
            },
        ]

        return result

    # =============================================
    # 固定长度
    # =============================================

    fixed_length = extract_fixed_length(
        rule_text
    )

    if fixed_length is not None:

        values = (
            build_fixed_length_boundaries(
                fixed_length
            )
        )

        result[
            "boundary_type"
        ] = "fixed_length"

        result[
            "boundary_values"
        ] = values

        result[
            "test_points"
        ] = [
            {
                "value":
                    max(
                        0,
                        fixed_length - 1
                    ),

                "type":
                    "边界外-少1位",

                "expected":
                    "无效",
            },

            {
                "value":
                    fixed_length,

                "type":
                    "有效边界",

                "expected":
                    "有效",
            },

            {
                "value":
                    fixed_length + 1,

                "type":
                    "边界外-多1位",

                "expected":
                    "无效",
            },
        ]

        return result

    return result


def build_boundary_prompt_context(
    field_name,
    rule_text
):
    """
    生成可直接放进 Prompt 的边界规则文本。
    """

    result = analyze_boundary_rules(
        field_name,
        rule_text
    )

    if not result[
        "boundary_type"
    ]:

        return ""

    lines = [
        f"字段：{result['field']}",
        f"规则：{result['rule']}",
        "边界值测试要求：",
    ]

    for item in result[
        "test_points"
    ]:

        lines.append(
            f"- {item['type']}："
            f"{item['value']}，"
            f"预期：{item['expected']}"
        )

    return "\n".join(
        lines
    )
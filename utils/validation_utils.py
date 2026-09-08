from collections import Counter


VALID_PRIORITIES = {
    "P0",
    "P1",
    "P2",
}

VALID_HTTP_METHODS = {
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "HEAD",
    "OPTIONS",
}


# =========================================================
# 1. 通用文本处理
# =========================================================

def safe_text(value):
    """
    将字段安全转换成字符串。
    """

    if value is None:
        return ""

    return str(value).strip()


def normalize_priority(value):
    """
    优先级标准化。

    P0 / p0 / P0空格 -> P0

    不合法时不强制改成 P2，
    返回空字符串，由校验报告记录问题。
    """

    value = safe_text(value).upper()

    if value in VALID_PRIORITIES:
        return value

    return ""


def normalize_http_method(value):
    """
    HTTP Method 标准化。
    """

    value = safe_text(value).upper()

    if value in VALID_HTTP_METHODS:
        return value

    return value


# =========================================================
# 2. 功能测试用例规范化
# =========================================================

def normalize_functional_case(case):
    """
    规范单条功能测试用例字段。
    """

    normalized = dict(case)

    normalized["case_id"] = safe_text(
        case.get("case_id")
    )

    normalized["module"] = safe_text(
        case.get("module")
    )

    normalized["title"] = safe_text(
        case.get("title")
    )

    normalized["precondition"] = safe_text(
        case.get("precondition")
    )

    normalized["steps"] = safe_text(
        case.get("steps")
    )

    normalized["test_data"] = safe_text(
        case.get("test_data")
    )

    normalized["expected_result"] = safe_text(
        case.get("expected_result")
    )

    normalized["priority"] = (
        normalize_priority(
            case.get("priority")
        )
    )

    return normalized


def normalize_functional_cases(cases):
    """
    批量规范功能测试用例。
    """

    result = []

    for case in cases:

        if not isinstance(case, dict):
            continue

        result.append(
            normalize_functional_case(
                case
            )
        )

    return result


# =========================================================
# 3. 接口测试用例规范化
# =========================================================

def normalize_api_case(case):
    """
    规范单条接口测试用例。
    """

    normalized = dict(case)

    normalized["case_id"] = safe_text(
        case.get("case_id")
    )

    normalized["module"] = safe_text(
        case.get("module")
    )

    normalized["title"] = safe_text(
        case.get("title")
    )

    normalized["method"] = (
        normalize_http_method(
            case.get("method")
        )
    )

    normalized["url"] = safe_text(
        case.get("url")
    )

    normalized["headers"] = safe_text(
        case.get("headers")
    )

    normalized["request_data"] = safe_text(
        case.get("request_data")
    )

    normalized["expected_http_status"] = (
        safe_text(
            case.get(
                "expected_http_status"
            )
        )
    )

    normalized["expected_business_result"] = (
        safe_text(
            case.get(
                "expected_business_result"
            )
        )
    )

    normalized["priority"] = (
        normalize_priority(
            case.get("priority")
        )
    )

    return normalized


def normalize_api_cases(cases):
    """
    批量规范接口测试用例。
    """

    result = []

    for case in cases:

        if not isinstance(case, dict):
            continue

        result.append(
            normalize_api_case(
                case
            )
        )

    return result


# =========================================================
# 4. 重复检查
# =========================================================

def find_duplicate_values(
    values
):
    """
    返回重复出现的非空值。
    """

    cleaned = [
        safe_text(value)
        for value in values
        if safe_text(value)
    ]

    counter = Counter(
        cleaned
    )

    return [
        value
        for value, count
        in counter.items()
        if count > 1
    ]


# =========================================================
# 5. 功能用例校验
# =========================================================

def validate_functional_cases(cases):
    """
    校验功能测试用例。

    返回：
    {
        total,
        valid,
        invalid,
        error_count,
        warning_count,
        issues
    }
    """

    issues = []

    if not isinstance(cases, list):

        return {
            "total": 0,
            "valid": 0,
            "invalid": 0,
            "error_count": 1,
            "warning_count": 0,
            "issues": [
                {
                    "case_id": "",
                    "level": "ERROR",
                    "field": "root",
                    "message":
                        "测试用例不是 JSON 数组",
                }
            ],
        }

    invalid_indexes = set()

    for index, case in enumerate(
        cases,
        start=1
    ):

        case_id = safe_text(
            case.get("case_id")
            if isinstance(case, dict)
            else ""
        )

        display_id = (
            case_id
            or f"第{index}条"
        )

        if not isinstance(
            case,
            dict
        ):

            issues.append(
                {
                    "case_id": display_id,
                    "level": "ERROR",
                    "field": "case",
                    "message":
                        "测试用例不是对象类型",
                }
            )

            invalid_indexes.add(
                index
            )

            continue

        required_fields = {
            "case_id":
                "用例编号为空",

            "module":
                "测试模块为空",

            "title":
                "测试标题为空",

            "steps":
                "操作步骤为空",

            "expected_result":
                "预期结果为空",

            "priority":
                "优先级为空或不合法",
        }

        for field, message in (
            required_fields.items()
        ):

            value = safe_text(
                case.get(field)
            )

            if (
                field == "priority"
                and normalize_priority(
                    value
                )
            ):
                continue

            if not value:

                issues.append(
                    {
                        "case_id":
                            display_id,

                        "level":
                            "ERROR",

                        "field":
                            field,

                        "message":
                            message,
                    }
                )

                invalid_indexes.add(
                    index
                )

        priority = safe_text(
            case.get("priority")
        ).upper()

        if (
            priority
            and priority
            not in VALID_PRIORITIES
        ):

            issues.append(
                {
                    "case_id":
                        display_id,

                    "level":
                        "ERROR",

                    "field":
                        "priority",

                    "message":
                        f"非法优先级：{priority}",
                }
            )

            invalid_indexes.add(
                index
            )

    duplicate_ids = (
        find_duplicate_values(
            [
                case.get(
                    "case_id",
                    ""
                )
                for case in cases
                if isinstance(
                    case,
                    dict
                )
            ]
        )
    )

    for value in duplicate_ids:

        issues.append(
            {
                "case_id": value,
                "level": "ERROR",
                "field": "case_id",
                "message":
                    f"用例编号重复：{value}",
            }
        )

    duplicate_titles = (
        find_duplicate_values(
            [
                case.get(
                    "title",
                    ""
                )
                for case in cases
                if isinstance(
                    case,
                    dict
                )
            ]
        )
    )

    for value in duplicate_titles:

        issues.append(
            {
                "case_id": "",
                "level": "WARNING",
                "field": "title",
                "message":
                    f"测试标题可能重复：{value}",
            }
        )

    error_count = sum(
        item["level"] == "ERROR"
        for item in issues
    )

    warning_count = sum(
        item["level"] == "WARNING"
        for item in issues
    )

    invalid = len(
        invalid_indexes
    )

    return {
        "total":
            len(cases),

        "valid":
            len(cases) - invalid,

        "invalid":
            invalid,

        "error_count":
            error_count,

        "warning_count":
            warning_count,

        "issues":
            issues,
    }


# =========================================================
# 6. 接口用例校验
# =========================================================

def validate_api_cases(cases):
    """
    校验接口测试用例。
    """

    issues = []

    if not isinstance(cases, list):

        return {
            "total": 0,
            "valid": 0,
            "invalid": 0,
            "error_count": 1,
            "warning_count": 0,
            "issues": [
                {
                    "case_id": "",
                    "level": "ERROR",
                    "field": "root",
                    "message":
                        "接口用例不是 JSON 数组",
                }
            ],
        }

    invalid_indexes = set()

    for index, case in enumerate(
        cases,
        start=1
    ):

        if not isinstance(
            case,
            dict
        ):

            issues.append(
                {
                    "case_id":
                        f"第{index}条",

                    "level":
                        "ERROR",

                    "field":
                        "case",

                    "message":
                        "接口用例不是对象类型",
                }
            )

            invalid_indexes.add(
                index
            )

            continue

        case_id = safe_text(
            case.get("case_id")
        )

        display_id = (
            case_id
            or f"第{index}条"
        )

        required_fields = {
            "case_id":
                "接口用例编号为空",

            "module":
                "测试模块为空",

            "title":
                "测试标题为空",

            "method":
                "请求方式为空",

            "url":
                "URL为空",

            "expected_http_status":
                "预期HTTP状态码为空",

            "expected_business_result":
                "预期业务结果为空",

            "priority":
                "优先级为空或不合法",
        }

        for field, message in (
            required_fields.items()
        ):

            value = safe_text(
                case.get(field)
            )

            if (
                field == "priority"
                and normalize_priority(
                    value
                )
            ):
                continue

            if not value:

                issues.append(
                    {
                        "case_id":
                            display_id,

                        "level":
                            "ERROR",

                        "field":
                            field,

                        "message":
                            message,
                    }
                )

                invalid_indexes.add(
                    index
                )

        method = safe_text(
            case.get("method")
        ).upper()

        if (
            method
            and method
            not in VALID_HTTP_METHODS
        ):

            issues.append(
                {
                    "case_id":
                        display_id,

                    "level":
                        "ERROR",

                    "field":
                        "method",

                    "message":
                        f"非法HTTP请求方式：{method}",
                }
            )

            invalid_indexes.add(
                index
            )

        priority = safe_text(
            case.get("priority")
        ).upper()

        if (
            priority
            and priority
            not in VALID_PRIORITIES
        ):

            issues.append(
                {
                    "case_id":
                        display_id,

                    "level":
                        "ERROR",

                    "field":
                        "priority",

                    "message":
                        f"非法优先级：{priority}",
                }
            )

            invalid_indexes.add(
                index
            )

        http_status = safe_text(
            case.get(
                "expected_http_status"
            )
        )

        if http_status:

            try:

                status_int = int(
                    http_status
                )

                if not (
                    100
                    <= status_int
                    <= 599
                ):

                    raise ValueError

            except Exception:

                issues.append(
                    {
                        "case_id":
                            display_id,

                        "level":
                            "WARNING",

                        "field":
                            "expected_http_status",

                        "message":
                            f"HTTP状态码格式可疑：{http_status}",
                    }
                )

    duplicate_ids = (
        find_duplicate_values(
            [
                case.get(
                    "case_id",
                    ""
                )
                for case in cases
                if isinstance(
                    case,
                    dict
                )
            ]
        )
    )

    for value in duplicate_ids:

        issues.append(
            {
                "case_id":
                    value,

                "level":
                    "ERROR",

                "field":
                    "case_id",

                "message":
                    f"接口用例编号重复：{value}",
            }
        )

    duplicate_titles = (
        find_duplicate_values(
            [
                case.get(
                    "title",
                    ""
                )
                for case in cases
                if isinstance(
                    case,
                    dict
                )
            ]
        )
    )

    for value in duplicate_titles:

        issues.append(
            {
                "case_id": "",
                "level": "WARNING",
                "field": "title",
                "message":
                    f"接口测试标题可能重复：{value}",
            }
        )

    error_count = sum(
        item["level"] == "ERROR"
        for item in issues
    )

    warning_count = sum(
        item["level"] == "WARNING"
        for item in issues
    )

    invalid = len(
        invalid_indexes
    )

    return {
        "total":
            len(cases),

        "valid":
            len(cases) - invalid,

        "invalid":
            invalid,

        "error_count":
            error_count,

        "warning_count":
            warning_count,

        "issues":
            issues,
    }
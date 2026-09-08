#功能测试用例接口测试用例DataFrame转换用例编号
import pandas as pd


FUNCTIONAL_COLUMNS = [
    "用例编号",
    "测试模块",
    "测试标题",
    "前置条件",
    "操作步骤",
    "测试数据",
    "预期结果",
    "优先级",
]


API_COLUMNS = [
    "用例编号",
    "测试模块",
    "测试标题",
    "请求方式",
    "URL",
    "Headers",
    "请求数据",
    "预期HTTP状态码",
    "预期业务结果",
    "优先级",
]


def normalize_case_ids(
    test_cases,
    prefix="TC"
):
    """
    重新整理用例编号。
    """

    normalized = []

    for index, original_case in enumerate(
        test_cases,
        start=1
    ):
        case = dict(original_case)

        case["case_id"] = (
            f"{prefix}{index:03d}"
        )

        normalized.append(case)

    return normalized


def functional_cases_to_dataframe(
    test_cases
):
    """
    功能用例 JSON -> DataFrame。
    """

    rows = []

    for case in test_cases:
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

                "前置条件":
                    case.get(
                        "precondition",
                        ""
                    ),

                "操作步骤":
                    case.get(
                        "steps",
                        ""
                    ),

                "测试数据":
                    case.get(
                        "test_data",
                        ""
                    ),

                "预期结果":
                    case.get(
                        "expected_result",
                        ""
                    ),

                "优先级":
                    case.get(
                        "priority",
                        ""
                    ),
            }
        )

    return pd.DataFrame(
        rows,
        columns=FUNCTIONAL_COLUMNS
    )


def dataframe_to_functional_cases(
    dataframe
):
    """
    DataFrame -> 功能测试用例。
    """

    cases = []

    if dataframe is None:
        return cases

    for _, row in dataframe.iterrows():
        cases.append(
            {
                "case_id": str(
                    row.get(
                        "用例编号",
                        ""
                    )
                ).strip(),

                "module": str(
                    row.get(
                        "测试模块",
                        ""
                    )
                ).strip(),

                "title": str(
                    row.get(
                        "测试标题",
                        ""
                    )
                ).strip(),

                "precondition": str(
                    row.get(
                        "前置条件",
                        ""
                    )
                ).strip(),

                "steps": str(
                    row.get(
                        "操作步骤",
                        ""
                    )
                ).strip(),

                "test_data": str(
                    row.get(
                        "测试数据",
                        ""
                    )
                ).strip(),

                "expected_result": str(
                    row.get(
                        "预期结果",
                        ""
                    )
                ).strip(),

                "priority": str(
                    row.get(
                        "优先级",
                        ""
                    )
                ).strip(),
            }
        )

    return cases


def api_cases_to_dataframe(
    test_cases
):
    """
    接口用例 JSON -> DataFrame。
    """

    rows = []

    for case in test_cases:
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
                    ),
            }
        )

    return pd.DataFrame(
        rows,
        columns=API_COLUMNS
    )


def dataframe_to_api_cases(
    dataframe
):
    """
    DataFrame -> 接口测试用例。
    """

    cases = []

    if dataframe is None:
        return cases

    for _, row in dataframe.iterrows():
        cases.append(
            {
                "case_id": str(
                    row.get(
                        "用例编号",
                        ""
                    )
                ).strip(),

                "module": str(
                    row.get(
                        "测试模块",
                        ""
                    )
                ).strip(),

                "title": str(
                    row.get(
                        "测试标题",
                        ""
                    )
                ).strip(),

                "method": str(
                    row.get(
                        "请求方式",
                        ""
                    )
                ).strip(),

                "url": str(
                    row.get(
                        "URL",
                        ""
                    )
                ).strip(),

                "headers": str(
                    row.get(
                        "Headers",
                        ""
                    )
                ).strip(),

                "request_data": str(
                    row.get(
                        "请求数据",
                        ""
                    )
                ).strip(),

                "expected_http_status": str(
                    row.get(
                        "预期HTTP状态码",
                        ""
                    )
                ).strip(),

                "expected_business_result": str(
                    row.get(
                        "预期业务结果",
                        ""
                    )
                ).strip(),

                "priority": str(
                    row.get(
                        "优先级",
                        ""
                    )
                ).strip(),
            }
        )

    return cases
def build_api_analysis_prompt(
    api_name,
    request_method,
    api_url,
    api_description,
    headers_text,
    request_body,
    success_response,
    error_response
):
    return f"""
你是一名高级接口测试工程师。

请根据下面接口信息进行接口分析。

请输出：

## 一、接口用途

## 二、请求参数分析

## 三、响应结构分析

## 四、明确业务规则

## 五、接口风险

## 六、测试重点

## 七、需求待确认

规则：

1. 不允许创造接口文档中不存在的业务规则。
2. 不明确的信息必须标记【需求待确认】。
3. 请求和响应示例只能作为接口信息依据。
4. 分析重点面向接口测试。

接口名称：

{api_name}

请求方法：

{request_method}

接口 URL：

{api_url}

接口需求：

{api_description}

Headers：

{headers_text}

Request Body / Params：

{request_body}

成功响应：

{success_response}

异常响应：

{error_response}
"""


def build_api_test_point_prompt(
    api_name,
    request_method,
    api_url,
    api_description,
    api_analysis
):
    return f"""
你是一名高级接口测试工程师。

根据接口需求和接口分析生成完整接口测试点。

必须考虑：

1. 正常请求
2. 必填参数缺失
3. 参数为空
4. 参数类型错误
5. 参数长度
6. 参数边界
7. 参数格式
8. 非法参数
9. Header 校验
10. Content-Type
11. 鉴权
12. Token
13. Token 缺失
14. Token 无效
15. Token 过期
16. 权限不足
17. 重复提交
18. 幂等性
19. HTTP 状态码
20. 业务状态码
21. 响应字段
22. 响应数据类型
23. 超时
24. 服务异常
25. 并发风险
26. 安全风险
27. 需求待确认

要求：

1. 不允许创造接口需求中不存在的业务规则。
2. 没有明确说明的规则标记【需求待确认】。
3. 不要为了增加数量而生成无效测试点。
4. 优先关注业务核心风险。

接口名称：

{api_name}

请求方法：

{request_method}

接口 URL：

{api_url}

接口需求：

{api_description}

接口分析：

{api_analysis}
"""


def build_api_case_prompt(
    api_name,
    request_method,
    api_url,
    api_description,
    headers_text,
    request_body,
    success_response,
    error_response,
    api_test_points
):
    return f"""
你是一名高级接口测试工程师。

根据接口信息和测试点生成完整接口测试用例。

只返回合法 JSON 数组。

每条用例字段必须包含：

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

字段要求：

case_id：
从 API001 开始。

priority：
只能使用：

P0
P1
P2

测试要求：

1. 覆盖正常业务请求。
2. 覆盖必填参数缺失。
3. 覆盖参数为空。
4. 覆盖参数类型错误。
5. 覆盖参数格式错误。
6. 覆盖明确的边界值。
7. 覆盖 Header 异常。
8. 覆盖鉴权异常。
9. 覆盖 Token 缺失。
10. 覆盖 Token 无效。
11. 覆盖权限不足。
12. 需求涉及重复提交时检查重复提交。
13. 检查 HTTP 状态码。
14. 检查业务返回结果。
15. 检查必要响应字段。
16. 考虑超时和服务异常。
17. 不允许自行创造业务规则。
18. 未明确的预期结果使用【需求待确认】。
19. 避免重复用例。
20. headers 使用字符串。
21. request_data 使用字符串。
22. 只输出 JSON 数组。
23. 不输出 Markdown。
24. 不输出 ```json。
25. 不解释生成过程。

接口名称：

{api_name}

请求方法：

{request_method}

接口 URL：

{api_url}

接口需求：

{api_description}

Headers：

{headers_text}

Request Body / Params：

{request_body}

成功响应：

{success_response}

异常响应：

{error_response}

接口测试点：

{api_test_points}
"""


def build_pytest_script_prompt(
    api_name,
    request_method,
    api_url,
    headers_text,
    api_description,
    current_cases_json
):
    return f"""
你是一名高级 Python 接口自动化测试工程师。

根据接口信息和接口测试用例，
生成一份可以继续维护的 Pytest + Requests 自动化测试脚本。

要求：

1. 使用 pytest。
2. 使用 requests。
3. 使用 @pytest.mark.parametrize 参数化测试。
4. 请求 timeout=10。
5. 校验 HTTP 状态码。
6. 需求明确时校验业务 code。
7. 需求明确时校验业务 message。
8. 对未明确的业务断言使用 TODO 注释。
9. 不允许在代码中写 API Key。
10. 不允许在代码中写真实 Token。
11. 测试数据需要敏感信息时使用占位符：

<VALID_PHONE>
<VALID_PASSWORD>
<VALID_TOKEN>

12. JSON 字符串需要转换时使用 json.loads。
13. GET 请求使用 params。
14. POST 请求使用 json。
15. PUT 请求使用 json。
16. PATCH 请求使用 json。
17. DELETE 根据接口信息合理处理。
18. 捕获 requests.RequestException。
19. 每条自动化用例需要能够对应接口测试用例。
20. 代码保持清晰，方便测试人员后续修改。
21. 最后加入：

if __name__ == "__main__":
    pytest.main(["-v", __file__])

22. 只输出完整 Python 代码。
23. 不输出 Markdown。
24. 不输出 ```python。
25. 不解释代码。

接口名称：

{api_name}

请求方法：

{request_method}

接口 URL：

{api_url}

Headers：

{headers_text}

接口需求：

{api_description}

当前接口测试用例：

{current_cases_json}
"""
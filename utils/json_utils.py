import json

try:
    from json_repair import repair_json
except ImportError:
    repair_json = None


def clean_json_text(content):
    """
    清理 AI 返回的 Markdown JSON 代码块。
    """

    if not content:
        return ""

    content = str(content).strip()

    if content.startswith("```json"):
        content = content[len("```json"):].strip()

    elif content.startswith("```JSON"):
        content = content[len("```JSON"):].strip()

    elif content.startswith("```"):
        content = content[3:].strip()

    if content.endswith("```"):
        content = content[:-3].strip()

    return content.strip()


def try_repair_json(content):
    """
    使用 json-repair 修复不规范 JSON。
    """

    if not content:
        return None

    if repair_json is None:
        return None

    try:
        repaired = repair_json(content)

        if isinstance(repaired, (list, dict)):
            return repaired

        return json.loads(repaired)

    except Exception:
        return None


def parse_json_list(content):
    """
    AI 输出 -> JSON 数组。
    """

    cleaned = clean_json_text(content)

    if not cleaned:
        return None

    # 1. 直接解析
    try:
        result = json.loads(cleaned)

        if isinstance(result, list):
            return result

    except Exception:
        pass

    # 2. 提取 []
    start = cleaned.find("[")
    end = cleaned.rfind("]")

    if (
        start != -1
        and end != -1
        and end > start
    ):
        json_part = cleaned[start:end + 1]

        try:
            result = json.loads(json_part)

            if isinstance(result, list):
                return result

        except Exception:
            pass

        repaired = try_repair_json(json_part)

        if isinstance(repaired, list):
            return repaired

    # 3. 修复完整内容
    repaired = try_repair_json(cleaned)

    if isinstance(repaired, list):
        return repaired

    return None


def parse_json_dict(content):
    """
    AI 输出 -> JSON 对象。
    """

    cleaned = clean_json_text(content)

    if not cleaned:
        return None

    # 1. 直接解析
    try:
        result = json.loads(cleaned)

        if isinstance(result, dict):
            return result

    except Exception:
        pass

    # 2. 提取 {}
    start = cleaned.find("{")
    end = cleaned.rfind("}")

    if (
        start != -1
        and end != -1
        and end > start
    ):
        json_part = cleaned[start:end + 1]

        try:
            result = json.loads(json_part)

            if isinstance(result, dict):
                return result

        except Exception:
            pass

        repaired = try_repair_json(json_part)

        if isinstance(repaired, dict):
            return repaired

    # 3. 修复完整内容
    repaired = try_repair_json(cleaned)

    if isinstance(repaired, dict):
        return repaired

    return None


def clean_python_code(content):
    """
    清理 AI 返回的 Python Markdown 代码块。
    """

    if not content:
        return ""

    content = str(content).strip()

    if content.startswith("```python"):
        content = content[len("```python"):].strip()

    elif content.startswith("```py"):
        content = content[len("```py"):].strip()

    elif content.startswith("```"):
        content = content[3:].strip()

    if content.endswith("```"):
        content = content[:-3].strip()

    return content.strip()
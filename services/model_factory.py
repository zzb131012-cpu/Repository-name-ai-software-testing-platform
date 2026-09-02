import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


load_dotenv()


def get_model():
    """
    根据 .env 中的 AI_PROVIDER
    统一创建大模型实例。

    前端页面不直接关心具体模型厂商。
    """

    provider = os.getenv(
        "AI_PROVIDER",
        "deepseek"
    ).strip().lower()

    temperature = float(
        os.getenv(
            "AI_TEMPERATURE",
            "0"
        )
    )

    # =====================================================
    # DeepSeek
    # =====================================================

    if provider == "deepseek":

        api_key = os.getenv(
            "DEEPSEEK_API_KEY"
        )

        model_name = os.getenv(
            "DEEPSEEK_MODEL",
            "deepseek-chat"
        )

        base_url = os.getenv(
            "DEEPSEEK_BASE_URL",
            "https://api.deepseek.com"
        )

        if not api_key:
            raise ValueError(
                "缺少 DEEPSEEK_API_KEY"
            )

        return ChatOpenAI(
            model=model_name,
            api_key=api_key,
            base_url=base_url,
            temperature=temperature
        )

    # =====================================================
    # OpenAI
    # =====================================================

    if provider == "openai":

        api_key = os.getenv(
            "OPENAI_API_KEY"
        )

        model_name = os.getenv(
            "OPENAI_MODEL"
        )

        if not api_key:
            raise ValueError(
                "缺少 OPENAI_API_KEY"
            )

        if not model_name:
            raise ValueError(
                "缺少 OPENAI_MODEL"
            )

        return ChatOpenAI(
            model=model_name,
            api_key=api_key,
            temperature=temperature
        )

    # =====================================================
    # Qwen
    # =====================================================

    if provider == "qwen":

        api_key = os.getenv(
            "QWEN_API_KEY"
        )

        model_name = os.getenv(
            "QWEN_MODEL",
            "qwen-plus"
        )

        base_url = os.getenv(
            "QWEN_BASE_URL",
            "https://dashscope.aliyuncs.com/compatible-mode/v1"
        )

        if not api_key:
            raise ValueError(
                "缺少 QWEN_API_KEY"
            )

        return ChatOpenAI(
            model=model_name,
            api_key=api_key,
            base_url=base_url,
            temperature=temperature
        )

    # =====================================================
    # GLM
    # =====================================================

    if provider == "glm":

        api_key = os.getenv(
            "GLM_API_KEY"
        )

        model_name = os.getenv(
            "GLM_MODEL"
        )

        base_url = os.getenv(
            "GLM_BASE_URL",
            "https://open.bigmodel.cn/api/paas/v4/"
        )

        if not api_key:
            raise ValueError(
                "缺少 GLM_API_KEY"
            )

        if not model_name:
            raise ValueError(
                "缺少 GLM_MODEL"
            )

        return ChatOpenAI(
            model=model_name,
            api_key=api_key,
            base_url=base_url,
            temperature=temperature
        )

    # =====================================================
    # 自定义 OpenAI Compatible
    # =====================================================

    if provider == "custom":

        api_key = os.getenv(
            "CUSTOM_API_KEY"
        )

        model_name = os.getenv(
            "CUSTOM_MODEL"
        )

        base_url = os.getenv(
            "CUSTOM_BASE_URL"
        )

        if not api_key:
            raise ValueError(
                "缺少 CUSTOM_API_KEY"
            )

        if not model_name:
            raise ValueError(
                "缺少 CUSTOM_MODEL"
            )

        if not base_url:
            raise ValueError(
                "缺少 CUSTOM_BASE_URL"
            )

        return ChatOpenAI(
            model=model_name,
            api_key=api_key,
            base_url=base_url,
            temperature=temperature
        )

    raise ValueError(
        f"暂不支持的 AI_PROVIDER：{provider}"
    )
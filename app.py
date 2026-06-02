"""Local Hy-MT2 translation web app for Apple Silicon Macs."""

from __future__ import annotations

import os
from functools import lru_cache
from threading import Lock

import gradio as gr
from mlx_lm import generate, load
from mlx_lm.sample_utils import make_logits_processors, make_sampler

MODEL_PATH = os.getenv("MODEL_PATH", "mlx-community/Hy-MT2-1.8B")
SERVER_NAME = os.getenv("SERVER_NAME", "0.0.0.0")
SERVER_PORT = int(os.getenv("SERVER_PORT", "7860"))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "4096"))

LANGUAGES = [
    "中文",
    "英语",
    "法语",
    "葡萄牙语",
    "西班牙语",
    "日语",
    "土耳其语",
    "俄语",
    "阿拉伯语",
    "韩语",
    "泰语",
    "意大利语",
    "德语",
]

SAMPLER = make_sampler(temp=0.7, top_p=0.6, top_k=20)
LOGITS_PROCESSORS = make_logits_processors(repetition_penalty=1.05)
MODEL_LOCK = Lock()


@lru_cache(maxsize=1)
def get_model():
    """Load the MLX model once, when the first translation starts."""
    return load(MODEL_PATH)


def build_prompt(source_language: str, target_language: str, text: str) -> str:
    """Build a Hy-MT2 translation prompt using the model's recommended format."""
    return (
        f"将以下{source_language}文本翻译为{target_language}，"
        "注意只需要输出翻译后的结果，不要额外解释：\n\n"
        f"{text}"
    )


def translate(source_language: str, target_language: str, text: str) -> str:
    """Translate text with the local Hy-MT2 MLX checkpoint."""
    source_text = text.strip()
    if not source_text:
        raise gr.Error("请输入需要翻译的文字。")
    if source_language == target_language:
        return source_text

    prompt = build_prompt(source_language, target_language, source_text)
    try:
        with MODEL_LOCK:
            model, tokenizer = get_model()
            formatted_prompt = tokenizer.apply_chat_template(
                [{"role": "user", "content": prompt}],
                tokenize=False,
                add_generation_prompt=True,
            )
            result = generate(
                model,
                tokenizer,
                prompt=formatted_prompt,
                max_tokens=MAX_TOKENS,
                sampler=SAMPLER,
                logits_processors=LOGITS_PROCESSORS,
                verbose=False,
            )
    except Exception as exc:
        raise gr.Error(f"翻译失败：{exc}") from exc

    return result.strip()


def create_demo() -> gr.Blocks:
    """Create the Gradio interface."""
    with gr.Blocks(title="Hy-MT2 本地翻译") as demo:
        gr.Markdown(
            """
            # Hy-MT2 本地翻译
            基于 `mlx-community/Hy-MT2-1.8B` 和 MLX，在 Mac 本地完成翻译。
            """
        )
        with gr.Row():
            source_language = gr.Dropdown(
                choices=LANGUAGES,
                value="中文",
                label="输入语言",
            )
            target_language = gr.Dropdown(
                choices=LANGUAGES,
                value="英语",
                label="输出语言",
            )

        source_text = gr.Textbox(
            label="翻译文字",
            placeholder="请输入需要翻译的内容",
            lines=8,
            max_lines=16,
            autofocus=True,
        )
        translate_button = gr.Button("翻译", variant="primary")
        translated_text = gr.Textbox(
            label="翻译结果",
            lines=8,
            max_lines=16,
            interactive=False,
            buttons=["copy"],
        )

        translate_button.click(
            fn=translate,
            inputs=[source_language, target_language, source_text],
            outputs=translated_text,
        )

    return demo


if __name__ == "__main__":
    create_demo().queue(default_concurrency_limit=1).launch(
        server_name=SERVER_NAME,
        server_port=SERVER_PORT,
        show_error=True,
    )

import gradio as gr
from groq import Groq


def correct_grammar(text, api_key):
    if not text or not text.strip():
        return "Please enter some text."

    if not api_key or not api_key.strip():
        return "Please enter your Groq API key."

    try:
        client = Groq(api_key=api_key.strip())

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an English grammar correction assistant. "
                        "Correct grammar, spelling, and punctuation errors. "
                        "Preserve the original meaning and writing style. "
                        "Do not rewrite sentences that are already correct. "
                        "Return only the corrected text, without explanations."
                    )
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
            temperature=0.2
        )

        return response.choices[0].message.content.strip()

    except Exception as error:
        return f"An error occurred: {str(error)}"



demo = gr.Interface(
    fn=correct_grammar,
    inputs=[
        gr.Textbox(
            label="Enter your English text",
            placeholder="Type or paste your text here...",
            lines=8
        ),
        gr.Textbox(
            label="Groq API Key",
            placeholder="Enter your API key",
            type="password"
        )
    ],
    outputs=gr.Textbox(
        label="Corrected text",
        lines=8
    ),
    title="Text Assistant",
    description=(
        "Welcome to Text Assistant! This application helps you "
        "improve your English writing by automatically correcting "
        "grammar, spelling, and punctuation errors. Simply enter your "
        "text, provide your Groq API key, and click 'Correct grammar' "
        "to receive an improved version of your text. "
        "The application uses an AI-powered language model to make "
        "your writing clearer, more accurate, and grammatically correct."
    ),
    submit_btn="Correct grammar",
    clear_btn="Clear"
)


if __name__ == "__main__":
    import os

demo.launch(
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", 7860))
)

import openai
import os
import random
from typing import Optional, List, Union


def generate_answer(prompt, models: Optional[Union[str, List[str]]] = None, role: Optional[str] = None):
    if models is None:
        models = ["gpt-3.5-turbo", "gpt-3.5-turbo-16k", "gpt-3.5-turbo-16k-0613"]
    if role is None:
        role = "You’re a kind helpful assistant"
    idx = random.randint(0, len(models) - 1)
    model = models[idx]
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "system", "content": role}, {"role": "user", "content": prompt}],
        api_key=os.environ.get("OPENAI_API_KEY"),
        max_tokens=512,
        temperature=1.0,
    )
    try:
        return response["choices"][0]["message"]["content"].strip()
    except IndexError:
        return ""


__all__ = ["generate_answer"]

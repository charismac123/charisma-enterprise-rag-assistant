#!/usr/bin/env python3
"""Quick smoke test for a local Ollama instance."""

import ollama

response = ollama.chat(
    model='llama3',
    messages=[
        {
            'role': 'user',
            'content': 'Explain Retrieval-Augmented Generation in one sentence.'
        }
    ]
)

print(response['message']['content'])

import requests
import os
import openai
import networkx as nx
import matplotlib.pyplot as plt
from flask import Flask, render_template
import sys
# import openai

# client = openai.OpenAI(
#     api_key="079e0597-f447-4b89-af13-96e50ab491ea",
#     base_url="https://api.sambanova.ai/v1",
# )

# response = client.chat.completions.create(
#     model="DeepSeek-R1",
#     messages=[{"role":"system","content":"You are a helpful assistant"},{"role":"user","content":"What's 2+2?"}],
#     temperature=0.1,
#     top_p=0.1
# )

# print(response.choices[0].message.content)


fig = plt.figure(figsize=(6, 4))  # Adjust size if needed
plt.axis('off')  # No axes

# Optional: fill background with white explicitly (some backends default to transparent)
fig.patch.set_facecolor('white')

# Save as PNG
script_dir = os.path.dirname(__file__)
static_folder = os.path.abspath(os.path.join(script_dir, "..", "static"))
plt.savefig(os.path.join(static_folder, "default.png"), bbox_inches='tight', pad_inches=0)
plt.close()
import requests
import os
import openai
import networkx as nx
import matplotlib.pyplot as plt
from flask import Flask, render_template
import sys

book_id = 12345
content_url = f"https://www.gutenberg.org/files/{book_id}/{book_id}-0.txt"
metadata_url = f"https://www.gutenberg.org/ebooks/{book_id}"

# Get book content
content_response = requests.get(content_url)
content = content_response.text

#print(content[0:len(content)//100])

# Get metadata
metadata_response = requests.get(metadata_url)





client = openai.OpenAI(
    api_key="37e22f43-0bd5-4862-974e-bbc1340fb984",
    base_url="https://api.sambanova.ai/v1",
)

response = client.chat.completions.create(
    model="Llama-3.1-Swallow-70B-Instruct-v0.3",
    messages = [
        {"role": "system", "content": "Provide only the final answer. Do not include any internal chain-of-thought or explanations. i.e (Here are the character interactions from the)"},
        {
            "role": "user",
            "content": (
                "Read through this text and write a list of each interaction between characters that was mentioned in the text."
                "I am using this data to create a graph, so please make sure you closely follow this format for each interaction"
                "First, we want to note the characters involved in a specific interaction. Then, we want to note the number of times each two characters interacted."
                "For example, in this example text (This isn't the text i need you to work on): Abdul said hi to Saad, Saad said hi to owais, Saad asked Abdul a question, owais said hi to Abdul."
                "The list I need would look exactly like this: (Abdul, Saad): 2, (Saad, owais): 2, (Saad, Abdul): 1"
                "Please provide the list only. Your answer is getting immediatly parsed into a list, so don't answer with an explination or a 'here is the list'"
                "Now do this for the text below:"
                + content[0:len(content)//10]
            )
        }
        ],

    temperature=0.1,
    top_p=0.1,
)

#print(response.choices[0].message.content)
lines = response.choices[0].message.content.splitlines()

# Filter lines that start with "* ("
filtered_lines = [line for line in lines if line.strip().startswith("* (")]

# Join them back together
result = "\n".join(filtered_lines)
print(result)
#print("First resopnse list:")
interaction_list = result.replace("* ", "").split("\n")
for interaction in interaction_list:
    interaction = interaction.split(": ")
    print(interaction[0])
    print(interaction[1])
    break
import requests
import os
import openai
import networkx as nx
import matplotlib.pyplot as plt
import sys

def get_content(book_id):

    content_url = f"https://www.gutenberg.org/files/{book_id}/{book_id}-0.txt"
    metadata_url = f"https://www.gutenberg.org/ebooks/{book_id}"

    # Get book content
    content_response = requests.get(content_url)
    content = content_response.text

    #print(content[0:len(content)//100])

    # Get metadata
    metadata_response = requests.get(metadata_url)
    return content, metadata_response.text




# def generate_list_of_interactions(content):
#     client = openai.OpenAI(
#         api_key="37e22f43-0bd5-4862-974e-bbc1340fb984",
#         base_url="https://api.sambanova.ai/v1",
#     )

#     response = client.chat.completions.create(
#         model="Llama-3.1-Swallow-70B-Instruct-v0.3",

#         messages = [
#         {"role": "system", "content": "Provide only the final answer. Do not include any internal chain-of-thought or explanations. i.e (Here are the character interactions from the)"},
#         {
#             "role": "user",
#             "content": (
#                 "Please provide every character interaction as a list of tuples like (charA, charB). Stick to this format and this format only. Do not do anything diffierent from the format"
#                 "don't use bullet point or any other formatting (don'nt write * before each one)."
#                 "using just first names for the first chapter. Filter out duplicates. "
#                 "Please only provide the list. "
#                 + content[0:len(content)//10] +
#                 "please only use this format and no other format. here is an exacty template I want you to follow:"
#                 "(charA, charB)"
#                 "(charC, charD)"
#                 "(charA, charC)"
#                 "(charB, charD)"
#             )
#         }
#         ],
#         temperature=0.1,
#         top_p=0.1,
#     )
#     print(response.choices[0].message.content)
#     interaction_list = response.choices[0].message.content.split("\n")
#     return interaction_list

def generate_list_of_interactions(content):
    openai.api_key = "37e22f43-0bd5-4862-974e-bbc1340fb984"
    openai.api_base = "https://api.sambanova.ai/v1"

    response = openai.ChatCompletion.create(
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
    print(" AI RESOPONCE:")
    print(response.choices[0].message.content)
    print("-----------------------------------------------------")
    lines = response.choices[0].message.content.splitlines()
    # Filter lines that start with "* ("
    filtered_lines = [line for line in lines if line.strip().startswith("* (")]
    # Join them back together
    result = "\n".join(filtered_lines)
    result = result.replace("* ", "").split("\n")
    return result

def generate_graph(interactions):
    import matplotlib.pyplot as plt
    import networkx as nx

    g = nx.Graph()
    # Parse each interaction from your list. Expected format: "(charA, charB): num"
    for interaction in interactions:
        try:
            # Split into character pair and number parts
            pair_str, num_str = interaction.split(": ")
            # Remove surrounding parentheses and extra spaces
            pair_str = pair_str.strip()[1:-1]  # removes the first and last character
            charA, charB = [name.strip() for name in pair_str.split(",")]
            num = int(num_str.strip())
            g.add_edge(charA, charB, weight=num)
        except Exception as e:
            print(f"Skipping line due to error: {interaction} -> {e}")

    # Create positions for nodes using spring layout
    pos = nx.spring_layout(g, seed=42, k=0.5, iterations=200)


    # Create a new figure
    plt.figure()

    # Draw the graph with custom styling
    nx.draw(
        g, pos,
        edge_color='black', width=1, linewidths=1,
        node_size=500, node_color='pink', alpha=0.9,
        labels={node: node for node in g.nodes()}
    )

    # Get edge labels (the weight values) and draw them
    edge_labels = nx.get_edge_attributes(g, 'weight')
    nx.draw_networkx_edge_labels(
        g, pos,
        edge_labels=edge_labels,
        font_color='red'
    )

    # Remove axes for a cleaner look
    plt.axis('off')

    # Save the graph image in the static folder
    script_dir = os.path.dirname(__file__)
    static_folder = os.path.abspath(os.path.join(script_dir, "..", "static"))
    plt.savefig(os.path.join(static_folder, "graph.png"))
    plt.close()










def main(book_id):
    print(f"Python main() called with book_id={book_id}")

    content, metadata = get_content(book_id)
    if not content:
        print("No content returned. Possibly invalid book_id or request failure.")
        return

    print("Content fetched successfully.")
    interactions = generate_list_of_interactions(content)

    if not interactions:
        print("No interactions extracted. Possibly AI returned nothing.")
        return

    print(f"Extracted {len(interactions)} interactions. Generating graph...")
    generate_graph(interactions)
    print("Graph generation complete.")

if __name__ == "__main__":
    book_id = sys.argv[1] if len(sys.argv) > 1 else "12345"
    main(book_id)
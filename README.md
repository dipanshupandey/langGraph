# Learning Agentic AI with LangGraph

This repository holds my notes and practice notebooks while learning how to build agentic AI workflows with [LangGraph](https://langchain-ai.github.io/langgraph/).

It is a personal learning project, not production code.

## Contents

| Notebook | Topic |
| --- | --- |
| `1_BMI_Workflow.ipynb` | First workflow: a `TypedDict` state and a node that calculates BMI |
| `2_Simple_LLM_Workflow.ipynb` | Simple LLM workflow: a node that sends a prompt to a Cohere model and stores the answer in state |
| `3_Prompt_Chaining.ipynb` | Prompt chaining: a 3-step workflow (outline, content, evaluation) where each node's output feeds the next |

More notebooks will be added as I progress.

## Setup

```zsh
python3 -m venv myenv
source myenv/bin/activate
pip install langgraph cohere python-dotenv jupyter
```

Create a `.env` file in the project root with your API key (it is git-ignored, so it is never committed):

```
COHERE_API_KEY=your-key-here
```

Then open a notebook in VS Code or run `jupyter notebook`.

## Concepts covered so far

- Defining graph state with `TypedDict`
- Writing nodes as plain Python functions that take and return state
- Building graphs with `StateGraph` and running them with `invoke`
- Calling an LLM (Cohere) from a node using the chat message format
- Loading API keys from a `.env` file instead of hardcoding them
- Handling reasoning-model responses by extracting only the text item from the content list
- Prompt chaining: connecting nodes in sequence with `add_edge`, using `START` and `END`
- Rendering LLM output in notebooks with `IPython.display.Markdown`

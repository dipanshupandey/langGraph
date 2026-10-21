# Learning Agentic AI with LangGraph

This repository holds my notes and practice notebooks while learning how to build agentic AI workflows with [LangGraph](https://langchain-ai.github.io/langgraph/).

It is a personal learning project, not production code.

## Contents

| Notebook | Topic |
| --- | --- |
| `1_BMI_Workflow.ipynb` | First workflow: a `TypedDict` state and a node that calculates BMI |

More notebooks will be added as I progress.

## Setup

```zsh
python3 -m venv myenv
source myenv/bin/activate
pip install langgraph jupyter
```

Then open a notebook in VS Code or run `jupyter notebook`.

## Concepts covered so far

- Defining graph state with `TypedDict`
- Writing nodes as plain Python functions that take and return state
- Building graphs with `StateGraph`

# Learning Agentic AI with LangGraph

This repository holds my notes and practice notebooks while learning how to build agentic AI workflows with [LangGraph](https://langchain-ai.github.io/langgraph/).

It is a personal learning project, not production code.

## Contents

| Notebook | Topic |
| --- | --- |
| `1_BMI_Workflow.ipynb` | First workflow: a `TypedDict` state and a node that calculates BMI |
| `2_Simple_LLM_Workflow.ipynb` | Simple LLM workflow: a node that sends a prompt to a Cohere model and stores the answer in state |
| `3_Prompt_Chaining.ipynb` | Prompt chaining: a 3-step workflow (outline, content, evaluation) where each node's output feeds the next |
| `4_Parallel_simple_workflow.ipynb` | Parallel workflow: three independent cricket-stat nodes (strike rate, boundary %, boundaries per delivery) run in parallel and merge into a summary node |
| `5_Parallel_LLM_workflow.ipynb` | Parallel LLM workflow: an essay is evaluated in parallel for language, depth of analysis, and clarity, using structured output; scores are collected with a reducer and averaged |
| `6_Conditional_Simple_Workflow.ipynb` | Conditional workflow: a node generates random marks, and a routing function sends the graph to a fail, average, or good node based on the score |
| `7_Conditional_LLM_Workflow.ipynb` | Conditional LLM workflow: an LLM classifies a review as positive or negative; positive reviews get a thank-you reply, negative ones are diagnosed (issue type, tone, urgency) with structured output and get a support reply |
| `8_Iterative_LLM_Workflow.ipynb` | Iterative (loop) LLM workflow: one model generates a tweet, a second evaluates it with structured output, and a third rewrites it from the feedback; the loop repeats until the tweet is approved or a maximum iteration count is reached |
| `9_Project_Chatbot.ipynb` | Chatbot project: a single-node LangGraph chatbot using a Cohere model, with conversation memory per `thread_id` (via `MemorySaver`) and a terminal chat loop |

More notebooks will be added as I progress.

## Setup

```zsh
python3 -m venv myenv
source myenv/bin/activate
pip install langgraph cohere langchain-cohere pydantic python-dotenv jupyter
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
- Parallel workflows: fanning out from `START` to several nodes and merging them into one node
- Returning partial state updates (e.g. `{'sr': sr}`) so parallel nodes don't write the same key
- How LangGraph runs supersteps: parallel nodes read a state snapshot, and their updates are applied together after all of them finish
- Pydantic models (`BaseModel`, `Field`) for validated data schemas
- Structured output with `model.with_structured_output(Schema)` from LangChain, which returns a typed object instead of free text
- Using `ChatCohere` (`langchain-cohere`) instead of the raw Cohere SDK, since `with_structured_output` is a LangChain method
- Cohere's structured output does not support numeric constraints like `ge`/`le`, so the allowed range goes in the field description
- Reducers (`Annotated[list[int], operator.add]`) to safely combine values written by parallel nodes
- Conditional workflows: `add_conditional_edges` with a routing function that returns the name of the next node
- Mapping routing-function outputs to node names with a path map, so only one branch runs
- Using an LLM to decide the route: structured output with `Literal` fields (e.g. sentiment, issue type, tone, urgency) feeding a routing function
- Nodes on a skipped branch never run, so their state keys (e.g. `diagnosis` for positive reviews) are missing from the final state
- Extracting plain text from a reasoning model's content list with a small helper (`get_text`)
- Giving the LLM the original input (not just extracted labels) in later prompts so replies stay specific, and not letting it invent actions it can't perform
- Iterative workflows: a conditional edge that routes back to an earlier node (evaluate, optimize, evaluate, ...) to form a loop
- Stopping a loop safely with an iteration counter and a max-iteration limit in state
- Using a different Cohere model per role (generator, evaluator, optimizer) and setting `temperature` per role (high for creative, `0` for evaluation)
- Building prompts with `SystemMessage` and `HumanMessage` from `langchain_core.messages`, and calling models with `.invoke(...)` (models are not called directly)
- Accumulating history across loop passes with reducer fields (`tweetHistory`, `feedBackHistory`)
- Testing a loop by forcing the evaluator to reject for a few rounds, since a lenient evaluator may approve on the first pass
- Chatbot state with `messages: Annotated[list[BaseMessage], add_messages]`, where nodes return new messages as a list and `add_messages` appends them
- Invoking a graph with a dict that matches the state (`{"messages": [HumanMessage(...)]}`), not a raw string
- Conversation memory with a checkpointer (`MemorySaver`) and a `thread_id` in the config: the same `thread_id` continues a conversation, a new one starts fresh
- `MemorySaver` keeps memory only in the running process; a database-backed checkpointer is needed to persist chats across restarts
- Structured output returns a Pydantic object, not a message, so it must be converted (e.g. to `AIMessage`) before going into `messages`

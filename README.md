# CodeEx

### Aim:
To build a platform where a Large Language Model (LLM) is deployed and used for various coding related tasks, such as, Python Coding, SQL Queries, Shell Scripting, etc.

### Large Language Model Used:
* Model Name: `meta-llama/CodeLlama-7b-Instruct-hf`
* Parameters: 6.74 B Parameters
* Context Length: Up to 16,384 tokens
* Architecture: Auto-regressive Transformer with Grouped-Query Attention (GQA) for scalable inference
* Space taken on GPU: ~28 GiB when loaded on full precision (fp32) and ~14 GiB when quantized to half precision (fp16).

**Why this above model?**
During developing this, compared two models:
* StarCoder (TechxGenus/starcoder2-7b-instruct) and CodeLlama (meta-llama/CodeLlama-7b-Instruct-hf).
* Both of the above models are equally good, with CodeLlama having a slight edge in terms of better code generation and optimisation of code.

## Currently how this works:
* There is a file named `prompt_template.json`, currently consisting of 5 prompt templates:
    + `sql_query`
    + `shell_script`
    + `python_code`
    + `java_class`
    + `javascript_function`

* The core of the project lies in `generation_pipeline.py`, the model is loaded using the `ModelHandler` class in `model_handler.py`, further the entire pipepline and chain is defined here.

## Further scope:
* Further extension in terms of addition of support to many other languages, such as Angular, HTML, or support related to Node.js, MongoDB, etc.
* Using better models as available in the near future.
* Implmenting RAG based approach, such as creating vector stores for Python, JS, etc. and letting the LLM interact with them for better outputs.

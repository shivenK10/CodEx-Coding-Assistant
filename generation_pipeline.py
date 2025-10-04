import json
from model_handler import ModelHandler
from transformers import pipeline
from langchain_huggingface import HuggingFacePipeline
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from logger import Logger

# Initialize logger
log = Logger("Generation Pipeline Logs", True, "Logs/generation.log", "DEV")

# Load model once, with correct argument order: model_name, quantize, model_path
model = ModelHandler(
    model_name="meta-llama/CodeLlama-7b-Instruct-hf",
    model_path="",
    quantize=True
)
loaded_model, corresponding_tokenizer = model.load_model()

def load_prompt_templates():
    """Load prompt templates and drop HTML, CSS, Angular entries."""
    try:
        with open('prompt_template.json', 'r') as f:
            templates = json.load(f)
        log.info("Prompt templates loaded successfully")
        return templates
    except FileNotFoundError:
        log.error("prompt_template.json file not found")
        return {}
    except json.JSONDecodeError:
        log.error("Error parsing prompt_template.json")
        return {}

def gen_chain():
    """Create the generation pipeline (text-generation → parser)."""
    pipe = pipeline(
        "text-generation",
        model=loaded_model,
        tokenizer=corresponding_tokenizer,
        max_new_tokens=10000,
        do_sample=True,
        temperature=0.3,
        eos_token_id=corresponding_tokenizer.eos_token_id,
        pad_token_id=corresponding_tokenizer.eos_token_id,
        return_full_text=False,
    )
    return HuggingFacePipeline(pipeline=pipe) | StrOutputParser()

# Initialize chain and templates
chain = gen_chain()
prompt_templates = load_prompt_templates()

def generate_code(template_type: str, specification: str) -> str:
    """Generate code for a given template type and user specification."""
    if template_type not in prompt_templates:
        log.error(f"Template type '{template_type}' not found")
        return f"Error: Template type '{template_type}' not found"

    try:
        template_content = prompt_templates[template_type]
        prompt = PromptTemplate.from_template(template=template_content)
        specific_chain = prompt | chain
        result = specific_chain.invoke({"specification": specification})
        log.info(f"Successfully generated {template_type}")
        return result
    except Exception as e:
        log.error(f"Error generating {template_type}: {e}")
        return f"Error generating code: {e}"

def get_available_templates():
    """Return the list of enabled template keys."""
    return list(prompt_templates.keys())

def get_template_display_names():
    """Map template keys to human-friendly names."""
    return {
        'sql_query': 'SQL Query',
        'shell_script': 'Shell Script',
        'python_code': 'Python Code',
        'java_class': 'Java Class',
        'javascript_function': 'JavaScript Function'
    }

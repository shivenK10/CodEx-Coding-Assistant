import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from logger import Logger

log = Logger("Model Loader Logs", True, "./Logs/model.logs", "DEV")

class ModelHandler:
    def __init__(self, model_name: str, model_path: str, quantize: bool = False):
        """
        Initialization of class arguments.

        1. model_name -> str -> Hugging face repo id.\n
        2. model_path -> str -> Provide the path for ".cache" where the model is kept, if not done and have space on disk provide "".
        3. quantize -> bool -> Whether to not quantize the model.\n
        """
        self.model_name = model_name
        self.model_path = model_path
        self.quantize = quantize

        log.debug("Initialisation done successfully!")
    
    def load_model(self):
        """
        Loads the tokenizer and model according to the initialization parameters.

        Returns:
            model: The loaded AutoModelForCausalLM on the specified device.
            tokenizer: The corresponding AutoTokenizer.
        """
        if self.model_path == "":
            try:
                tokenizer = AutoTokenizer.from_pretrained(self.model_name, local_files_only=True)
                log.info("Model's Tokenizer successfull loaded!")
                if self.quantize:
                    model = AutoModelForCausalLM.from_pretrained(
                        self.model_name,
                        low_cpu_mem_usage=True,
                        torch_dtype=torch.float16,
                        device_map="auto",
                        local_files_only=True
                    )
                else:
                    model = AutoModelForCausalLM.from_pretrained(
                            self.model_name,
                            low_cpu_mem_usage=True,
                            device_map="auto",
                            local_files_only=True
                        )
            except OSError:
                log.error("Model not found.")
                log.info("Beginning model download.")
                tokenizer = AutoTokenizer.from_pretrained(self.model_name)
                if self.quantize:
                    model = AutoModelForCausalLM.from_pretrained(
                        self.model_name,
                        low_cpu_mem_usage=True,
                        torch_dtype=torch.float16,
                        device_map="auto",
                    )
                else:
                    model = AutoModelForCausalLM.from_pretrained(
                            self.model_name,
                            low_cpu_mem_usage=True,
                            device_map="auto",
                        )
            
            log.info("Model Loaded successfully!")

        else:
            try:
                tokenizer = AutoTokenizer.from_pretrained(self.model_name, cache_dir=self.model_path, local_files_only=True)
                log.info("Model's Tokenizer successfull loaded!")
                if self.quantize:
                    model = AutoModelForCausalLM.from_pretrained(
                        self.model_name,
                        low_cpu_mem_usage=True,
                        torch_dtype=torch.float16,
                        device_map="auto",
                        local_files_only=True,
                        cache_dir=self.model_path
                    )
                else:
                    model = AutoModelForCausalLM.from_pretrained(
                            self.model_name,
                            low_cpu_mem_usage=True,
                            device_map="auto",
                            local_files_only=True,
                            cache_dir=self.model_path
                        )
            except OSError:
                log.error("Model not found at the given directory.")
                log.info("Beginning model download.")
                tokenizer = AutoTokenizer.from_pretrained(self.model_name, cache_dir=self.model_path)
                if self.quantize:
                    model = AutoModelForCausalLM.from_pretrained(
                        self.model_name,
                        low_cpu_mem_usage=True,
                        torch_dtype=torch.float16,
                        device_map="auto",
                        cache_dir=self.model_path
                    )
                else:
                    model = AutoModelForCausalLM.from_pretrained(
                            self.model_name,
                            low_cpu_mem_usage=True,
                            device_map="auto",
                            cache_dir=self.model_path
                        )
            
            log.info("Model Loaded successfully!")
        return model, tokenizer

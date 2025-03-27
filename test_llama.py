from llama_cpp import Llama

# Load the model
MODEL_PATH = "models/mistral-7b-instruct.Q4_K_M.gguf"
llm = Llama(model_path=MODEL_PATH, n_ctx=512, n_batch=16)  # Reduce context length and batch size

# Test the AI model
prompt = "What is the capital of France?"
response = llm(prompt, max_tokens=50)

print("AI Response:", response["choices"][0]["text"].strip())


import time

def measure_performance(func):
    """Decorator to measure execution time and tokens of an LLM call."""
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        
        # Execute the function
        result = func(*args, **kwargs)
        
        end_time = time.perf_counter()
        duration = end_time - start_time
        
        # Note: Local Ollama models don't always return token counts via invoke() 
        # unless specifically requested or if using a callback.
        # We estimate here based on average characters per token (4 chars = 1 token)
        # for teaching purposes, or attempt to extract from metadata if available.
        
        input_text = str(args[0]) if args else ""
        output_text = str(result)
        
        input_tokens = len(input_text) // 4
        output_tokens = len(output_text) // 4
        total_tokens = input_tokens + output_tokens
        
        # Local model cost is $0, but we can display a mock "cloud comparison" cost
        # GPT-4o style pricing: $5.00 / 1M input, $15.00 / 1M output
        mock_cost = (input_tokens * 0.000005) + (output_tokens * 0.000015)
        
        print("\n--- PERFORMANCE METRICS ---")
        print(f"⏱️ Time Taken: {duration:.2f} seconds")
        print(f"📥 Input Tokens (Est): {input_tokens}")
        print(f"📤 Output Tokens (Est): {output_tokens}")
        print(f"💰 Mock Cloud Cost: ${mock_cost:.6f}")
        print("---------------------------\n")
        
        return result
    return wrapper

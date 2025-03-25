import subprocess


class LocalLLM:
    # LocalLLM is a wrapper for local LLMs using the Ollama CLI.
    def __init__(self, model_name="mistral"):
        self.model = model_name

    def generate(self, prompt: str) -> str:
        """Call local LLM via Ollama."""
        result = subprocess.run(
            ["ollama", "run", self.model],
            input=prompt.encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        output = result.stdout.decode()
        return self._clean_output(output)

    def _clean_output(self, raw_output):
        """Optional: Clean response based on model's output format."""
        return raw_output.strip()

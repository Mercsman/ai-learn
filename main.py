import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.prompts import system_prompt
from call_function import available_functions, call_function


def main():
    # -----------------------------
    # Argument parsing
    # -----------------------------
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    # -----------------------------
    # Environment setup
    # -----------------------------
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not set")

    client = genai.Client(api_key=api_key)

    # -----------------------------
    # Initial conversation
    # -----------------------------
    messages = [
        types.Content(
            role="user",
            parts=[types.Part(text=args.user_prompt)],
        )
    ]

    # -----------------------------
    # Agent loop
    # -----------------------------
    for iteration in range(20):
        if args.verbose:
            print(f"\n--- Iteration {iteration + 1} ---")

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt,
            ),
        )

        # Add model thoughts to memory
        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

        # -----------------------------
        # Handle tool calls
        # -----------------------------
        if response.function_calls:
            function_results = []

            for function_call in response.function_calls:
                print(f"Calling function: {function_call.name}({function_call.args})")

                result = call_function(function_call, verbose=args.verbose)
                function_results.append(result.parts[0])

            # Feed tool results back to model
            messages.append(
                types.Content(
                    role="user",
                    parts=function_results,
                )
            )
            continue

        # -----------------------------
        # Final answer
        # -----------------------------
        print(response.text)
        return

    # -----------------------------
    # Safety exit
    # -----------------------------
    print("Error: agent did not finish within 20 iterations.")
    exit(1)


if __name__ == "__main__":
    main()

import openai
import time

def call_openai(prompt: str) -> str:
    """
    Call the OpenAI API and return the generated text.

    Args:
        prompt (str): The prompt to generate text from.

    Returns:
        str: The generated text.
    """
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0,
            max_tokens=60,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        return response.choices[0]['text'].strip()
    except openai.error.RateLimitError:
        # Catch the rate limit error and wait for one minute before trying again
        print("Rate limit reached. Waiting for 80 seconds before trying again...")
        time.sleep(80)
    except Exception as e:
        # Catch any exceptions thrown by the OpenAI API and print the error message
        print(f"Error calling OpenAI API: \nError Type: {type(e)}\nError Message: {e}")
        return "Error calling OpenAI API"


class GenderGuesser:
    def __init__(self, data_dict: dict, openai_apikey: str):
        self.data_dict = data_dict
        self.openai_apikey = openai_apikey

        # init api
        openai.api_key = openai_apikey

    def gender_guesser(self, name: str)-> str:
        name = str(name).capitalize()
        if name in self.data_dict:
            return self.data_dict[name]
        else:
            print(f"--{name}-- is not found in the databse. Using chatgpt...")
            prompt = f"""
            Guess the gender of someone named {name}
            If Male, return M
            If Female, return F
            If Androgenous, return A
            """
            gender = call_openai(prompt)
            print(f"{name} is suggested to be of gender = {gender}\n")
            self.data_dict[name] = gender

            return gender
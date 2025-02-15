from crewai.flow.flow import Flow, start, listen, router
from litellm import completion

class ChainOfThought(Flow):
    API_KEY = "GEMINI_API_KEY"
    model = "GEMINI_MODEL"

    @start()
    def extract_the_issue(self):
        """
        First LLM Call: Extract the issue from the customer email
        """
        response = completion(
            model=self.model,
            api_key=self.API_KEY,
            messages=[
                {"role": "system", "content": "You are a customer support agent. Your task is to extract the issue from the user email."},
                {"role": "user", "content": "Extract the main issue and concerns from the following email: Hi, I recently purchased a laptop from your store, but it has been malfunctioning. I am very disappointed with the quality and would like to know what can be done about it."}
            ]
        )
        issue = response.choices[0].message.content
        self.state["issue"] = issue
        return issue

    @listen(extract_the_issue)
    def generate_draft_response(self):
        """
        Second LLM Call: Draft a response to the customer email
        """
        issue1 = self.state["issue"]
        response = completion(
            model=self.model,
            api_key=self.API_KEY,
            messages=[
                {"role": "system", "content": "You are a customer support agent. Your task is to draft a response to the user email."},
                {"role": "user", "content": f"Draft a response addressing the following customer issue: {issue1}. Ensure the response is clear, professional, and empathetic. Do not ask for name, email, or other personal information."}
            ]
        )
        draft_response = response.choices[0].message.content
        self.state["draft_response"] = draft_response
        return draft_response

    @router(generate_draft_response)
    def checking_the_response(self):
        """
        Gate function to check if the draft response includes empathetic language.
        """
        draft_response = self.state["draft_response"]
        if "sorry" in draft_response.lower() or "apologies" in draft_response.lower():
            return "polish_response"
        else:
            return "final_response_generator"

    @listen("polish_response")
    def polish_the_response(self):
        """
        Third LLM Call: Re-draft the response to include empathetic language
        """
        response2 = self.state["draft_response"]
        response = completion(
            model=self.model,
            api_key=self.API_KEY,
            messages=[
                {"role": "system", "content": "You are a customer support agent. Your task is to polish the draft response to make it more engaging and empathetic."},
                {"role": "user", "content": f"Re-draft the following response to include empathetic language: {response2}. Rewrite it to better express the customer's concern. Do not ask for personal details."}
            ]
        )
        response = response.choices[0].message.content
        self.state["response"] = response
        print(f"Re-polished response: {response}")
        return response

    @listen("final_response_generator")
    def re_polish_response(self):
        """
        Fourth LLM Call: Polish the response to make it more engaging and professional
        """
        response3 = self.state.get("response")
        response = completion(
            model=self.model,
            api_key=self.API_KEY,
            messages=[
                {"role": "system", "content": "You are a customer support agent. Your task is to polish the response to make it more engaging and professional."},
                {"role": "user", "content": f"Polish the following response to make it more engaging and professional: {response3}. Ensure it is empathetic and professional."}
            ]
        )
        polished_response = response.choices[0].message.content
        self.state["polished_response"] = polished_response
        return polished_response

    @listen(re_polish_response)
    def write_in_file(self):
        """
        Fifth LLM Call: Write the polished response to a file
        """
        polished_response = self.state["polished_response"]
        with open("response.txt", "w") as file:
            file.write(polished_response)
        print("Response written to file: response.txt")
        return "response_written"


def main():
    flow = ChainOfThought()
    flow.kickoff()

def mainplot():
    flow = ChainOfThought()
    flow.plot()

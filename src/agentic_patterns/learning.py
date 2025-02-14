#learning crewai ROUTES 

from crewai.flow.flow import Flow, start, listen, router
from litellm import completion

class Learning(Flow):
    API_KEY = "AIzaSyDoT0HSp2FtrDrsuF16taPk6rYbShwnbGQ"
    model = "gemini/gemini-1.5-pro"

    @start()
    def Question(self):
        response = completion(
            model=self.model,
            api_key=self.API_KEY,
            messages=[
                {"role": "user", "content": "Ask me a question about crewai"}
            ]
        )
        question = response["choices"][0]["message"]["content"]
        print(f"The Question is: {question}")
        return question

    @router(Question)
    def routing(self):
        if False:
            return "one_line_answer"
        else:
            return "answer_in_detail"

    @listen("answer_in_detail")
    def Detail_answer(self, question):
        response = completion(
            model=self.model,
            api_key=self.API_KEY,   
            messages=[
                {"role": "user", "content": f"Answer the following question: {question}"}
            ]
        )
        answer2 = response["choices"][0]["message"]["content"]
        print(f"The Answer is: {answer2}")
        return answer2

    @listen("one_line_answer")
    def One_line_answer(self, question):
        response = completion(
            model=self.model,
            api_key=self.API_KEY,   
            messages=[
                {"role": "user", "content": f"Answer the following question in one line: {question}"}
            ]
        )
        answer1 = response["choices"][0]["message"]["content"]
        print(f"The Answer is: {answer1}")
        return answer1

    
        
        


def main():
    flow = Learning()
    flow.kickoff()

def mainplot():
    flow = Learning()
    flow.plot()


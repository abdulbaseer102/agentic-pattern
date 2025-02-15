#learning crewai ROUTES 

from crewai.flow.flow import Flow, start, listen, router
from litellm import completion

class Learning(Flow):
    API_KEY = "AIzaSyDoT0HSp2FtrDrsuF16taPk6rYbShwnbGQ"
    model = "gemini/gemini-1.5-flash"

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
        self.state["question"] = question
        return question
    
    @listen(Question)
    def re_draft_response(self):
        question = self.state.get("question")
        response = completion(
            model=self.model,
            api_key=self.API_KEY,
            messages=[
                {"role": "user", "content": f"Answer the following question: {question}"}
            ]
        )
        answer = response["choices"][0]["message"]["content"]
        return answer

    @router(re_draft_response)
    def routing(self):
        if False:
            return "one_line_answer"
        elif False:
            return "answer_in_detail"
        else:
            return "answer_in_more_detail"
        

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
    
    @listen("answer_in_more_detail")
    def more_detail_answer(self, question):
        response = completion(
            model=self.model,
            api_key=self.API_KEY,   
            messages=[
                {"role": "user", "content": f"Answer the following question in more detail: {question}"}
            ]
        )
        answer3 = response["choices"][0]["message"]["content"]
        self.state["answer3"] = answer3
        return answer3
        

    @listen(more_detail_answer)
    def write_in_file(self, question):
         answer3 = self.state.get("answer3")
         with open("response.txt", "w") as file:
            file.write(answer3)
         print(f"Response written to file: response.txt")
         return "response_written"

    

def main():
    flow = Learning()
    flow.kickoff()

def mainplot():
    flow = Learning()
    flow.plot()


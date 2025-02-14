from crewai.flow.flow import Flow, start, listen, router
from litellm import completion

class ChainOfThought(Flow):
 
    API_KEY = "GEMINI_API_KEY"
    model = "gemini/gemini-1.5-flash"

 #chain of thought flow pattern with gemini model 1.5 flash

    @start()
    def Question(self):
        response = completion(
            model=self.model,
            api_key=self.API_KEY,
            messages=[
                {"role": "user", "content": "Ask me a very hard question with the help of chain of thought flow pattern"}
            ]
           
        )
        question = response["choices"][0]["message"]["content"]
        print(f"The Question is: {question}")
        return question
    
    @router(Question)
    def routing(self):
    # Route based on the is_tech flag.
        if False:
            return "detaild"
        else:
            return "simplyfy"

    
    @listen("detaild")
    def detaild_answer(self, question):
        response = completion(
            model=self.model,
            api_key=self.API_KEY,
            messages=[
                {"role": "user", "content": f" give me the following question`s answer in a detail way: {question}"}
            ]
        )
        answers2 = response["choices"][0]["message"]["content"]
        print(f"generated answers: {answers}")
        return answers
    
    @listen("simplyfy")
    def simplefy_answer(self, question):
        response = completion(
            model=self.model,
            api_key=self.API_KEY,
            messages=[
                {"role": "user", "content": f" Give me the following question`s answer in a simple way: {question}"}
            ]
        )
        answers = response["choices"][0]["message"]["content"]
        print(f"generated answers: {answers}")
        return answers


    
   
def main():
    flow = ChainOfThought()
    flow.kickoff()
    
def mainplot():
    flow = ChainOfThought()
    flow.plot()


            
        


     
        
        
    


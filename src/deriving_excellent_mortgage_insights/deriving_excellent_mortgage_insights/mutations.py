from typing import Optional
import strawberry as sb

from transformers import pipeline
question_answerer = pipeline("question-answering")

@sb.input
class ModelInference:
    context: str
    question: str


@sb.input
class MortgageLookup:
    debt: Optional[float]
    savings: Optional[float]
    income: Optional[float]

@sb.type
class MortgageLookupResponse:
    debt: Optional[float]
    savings: Optional[float]
    income: Optional[float]

def calculate_mortage_score(income, savings, debt):
    return income + savings / 10 ** 2 - debt / 10 ** 3


def get_mortgage_range_from_score(mortgage_score):
    buckets = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
    for bucket in buckets:
        if mortgage_score < bucket:
            return bucket
    return bucket


class Prediction:
    def predict(self, inputs: ModelInference):
        return question_answerer(question=inputs.question, context=inputs.context)

    def extract_number(self, text):
        return [int(s) for s in text.split() if s.isdigit()][0]
    def extract_income(self, inputs: ModelInference) -> str:
        prediction = self.predict(inputs)
        if prediction["score"] < 0.6:
            return None
        return self.extract_number(prediction["answer"])

    def extract_savings(self, inputs: ModelInference) -> str:
        prediction = self.predict(inputs)
        if prediction["score"] < 0.6:
            return None
        return self.extract_number(prediction["answer"])

    def extract_debt(self, inputs: ModelInference) -> str:
        prediction = self.predict(inputs)
        if prediction["score"] < 0.6:
            return None
        return self.extract_number(prediction["answer"])

    

@sb.type
class Mutation:

    @sb.mutation
    def get_mortgage_insights(self, context: str) -> MortgageLookupResponse:
        model_prediction = Prediction()
        income = model_prediction.extract_income(ModelInference(context=context, question="What is my income?"))
        savings = model_prediction.extract_savings(ModelInference(context=context, question="What are my savings?"))
        debt = model_prediction.extract_debt(ModelInference(context=context, question="What is my debt?"))
        return MortgageLookupResponse(income=income, savings=savings, debt=debt)



    @sb.mutation
    def calculate_max_mortgage(self, inputs: MortgageLookup) -> str:
        mortgage_score = calculate_mortage_score(
            inputs.income, inputs.savings, inputs.debt)
        end_range = get_mortgage_range_from_score(mortgage_score)
        return "You can borrow up to ${}".format(end_range)

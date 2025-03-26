from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI

class RecommendationGenerator:
    def __init__(self):
        """Initialize the recommendation generator with LLM components."""
        self.llm = ChatOpenAI(
            temperature=0.7,
            model_name="gpt-3.5-turbo",
        )
        
        self.recommendation_template = """
       For the MBTI personality type {mbti_type}, provide 3 highly tailored recommendations in each category:

        Music:
        - Recommend 3 artists/songs that perfectly match the {traits} personality
        - Provide a brief, compelling 1-sentence description for each recommendation

        Books:
        - Suggest 3 books that would deeply resonate with this personality type
        - Include a concise, intriguing description for each book recommendation

        Movies:
        - Select 3 films that capture the essence of this personality type
        - Write a short, vivid description highlighting why each movie would appeal to them

        Ensure recommendations are specific, engaging, and reflect the unique characteristics of {mbti_type}.
        Use an enthusiastic and personalized tone.
        """
        
        self.prompt = PromptTemplate(
            input_variables=["mbti_type", "traits"],
            template=self.recommendation_template
        )
        
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)
        
        # MBTI type traits mapping
        self.mbti_traits = {
            "ISTJ": "practical, detail-oriented, and traditional",
            "ISFJ": "nurturing, detail-focused, and service-oriented",
            "INFJ": "insightful, creative, and idealistic",
            "INTJ": "analytical, strategic, and independent",
            "ISTP": "logical, practical, and adaptable",
            "ISFP": "artistic, sensitive, and spontaneous",
            "INFP": "idealistic, empathetic, and creative",
            "INTP": "logical, innovative, and analytical",
            "ESTP": "energetic, practical, and spontaneous",
            "ESFP": "enthusiastic, spontaneous, and fun-loving",
            "ENFP": "enthusiastic, creative, and people-oriented",
            "ENTP": "innovative, entrepreneurial, and adaptable",
            "ESTJ": "organized, practical, and traditional",
            "ESFJ": "warm, practical, and people-oriented",
            "ENFJ": "charismatic, idealistic, and people-focused",
            "ENTJ": "strategic, logical, and efficient"
        }
    
    def generate_recommendations(self, mbti_type):
        """Generate personalized recommendations based on MBTI type."""
        if mbti_type not in self.mbti_traits:
            raise ValueError(f"Invalid MBTI type: {mbti_type}")
            
        traits = self.mbti_traits[mbti_type]
        
        # Generate recommendations using LLM
        result = self.chain.run(mbti_type=mbti_type, traits=traits)
        
        return result 
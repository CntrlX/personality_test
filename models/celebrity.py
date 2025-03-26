from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI

class CelebrityDoppelgangerGenerator:
    def __init__(self):
        """Initialize the celebrity doppelganger generator with LLM components."""
        self.llm = ChatOpenAI(
            temperature=0.7,
            model_name="gpt-3.5-turbo",
        )
        
        self.doppelganger_template = """
        For the MBTI personality type {mbti_type}, identify 3 celebrity doppelgangers that embody the {traits} characteristics:

        - Select celebrities who authentically represent the core traits of {mbti_type}
        - Provide a brief, insightful description that captures their personality essence
        - Highlight specific qualities that make them a quintessential match for this personality type

        Ensure the descriptions are nuanced, perceptive, and reveal the unique personality dimensions of each celebrity.
        Use a thoughtful and descriptive tone that goes beyond surface-level observations.
        """
        
        self.prompt = PromptTemplate(
            input_variables=["mbti_type", "traits"],
            template=self.doppelganger_template
        )
        
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)
        
        # MBTI type traits mapping (same as in recommendation generator)
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
    
    def find_doppelgangers(self, mbti_type):
        """Generate celebrity doppelgangers based on MBTI type."""
        if mbti_type not in self.mbti_traits:
            raise ValueError(f"Invalid MBTI type: {mbti_type}")
            
        traits = self.mbti_traits[mbti_type]
        
        # Generate doppelganger recommendations using LLM
        result = self.chain.run(mbti_type=mbti_type, traits=traits)
        
        return result

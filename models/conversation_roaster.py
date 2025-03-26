import os
import sys
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI

class PersonalityRoastGenerator:
    def __init__(self):
        """Initialize the personality roast generator with LLM components."""
        # Check for OpenAI API key
        if not os.environ.get("OPENAI_API_KEY"):
            print("ERROR: OPENAI_API_KEY environment variable is not set.")
            print("Please set it in the .env file or as an environment variable.")
            sys.exit(1)
        
        # Setup OpenAI model
        self.llm = ChatOpenAI(
            temperature=0.8,  # Higher temperature for more creative roasting
            model_name="gpt-3.5-turbo",
        )
        
        # Roast template with nuanced humor for each MBTI type
        self.roast_template = """
        Create a witty, good-humored roast that playfully highlights the stereotypical quirks of the {mbti_type} personality type.

        Consider these conversation details for personalization:
        Conversation Context: {conversation_context}

        Guidelines for the roast:
        - Keep it light-hearted and funny, not mean-spirited
        - Use clever wordplay and observational humor
        - Highlight the unique personality traits in a humorous way
        - Make it sound like a friendly, teasing joke a close friend might make
        - Aim for maximum comedic effect while maintaining respect

        Roast Format:
        A punchy, 3-4 sentence roast that captures the essence of {mbti_type} with humor and warmth.
        """
        
        # MBTI type roast characteristics
        self.mbti_roast_traits = {
            "ISTJ": "the overly serious, rule-following perfectionist",
            "ISFJ": "the people-pleasing, detail-obsessed caretaker",
            "INFJ": "the mysterious, overthinking idealist",
            "INTJ": "the know-it-all strategic mastermind",
            "ISTP": "the cool, detached problem-solving lone wolf",
            "ISFP": "the sensitive artist who's low-key dramatic",
            "INFP": "the dreamy, perpetually misunderstood poet",
            "INTP": "the absent-minded genius living in their head",
            "ESTP": "the adrenaline junkie who thinks rules are suggestions",
            "ESFP": "the party animal who's always the center of attention",
            "ENFP": "the enthusiastic idea machine with 1000 unfinished projects",
            "ENTP": "the argumentative devil's advocate who loves intellectual chaos",
            "ESTJ": "the bossy spreadsheet lover who runs everything",
            "ESFJ": "the social butterfly obsessed with everyone's approval",
            "ENFJ": "the charismatic life coach who wants to save the world",
            "ENTJ": "the ambitious bulldozer who sees life as a strategy game"
        }
        
        # Create prompt template
        self.prompt = PromptTemplate(
            input_variables=["mbti_type", "conversation_context"],
            template=self.roast_template
        )
        
        # Create LLM chain
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)
    
    def generate_roast(self, mbti_type, conversation, max_context_length=500):
        """
        Generate a personalized roast based on MBTI type and conversation context.
        
        Args:
            mbti_type (str): The MBTI personality type
            conversation (ConversationChain): The conversation chain to extract context
            max_context_length (int, optional): Maximum length of context to include. Defaults to 500.
        
        Returns:
            str: A humorous roast tailored to the MBTI type
        """
        if mbti_type not in self.mbti_roast_traits:
            raise ValueError(f"Invalid MBTI type: {mbti_type}")
        
        # Extract conversation context (truncate to avoid overwhelming the model)
        try:
            conversation_context = conversation.memory.chat_memory.messages[-5:]
            context_str = " ".join([msg.content for msg in conversation_context])
            context_str = context_str[:max_context_length]
        except Exception:
            context_str = "No specific context available"
        
        # Generate roast
        try:
            roast = self.chain.run(
                mbti_type=mbti_type, 
                conversation_context=context_str
            )
            return roast
        except Exception as e:
            print(f"Error generating roast: {e}")
            return f"Looks like a {mbti_type} can't even handle a good roast! 😉"

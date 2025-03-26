import os
import sys
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI

class CareerInsightsGenerator:
    def __init__(self):
        """Initialize the career insights generator with LLM components."""
        # Check for OpenAI API key
        if not os.environ.get("OPENAI_API_KEY"):
            print("ERROR: OPENAI_API_KEY environment variable is not set.")
            print("Please set it in the .env file or as an environment variable.")
            sys.exit(1)
        
        # Setup OpenAI model
        self.llm = ChatOpenAI(
            temperature=0.7,
            model_name="gpt-3.5-turbo",
        )
        
        # Career insights template
        self.insights_template = """
        Generate comprehensive career insights for the {mbti_type} personality type.

        Conversation Context: {conversation_context}

        Provide a detailed analysis covering:
        1. Workplace Dynamics: How this personality type approaches work, 
           their ideal work environment, and professional motivations
        2. Perfect Career Paths: Roles and industries that align with 
           their natural strengths and personality traits
        3. Specific Career Strengths
        4. Potential Career Challenges

        Key Considerations:
        - Reflect the unique characteristics of {mbti_type}
        - Incorporate insights from the conversation context
        - Be nuanced and avoid stereotyping
        - Provide actionable and empathetic insights

        Output Format:
        A JSON object with detailed career insights
        """
        
        # Predefined career insights for MBTI types
        self.career_insights = {
            "INTJ": {
                "workplace": "In the world of careers, you thrive on cognitive challenges but resist structured physical activity, suggesting you seek mental rather than physical flow states. Creative problem-solving energizes you, whether it's cracking code or capturing moments through a lens.",
                "perfect_career": "Those who work like you need constant intellectual stimulation and tend to dive deep into self-directed learning after hours. While you accept practical compromises for stability, you'll only find true fulfillment in roles that let you push boundaries and explore emerging technologies.",
                "strengths": [
                    "Analytical", "Determined", "Curious", 
                    "Focused", "Strategic", "Innovative"
                ],
                "weaknesses": [
                    "Perfectionist", "Restless", "Stubborn", 
                    "Hesitant", "Overly Critical", "Difficulty Collaborating"
                ],
                "ideal_careers": [
                    "Software Architect", 
                    "Research Scientist", 
                    "Strategic Consultant", 
                    "Technology Strategist", 
                    "Innovation Manager"
                ]
            },
            "INFJ": {
                "workplace": "You excel in environments that allow for deep, meaningful work with a clear purpose. Your intuitive nature helps you see complex systems and human dynamics that others might miss.",
                "perfect_career": "Your ideal career combines intellectual depth with human impact. You thrive in roles that allow you to create positive change, whether through counseling, writing, design, or strategic planning.",
                "strengths": [
                    "Empathetic", "Insightful", "Visionary", 
                    "Passionate", "Creative", "Purpose-Driven"
                ],
                "weaknesses": [
                    "Idealistic", "Sensitive", "Burnout-Prone", 
                    "Conflict-Avoidant", "Perfectionistic", "Overwhelmed"
                ],
                "ideal_careers": [
                    "Counselor", 
                    "Non-Profit Leader", 
                    "Social Worker", 
                    "Creative Director", 
                    "Educational Consultant"
                ]
            },
            # Add more MBTI types as needed
            "DEFAULT": {
                "workplace": "You approach professional environments with a unique blend of your personality traits, seeking roles that align with your core values and personal growth.",
                "perfect_career": "Your career path is characterized by continuous learning, adaptability, and a drive to make meaningful contributions in your chosen field.",
                "strengths": [
                    "Adaptable", "Passionate", "Committed", 
                    "Innovative", "Thoughtful"
                ],
                "weaknesses": [
                    "Complex", "Challenging", "Evolving", 
                    "Introspective", "Nuanced"
                ],
                "ideal_careers": [
                    "Versatile Professional", 
                    "Adaptive Specialist", 
                    "Innovative Contributor"
                ]
            }
        }
        
        # Create prompt template
        self.prompt = PromptTemplate(
            input_variables=["mbti_type", "conversation_context"],
            template=self.insights_template
        )
        
        # Create LLM chain
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)
    
    def generate_career_insights(self, mbti_type, conversation, max_context_length=500):
        """
        Generate career insights for a specific MBTI type.
        
        Args:
            mbti_type (str): The MBTI personality type
            conversation (ConversationChain): The conversation chain to extract context
            max_context_length (int, optional): Maximum length of context to include. Defaults to 500.
        
        Returns:
            dict: Detailed career insights
        """
        # Extract conversation context
        try:
            conversation_context = conversation.memory.chat_memory.messages[-5:]
            context_str = " ".join([msg.content for msg in conversation_context])
            context_str = context_str[:max_context_length]
        except Exception:
            context_str = "No specific context available"
        
        # Use predefined insights or default
        insights = self.career_insights.get(mbti_type, self.career_insights["DEFAULT"])
        
        # Try to generate more personalized insights using LLM
        try:
            llm_result = self.chain.run(
                mbti_type=mbti_type, 
                conversation_context=context_str
            )
            # Additional processing of LLM result could be added here
        except Exception as e:
            print(f"LLM insights generation failed: {e}")
        
        return insights
    
    def format_career_insights(self, insights):
        """
        Format the career insights into a readable output.
        
        Args:
            insights (dict): Dictionary of career insights
        
        Returns:
            str: Formatted career insights
        """
        # Format insights
        output = "**Career**\n"
        output += "**Your workplace**\n"
        output += f"{insights['workplace']}\n\n"
        
        output += "**Your perfect career**\n"
        output += f"{insights['perfect_career']}\n\n"
        
        # Format strengths and weaknesses
        output += "**Strengths and weaknesses**\n"
        
        # Strengths
        for strength in insights['strengths']:
            output += f"**{strength}**\n"
        
        # Weaknesses
        for weakness in insights['weaknesses']:
            output += f"**{weakness}**\n"
        
        return output
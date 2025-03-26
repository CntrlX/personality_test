import os
import sys
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI

class RelationshipInsightsGenerator:
    def __init__(self):
        """Initialize the relationship insights generator with LLM components."""
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
        
        # Relationship insights template
        self.insights_template = """
        Generate comprehensive relationship insights for the {mbti_type} personality type.

        Conversation Context: {conversation_context}

        Provide a detailed analysis covering:
        1. Relationship Summary: How this personality type approaches relationships, 
           their core needs, communication style, and emotional landscape
        2. Specific Strengths in Relationships
        3. Potential Challenges in Relationships

        Key Considerations:
        - Reflect the unique characteristics of {mbti_type}
        - Incorporate insights from the conversation context
        - Be nuanced and avoid stereotyping
        - Provide actionable and empathetic insights

        Output Format:
        A JSON object with detailed relationship insights
        """
        
        # Predefined relationship insights for MBTI types
        self.relationship_insights = {
            "INTJ": {
                "summary": "You gravitate towards intellectual pursuits and find comfort in structured, analytical environments. In relationships, you seek partners who can match your depth of curiosity while accepting your need for mental stimulation over physical activity. Your perfectionist tendencies extend beyond work into personal goals, but you maintain a healthy self-image despite acknowledging areas for improvement.",
                "strengths": [
                    "Accepting", "Patient", "Authentic", 
                    "Observant", "Loyal", "Supportive"
                ],
                "weaknesses": [
                    "Reserved", "Distant", "Self-conscious", 
                    "Analytical", "Perfectionistic", "Challenging to read"
                ]
            },
            "INFJ": {
                "summary": "You seek deep, meaningful connections that transcend surface-level interactions. Relationships for you are about emotional depth, mutual growth, and shared values. You're naturally intuitive, often sensing your partner's unspoken needs while maintaining a delicate balance between empathy and personal boundaries.",
                "strengths": [
                    "Empathetic", "Insightful", "Supportive", 
                    "Compassionate", "Deep", "Committed"
                ],
                "weaknesses": [
                    "Idealistic", "Sensitive", "Overanalyzing", 
                    "People-pleasing", "Conflict-avoidant", "Emotionally intense"
                ]
            },
            # Add more MBTI types as needed
            "DEFAULT": {
                "summary": "You approach relationships with a unique blend of your personality traits, seeking connections that align with your core values and personal growth. Your approach to partnerships is nuanced, balancing emotional needs with individual aspirations.",
                "strengths": [
                    "Authentic", "Caring", "Adaptable", 
                    "Committed", "Understanding"
                ],
                "weaknesses": [
                    "Complex", "Challenging", "Nuanced", 
                    "Evolving", "Introspective"
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
    
    def generate_relationship_insights(self, mbti_type, conversation, max_context_length=500):
        """
        Generate relationship insights for a specific MBTI type.
        
        Args:
            mbti_type (str): The MBTI personality type
            conversation (ConversationChain): The conversation chain to extract context
            max_context_length (int, optional): Maximum length of context to include. Defaults to 500.
        
        Returns:
            dict: Detailed relationship insights
        """
        # Extract conversation context
        try:
            conversation_context = conversation.memory.chat_memory.messages[-5:]
            context_str = " ".join([msg.content for msg in conversation_context])
            context_str = context_str[:max_context_length]
        except Exception:
            context_str = "No specific context available"
        
        # Use predefined insights or default
        insights = self.relationship_insights.get(mbti_type, self.relationship_insights["DEFAULT"])
        
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
    
    def format_relationship_insights(self, insights):
        """
        Format the relationship insights into a readable output.
        
        Args:
            insights (dict): Dictionary of relationship insights
        
        Returns:
            str: Formatted relationship insights
        """
        # Format summary
        output = "**Relationships**\n"
        output += "**Summary**\n"
        output += f"{insights['summary']}\n\n"
        
        # Format strengths and weaknesses
        output += "**Strengths and weaknesses**\n"
        
        # Strengths
        for strength in insights['strengths']:
            output += f"**{strength}**\n"
        
        # Weaknesses
        for weakness in insights['weaknesses']:
            output += f"**{weakness}**\n"
        
        return output
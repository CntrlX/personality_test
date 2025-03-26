import json
import os
import sys
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI

class PersonalityTraitsAnalyzer:
    def __init__(self):
        """Initialize the personality traits analyzer with LLM components."""
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
        
        # Traits analysis template
        self.traits_template = """
        Analyze the conversation context and MBTI type to generate a comprehensive 
        five-factor personality model (Big Five) breakdown.

        MBTI Type: {mbti_type}
        Conversation Context: {conversation_context}

        For each of the following traits, provide:
        1. A percentage score (0-100%)
        2. A descriptive label
        3. 3 specific descriptors that capture the essence of the trait

        Traits to analyze:
        - Extraversion
        - Openness
        - Conscientiousness
        - Agreeableness
        - Neuroticism

        Ensure the analysis is:
        - Nuanced and specific to the individual
        - Based on the conversation details
        - Reflective of both the MBTI type and conversation context
        - Providing insightful, personalized observations

        Output Format:
        A JSON object with detailed trait breakdowns
        """
        
        # MBTI to Big Five trait tendencies mapping
        self.mbti_trait_mapping = {
            "ISTJ": {
                "Extraversion": (30, "Introverted", "Reserved, Focused, Independent"),
                "Openness": (40, "Practical", "Conventional, Detail-oriented, Systematic"),
                "Conscientiousness": (95, "Highly Conscientious", "Organized, Disciplined, Meticulous"),
                "Agreeableness": (70, "Cooperative", "Supportive, Loyal, Considerate"),
                "Neuroticism": (40, "Stable", "Calm, Composed, Resilient")
            },
            "INTJ": {
                "Extraversion": (35, "Introverted", "Strategic, Analytical, Independent"),
                "Openness": (90, "Highly Open", "Innovative, Intellectual, Curious"),
                "Conscientiousness": (85, "Very Conscientious", "Precise, Goal-oriented, Systematic"),
                "Agreeableness": (50, "Balanced", "Critical, Direct, Objective"),
                "Neuroticism": (45, "Moderately Stable", "Controlled, Introspective, Measured")
            },
            # Add mappings for other MBTI types...
            # DEFAULT mapping for types not specifically defined
            "DEFAULT": {
                "Extraversion": (50, "Moderate", "Balanced, Adaptable, Flexible"),
                "Openness": (60, "Moderately Open", "Curious, Creative, Receptive"),
                "Conscientiousness": (65, "Somewhat Conscientious", "Responsible, Organized, Reliable"),
                "Agreeableness": (60, "Moderately Agreeable", "Kind, Cooperative, Supportive"),
                "Neuroticism": (50, "Average", "Emotionally Balanced, Adaptable, Resilient")
            }
        }
        
        # Create prompt template
        self.prompt = PromptTemplate(
            input_variables=["mbti_type", "conversation_context"],
            template=self.traits_template
        )
        
        # Create LLM chain
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)
    
    def analyze_personality_traits(self, mbti_type, conversation, max_context_length=500):
        """
        Generate a detailed personality traits analysis.
        
        Args:
            mbti_type (str): The MBTI personality type
            conversation (ConversationChain): The conversation chain to extract context
            max_context_length (int, optional): Maximum length of context to include. Defaults to 500.
        
        Returns:
            dict: A detailed breakdown of personality traits
        """
        # Extract conversation context
        try:
            conversation_context = conversation.memory.chat_memory.messages[-5:]
            context_str = " ".join([msg.content for msg in conversation_context])
            context_str = context_str[:max_context_length]
        except Exception:
            context_str = "No specific context available"
        
        # Use predefined mapping if available, otherwise use default
        trait_base = self.mbti_trait_mapping.get(mbti_type, self.mbti_trait_mapping["DEFAULT"])
        
        # Try to generate more personalized traits using LLM
        try:
            llm_result = self.chain.run(
                mbti_type=mbti_type, 
                conversation_context=context_str
            )
            # Attempt to parse LLM result and refine traits
            try:
                parsed_traits = json.loads(llm_result)
                # Merge or override base traits with LLM insights
                for trait in trait_base:
                    if trait in parsed_traits:
                        trait_base[trait] = parsed_traits[trait]
            except (json.JSONDecodeError, TypeError):
                # If parsing fails, keep base traits
                pass
        except Exception as e:
            print(f"LLM trait generation failed: {e}")
        
        return trait_base
    
    def format_traits_output(self, traits):
        """
        Format the traits analysis into a readable string.
        
        Args:
            traits (dict): Dictionary of personality traits
        
        Returns:
            str: Formatted traits output
        """
        formatted_output = []
        for trait, (percentage, label, descriptors) in traits.items():
            trait_output = (
                f"**{percentage}%**\n"
                f"**{label}**\n"
                f"**{descriptors}**"
            )
            formatted_output.append(trait_output)
        
        return "\n\n".join(formatted_output)
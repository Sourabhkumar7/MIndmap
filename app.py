import openai
from educhain import Educhain
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv("key.env")
openai.api_key = os.getenv('OPENAI_API_KEY')
client = Educhain()

st.title("Mind Map Generator")
st.write("Generate a mind map for a given topic using Educhain and OpenAI.")
topic = st.text_input("Enter the topic for the lesson plan:", "Newton's Laws of Motion")

if st.button("Generate Mind Map"):
    
    st.info("Generating lesson plan...")
    try:
        lesson_plan = client.content_engine.generate_lesson_plan(topic=topic)
        plan_data = lesson_plan.json()

        
        st.info("Generating mind map using OpenAI...")
        prompt = f"""
        You are an assistant that structures content into a mind map.
        Here is a lesson plan on "{topic}": {plan_data}

        Convert this lesson plan into a hierarchical structure for a mind map:
        - Main topic
          - Subtopic 1
            - Supporting details
          - Subtopic 2
            - Supporting details
        """
        
       
        client=OpenAI()
        response = client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1500,
        temperature=0.1
        )
        
        mind_map = response["choices"][0]["message"]["content"].strip()
        st.subheader("Generated Mind Map")
        st.text_area("Mind Map Structure", mind_map, height=300)
    except Exception as e:
        st.error(f"An error occurred: {e}")

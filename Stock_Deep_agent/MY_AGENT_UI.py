import streamlit as st


# Core agent functions relevant for solo developer
def idea_generation_agent():
    return "Innovative business ideas generated successfully!"


def marketing_ideas_agent():
    return "Creative marketing strategies ready!"


def sales_boost_agent():
    return "Upsell and churn-kill tactics applied successfully!"


def financial_advice_agent():
    return "Your financial plan is on track."


def product_development_agent():
    return "Product development roadmap and feature planning ready."


def customer_support_agent():
    return "Customer support best practices and ticket resolution insights."


agents = [
    ('Idea Generation', idea_generation_agent),
    ('Marketing Ideas', marketing_ideas_agent),
    ('Sales Boost Ideas', sales_boost_agent),
    ('Financial Advice', financial_advice_agent),
    ('Product Development', product_development_agent),
    ('Customer Support', customer_support_agent),
]


# CSS for styling and layout with updated gradient
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #ffffff, #4326fc);
        background-size: 600% 600%;
        animation: GradientAnimation 15s ease infinite;
        min-height: 100vh;
        color: white;
        padding: 2rem 3rem;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    @keyframes GradientAnimation {
        0%{background-position:0% 50%}
        50%{background-position:100% 50%}
        100%{background-position:0% 50%}
    }
    .stApp > div[data-testid="stVerticalBlock"] {
        background: rgba(255,255,255,0.1);
        border-radius: 15px;
        padding: 1.5rem 2rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.18);
    }
    div.stButton > button {
        height: 55px;
        width: 100%;
        font-size: 16px;
        margin: 8px 0;
        border-radius: 10px;
        background: linear-gradient(90deg, #a4508b, #5f0a87);
        color: white;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(101, 41, 131, 0.4);
        transition: background 0.3s ease, box-shadow 0.3s ease;
    }
    div.stButton > button:hover {
        background: linear-gradient(90deg, #5f0a87, #a4508b);
        box-shadow: 0 6px 20px rgba(101, 41, 131, 0.7);
        cursor: pointer;
    }
    
    .stSuccess {
        margin-top: 6px;
        margin-bottom: 12px;
        font-size: 14px !important;
    }
</style>
""", unsafe_allow_html=True)


st.title('Business Support Agents')


cols = st.columns(3)
for i, (label, func) in enumerate(agents):
    col = cols[i % 3]
    with col:
        if st.button(label, key=label):
            message = func()
            st.success(message)

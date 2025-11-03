# First, install dependencies in your venv (activate it first):
# pip install langchain langchain-community langchain-openai yfinance tensorflow scikit-learn

import os
from typing import Optional
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from tensorflow.keras.models import load_model
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain import hub

# Set your OpenAI API key (get one from https://platform.openai.com/account/api-keys)
os.environ["OPENAI_API_KEY"] = ""

# Assume you have saved the LSTM model from previous code as 'lstm_model.h5'
# If not, train and save it first using the earlier script.

@tool
def get_stock_data(symbol: str, period: str = "2y") -> str:
    """Fetch historical stock data for a given symbol and period (e.g., '1y', '2y')."""
    try:
        data = yf.download(symbol, period=period)
        if data.empty:
            return f"No data found for {symbol}"
        return data['Close'].tail(10).to_dict()  # Return last 10 closing prices as dict
    except Exception as e:
        return f"Error fetching data: {str(e)}"

@tool
def predict_stock_price(symbol: str, days_ahead: int = 1) -> str:
    """Predict future stock price using the pre-trained LSTM model. Provide symbol and days to predict ahead."""
    try:
        # Fetch recent data (last 1 year for training/prediction context)
        data = yf.download(symbol, period="1y")['Close'].values.reshape(-1, 1)
        
        # Normalize
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(data)
        
        # Prepare input (use last 60 days as in previous model)
        time_step = 60
        if len(scaled_data) < time_step + days_ahead:
            return "Insufficient data for prediction."
        
        X = scaled_data[-time_step:].reshape(1, time_step, 1)
        
        # Load model and predict
        model = load_model('lstm_model.h5')
        prediction_scaled = model.predict(X)
        prediction = scaler.inverse_transform(prediction_scaled)[0][0]
        
        current_price = data[-1][0]
        return f"Current price for {symbol}: ${current_price:.2f}. Predicted price {days_ahead} day(s) ahead: ${prediction:.2f}"
    except Exception as e:
        return f"Error in prediction: {str(e)}"

# LLM setup (using OpenAI; replace with other providers if needed)
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Pull the prompt from LangChain hub (or define custom)
prompt = hub.pull("hwchase17/openai-functions-agent")  # Basic agent prompt for tool calling

# Create the agent
tools = [get_stock_data, predict_stock_price]
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Example usage
if __name__ == "__main__":
    query = "Predict the price of AAPL for 1 day ahead."
    response = agent_executor.invoke({"input": query})
    print(response['output'])
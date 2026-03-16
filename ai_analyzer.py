import requests
import json
from typing import List, Dict
import os
class AINewsAnalyzer:
    """Analyze news using AI/LLM to determine market impact"""
    
    def __init__(self, api_key: str, llm_endpoint: str):
        self.api_key = os.getenv('API_KEY')
        self.llm_endpoint = os.getenv('LLM_ENDPOINT')
    
    def analyze_news(self, news_list: List[Dict]) -> Dict:
        """Send news to AI for analysis"""
        
        # Prepare news summary for AI
        news_text = self._prepare_news_for_ai(news_list)
        
        # Create prompt
        prompt = f"""You are an expert Indian stock market analyst. Analyze the following news articles and provide:

1. **MARKET IMPACT**: How will these news affect BSE/NSE? (Positive/Negative/Neutral)
2. **AFFECTED SECTORS**: Which sectors will be most impacted? (IT, Banking, Pharma, Auto, etc.)
3. **SPECIFIC STOCKS**: Any specific companies mentioned that will be affected?
4. **SENTIMENT SCORE**: Rate overall market sentiment (1-10, where 1=Very Bearish, 10=Very Bullish)
5. **KEY INSIGHTS**: Top 3-5 key takeaways for investors
6. **SUMMARY**: Brief 3-4 sentence summary of market outlook

NEWS ARTICLES:
{news_text}

Provide response in JSON format:
{{
    "market_impact": "Positive/Negative/Neutral",
    "sentiment_score": 5,
    "affected_sectors": ["IT", "Banking"],
    "specific_stocks": ["TCS", "HDFC Bank"],
    "key_insights": ["point 1", "point 2"],
    "summary": "brief summary here",
    "detailed_analysis": "detailed analysis here"
}}"""
        
        # Call AI API
        try:
            response = self._call_llm(prompt)
            return self._parse_ai_response(response)
        except Exception as e:
            print(f"AI Analysis Error: {e}")
            return self._fallback_analysis(news_list)
    
    def _prepare_news_for_ai(self, news_list: List[Dict]) -> str:
        """Format news for AI input"""
        news_text = ""
        for idx, news in enumerate(news_list[:15], 1):  # Limit to 15 for token efficiency
            news_text += f"\n{idx}. {news['title']}\n"
            news_text += f"   Source: {news['source']}\n"
            news_text += f"   {news['description'][:200]}\n"
        return news_text
    
    def _call_llm(self, prompt: str) -> str:
        """Call LLM API endpoint"""
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        
        payload = {
            'model': 'gpt-4',  # or your model name
            'messages': [
                {'role': 'system', 'content': 'You are an expert Indian stock market analyst.'},
                {'role': 'user', 'content': prompt}
            ],
            'temperature': 0.3,
            'max_tokens': 2000
        }
        
        response = requests.post(self.llm_endpoint, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        return result['choices'][0]['message']['content']
    
    def _parse_ai_response(self, response: str) -> Dict:
        """Parse AI response to structured format"""
        try:
            # Extract JSON from response
            start = response.find('{')
            end = response.rfind('}') + 1
            json_str = response[start:end]
            return json.loads(json_str)
        except:
            # If JSON parsing fails, return text response
            return {
                'market_impact': 'Neutral',
                'sentiment_score': 5,
                'affected_sectors': [],
                'specific_stocks': [],
                'key_insights': [],
                'summary': response[:500],
                'detailed_analysis': response
            }
    
    def _fallback_analysis(self, news_list: List[Dict]) -> Dict:
        """Fallback analysis if AI fails"""
        return {
            'market_impact': 'Neutral',
            'sentiment_score': 5,
            'affected_sectors': ['General Market'],
            'specific_stocks': [],
            'key_insights': [
                f'Total {len(news_list)} news articles analyzed',
                'AI analysis unavailable - using fallback mode'
            ],
            'summary': f'Analyzed {len(news_list)} news articles from Indian financial sources.',
            'detailed_analysis': 'AI analysis service is currently unavailable.'
        }
    
    def categorize_by_impact(self, news_list: List[Dict], analysis: Dict) -> Dict:
        """Categorize news by market impact"""
        categories = {
            'high_impact': [],
            'sector_specific': [],
            'company_specific': [],
            'general': []
        }
        
        high_impact_keywords = ['rbi', 'sebi', 'government', 'policy', 'budget', 'gdp', 'inflation', 'rate']
        sector_keywords = ['banking', 'it', 'pharma', 'auto', 'metal', 'fmcg', 'telecom', 'energy']
        
        for news in news_list:
            text = (news['title'] + ' ' + news['description']).lower()
            
            if any(keyword in text for keyword in high_impact_keywords):
                categories['high_impact'].append(news)
            elif any(keyword in text for keyword in sector_keywords):
                categories['sector_specific'].append(news)
            elif any(stock in text for stock in analysis.get('specific_stocks', [])):
                categories['company_specific'].append(news)
            else:
                categories['general'].append(news)
        
        return categories
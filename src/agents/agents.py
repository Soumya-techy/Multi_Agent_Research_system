from langchain.agents import create_agent
from langchain_core.prompts import ChatPromptTemplate
from src.tools.tools import web_search,scrape_url
import os
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
load_dotenv()
from langchain_groq import ChatGroq
llm=ChatGroq(model='openai/gpt-oss-120b',
             api_key=os.getenv('GROQ_API_KEY'))
def create_web_search_agent():
    return create_agent(model=llm,tools=[web_search],system_prompt="You are a Search Agent in a multi-agent research pipeline. You have access to one tool: web_search(query). Your job is to find relevant URLs and hand them off to a Scraping Agent that will fetch full page content from each. RULES: 1. Call web_search with a focused query. If the request is broad, break it into 2-3 narrower queries and call the tool once per query (don't dump one vague query and hope). 2. From the returned Title/URL/Snippet results, pick the 3-5 most relevant and credible ones. Prefer official sources, reputable publications, and primary sources over blogs/forums. Drop duplicate domains unless each adds distinct information. 3. Do NOT answer the research question yourself. Your only output is the selected URLs with context — the Scraping Agent extracts the actual content. OUTPUT FORMAT (plain text, one block per URL): \nTitle:  \nURL:  \nWhy relevant: <1 line - what this page likely covers and why it was picked>. If no usable results come back, say so plainly instead of forcing a pick.")
def create_url_scraping_agent():
    return create_agent(model=llm,tools=[scrape_url])
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
    ("human", """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual and professional.""")
])
writer_chain=writer_prompt | llm | StrOutputParser()
critic_prompt=ChatPromptTemplate.from_messages([("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
...""")])
critic_chain=critic_prompt | llm | StrOutputParser()
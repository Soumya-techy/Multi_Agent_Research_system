from src.agents.agents import create_web_search_agent,create_url_scraping_agent,writer_chain,critic_chain
def research_pipeline(topic:str):
    state={}
    print('\n'+'='*50)
    print('Web search agent is working...')
    print('='*50)
    web_search=create_web_search_agent()
    result1=web_search.invoke({'messages':['human',f"Find recent, reliable and detailed information about: {topic}"]})
    state['search_results']=result1['messages'][-1].content

    print('\n'+'='*50)
    print('Web scraping agent is working...')
    print('='*50)
    web_scrap=create_url_scraping_agent()
    result2=web_scrap.invoke({'messages':['human',f"Based on the following search result about {topic}. \npick the most relevant URL and scrape it for deeper content. \n Search Results: {state['search_results']}"]})
    state['scraped_content']=result2['messages'][-1].content

    print('\n'+'='*50)
    print('Writing agent is working...')
    print('='*50)
    research_combined=(f"Searched results: {state['search_results']}",
                       f"Detailed Scraped content: {state['scraped_content']}")
    state['report']=writer_chain.invoke({'topic':topic,'research':research_combined})

    print('\n'+'='*50)
    print('Critic agent is working...')
    print('='*50)
    state['feedback']=critic_chain.invoke({'report':state['report']})
    return state
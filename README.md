# Multi-Agent Research System

An open-source research assistant that turns a topic into a structured research report through a focused, four-stage agent workflow. It searches the web, extracts readable page content, writes a report, and then asks a dedicated critic to evaluate the result.

The project is built with LangChain, Groq, Tavily, and Streamlit.

## Features

- **Specialized agent workflow** — separate search, scraping, writing, and critique stages.
- **Web search with Tavily** — gathers up to five results per focused query and asks the search agent to select the most useful, credible sources.
- **Resilient content extraction** — attempts extraction with Trafilatura, Readability, and BeautifulSoup fallbacks.
- **Structured reports** — creates an introduction, key findings, conclusion, and source list.
- **Quality review** — scores the generated report and returns strengths, improvement areas, and a concise verdict.
- **Streamlit UI** — inspect the report, critic feedback, selected sources, raw scraped content, and download a Markdown copy.

## How it works

```text
Research topic
     |
     v
Search agent ── Tavily search ──> Selected source URLs
     |
     v
Scraping agent ── Trafilatura / Readability / BeautifulSoup ──> Clean page content
     |
     v
Writer chain (Groq LLM) ──> Structured research report
     |
     v
Critic chain (Groq LLM) ──> Score, strengths, improvements, verdict
```

### Pipeline stages

1. **Search** — The search agent turns the requested topic into focused searches, evaluates Tavily results, and returns selected URLs with brief relevance notes.
2. **Scrape** — The scraping agent selects a relevant URL and uses the scraping tool to extract readable text. Extracted content is capped at 5,000 characters.
3. **Write** — The writer receives both the selected sources and extracted content and produces a detailed report.
4. **Critique** — The critic reviews the report and returns a score out of 10, strengths, areas to improve, and a one-line verdict.

## Tech stack

| Area | Technology |
| --- | --- |
| Agent orchestration | LangChain |
| LLM provider | Groq (`openai/gpt-oss-120b`) |
| Web search | Tavily |
| Content extraction | Trafilatura, Readability-LXML, BeautifulSoup |
| Web interface | Streamlit |

## Prerequisites

- Python 3.9 or later
- A [Groq API key](https://console.groq.com/keys)
- A [Tavily API key](https://app.tavily.com/)

## Getting started

### 1. Clone the repository

```bash
git clone https://github.com/Soumya-techy/Multi_Agent_Research_system.git
cd Multi_Agent_Research_system
```

### 2. Create and activate a virtual environment

<details>
<summary>Windows (PowerShell)</summary>

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

</details>

<details>
<summary>macOS / Linux</summary>

```bash
python3 -m venv .venv
source .venv/bin/activate
```

</details>

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Configure API keys

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

`load_dotenv()` reads these values when the agents and tools are initialized. Keep `.env` private; it is already excluded by `.gitignore`.

### 5. Start the application

```bash
streamlit run app.py
```

Open the local URL printed by Streamlit, enter a topic, and select **Start research**. A completed run remains visible in the page while you inspect its outputs or download the report.

## Project structure

```text
Multi_Agent_Research_system/
├── app.py                     # Streamlit interface and report viewer
├── requirements.txt           # Python dependencies
├── src/
│   ├── agents/
│   │   └── agents.py           # Search/scraping agents plus writer and critic chains
│   ├── pipelines/
│   │   └── pipelines.py        # Four-stage research orchestration
│   └── tools/
│       └── tools.py            # Tavily search and multi-strategy URL scraper
├── LICENSE                     # Apache License 2.0
└── .gitignore
```

## Output

Each run returns a dictionary with the following fields:

| Field | Description |
| --- | --- |
| `search_results` | Source titles, URLs, snippets, and relevance notes selected by the search agent. |
| `scraped_content` | Text returned by the scraper for the selected page. |
| `report` | The generated research report. |
| `feedback` | The critic's score and review of the report. |

## Troubleshooting

### `ModuleNotFoundError: No module named 'langchain'`

Streamlit is using a Python environment that does not contain the project dependencies. Activate the project virtual environment and reinstall the requirements:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Using `python -m streamlit` ensures that Streamlit uses the same interpreter where the packages were installed.

### API key or authentication errors

Verify that both `GROQ_API_KEY` and `TAVILY_API_KEY` are present in `.env`, contain no quotes unless the key itself requires them, and that your accounts have active API access.

### A page cannot be scraped

Some pages block automated requests, require authentication, or render their content only in JavaScript. The scraper returns an error message or whatever readable content its fallback strategies can obtain; try a more accessible source or refine the topic.

## Limitations

- The scraper works on one URL selected by the scraping agent per run.
- Search and generated reports can contain inaccuracies; verify important claims against the cited source pages.
- Access-restricted, paywalled, JavaScript-heavy, or bot-protected sites may not yield usable content.

## Contributing

Contributions are welcome. To propose a change:

1. Fork the repository and create a feature branch.
2. Keep changes focused and describe the motivation in your pull request.
3. Test the Streamlit workflow and any modified pipeline behavior before opening the pull request.

Ideas for contributions include improving source selection, supporting multiple scraped URLs, adding report citations, and making progress updates more granular.

## License

This project is licensed under the [Apache License 2.0](LICENSE).

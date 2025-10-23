# AI Multi-Agent Deal Finder

An intelligent deal-finding system that uses multiple AI agents to scan RSS feeds, analyze product deals, estimate market values, and identify profitable opportunities. The system features a web dashboard built with Streamlit for easy interaction and visualization.

## 🎯 Overview

This project implements a multi-agent AI system that:
- **Scans RSS feeds** for product deals from various sources
- **Analyzes deals** using AI to extract product descriptions and prices
- **Estimates market values** using machine learning models
- **Identifies profitable opportunities** where deals offer significant discounts
- **Provides notifications** for high-value opportunities
- **Visualizes data** through an interactive web dashboard

## 🏗️ Architecture

The system consists of several specialized AI agents:

- **Planning Agent**: Orchestrates the entire workflow
- **Scanner Agent**: Scans RSS feeds and extracts deal information
- **Ensemble Agent**: Estimates product values using multiple ML models
- **Messaging Agent**: Sends notifications for profitable deals
- **Frontier Agent**: Handles advanced deal analysis
- **Specialist Agent**: Provides domain-specific expertise

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Hugging Face token (optional, for advanced models)
- Twilio credentials (optional, for SMS notifications)
- Pushover credentials (optional, for push notifications)

### Demo

*Interactive Streamlit dashboard showing real-time deal analysis and opportunity tracking*

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/MarwanAshraf22/AI-Multi-Agent-Deal-Finder.git
   cd "AI Multi-Agent Deal Finder"
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   If you don't have a requirements.txt file, install the core dependencies:
   ```bash
   pip install openai chromadb streamlit pandas plotly numpy scikit-learn beautifulsoup4 feedparser requests python-dotenv twilio pydantic tqdm
   ```

3. **Set up environment variables**
   
   Copy the example environment file and fill in your values:
   ```bash
   cp env.example .env
   ```
   
   Edit `.env` with your actual API keys and credentials:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   HF_TOKEN=your_huggingface_token_here
   TWILIO_ACCOUNT_SID=your_twilio_sid_here
   TWILIO_AUTH_TOKEN=your_twilio_auth_token_here
   TWILIO_FROM=your_twilio_phone_number
   MY_PHONE_NUMBER=your_phone_number
   PUSHOVER_USER=your_pushover_user
   PUSHOVER_TOKEN=your_pushover_token
   ```

## 🎮 Usage

### Web Dashboard 

Launch the interactive Streamlit dashboard:

```bash
streamlit run deal_agent_streamlit.py
```

The dashboard provides:
- **Real-time deal scanning** with a single click
- **Interactive visualizations** of product embeddings
- **Opportunity tracking** with detailed metrics
- **Export functionality** for deal data
- **Memory management** tools


## 📊 Features

### Deal Scanning
- Monitors multiple RSS feeds from deal sites
- Extracts product descriptions and prices
- Filters out low-quality or unclear deals
- Avoids duplicate processing

### AI-Powered Analysis
- Uses GPT-4 to analyze deal descriptions
- Estimates market values using ensemble methods
- Calculates discount percentages
- Identifies high-value opportunities

### Data Visualization
- 3D t-SNE visualization of product embeddings
- Category distribution charts
- Discount trend analysis
- Interactive opportunity explorer

### Notification System
- SMS alerts via Twilio (optional)
- Push notifications via Pushover (optional)
- Configurable discount thresholds
- Smart filtering to avoid spam

## 🔧 Configuration

### Deal Thresholds
Modify the minimum discount threshold in `agents/planning_agent.py`:
```python
DEAL_THRESHOLD = 50  # Minimum discount in dollars
```

### RSS Feeds
Add or modify RSS feeds in `agents/deals.py`:
```python
feeds = [
    "https://www.dealnews.com/c142/Electronics/?rss=1",
    "https://www.dealnews.com/c39/Computers/?rss=1",
    # Add more feeds here
]
```

### Model Settings
Adjust AI model parameters in the respective agent files:
- Scanner Agent: `agents/scanner_agent.py`
- Ensemble Agent: `agents/ensemble_agent.py`

## 📁 Project Structure

```
AI Multi-Agent Deal Finder/
├── agents/                    # AI agent implementations
│   ├── agent.py              # Base agent class
│   ├── deals.py              # Deal data models and RSS scraping
│   ├── ensemble_agent.py     # Value estimation agent
│   ├── frontier_agent.py     # Advanced analysis agent
│   ├── messaging_agent.py   # Notification agent
│   ├── planning_agent.py     # Workflow orchestration
│   ├── random_forest_agent.py # ML model agent
│   ├── scanner_agent.py      # Deal scanning agent
│   └── specialist_agent.py   # Domain expertise agent
├── deal_agent_framework.py   # Core framework
├── deal_agent_streamlit.py   # Web dashboard
├── days/                     # Development notebooks
│   └── day*.ipynb           # Daily development files
├── pricer_service*.py        # Modal deployment services
├── items.py                  # Product item models
├── testing.py               # Testing utilities
└── README.md                # This file
```

## 🛠️ Advanced Usage

### Modal Deployment

The project includes Modal deployment configurations for cloud-based pricing services:

```bash
# Deploy pricing service
modal deploy pricer_service.py

# Deploy ephemeral pricing service
modal deploy pricer_ephemeral.py
```

### Custom Models

Train your own pricing models using the Jupyter notebooks:
1. Start with `days/day2.0.ipynb` for data preparation
2. Use `days/day2.1.ipynb` through `days/day2.4.ipynb` for model training
3. Deploy using the Modal services

### Memory Management

The system maintains a persistent memory of opportunities:
- Stored in `memory.json`
- Automatically updated with new findings
- Can be cleared via the dashboard or manually

## 🐛 Troubleshooting

### Common Issues

1. **OpenAI API Errors**
   - Verify your API key is correct
   - Check your API usage limits
   - Ensure you have sufficient credits

2. **ChromaDB Issues**
   - Delete the `products_vectorstore` folder to reset
   - Check disk space availability

3. **RSS Feed Errors**
   - Some feeds may be temporarily unavailable
   - Check your internet connection
   - Verify feed URLs are still active

4. **Memory Issues**
   - Clear the `memory.json` file if corrupted
   - Use the dashboard's clear memory function

### Performance Optimization

- Adjust the number of deals processed per run
- Modify RSS feed update frequency
- Use smaller embedding models for faster processing
- Enable GPU acceleration for ML models

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenAI for GPT-4 API access
- Hugging Face for model hosting
- DealNews for RSS feed data
- Streamlit for the web dashboard framework
- Modal for cloud deployment infrastructure

## 📞 Support

For questions or issues:
1. Check the troubleshooting section above
2. Review the Jupyter notebooks for implementation details
3. Open an issue on GitHub
4. Contact the development team

---


# AI-Powered SQL Agent

A sophisticated, intelligent SQL Agent that leverages advanced AI models to transform natural language queries into executable SQL statements. This project enables users to interact with databases using conversational language, making data access more intuitive and accessible.


### Core Features

- **Intelligent Query Generation**
  - Converts natural language to SQL automatically
  - Supports complex queries with JOINs, aggregations, and subqueries
  - Handles ambiguous questions with clarification prompts

- **Database Schema Integration**
  - Automatic schema discovery and understanding
  - Support for table relationships and constraints
  - Dynamic context building from database metadata

- **AI-Powered Processing**
  - Integration with advanced language models (GPT-4, Claude, etc.)
  - Few-shot learning capabilities
  - Continuous improvement through feedback mechanisms

- **Query Optimization**
  - Automatic query optimization suggestions
  - Performance analysis and recommendations
  - Index utilization awareness

- **Security & Compliance**
  - Query validation and sanitization
  - Role-based access control integration
  - Audit logging for all generated queries

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip or conda package manager
- Database credentials (MySQL, PostgreSQL, SQL Server, or SQLite)
- API key for supported AI models (OpenAI, Anthropic, etc.)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/mshelar08/M.git
   cd M
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` with your configuration:
   ```
   # Database Configuration
   DB_TYPE=postgresql
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=your_database
   DB_USER=your_username
   DB_PASSWORD=your_password

   # AI Model Configuration
   AI_PROVIDER=openai
   AI_API_KEY=your_api_key
   AI_MODEL=gpt-4

   # Application Configuration
   LOG_LEVEL=INFO
   DEBUG=False
   ```

5. **Verify installation**
   ```bash
   python -m pytest tests/
   ```

## 📖 Usage

### Command Line Interface

#### Basic Query
```bash
python agent.py --query "How many customers do we have?"
```

#### With Database Configuration
```bash
python agent.py \
  --query "Show me the top 10 products by revenue" \
  --db-type postgresql \
  --db-host localhost \
  --db-name sales_db
```

#### Interactive Mode
```bash
python agent.py --interactive
```
Then type your questions:
```
> What is the total revenue for 2024?
> Show me customers from New York
> Give me the average order value per customer
```

### Python API

#### Basic Usage
```python
from sql_agent import SQLAgent

# Initialize the agent
agent = SQLAgent(
    db_type="postgresql",
    db_host="localhost",
    db_name="mydb",
    db_user="user",
    db_password="password"
)

# Generate and execute query
result = agent.query("What are the top 5 customers by total spending?")
print(result.data)
print(result.sql_generated)  # View the generated SQL
```

#### Advanced Usage with Custom Configuration
```python
from sql_agent import SQLAgent, QueryConfig

config = QueryConfig(
    timeout=30,
    max_results=1000,
    explain=True,  # Include query plan
    optimize=True  # Request optimization suggestions
)

agent = SQLAgent(
    db_type="mysql",
    db_host="prod.example.com",
    config=config
)

# Process natural language query
response = agent.query(
    "List all orders from premium customers placed in the last quarter",
    return_sql=True,
    validate_only=False
)

print(f"Generated SQL:\n{response.sql_generated}")
print(f"Results:\n{response.data}")
print(f"Execution Time: {response.execution_time}ms")
```

#### Handling Errors and Clarifications
```python
from sql_agent import SQLAgent, QueryValidationError

agent = SQLAgent(db_type="postgresql", db_name="analytics")

try:
    result = agent.query("Get me the latest data")
except QueryValidationError as e:
    print(f"Query validation failed: {e.message}")
    print(f"Suggestions: {e.suggestions}")
except Exception as e:
    print(f"Error: {e}")
```

### Web API

Start the API server:
```bash
python api_server.py --port 8000
```

#### REST Endpoints

**POST /api/query**
```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the revenue trend for the last 6 months?",
    "database": "sales_db",
    "return_sql": true,
    "limit": 100
  }'
```

Response:
```json
{
  "status": "success",
  "data": [
    {"month": "2025-07", "revenue": 150000},
    {"month": "2025-08", "revenue": 175000}
  ],
  "sql_generated": "SELECT DATE_TRUNC('month', order_date) as month, SUM(amount) as revenue FROM orders WHERE order_date >= NOW() - INTERVAL '6 months' GROUP BY DATE_TRUNC('month', order_date) ORDER BY month",
  "execution_time_ms": 245
}
```

**POST /api/validate**
```bash
curl -X POST http://localhost:8000/api/validate \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Who is the best customer?",
    "database": "sales_db"
  }'
```

Response:
```json
{
  "is_valid": false,
  "clarifications_needed": [
    "What metric defines 'best' (spend, frequency, recency)?",
    "Time period to consider?"
  ],
  "suggestions": [
    "Show me customers by total spending",
    "List most frequent customers",
    "Find customers with highest average order value"
  ]
}
```

## 📊 Examples

### Example 1: Sales Analysis
```python
agent = SQLAgent(db_name="ecommerce")

# Question: "What are our best-selling products this month?"
result = agent.query("What are our best-selling products this month?")

# Generated SQL:
# SELECT product_id, product_name, SUM(quantity) as total_sold
# FROM order_items oi
# JOIN products p ON oi.product_id = p.id
# JOIN orders o ON oi.order_id = o.id
# WHERE YEAR(o.order_date) = YEAR(CURRENT_DATE)
#   AND MONTH(o.order_date) = MONTH(CURRENT_DATE)
# GROUP BY product_id, product_name
# ORDER BY total_sold DESC
# LIMIT 10
```

### Example 2: Customer Segmentation
```python
# Question: "Segment customers by their spending patterns"
result = agent.query(
    "Show me customer segments based on annual spending",
    return_sql=True
)

# Generated SQL:
# SELECT 
#   customer_id,
#   customer_name,
#   SUM(order_total) as annual_spending,
#   CASE 
#     WHEN SUM(order_total) > 50000 THEN 'Premium'
#     WHEN SUM(order_total) > 10000 THEN 'Gold'
#     WHEN SUM(order_total) > 1000 THEN 'Silver'
#     ELSE 'Bronze'
#   END as segment
# FROM orders
# WHERE YEAR(order_date) = YEAR(CURRENT_DATE)
# GROUP BY customer_id, customer_name
# ORDER BY annual_spending DESC
```

### Example 3: Time Series Analysis
```python
# Question: "Show me daily revenue for the past month"
result = agent.query(
    "Display the revenue trend for each day in the last 30 days"
)

# Returns a time series with daily breakdown
```

## 🔧 Configuration

### Database Support

| Database | Status | Min Version |
|----------|--------|-------------|
| PostgreSQL | ✅ Supported | 10.0+ |
| MySQL | ✅ Supported | 5.7+ |
| SQL Server | ✅ Supported | 2016+ |
| SQLite | ✅ Supported | 3.0+ |
| Snowflake | ✅ Supported | Latest |
| BigQuery | ✅ Supported | Latest |

### AI Model Support

| Provider | Models | Status |
|----------|--------|--------|
| OpenAI | GPT-4, GPT-3.5 | ✅ Supported |
| Anthropic | Claude 3, Claude 2 | ✅ Supported |
| Google | PaLM, Gemini | ✅ Supported |
| Open Source | LLaMA, Mistral | ✅ Supported |

## 🛡️ Security

### Best Practices

1. **API Key Management**
   - Never commit API keys to version control
   - Use environment variables or secure vaults
   - Rotate keys regularly

2. **Database Security**
   - Use connection pooling
   - Implement SSL/TLS for connections
   - Use read-only database accounts where possible
   - Implement query result filtering based on user roles

3. **Query Validation**
   - All generated queries are validated before execution
   - Dangerous operations (DROP, DELETE) require explicit confirmation
   - Query timeout enforcement prevents long-running queries

4. **Audit Logging**
   ```python
   # View logs
   tail -f logs/sql_agent.log
   ```

## 📝 Logging

### Log Levels

```python
import logging
from sql_agent import SQLAgent

# Set logging level
logging.basicConfig(level=logging.DEBUG)

agent = SQLAgent(db_name="mydb")
# Now debug information will be displayed
```

### Log Examples

```
2026-01-12 18:11:29 INFO: Query received: "Show me top customers"
2026-01-12 18:11:30 DEBUG: Schema discovered: 5 tables, 47 columns
2026-01-12 18:11:31 DEBUG: AI Model Input: [schema info] + [user query]
2026-01-12 18:11:32 INFO: SQL Generated: SELECT * FROM customers...
2026-01-12 18:11:32 INFO: Query executed successfully in 145ms
2026-01-12 18:11:32 INFO: Returned 25 rows
```

## 🧪 Testing

### Run All Tests
```bash
pytest tests/
```

### Run Specific Test Suite
```bash
pytest tests/test_query_generation.py
pytest tests/test_database_integration.py
pytest tests/test_ai_models.py
```

### Run with Coverage
```bash
pytest --cov=sql_agent tests/
```

## 📚 Documentation

For detailed documentation, visit:
- [API Documentation](docs/API.md)
- [Architecture Guide](docs/ARCHITECTURE.md)
- [Database Schema Guide](docs/DATABASE_SCHEMA.md)
- [Troubleshooting Guide](docs/TROUBLESHOOTING.md)

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup
```bash
git clone https://github.com/mshelar08/M.git
cd M
pip install -r requirements-dev.txt
pre-commit install
```

## 📋 Roadmap

- [ ] Multi-language support (Spanish, French, German)
- [ ] Real-time query suggestions
- [ ] Query performance predictions
- [ ] Graph database support (Neo4j)
- [ ] Federated query support
- [ ] Advanced caching mechanisms
- [ ] Mobile app integration
- [ ] Browser extension for seamless integration

## 🐛 Known Issues

- Complex nested queries may require clarification
- Some database-specific functions may need optimization
- Rate limiting applies to free API tier users

For more information, see [ISSUES](docs/KNOWN_ISSUES.md).

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 💬 Support & Community

- **Issues & Bugs**: [GitHub Issues](https://github.com/mshelar08/M/issues)
- **Discussions**: [GitHub Discussions](https://github.com/mshelar08/M/discussions)
- **Email**: support@example.com
- **Documentation**: [Full Docs](https://docs.example.com)

## 🙏 Acknowledgments

- Thanks to the open-source community for inspiration and tools
- Special thanks to contributors and testers
- Powered by state-of-the-art language models

## 📈 Project Status

| Metric | Status |
|--------|--------|
| Build | ![Build](https://img.shields.io/badge/build-passing-brightgreen) |
| Tests | ![Tests](https://img.shields.io/badge/tests-95%25-brightgreen) |
| Coverage | ![Coverage](https://img.shields.io/badge/coverage-88%25-green) |
| License | ![License](https://img.shields.io/badge/license-MIT-blue) |
| Python | ![Python](https://img.shields.io/badge/python-3.8+-blue) |

---

**Last Updated**: 2026-01-12  
**Version**: 1.0.0  
**Maintainer**: [@mshelar08](https://github.com/mshelar08)

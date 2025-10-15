# Security Scanner with AI Integration

A comprehensive web security scanning application with AI-powered vulnerability analysis and remediation recommendations.

## 🚀 Features

### Enhanced Security Scanning
- **HTTP Headers Analysis**: Comprehensive security header validation with detailed remediation
- **SSL/TLS Assessment**: Certificate analysis, protocol version checking, and cipher suite validation
- **Port Scanning**: Network port analysis with security implications and service detection
- **Vulnerability Detection**: OWASP Top 10 compliance checking

### AI-Powered Analysis
- **OpenRouter Integration**: Support for multiple AI models including Llama 2, Claude, and GPT
- **Google Gemini Integration**: Free AI analysis using Gemini Pro
- **Intelligent Remediation**: Context-aware security recommendations with code examples
- **Risk Prioritization**: AI-driven vulnerability prioritization and remediation steps

## 🛠️ Setup Instructions

### Prerequisites
- Docker and Docker Compose
- API keys for AI providers (OpenRouter or Gemini)

### 1. Clone and Configure

```bash
git clone <repository-url>
cd security-scanner
```

### 2. Set Up Environment Variables

**Option A: Use the setup script (Recommended)**
```bash
python3 setup_api_keys.py
```

**Option B: Manual setup**
```bash
# Copy the example environment file
cp .env.example .env

# Edit the .env file with your actual API keys
nano .env
```

### 3. Get API Keys

**You need at least one AI provider API key for the application to work:**

#### OpenRouter (Recommended)
1. Visit [OpenRouter.ai](https://openrouter.ai/)
2. Sign up and get your API key
3. Add to `.env` file

#### Google Gemini (Free Option)
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add to `.env` file

### 4. Test Your Setup

Before starting the application, test your API keys:

```bash
# Test API keys and configuration
python3 standalone_test.py
```

This will verify:
- ✅ File structure is correct
- ✅ Docker configuration is valid
- ✅ API keys are working (if provided)

### 5. Start the Application

```bash
docker-compose up -d
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### 6. Verify Installation

Run the integration test:

```bash
python3 test_integration.py
```

## 📊 Scanner Improvements

### Enhanced HTTP Headers Scanner
- **Comprehensive Header Validation**: Checks 7+ security headers with detailed analysis
- **Configuration Validation**: Validates header values, not just presence
- **Information Disclosure Detection**: Identifies server information leaks
- **Detailed Remediation**: Specific code examples and configuration guidance

### Advanced SSL/TLS Scanner
- **Multi-Version Testing**: Tests all TLS versions for compatibility
- **Certificate Analysis**: Expiration, validity period, and hostname validation
- **Cipher Suite Testing**: Identifies weak encryption algorithms
- **Security Pattern Detection**: Finds common SSL misconfigurations

### Intelligent Port Scanner
- **Service Detection**: Identifies running services and versions
- **Security Risk Assessment**: Categorizes ports by security implications
- **Configuration Analysis**: Detects development servers in production
- **Database Exposure Detection**: Identifies exposed database services

## 🤖 AI Integration

### Supported Providers

#### OpenRouter
- **Models**: Llama 2 (70B, 13B), Claude 3 Sonnet, GPT-3.5/4
- **Features**: High-quality analysis, multiple model options
- **Cost**: Pay-per-use pricing

#### Google Gemini
- **Models**: Gemini Pro, Gemini Pro Vision
- **Features**: Free tier available, good performance
- **Cost**: Free with usage limits

### AI Analysis Features
- **Risk Assessment**: Overall security posture evaluation
- **Prioritized Remediation**: Actionable steps ordered by severity
- **Code Examples**: Specific implementation guidance
- **Compliance Notes**: OWASP, NIST, and other framework references

## 🔧 API Endpoints

### AI Analysis
- `POST /api/v1/ai/analyze` - Analyze scan findings
- `GET /api/v1/ai/providers` - List available AI providers
- `GET /api/v1/ai/analysis/{scan_id}` - Get existing analysis

### Security Scans
- `POST /api/v1/scans` - Start new security scan
- `GET /api/v1/scans` - List all scans
- `GET /api/v1/scans/{scan_id}` - Get scan details

## 🐛 Troubleshooting

### Common Issues

#### No AI Providers Available
```
Error: No AI providers available
```
**Solution**: Ensure at least one API key is set in the `.env` file

#### Scanner Timeout
```
Error: Scanner timeout
```
**Solution**: Check network connectivity and target URL accessibility

#### Database Connection Issues
```
Error: Database connection failed
```
**Solution**: Ensure PostgreSQL container is running and accessible

### Debug Mode

Enable debug logging by setting:
```bash
LOG_LEVEL=DEBUG
```

## 🔒 Security Considerations

- Change default secret keys in production
- Use strong API keys and rotate regularly
- Limit network access to database containers
- Regularly update dependencies
- Monitor API usage and costs

## 📈 Performance Optimization

- Use specific scan types instead of full scans when possible
- Implement rate limiting for AI API calls
- Cache analysis results for repeated scans
- Monitor resource usage in production

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the API documentation at `/docs`
3. Open an issue on GitHub
4. Contact the development team

---

**Note**: This application is for authorized security testing only. Always ensure you have permission to scan target websites.
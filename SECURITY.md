# Security Policy

## Supported Versions

We currently support the following versions with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability, please **do not** open a public issue. Instead, please email the maintainer directly or use GitHub's private vulnerability reporting feature.

### What to Report

- API key leaks or exposure
- Authentication/authorization issues
- Data exposure or privacy concerns
- Injection vulnerabilities
- Any other security-related issues

### What NOT to Report

- Issues with API rate limits
- Model availability issues
- General bugs (use regular issues for these)

## Security Best Practices

When using Promptizer:

1. **Never commit `.env` files** - They are in `.gitignore` for a reason
2. **Use environment variables** - Never hardcode API keys
3. **Rotate API keys regularly** - Especially if you suspect they've been compromised
4. **Review API usage** - Monitor your API usage for unexpected activity
5. **Keep dependencies updated** - Run `poetry update` regularly

## Response Time

We aim to respond to security reports within 48 hours and provide a fix within 7 days for critical issues.


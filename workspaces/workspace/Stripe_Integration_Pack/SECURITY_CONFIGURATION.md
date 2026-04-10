# Stripe Integration Pack - Security Configuration Guide

## 🔒 Enterprise-Grade Security Setup

### PCI DSS Compliance Checklist

#### Requirement 1: Secure Network
```bash
# Install and configure firewall
sudo apt-get install ufw
sudo ufw enable
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Configure network segmentation
# Isolate payment processing network
sudo iptables -A INPUT -s 10.0.0.0/8 -j DROP
sudo iptables -A INPUT -s 172.16.0.0/12 -j DROP
sudo iptables -A INPUT -s 192.168.0.0/16 -j DROP
```

#### Requirement 2: Secure Configuration
```bash
# Remove default passwords
# Change all default system passwords
sudo passwd root
sudo passwd ubuntu

# Disable unnecessary services
sudo systemctl disable telnet
sudo systemctl disable ftp
sudo systemctl disable rsh

# Secure system configuration
sudo chmod 600 /etc/passwd
sudo chmod 600 /etc/shadow
sudo chmod 600 /etc/group
```

#### Requirement 3: Protect Stored Data
```bash
# Encrypt sensitive data
# Setup disk encryption
sudo apt-get install cryptsetup
sudo cryptsetup luksFormat /dev/sda1

# Secure API key storage
mkdir -p /etc/stripe/keys
chmod 700 /etc/stripe/keys

# Create encrypted key storage
openssl enc -aes-256-cbc -salt -in api_keys.txt -out api_keys.enc
```

#### Requirement 4: Encrypt Transmission
```bash
# Setup SSL/TLS certificates
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com

# Generate strong DH parameters
sudo openssl dhparam -out /etc/ssl/certs/dhparam.pem 4096

# Configure TLS 1.3 only
# Edit nginx configuration
ssl_protocols TLSv1.3;
ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
```

#### Requirement 5: Anti-Virus & Maintenance
```bash
# Install and configure anti-virus
sudo apt-get install clamav clamav-daemon
sudo freshclam
sudo systemctl enable clamav-daemon

# Setup automatic updates
sudo apt-get install unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades

# Configure log monitoring
sudo apt-get install logwatch
sudo logwatch --detail High --mailto admin@yourdomain.com --service all --range today
```

#### Requirement 6: Secure Systems
```bash
# Implement access controls
# Setup role-based access
sudo apt-get install acl

# Configure sudo access
sudo visudo
# Add: %stripe-admin ALL=(ALL) NOPASSWD: /usr/local/bin/stripe-*

# Setup monitoring and logging
sudo apt-get install auditd
sudo systemctl enable auditd
```

## 🛡️ Advanced Security Configurations

### Web Application Firewall (WAF)
```bash
# Install ModSecurity
sudo apt-get install libapache2-mod-security2
sudo a2enmod security2

# Configure OWASP rules
git clone https://github.com/SpiderLabs/owasp-modsecurity-crs.git
sudo cp -r owasp-modsecurity-crs/rules/ /etc/modsecurity/

# Enable SQL injection protection
SecRule ARGS "@detectSQLi" \
    "id:1001,\
    phase:2,\
    block,\
    msg:'SQL Injection Attack Detected',\
    logdata:'Matched Data: %{MATCHED_VAR} found within %{MATCHED_VAR_NAME}',\
    tag:'application-multi',\
    tag:'language-multi',\
    tag:'platform-multi',\
    tag:'attack-sqli'"
```

### Intrusion Detection System
```bash
# Install and configure Snort
sudo apt-get install snort
sudo snort -Q -A console -c /etc/snort/snort.conf

# Setup custom rules for payment processing
cat > /etc/snort/rules/stripe.rules << EOF
alert tcp any any -> any 443 (msg:"Stripe API Access"; sid:100001;)
alert tcp any any -> any 80 (msg:"HTTP Payment Request"; sid:100002;)
alert ip any any -> any any (msg:"Suspicious Payment Activity"; sid:100003;)
EOF
```

### Database Security
```bash
# MySQL security hardening
mysql_secure_installation

# Create dedicated Stripe database user
mysql -u root -p
CREATE USER 'stripe_user'@'localhost' IDENTIFIED BY 'StrongPassword123!';
CREATE DATABASE stripe_payments;
GRANT SELECT, INSERT, UPDATE ON stripe_payments.* TO 'stripe_user'@'localhost';
FLUSH PRIVILEGES;

# Enable MySQL encryption
SET GLOBAL innodb_encrypt_tables=ON;
SET GLOBAL innodb_encrypt_log=ON;
```

## 🔐 API Security Implementation

### Rate Limiting Configuration
```bash
# Install rate limiting tools
sudo apt-get install redis-server
sudo systemctl enable redis-server

# Configure API rate limiting
cat > /etc/nginx/conf.d/rate-limiting.conf << EOF
limit_req_zone \$binary_remote_addr zone=api:10m rate=10r/s;
limit_req_zone \$binary_remote_addr zone=payment:10m rate=2r/s;

server {
    location /api/ {
        limit_req zone=api burst=20 nodelay;
    }
    
    location /api/payment/ {
        limit_req zone=payment burst=5 nodelay;
    }
}
EOF
```

### Input Validation & Sanitization
```python
#!/usr/bin/env python3
# Secure input validation for Stripe integration

import re
import html
from decimal import Decimal
from typing import Optional

class PaymentValidator:
    def __init__(self):
        self.amount_pattern = re.compile(r'^\d+(\.\d{1,2})?$')
        self.currency_pattern = re.compile(r'^[A-Z]{3}$')
        self.email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    
    def validate_amount(self, amount: str) -> Optional[Decimal]:
        """Validate and sanitize payment amount"""
        if not self.amount_pattern.match(amount):
            raise ValueError("Invalid amount format")
        
        try:
            decimal_amount = Decimal(amount)
            if decimal_amount <= 0 or decimal_amount > 999999.99:
                raise ValueError("Amount out of valid range")
            return decimal_amount
        except:
            raise ValueError("Invalid amount")
    
    def validate_currency(self, currency: str) -> str:
        """Validate currency code"""
        currency = html.escape(currency.strip().upper())
        if not self.currency_pattern.match(currency):
            raise ValueError("Invalid currency code")
        return currency
    
    def validate_email(self, email: str) -> str:
        """Validate and sanitize email address"""
        email = html.escape(email.strip().lower())
        if not self.email_pattern.match(email):
            raise ValueError("Invalid email format")
        return email
    
    def validate_card_number(self, card_number: str) -> str:
        """Validate credit card number using Luhn algorithm"""
        card_number = re.sub(r'\D', '', card_number)
        
        if len(card_number) < 13 or len(card_number) > 19:
            raise ValueError("Invalid card number length")
        
        # Luhn algorithm check
        def luhn_check(card_num):
            digits = [int(d) for d in card_num]
            odd_digits = digits[-1::-2]
            even_digits = digits[-2::-2]
            checksum = sum(odd_digits)
            for d in even_digits:
                checksum += sum(divmod(d * 2, 10))
            return checksum % 10 == 0
        
        if not luhn_check(card_number):
            raise ValueError("Invalid card number")
        
        return card_number

# Usage example
validator = PaymentValidator()
try:
    amount = validator.validate_amount("19.99")
    currency = validator.validate_currency("USD")
    email = validator.validate_email("customer@example.com")
    print(f"Valid payment: {amount} {currency} for {email}")
except ValueError as e:
    print(f"Validation error: {e}")
```

## 🚨 Fraud Prevention System

### Machine Learning Fraud Detection
```python
#!/usr/bin/env python3
# ML-based fraud detection for Stripe payments

import numpy as np
from sklearn.ensemble import IsolationForest
from datetime import datetime
import redis

class FraudDetector:
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
        self.model = IsolationForest(contamination=0.1, random_state=42)
        self.risk_threshold = 0.7
    
    def extract_features(self, payment_data):
        """Extract features for fraud detection"""
        features = []
        
        # Transaction amount features
        amount = float(payment_data['amount'])
        features.append(amount)
        features.append(1 if amount > 1000 else 0)  # High amount flag
        
        # Time-based features
        hour = datetime.now().hour
        features.append(hour)
        features.append(1 if hour < 6 or hour > 22 else 0)  # Unusual time flag
        
        # Velocity features
        customer_id = payment_data['customer_id']
        recent_transactions = self.get_recent_transactions(customer_id)
        features.append(len(recent_transactions))
        features.append(1 if len(recent_transactions) > 5 else 0)  # High velocity flag
        
        # Geographic features
        ip_country = payment_data.get('ip_country', 'unknown')
        card_country = payment_data.get('card_country', 'unknown')
        features.append(1 if ip_country != card_country else 0)  # Mismatch flag
        
        return np.array(features).reshape(1, -1)
    
    def get_recent_transactions(self, customer_id, hours=24):
        """Get recent transactions for velocity analysis"""
        key = f"transactions:{customer_id}"
        cutoff_time = datetime.now().timestamp() - (hours * 3600)
        
        recent_transactions = []
        for transaction in self.redis_client.lrange(key, 0, -1):
            transaction_time = float(transaction.decode().split(':')[0])
            if transaction_time > cutoff_time:
                recent_transactions.append(transaction)
        
        return recent_transactions
    
    def calculate_risk_score(self, payment_data):
        """Calculate fraud risk score"""
        features = self.extract_features(payment_data)
        anomaly_score = self.model.decision_function(features)[0]
        
        # Convert to risk score (0-1, where 1 is highest risk)
        risk_score = 1 - (anomaly_score + 1) / 2
        
        return risk_score
    
    def should_block_transaction(self, payment_data):
        """Determine if transaction should be blocked"""
        risk_score = self.calculate_risk_score(payment_data)
        
        # Additional rule-based checks
        if self.check_blacklist(payment_data):
            return True, "Blacklisted customer"
        
        if risk_score > self.risk_threshold:
            return True, f"High risk score: {risk_score:.2f}"
        
        return False, "Transaction approved"
    
    def check_blacklist(self, payment_data):
        """Check if customer/card is blacklisted"""
        blacklist_keys = [
            f"blacklist:customer:{payment_data.get('customer_id', '')}",
            f"blacklist:card:{payment_data.get('card_fingerprint', '')}",
            f"blacklist:ip:{payment_data.get('customer_ip', '')}"
        ]
        
        for key in blacklist_keys:
            if self.redis_client.exists(key):
                return True
        
        return False

# Usage example
fraud_detector = FraudDetector()
payment_data = {
    'amount': '99.99',
    'customer_id': 'cus_123456',
    'customer_ip': '192.168.1.100',
    'ip_country': 'US',
    'card_country': 'US',
    'card_fingerprint': 'card_abcdef123456'
}

should_block, reason = fraud_detector.should_block_transaction(payment_data)
print(f"Transaction decision: {'BLOCK' if should_block else 'APPROVE'} - {reason}")
```

## 📊 Security Monitoring & Alerting

### Real-time Security Dashboard
```bash
#!/bin/bash
# Security monitoring dashboard for Stripe integration

# Function to monitor failed login attempts
monitor_failed_logins() {
    local failed_attempts=$(grep "Failed password" /var/log/auth.log | wc -l)
    if [[ $failed_attempts -gt 10 ]]; then
        echo "⚠️  High number of failed login attempts: $failed_attempts"
        # Send alert
        curl -X POST "https://api.telegram.org/botYOUR_BOT_TOKEN/sendMessage" \
            -d "chat_id=YOUR_CHAT_ID&text=Security Alert: $failed_attempts failed login attempts"
    fi
}

# Function to monitor Stripe API errors
monitor_stripe_errors() {
    local error_count=$(grep -c "ERROR.*stripe" /var/log/stripe/api.log 2>/dev/null || echo 0)
    if [[ $error_count -gt 5 ]]; then
        echo "⚠️  High number of Stripe API errors: $error_count"
        # Send alert
        curl -X POST "https://api.telegram.org/botYOUR_BOT_TOKEN/sendMessage" \
            -d "chat_id=YOUR_CHAT_ID&text=Payment Alert: $error_count Stripe API errors"
    fi
}

# Function to monitor unusual payment patterns
monitor_payment_patterns() {
    # Check for unusual payment amounts
    local large_payments=$(grep -c "amount.*[5-9][0-9][0-9]" /var/log/stripe/payments.log 2>/dev/null || echo 0)
    if [[ $large_payments -gt 3 ]]; then
        echo "⚠️  Unusual number of large payments: $large_payments"
    fi
}

# Main monitoring loop
while true; do
    monitor_failed_logins
    monitor_stripe_errors
    monitor_payment_patterns
    sleep 300  # Check every 5 minutes
done
```

## 🛡️ Incident Response Plan

### Security Incident Response Script
```bash
#!/bin/bash
# Automated incident response for security breaches

incident_response() {
    local incident_type=$1
    local severity=$2
    
    echo "🚨 Security Incident Detected: $incident_type (Severity: $severity)"
    
    case $severity in
        "critical")
            # Immediate response for critical incidents
            echo "🚨 CRITICAL: Blocking all payment processing"
            systemctl stop stripe-payment-service
            
            # Isolate affected systems
            iptables -A INPUT -j DROP
            iptables -A OUTPUT -j DROP
            
            # Backup logs for forensics
            tar -czf /tmp/security-incident-$(date +%Y%m%d_%H%M%S).tar.gz /var/log/
            
            # Notify administrators
            echo "Critical security incident: $incident_type" | mail -s "URGENT: Security Breach" admin@yourdomain.com
            ;;
        "high")
            # High severity response
            echo "⚠️  HIGH: Implementing enhanced monitoring"
            # Increase logging level
            sed -i 's/log_level = "info"/log_level = "debug"/' /etc/stripe/stripe.conf
            
            # Enable additional security measures
            systemctl restart fail2ban
            ;;
        "medium")
            # Medium severity response
            echo "⚡ MEDIUM: Monitoring and alerting"
            # Enhanced monitoring
            ;;
    esac
    
    # Log incident
    echo "$(date): $incident_type incident - Severity: $severity" >> /var/log/security-incidents.log
}

# Usage
# incident_response "Unusual Payment Pattern" "high"
```

---

*This security configuration provides enterprise-grade protection for your payment processing. Regular updates and monitoring are essential for maintaining security.* 🔒
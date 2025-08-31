"""
Advanced configuration and environment management using Pydantic
Handles different deployment environments and configuration options with validation
"""

import os
import json
import configparser
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from pathlib import Path
from pydantic import BaseModel, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

@dataclass
class DatabaseConfig:
    """Database configuration"""
    type: str = 'sqlite'
    name: str = 'sentiment_analysis.db'
    host: str = 'localhost'
    port: int = 5432
    username: str = ''
    password: str = ''
    connection_pool_size: int = 10
    backup_enabled: bool = True
    backup_interval_hours: int = 24

@dataclass
class APIConfig:
    """API server configuration"""
    host: str = '0.0.0.0'
    port: int = 5000
    debug: bool = False
    cors_enabled: bool = True
    rate_limiting_enabled: bool = True
    max_requests_per_minute: int = 100
    api_key_required: bool = False
    api_keys: list = None

@dataclass
class NLPConfig:
    """NLP engine configuration"""
    language_detection_enabled: bool = True
    swahili_support_enabled: bool = True
    emoji_processing_enabled: bool = True
    spam_detection_enabled: bool = True
    sentiment_threshold: float = 0.1
    confidence_threshold: float = 0.5
    max_text_length: int = 5000
    preprocessing_enabled: bool = True

@dataclass
class MonitoringConfig:
    """Monitoring system configuration"""
    enabled: bool = True
    metrics_interval_seconds: int = 30
    health_check_interval_seconds: int = 60
    alert_email_enabled: bool = False
    alert_email_recipients: list = None
    alert_webhook_url: str = ''
    log_level: str = 'INFO'
    log_file: str = 'sentiment_analysis.log'
    log_rotation_enabled: bool = True
    log_max_size_mb: int = 50

@dataclass
class StreamingConfig:
    """WebSocket streaming configuration"""
    enabled: bool = True
    host: str = '0.0.0.0'
    port: int = 8765
    max_connections: int = 100
    ping_interval: int = 20
    ping_timeout: int = 10
    broadcast_interval_seconds: int = 30

@dataclass
class AnalyticsConfig:
    """Analytics configuration"""
    enabled: bool = True
    retention_days: int = 90
    trend_analysis_enabled: bool = True
    anomaly_detection_enabled: bool = True
    export_enabled: bool = True
    report_generation_enabled: bool = True

@dataclass
class SecurityConfig:
    """Security configuration"""
    encryption_enabled: bool = True
    data_anonymization_enabled: bool = True
    audit_logging_enabled: bool = True
    max_upload_size_mb: int = 10
    allowed_file_types: list = None
    ip_whitelist: list = None
    rate_limiting_strict: bool = False

class ConfigurationManager:
    """Manages all system configuration"""
    
    def __init__(self, config_file: str = 'config.ini', env: str = 'development'):
        self.config_file = config_file
        self.env = env
        self.config_data = {}
        
        # Default configurations
        self.database = DatabaseConfig()
        self.api = APIConfig()
        self.nlp = NLPConfig()
        self.monitoring = MonitoringConfig()
        self.streaming = StreamingConfig()
        self.analytics = AnalyticsConfig()
        self.security = SecurityConfig()
        
        # Load configuration
        self.load_configuration()
        self.apply_environment_overrides()
    
    def load_configuration(self):
        """Load configuration from file"""
        if os.path.exists(self.config_file):
            try:
                config = configparser.ConfigParser()
                config.read(self.config_file)
                
                # Load each section
                self._load_database_config(config)
                self._load_api_config(config)
                self._load_nlp_config(config)
                self._load_monitoring_config(config)
                self._load_streaming_config(config)
                self._load_analytics_config(config)
                self._load_security_config(config)
                
                print(f"✅ Configuration loaded from {self.config_file}")
                
            except Exception as e:
                print(f"⚠️  Error loading config file: {e}")
                print("🔧 Using default configuration")
        else:
            print(f"📝 Config file {self.config_file} not found, using defaults")
            self.create_default_config()
    
    def _load_database_config(self, config):
        """Load database configuration"""
        if 'database' in config:
            section = config['database']
            self.database.type = section.get('type', self.database.type)
            self.database.name = section.get('name', self.database.name)
            self.database.host = section.get('host', self.database.host)
            self.database.port = section.getint('port', self.database.port)
            self.database.username = section.get('username', self.database.username)
            self.database.password = section.get('password', self.database.password)
            self.database.connection_pool_size = section.getint('connection_pool_size', self.database.connection_pool_size)
            self.database.backup_enabled = section.getboolean('backup_enabled', self.database.backup_enabled)
            self.database.backup_interval_hours = section.getint('backup_interval_hours', self.database.backup_interval_hours)
    
    def _load_api_config(self, config):
        """Load API configuration"""
        if 'api' in config:
            section = config['api']
            self.api.host = section.get('host', self.api.host)
            self.api.port = section.getint('port', self.api.port)
            self.api.debug = section.getboolean('debug', self.api.debug)
            self.api.cors_enabled = section.getboolean('cors_enabled', self.api.cors_enabled)
            self.api.rate_limiting_enabled = section.getboolean('rate_limiting_enabled', self.api.rate_limiting_enabled)
            self.api.max_requests_per_minute = section.getint('max_requests_per_minute', self.api.max_requests_per_minute)
            self.api.api_key_required = section.getboolean('api_key_required', self.api.api_key_required)
    
    def _load_nlp_config(self, config):
        """Load NLP configuration"""
        if 'nlp' in config:
            section = config['nlp']
            self.nlp.language_detection_enabled = section.getboolean('language_detection_enabled', self.nlp.language_detection_enabled)
            self.nlp.swahili_support_enabled = section.getboolean('swahili_support_enabled', self.nlp.swahili_support_enabled)
            self.nlp.emoji_processing_enabled = section.getboolean('emoji_processing_enabled', self.nlp.emoji_processing_enabled)
            self.nlp.spam_detection_enabled = section.getboolean('spam_detection_enabled', self.nlp.spam_detection_enabled)
            self.nlp.sentiment_threshold = section.getfloat('sentiment_threshold', self.nlp.sentiment_threshold)
            self.nlp.confidence_threshold = section.getfloat('confidence_threshold', self.nlp.confidence_threshold)
            self.nlp.max_text_length = section.getint('max_text_length', self.nlp.max_text_length)
            self.nlp.preprocessing_enabled = section.getboolean('preprocessing_enabled', self.nlp.preprocessing_enabled)
    
    def _load_monitoring_config(self, config):
        """Load monitoring configuration"""
        if 'monitoring' in config:
            section = config['monitoring']
            self.monitoring.enabled = section.getboolean('enabled', self.monitoring.enabled)
            self.monitoring.metrics_interval_seconds = section.getint('metrics_interval_seconds', self.monitoring.metrics_interval_seconds)
            self.monitoring.health_check_interval_seconds = section.getint('health_check_interval_seconds', self.monitoring.health_check_interval_seconds)
            self.monitoring.alert_email_enabled = section.getboolean('alert_email_enabled', self.monitoring.alert_email_enabled)
            self.monitoring.alert_webhook_url = section.get('alert_webhook_url', self.monitoring.alert_webhook_url)
            self.monitoring.log_level = section.get('log_level', self.monitoring.log_level)
            self.monitoring.log_file = section.get('log_file', self.monitoring.log_file)
            self.monitoring.log_rotation_enabled = section.getboolean('log_rotation_enabled', self.monitoring.log_rotation_enabled)
            self.monitoring.log_max_size_mb = section.getint('log_max_size_mb', self.monitoring.log_max_size_mb)
    
    def _load_streaming_config(self, config):
        """Load streaming configuration"""
        if 'streaming' in config:
            section = config['streaming']
            self.streaming.enabled = section.getboolean('enabled', self.streaming.enabled)
            self.streaming.host = section.get('host', self.streaming.host)
            self.streaming.port = section.getint('port', self.streaming.port)
            self.streaming.max_connections = section.getint('max_connections', self.streaming.max_connections)
            self.streaming.ping_interval = section.getint('ping_interval', self.streaming.ping_interval)
            self.streaming.ping_timeout = section.getint('ping_timeout', self.streaming.ping_timeout)
            self.streaming.broadcast_interval_seconds = section.getint('broadcast_interval_seconds', self.streaming.broadcast_interval_seconds)
    
    def _load_analytics_config(self, config):
        """Load analytics configuration"""
        if 'analytics' in config:
            section = config['analytics']
            self.analytics.enabled = section.getboolean('enabled', self.analytics.enabled)
            self.analytics.retention_days = section.getint('retention_days', self.analytics.retention_days)
            self.analytics.trend_analysis_enabled = section.getboolean('trend_analysis_enabled', self.analytics.trend_analysis_enabled)
            self.analytics.anomaly_detection_enabled = section.getboolean('anomaly_detection_enabled', self.analytics.anomaly_detection_enabled)
            self.analytics.export_enabled = section.getboolean('export_enabled', self.analytics.export_enabled)
            self.analytics.report_generation_enabled = section.getboolean('report_generation_enabled', self.analytics.report_generation_enabled)
    
    def _load_security_config(self, config):
        """Load security configuration"""
        if 'security' in config:
            section = config['security']
            self.security.encryption_enabled = section.getboolean('encryption_enabled', self.security.encryption_enabled)
            self.security.data_anonymization_enabled = section.getboolean('data_anonymization_enabled', self.security.data_anonymization_enabled)
            self.security.audit_logging_enabled = section.getboolean('audit_logging_enabled', self.security.audit_logging_enabled)
            self.security.max_upload_size_mb = section.getint('max_upload_size_mb', self.security.max_upload_size_mb)
            self.security.rate_limiting_strict = section.getboolean('rate_limiting_strict', self.security.rate_limiting_strict)
    
    def apply_environment_overrides(self):
        """Apply environment-specific overrides"""
        if self.env == 'production':
            self._apply_production_config()
        elif self.env == 'testing':
            self._apply_testing_config()
        elif self.env == 'development':
            self._apply_development_config()
        
        # Apply environment variables
        self._apply_env_variables()
    
    def _apply_production_config(self):
        """Apply production environment settings"""
        self.api.debug = False
        self.api.api_key_required = True
        self.api.rate_limiting_enabled = True
        self.monitoring.log_level = 'WARNING'
        self.security.encryption_enabled = True
        self.security.audit_logging_enabled = True
        self.security.rate_limiting_strict = True
        
        print("🏭 Production configuration applied")
    
    def _apply_testing_config(self):
        """Apply testing environment settings"""
        self.database.name = 'test_sentiment_analysis.db'
        self.api.debug = True
        self.api.rate_limiting_enabled = False
        self.monitoring.enabled = False
        self.monitoring.log_level = 'DEBUG'
        self.security.rate_limiting_strict = False
        
        print("🧪 Testing configuration applied")
    
    def _apply_development_config(self):
        """Apply development environment settings"""
        self.api.debug = True
        self.api.cors_enabled = True
        self.api.rate_limiting_enabled = False
        self.monitoring.log_level = 'DEBUG'
        self.security.rate_limiting_strict = False
        
        print("🔧 Development configuration applied")
    
    def _apply_env_variables(self):
        """Apply environment variables"""
        # Database
        if os.getenv('DB_HOST'):
            self.database.host = os.getenv('DB_HOST')
        if os.getenv('DB_PORT'):
            self.database.port = int(os.getenv('DB_PORT'))
        if os.getenv('DB_NAME'):
            self.database.name = os.getenv('DB_NAME')
        if os.getenv('DB_USERNAME'):
            self.database.username = os.getenv('DB_USERNAME')
        if os.getenv('DB_PASSWORD'):
            self.database.password = os.getenv('DB_PASSWORD')
        
        # API
        if os.getenv('API_HOST'):
            self.api.host = os.getenv('API_HOST')
        if os.getenv('API_PORT'):
            self.api.port = int(os.getenv('API_PORT'))
        if os.getenv('API_DEBUG'):
            self.api.debug = os.getenv('API_DEBUG').lower() == 'true'
        
        # Monitoring
        if os.getenv('LOG_LEVEL'):
            self.monitoring.log_level = os.getenv('LOG_LEVEL')
        if os.getenv('ALERT_WEBHOOK_URL'):
            self.monitoring.alert_webhook_url = os.getenv('ALERT_WEBHOOK_URL')
        
        # Security
        if os.getenv('ENCRYPTION_ENABLED'):
            self.security.encryption_enabled = os.getenv('ENCRYPTION_ENABLED').lower() == 'true'
    
    def create_default_config(self):
        """Create default configuration file"""
        config = configparser.ConfigParser()
        
        # Database section
        config['database'] = {
            'type': self.database.type,
            'name': self.database.name,
            'host': self.database.host,
            'port': str(self.database.port),
            'username': self.database.username,
            'password': self.database.password,
            'connection_pool_size': str(self.database.connection_pool_size),
            'backup_enabled': str(self.database.backup_enabled),
            'backup_interval_hours': str(self.database.backup_interval_hours)
        }
        
        # API section
        config['api'] = {
            'host': self.api.host,
            'port': str(self.api.port),
            'debug': str(self.api.debug),
            'cors_enabled': str(self.api.cors_enabled),
            'rate_limiting_enabled': str(self.api.rate_limiting_enabled),
            'max_requests_per_minute': str(self.api.max_requests_per_minute),
            'api_key_required': str(self.api.api_key_required)
        }
        
        # NLP section
        config['nlp'] = {
            'language_detection_enabled': str(self.nlp.language_detection_enabled),
            'swahili_support_enabled': str(self.nlp.swahili_support_enabled),
            'emoji_processing_enabled': str(self.nlp.emoji_processing_enabled),
            'spam_detection_enabled': str(self.nlp.spam_detection_enabled),
            'sentiment_threshold': str(self.nlp.sentiment_threshold),
            'confidence_threshold': str(self.nlp.confidence_threshold),
            'max_text_length': str(self.nlp.max_text_length),
            'preprocessing_enabled': str(self.nlp.preprocessing_enabled)
        }
        
        # Monitoring section
        config['monitoring'] = {
            'enabled': str(self.monitoring.enabled),
            'metrics_interval_seconds': str(self.monitoring.metrics_interval_seconds),
            'health_check_interval_seconds': str(self.monitoring.health_check_interval_seconds),
            'alert_email_enabled': str(self.monitoring.alert_email_enabled),
            'alert_webhook_url': self.monitoring.alert_webhook_url,
            'log_level': self.monitoring.log_level,
            'log_file': self.monitoring.log_file,
            'log_rotation_enabled': str(self.monitoring.log_rotation_enabled),
            'log_max_size_mb': str(self.monitoring.log_max_size_mb)
        }
        
        # Streaming section
        config['streaming'] = {
            'enabled': str(self.streaming.enabled),
            'host': self.streaming.host,
            'port': str(self.streaming.port),
            'max_connections': str(self.streaming.max_connections),
            'ping_interval': str(self.streaming.ping_interval),
            'ping_timeout': str(self.streaming.ping_timeout),
            'broadcast_interval_seconds': str(self.streaming.broadcast_interval_seconds)
        }
        
        # Analytics section
        config['analytics'] = {
            'enabled': str(self.analytics.enabled),
            'retention_days': str(self.analytics.retention_days),
            'trend_analysis_enabled': str(self.analytics.trend_analysis_enabled),
            'anomaly_detection_enabled': str(self.analytics.anomaly_detection_enabled),
            'export_enabled': str(self.analytics.export_enabled),
            'report_generation_enabled': str(self.analytics.report_generation_enabled)
        }
        
        # Security section
        config['security'] = {
            'encryption_enabled': str(self.security.encryption_enabled),
            'data_anonymization_enabled': str(self.security.data_anonymization_enabled),
            'audit_logging_enabled': str(self.security.audit_logging_enabled),
            'max_upload_size_mb': str(self.security.max_upload_size_mb),
            'rate_limiting_strict': str(self.security.rate_limiting_strict)
        }
        
        # Write configuration file
        with open(self.config_file, 'w') as f:
            config.write(f)
        
        print(f"📝 Default configuration created: {self.config_file}")
    
    def get_database_url(self):
        """Get database connection URL"""
        if self.database.type == 'sqlite':
            return f"sqlite:///{self.database.name}"
        elif self.database.type == 'postgresql':
            return f"postgresql://{self.database.username}:{self.database.password}@{self.database.host}:{self.database.port}/{self.database.name}"
        elif self.database.type == 'mysql':
            return f"mysql://{self.database.username}:{self.database.password}@{self.database.host}:{self.database.port}/{self.database.name}"
        else:
            return f"sqlite:///{self.database.name}"
    
    def to_dict(self):
        """Convert configuration to dictionary"""
        return {
            'database': asdict(self.database),
            'api': asdict(self.api),
            'nlp': asdict(self.nlp),
            'monitoring': asdict(self.monitoring),
            'streaming': asdict(self.streaming),
            'analytics': asdict(self.analytics),
            'security': asdict(self.security),
            'environment': self.env
        }
    
    def save_config(self):
        """Save current configuration to file"""
        self.create_default_config()
    
    def validate_config(self):
        """Validate configuration"""
        issues = []
        
        # Validate ports
        if not (1 <= self.api.port <= 65535):
            issues.append(f"Invalid API port: {self.api.port}")
        
        if not (1 <= self.streaming.port <= 65535):
            issues.append(f"Invalid streaming port: {self.streaming.port}")
        
        if not (1 <= self.database.port <= 65535):
            issues.append(f"Invalid database port: {self.database.port}")
        
        # Validate thresholds
        if not (0 <= self.nlp.sentiment_threshold <= 1):
            issues.append(f"Invalid sentiment threshold: {self.nlp.sentiment_threshold}")
        
        if not (0 <= self.nlp.confidence_threshold <= 1):
            issues.append(f"Invalid confidence threshold: {self.nlp.confidence_threshold}")
        
        # Validate log level
        valid_log_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if self.monitoring.log_level not in valid_log_levels:
            issues.append(f"Invalid log level: {self.monitoring.log_level}")
        
        return issues
    
    def print_summary(self):
        """Print configuration summary"""
        print("\n🔧 Configuration Summary:")
        print(f"   Environment: {self.env}")
        print(f"   Database: {self.database.type} ({self.database.name})")
        print(f"   API Server: {self.api.host}:{self.api.port} (debug: {self.api.debug})")
        print(f"   Streaming: {self.streaming.host}:{self.streaming.port} (enabled: {self.streaming.enabled})")
        print(f"   Monitoring: {self.monitoring.enabled} (level: {self.monitoring.log_level})")
        print(f"   Analytics: {self.analytics.enabled} (retention: {self.analytics.retention_days} days)")
        print(f"   Security: encryption={self.security.encryption_enabled}, audit={self.security.audit_logging_enabled}")
        
        # Validation
        issues = self.validate_config()
        if issues:
            print(f"\n⚠️  Configuration Issues:")
            for issue in issues:
                print(f"   - {issue}")
        else:
            print(f"\n✅ Configuration is valid")

# Global configuration instance
config_manager = ConfigurationManager()

def get_config() -> ConfigurationManager:
    """Get the global configuration manager"""
    return config_manager

def load_config(config_file: str = 'config.ini', env: str = 'development') -> ConfigurationManager:
    """Load configuration with specific file and environment"""
    global config_manager
    config_manager = ConfigurationManager(config_file, env)
    return config_manager


# === PYDANTIC SETTINGS FOR PRODUCTION ===

class ProductionSettings(BaseSettings):
    """Production-ready settings with validation"""
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra='ignore'
    )
    
    # Flask Configuration
    SECRET_KEY: str = "change-this-in-production"
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 5000
    
    # Database
    DATABASE_URL: str = "sqlite:///sentiment_analysis.db"
    
    # News APIs
    NEWSAPI_KEY: Optional[str] = None
    GNEWS_API_KEY: Optional[str] = None
    CURRENTS_API_KEY: Optional[str] = None
    DEFAULT_NEWS_COUNTRY: str = "ke"  # Kenya by default
    
    # ML APIs
    HUGGINGFACE_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None  # Future integration
    
    # Security
    ALLOWED_ORIGINS: str = "*"  # Comma-separated list or "*"
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # Cache
    REDIS_URL: Optional[str] = None
    CACHE_TTL: int = 300  # 5 minutes
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"  # json or text
    
    @field_validator('ALLOWED_ORIGINS')
    @classmethod
    def validate_origins(cls, v):
        if v == "*":
            return ["*"]
        return [origin.strip() for origin in v.split(",")]
    
    @field_validator('LOG_LEVEL')
    @classmethod
    def validate_log_level(cls, v):
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"LOG_LEVEL must be one of {valid_levels}")
        return v.upper()


@lru_cache()
def get_production_settings() -> ProductionSettings:
    """Get cached production settings instance"""
    return ProductionSettings()


if __name__ == '__main__':
    # Demo configuration management
    print("🔧 Sentiment Analysis Configuration Manager")
    
    # Load configuration
    config = load_config()
    config.print_summary()
    
    # Save default config if needed
    if not os.path.exists('config.ini'):
        config.save_config()
        print("\n📝 Default configuration file created: config.ini")

"""
Configuration settings for GasBuddy API
"""
import os

class Config:
    """Base configuration."""
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')
    DEBUG = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'

    # Rate limiting (requests per minute per IP)
    RATE_LIMIT = int(os.getenv('RATE_LIMIT', '10'))

    # CORS settings
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*')

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    FLASK_ENV = 'development'

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    FLASK_ENV = 'production'

# Choose configuration based on environment
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': ProductionConfig
}

def get_config():
    """Get the current configuration."""
    config_name = os.getenv('FLASK_ENV', 'default')
    return config.get(config_name, config['default'])

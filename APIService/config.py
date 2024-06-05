class Config:
    SECRET_KEY = 'your_secret_key_here'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///mydatabase.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    SCHEDULER_API_ENABLED = True

    # Add scheduler job configuration
    JOBS = [
        {
            'id': 'job1',
            'func': 'app:check_bookings',
            'trigger': 'interval',
            'seconds': 86400  # Every 24 hours
        }
    ]
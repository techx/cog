import os
from hardwarecheckout import app

@app.template_filter()
def env_override(value, key):
  return os.getenv(key, value)
import os
from cog import app

@app.template_filter()
def env_override(value, key):
  return os.getenv(key, value)
import os

### App config ###

## These variables must be set as env variables ##

# Postgres SQL Connection String.
# Note: This is the default env variable name
# used for Heroku postgres deploys.
DB_URI = os.environ['DATABASE_URI']

# Random Secret for JWTs
SECRET = os.environ['SECRET']


### The following variables may all be set using environment 
### variables of the same name. The environment variable will
### take precedence over the value shown here. This is to allow 
### for deploy configuration without modifying the codebase at all. 
  
## Deploy settings ##

# HackerAPI event slug
EVENT_SLUG = 'hackthenorth2019'

# Enable/disable Flask debug mode. Should be set to 
# False on production deploys of Cog. 
DEBUG = True 

# Ensure that all attempts to visit an insecure version 
# of the page redirect to  https, and makes sure all 
# Cog-derived redirects use https. Recommended to set
# this to True if using an SSL-protected deploy. 
# Only works when DEBUG=False.
FORCE_SSL = False 

## Metadata ## 

HACKATHON_NAME = "Hack the North"

## Event logistical settings ##

# If true, lets users to make requests even if 
# item is out of stock
ENABLE_WAITLIST = True

# If True, requires hackers to submit a proposal
# for lotteried items
LOTTERY_REQUIRES_PROPOSAL = True

# If True, item type is set to CHECKOUT after an 
# item's lottery is run
CLOSE_LOTTERY_WHEN_RUN = False 

# If True, deny lottery requests that don't win
# item
DENY_LOTTERY_LOSERS = True

# Character limit for lottery proposals
# Set to 0 to disable char limit
LOTTERY_CHAR_LIMIT = 140 

# If True, display current lottery item stock to user
DISPLAY_LOTTERY_QUANTITY = True 

# If True, display current checkout item stock to user
DISPLAY_CHECKOUT_QUANTITY = True 

# If False, prevent users from submitting multiple
# requests for same lottery item
LOTTERY_MULTIPLE_SUBMISSIONS = False 

# The info text underneath the 'Lottery Required' section 
LOTTERY_TEXT = """We have a limited quantity of these items. Please fill out a 
brief proposal describing your project idea, and we'll randomly accept as many 
requests as we can 30 minutes after hacking starts."""

# The info text underneath the 'Checkout Required' section 
CHECKOUT_TEXT = """Click to request any of these items, and your request will
be approved when we have one available. Keep in mind we will ask to hold on
to a form of ID until the item is returned."""

# The info text underneath the 'No Checkout Required' section 
FREE_TEXT = """Just come to the hardware desk and ask for any of these
items!"""
import slack

from cog.config import SLACK_OAUTH_ACCESS_TOKEN

client = slack.WebClient(token=SLACK_OAUTH_ACCESS_TOKEN)

def send_slack(email, message):
    """Send a slack message *message* to *email*.
    Returns true if successful, false if not."""
    response = client.users_lookupByEmail(
        email=email
    )
    if not response["ok"]:
        return False
    user_id = response["user"]["id"]
    
    response = client.conversations_open(
        return_im=False,
        users=[user_id]
    )
    if not response["ok"]:
        return False
    dm_channel_id = response["channel"]["id"]

    response = client.chat_postMessage(
        channel=dm_channel_id,
        text=message)
    if not response["ok"]:
        return False
    return True
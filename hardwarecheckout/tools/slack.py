import slack

from hardwarecheckout.config import SLACK_OAUTH_ACCESS_TOKEN

client = slack.WebClient(token=SLACK_OAUTH_ACCESS_TOKEN)

def send_slack(email, message):
    """Send a slack message *message* to *email*.
    Returns true if successful, false if not."""
    try:
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
            text=message,
            mrkdwn=True)
        if not response["ok"]:
            return False
    except slack.errors.SlackApiError as e:
        print("Slack error: ", e)
        return False
    return True
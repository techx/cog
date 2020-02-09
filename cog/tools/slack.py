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

@slack.RTMClient.run_on(event='message')
def recv_slack_message(**payload):
    data = payload['data']
    web_client = payload['web_client']
    rtm_client = payload['rtm_client']
    # if 'Hello' in data.get('text', []):
    channel_id = data['channel']
    thread_ts = data['ts']
    user = data['user']
    web_client.chat_postMessage(
        channel=channel_id,
        text=f"Hi <@{user}>! This is an unmonitored Slack bot. Please direct all messages or questions to one of the organizers, or email hello@treehacks.com.",
        thread_ts=thread_ts
    )

rtm_client = slack.RTMClient(token=SLACK_OAUTH_ACCESS_TOKEN)
rtm_client.start()
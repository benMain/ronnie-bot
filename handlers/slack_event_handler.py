"""
Maps slack_events from the Events API to bot functions.

Author: Benjamin Main
Date : 03/16/2018
"""
from bots import chat_bot
from flask import make_response

chat_bot = chat_bot.ChatBot()


def _bot_verification():
    """Check Bot Verification Token."""
    return chat_bot.verification


def _bot_auth(auth_code):
    """Authenticate with OAuth."""
    chat_bot.auth(auth_code)


def _oauth_parameters():
    """Fetches oauth client_id and scope."""
    return chat_bot.oauth["client_id"], chat_bot.oauth["scope"]


def _event_handler(event_type, slack_event):
    """
    Ronnie Bot is made up of multiple sub-bots and routing events to
    the appropriate bot takes planning
    """

    # ============== Respond to Messages ============= #
    # Read Messages and Respond if necessary.

    if event_type == "message":
        if not is_from_bot(slack_event):
            if is_public_channel(slack_event["event"]["channel"]):
                #  chat_bot.insult_teammates(slack_event["event"])
                #  chat_bot.make_astronomy_post(slack_event["event"])
                chat_bot.techcrunch_post(slack_event["event"])
            else:
                chat_bot.chatter(slack_event["event"])
        return make_response("ChatBot posts the news...",
                             200,)

    # ============= Reaction Added Events ============= #
    # If people like things ChatBot does not like them.
    elif event_type == "reaction_added":
        chat_bot.react_negatively(slack_event["event"])
        return make_response("Chatbot votes against people", 200,)

    # =============== Pin Added Events ================ #
    # If the user has added an emoji reaction to the onboarding message
    elif event_type == "pin_added":
        return make_response("Welcome message updates with pin", 200,)

    # ============= Event Type Not Found! ============= #
    # If the event_type does not have a handler
    message = "You have not added an event handler for the %s" % event_type
    # Return a helpful error message
    return make_response(message, 200, {"X-Slack-No-Retry": 1})


def is_from_bot(slack_event):
    if("username" in slack_event["event"].keys()
            and "ronnie-bot" in slack_event["event"]["username"]):
        return True
    else:
        return False


def is_public_channel(channel_id):
    if "C" in channel_id[:1]:
        return True
    else:
        return False

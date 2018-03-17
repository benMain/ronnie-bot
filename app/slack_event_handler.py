"""
Maps slack_events from the Events API to bot functions.

Author: Benjamin Main
Date : 03/16/2018
"""
import bots.bot.bot as bot
from flask import make_response

pyBot = bot.Bot()
slack = pyBot.client


def _bot_verification():
    """Check Bot Verification Token."""
    return pyBot.verification


def _bot_auth(auth_code):
    """Authenticate with OAuth."""
    pyBot.auth(auth_code)


def _oauth_parameters():
    """Fetches oauth client_id and scope."""
    return pyBot.oauth["client_id"], pyBot.oauth["scope"]


def _event_handler(event_type, slack_event):
    """
    A helper function that routes events from Slack to our Bot
    by event type and subtype.

    Parameters
    ----------
    event_type : str
        type of event recieved from Slack
    slack_event : dict
        JSON response from a Slack reaction event

    Returns
    ----------
    obj
        Response object with 200 - ok or 500 - No Event Handler error

    """
    team_id = slack_event["team_id"]
    # ================ Team Join Events =============== #
    # When the user first joins a team, the type of event will be team_join
    if event_type == "team_join":
        user_id = slack_event["event"]["user"]["id"]
        # Send the onboarding message
        pyBot.onboarding_message(team_id, user_id)
        return make_response("Welcome Message Sent", 200,)

    # ============== Share Message Events ============= #
    # If the user has shared the onboarding message, the event type will be
    # message. We'll also need to check that this is a message that has been
    # shared by looking into the attachments for "is_shared".
    elif event_type == "message" and slack_event["event"].get("attachments"):
        user_id = slack_event["event"].get("user")
        if slack_event["event"]["attachments"][0].get("is_share"):
            # Update the onboarding message and check off "Share this Message"
            pyBot.update_share(team_id, user_id)
            return make_response("Welcome message updates with shared message",
                                 200,)

    # ============= Reaction Added Events ============= #
    # If the user has added an emoji reaction to the onboarding message
    elif event_type == "reaction_added":
        user_id = slack_event["event"]["user"]
        # Update the onboarding message
        pyBot.update_emoji(team_id, user_id)
        return make_response("Welcome message updates with reactji", 200,)

    # =============== Pin Added Events ================ #
    # If the user has added an emoji reaction to the onboarding message
    elif event_type == "pin_added":
        user_id = slack_event["event"]["user"]
        # Update the onboarding message
        pyBot.update_pin(team_id, user_id)
        return make_response("Welcome message updates with pin", 200,)

    # ============= Event Type Not Found! ============= #
    # If the event_type does not have a handler
    message = "You have not added an event handler for the %s" % event_type
    # Return a helpful error message
    return make_response(message, 200, {"X-Slack-No-Retry": 1})

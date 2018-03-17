# Ronnie Bot
## Slack Bot Using [Slack's Events API](https://api.slack.com/events-api) in Python
This bot is an example implementation of building a Slack App with Slack's Python SDK, [python-slackclient](http://python-slackclient.readthedocs.io/en/latest/).


#### Technical Requirements

- **[Python](https://www.python.org/downloads/)**, the programming language we're
going to use.
- **[Pip](https://pip.pypa.io/en/stable/installing/)**, the Python package manager
we'll use for installing packages we need.
- **[Virtualenv](https://virtualenv.pypa.io/en/latest/installation/)** or another
tool to manage a virtual environment

After you've cloned this repository locally, you'll want to create a virtual
environment to keep the dependencies for this project isolated from any other
project you may be working on.

If you're using `virtualenv` run the following commands from the root of your
project directory:

```bash
virtualenv venv
```

Then activate your new virtual environment:

```bash
source venv/bin/activate
```

After that, you can install all the Python packages this project will need with
this command:

```bash
pip install -r requirements.txt
```

###### Server Requirements

Slack will be delivering events to your app's server so your server needs to be able to receive incoming HTTPS traffic from Slack.

If you are running this project locally, you'll need to set up tunnels for Slack to connect to your endpoints. [Ngrok](https://ngrok.com/) is an easy to use tunneling tool that supports HTTPS, which is required by Slack.

You'll likely want to test events coming to your server without going through the actions on your Slack team.  [Postman](https://www.getpostman.com/) is a useful tool you can use to recreate requests sent from Slack to your server. This is especially helpful for events like user join, where the workflow to recreate the event requires quite a bit of set up.

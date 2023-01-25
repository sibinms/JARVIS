USER_NAMES = {
    "sibin-impress": "@sibin.ms",
    "abdulmuizzf": "@abdul",
}


def get_slack_rendered_message(reviewers_tag, created_user_tag, pull_request_data):
    slack_data = {
        "username": "JARVIS",
        "text": "PR Review Request",
        "blocks": [
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*{reviewers_tag} You have a PR review Request From {created_user_tag}:*"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*<{pull_request_data['pr']}|{pull_request_data['title']}>* \n\n Author: `{created_user_tag}` \t Reviewer: `{reviewers_tag}`"
                },
                "accessory": {
                    "type": "image",
                    "image_url": "https://raw.githubusercontent.com/quintessence/slack-icons/master/images/github-logo-slack-icon.png",
                    "alt_text": "github"
                }
            },
            {
                "type": "divider"
            },
        ]
    }
    return slack_data

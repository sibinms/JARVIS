from django.core.cache import cache


USER_NAMES = {
    "sibin-impress": "@sibin.ms",
    "abdulmuizzf": "@abdul",
    "sibinms": "@sibin.ms",
    "imp-joseseb91": "@jose.sebastian"
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
                    "image_url": "https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png",
                    "alt_text": "github"
                }
            },
            {
                "type": "divider"
            },
        ]
    }
    return slack_data


def slack_message_already_sent(pull_request_data):
    """
    If there is multiple reviewers Github will sent events per reviewers.
    We don't need to have multiple messages on slack for same PR with same reviewers
    """
    pr_id = pull_request_data.get("pr_id")
    reviewers = pull_request_data.get("reviewers")
    cache_key = f"{pr_id}-{reviewers}"
    if cache.get(cache_key) is None:
        pr_id = pull_request_data.get("pr_id")
        reviewers = pull_request_data.get("reviewers_tag")
        cache_key = f"{pr_id}-{reviewers}"
        cache.set(cache_key, pull_request_data, 60 * 3)
        return False
    return True

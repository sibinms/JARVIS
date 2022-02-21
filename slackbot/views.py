from pprint import pprint
import json
import sys
import requests

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
from slackbot.constants import USER_NAMES


class GithubWebhookAPIView(APIView):
    """
    API for handling events from Github
    {
    "action":
    "pr":
    "title":
    "reviewers":
    "created_by":
    }
    """
    PR_ACTIONS = ["review_requested"]
    SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"

    def get_pull_request_data(self, request):
        pull_request_data = {}
        action = request.data.get("action", "")
        print(action)
        if action in self.PR_ACTIONS:
            pull_request_data["action"] = action
            pull_request = request.data.get("pull_request", {})
            pr_url = pull_request.get("html_url", "")
            pull_request_data['pr'] = pr_url
            pr_created_user = pull_request.get("user", {})
            created_by = pr_created_user.get("login", "")
            pull_request_data['created_by'] = created_by
            pr_title = pull_request.get('title', "")
            pull_request_data['title'] = pr_title
            requested_reviewers = pull_request.get("requested_reviewers", [])
            reviewers = []
            for requested_reviewer in requested_reviewers:
                user = requested_reviewer.get("login")
                reviewers.append(user)
            if reviewers:
                pull_request_data['reviewers'] = reviewers
                return pull_request_data, True
        return pull_request_data, False

    def get_slack_data(self, pull_request_data):
        created_user_tag = USER_NAMES.get(pull_request_data['created_by'], "")
        reviewers = pull_request_data.get("reviewers", [])
        reviewers_tag = ""
        for reviewer in reviewers:
            reviewers_tag += f"{USER_NAMES.get(reviewer)}"
        print(reviewers_tag)
        slack_data = {
            "username": "JARVIS",
            # "channel" : "#somerandomcahnnel",
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

    def post(self, request, *args, **kwargs):
        # pprint(request.data)
        pull_request_data, is_valid_pr = self.get_pull_request_data(request)
        if is_valid_pr:
            pprint(pull_request_data)
            slack_data = self.get_slack_data(pull_request_data)
            print(slack_data)
            byte_length = str(sys.getsizeof(slack_data))
            headers = {'Content-Type': "application/json", 'Content-Length': byte_length}
            response = requests.post(self.SLACK_WEBHOOK_URL, data=json.dumps(slack_data), headers=headers)

        return Response(data="success", status=status.HTTP_200_OK)

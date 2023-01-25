from pprint import pprint
import json
import sys
import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from slackbot.utils import (
    get_slack_rendered_message,
    USER_NAMES
)

# Create your views here.


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

    def get_pull_request_data(self, request):
        pull_request_data = {}
        action = request.data.get("action", "")
        if action in self.PR_ACTIONS:
            pull_request_data["action"] = action

            # get PR URL
            pull_request = request.data.get("pull_request", {})
            pr_url = pull_request.get("html_url", "")
            pull_request_data['pr'] = pr_url

            # get PR created user details
            pr_created_user = pull_request.get("user", {})
            created_by = pr_created_user.get("login", "")
            pull_request_data['created_by'] = created_by

            # get PR title
            pr_title = pull_request.get('title', "")
            pull_request_data['title'] = pr_title

            # get PR review requested
            requested_reviewers = pull_request.get("requested_reviewers", [])
            reviewers = []
            for requested_reviewer in requested_reviewers:
                user = requested_reviewer.get("login")
                reviewers.append(user)

            if reviewers:
                pull_request_data['reviewers'] = reviewers
                return pull_request_data, True

        return pull_request_data, False

    def get_pr_creator_tag(self, pull_request_data):
        created_user_tag = USER_NAMES.get(pull_request_data['created_by'], "")
        return created_user_tag

    def get_pr_reviewers_tag(self, pull_request_data):
        reviewers = pull_request_data.get("reviewers", [])
        reviewers_tag = ""
        for reviewer in reviewers:
            reviewers_tag += f"{USER_NAMES.get(reviewer)}"

        return reviewers_tag

    def get_slack_message(self, pull_request_data):
        created_user_tag = self.get_pr_creator_tag(pull_request_data)
        reviewers_tag = self.get_pr_reviewers_tag(pull_request_data)
        slack_message = get_slack_rendered_message(
            reviewers_tag,
            created_user_tag,
            pull_request_data
        )
        return slack_message

    def post(self, request, *args, **kwargs):
        pull_request_data, is_valid_pr = self.get_pull_request_data(request)
        if is_valid_pr:
            pprint(pull_request_data)
            slack_data = self.get_slack_message(pull_request_data)
            print(slack_data)
            byte_length = str(sys.getsizeof(slack_data))
            headers = {'Content-Type': "application/json", 'Content-Length': byte_length}
            response = requests.post(settings.PR_REVIEW_SLACK_WEBHOOK, data=json.dumps(slack_data), headers=headers)

        return Response(data="success", status=status.HTTP_200_OK)

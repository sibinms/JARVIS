from pprint import pprint

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Create your views here.


class GithubWebhookAPIView(APIView):
    """
    API for handling events from Github
    {
    "action":
    "pr":
    "reviewers":
    "created_by":
    }
    """
    PR_ACTIONS = ["opened", "reopened", "review_requested"]

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
            requested_reviewers = pull_request.get("requested_reviewers", [])
            reviewers = []
            for requested_reviewer in requested_reviewers:
                user = requested_reviewer.get("login")
                reviewers.append(user)
            if reviewers:
                pull_request_data['reviewers'] = reviewers
                return pull_request_data, True
        return pull_request_data, False

    def post(self, request, *args, **kwargs):
        # pprint(request.data)
        pull_request_data, is_valid_pr = self.get_pull_request_data(request)
        if is_valid_pr:
            pprint(pull_request_data)

        return Response(data="success", status=status.HTTP_200_OK)

class RedditResponse:
    response = {}
    data = {}

    def __init__(self, data: dict):
        self.data = data

        data = self.data.get("data", {})
        childrens: list[dict] = data.get("children", [])
        info: dict = childrens[0].get("data")
        subreddit: str = info.get("subreddit")
        subreddit_name_prefixed: str = info.get("subreddit_name_prefixed")
        created_utc: float = info.get("created_utc")
        subreddit_subscribers: int = info.get("subreddit_subscribers")
        # print(info)


        self.response = {
            "subreddit": subreddit,
            "subreddit_name_prefixed": subreddit_name_prefixed,
            "created_utc": created_utc,
            "subreddit_subscribers": subreddit_subscribers
        }

    def get_responses(self):
        return self.response
from httpx import AsyncClient, ConnectTimeout, ReadTimeout
from appConstant import URL, SUCCEED, NOT_FOUND, TIMEOUT, HEADER
from exceptions import ApplicationException
from .RedditResponse import RedditResponse



class FetchRequest:

    async def fetch(self, subreddit: str):
        url = URL.format(subreddit)
        async with AsyncClient(timeout=TIMEOUT) as client:
            try:
                response = await client.get(url, headers = HEADER)
                print(response.status_code)
                if response.status_code == SUCCEED:
                    response = RedditResponse(response.json())
                    return response.get_responses()
                elif response.status_code == 302:
                    raise ApplicationException(f"Subreddit '{subreddit}' not found", code=NOT_FOUND)
                else:
                    raise Exception(f"Failed to fetch data for subreddit '{subreddit}' with status code {response.status_code}")
                    # return {"error": "An error occurred while fetching data"}
            except (ConnectTimeout, ReadTimeout):
                raise ApplicationException("Request timed out", code=400)
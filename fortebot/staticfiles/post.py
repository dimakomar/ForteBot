from slackclient import SlackClient
import os

sc = SlackClient('xoxb-258274331425-ehVXGlyfogny0BIAZggNl607')

# call = sc.api_call(
#   "chat.postMessage",
#   channel="D7LTDA0TF",
#   text="hello from python"
# )

history = sc.api_call(
  "im.history",
  channel="D7LTDA0TF"
)

print(history)

# list = sc.api_call(
#   "users.list"
# )

# print(list)
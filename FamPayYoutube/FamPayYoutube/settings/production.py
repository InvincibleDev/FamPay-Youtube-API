from FamPayYoutube.settings.base import *

DEBUG = False

ALLOWED_HOSTS = ['*']

CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = ['*']

print("\n" + "-" * 60)
print("Running server with production settings..")
print("-" * 60, "\n")

## FamPay Assignment 'Youtube API'

## Getting Started with the Project

To get started with the project:

     $ git clone ...

set the following environment variables in docker-compose.yml:

      SECRET_KEY
      IS_PRODUCTION
      FIELD_ENCRYPTION_KEYS

To run the project, Go to the root folder and run

      $ docker-compose up --build

To create Django superuser

      $ docker exec -it <container_id> python manage.py createsuperuser

To upload API KEYS

      use /apikeys/ endpoint to upload api key.

      Multiple API KEYS can be uploaded

## Api end point documentation:

| Api end-point  | Method | Authentication Required | Function  | Argument | Description   | Response |
| ---------------| ------ | ----------------------- | --------- | -------- | -----------   | -------- |
| /youtubevideo/| GET   | No | VideoViewset() | <strong> search query param can be given.<br/> ex: /youtubevideo/?search=football  </strong>| Returns Paginated Data of stored videos | Paginated Video Details |
| /apikeys/| GET, POST   | No | ApiKeyViewset() | None  | Used to upload and retrive API keys of YOUTUBE DATA Api | API keys stored in DB |

### Note

    Upload API KEY after running docker file.
    Every API key is stored in a encrypted field for safety.
    postman collection added in the repo

### Backend code test
- The solutions must be implemented in Python. You are free to choose any platform
version and additional dependencies but provide a justification for them.
- Follow PEP8 guidelines.
- Provide your code on a git repository (private one) on Github. Add the user FeverCodeReviews
as collaborator.

On this project we will evaluate:
- How you develop, style, and consistency of the code
- How the idea matches the given problem
- The software architecture

#### Description
We have an external company that provides us with different events that we fetch, this endpoint
changes every day, providing the new events for the future and removing the old ones.
The main purpose of the application to develop is to provide a HTTP endpoint to query the different events. This endpoint should accept a "start_date" and a "end_date" param, and return only the events within this time range.
- We should only receive the available events (the sell mode is online, the rest should be ignored)
- We should be able to request to this endpoint events from the past (since we have the app
running) and the future.

Considerations:
- The external company provides us an API in a remote server, let's assume the file is served on
this URL:
https://gist.githubusercontent.com/miguelgf/2885fe812638bfb33f785a977f8b7e3c/raw/0bef14cee7d8beb07ec9dabd6b009499f65b85f0/response.xml
- Try to get a fast result in terms of performance
- Don't include comments in your code, use the README.md to explain every decision and
assumptions you have made
- Think about this project as a long-term project for the future and how it will scale (add on the README.md the desitions you have made because of this)

If you have any questions about the test you can contact us


## Run
```shell script
docker-compose up -d --build
```

Check the API with http://127.0.0.1:8000/_health


## Documentation

http://127.0.0.1:8000/docs or http://127.0.0.1:8000/redoc

## Tests
```shell script
docker-compose exec api pytest -vvv .
```


## Considerations
* Using Docker for a project scalable desired to the future.
* API created with [FastAPI](https://fastapi.tiangolo.com), it is a new microframework for me, and I rescue it
 from my TODO list, I think the challenge is a good moment to learn it.
    * Modeling objects with Pydantic.
    * OpenAPI documentation, auto-generated.
* PyTest and TestClient for easy e2e tests.
* For schemas:
    - consider all parameters required except 'organizer_company_id' in BaseEvent.
    - zone is a list in Event.
    - only 1 Event inside of BaseEvent.

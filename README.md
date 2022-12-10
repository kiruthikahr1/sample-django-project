## Environment:
- Python version: 3.7
- Django version: 3.0.6

## Read-Only Files:
- app/tests.py
- manage.py

## Requirements:


In this challenge, your task is to implement a custom Exception Middleware to handle exceptions raised by the provided application according to the given requirements. The provided application raises 3 custom Exceptions defined in `app/exceptions`:

- `ObjectNotFoundException`
- `InvalidDataException`
- `ServiceException`


The idea is that the custom Exception Middleware must process the exceptions and act according to the following requirements:

1. Processing the `ObjectNotFoundException` instance results in rendering an `errors/404.html` template, with the exception instance passed as a context variable named `error` to this template.
2. Processing the `InvalidDataException` instance results in rendering an `errors/400.html` template, with the exception instance passed as a context variable named `error` to this template.
3. Processing the `ServiceException` instance results in rendering an `errors/5xx.html` template, with the exception instance passed as a context variable named `error` to this template.
4. Processing any other `Exception` instance results in rendering an `errors/5xx.html` template, with the exception instance passed as a context variable named `error` to this template.


Implementations for all required templates are provided in the `templates` directory. In order to define your custom Exception Middleware according to the above requirements, you will need to define it somewhere in the code, for example in a new file, and point to this implementation in part of `project/settings.py` that defines Middlewares.

# Mini Blog: Backend of a tini-tiny blog

## Description

This project contains the sources files for the mini blog backend. Also contains additional files and features related
to
the development and deployment of the project.

## Installation

Follow these instructions to setup the project locally. Also, docker support has been added to this project for making
the development setup easier.

- Clone the repository

```bash
git clone git@github.com:ajoydas/mini_blog.git
```

- You need to install python3 and project dependencies. This project is tested with python 3.9 and 3.10. Should work
  fine for python 3.6+.

```bash
cd mini_blog
pip install -r requirements.txt
```

Added support for configuring the app through environment variables utilizing `python-decouple` library.
A default `.env` file has been added to the repository for easy setup. Have a look and modify
if needed.

Start the server with the following commands-

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser # will be needed to access the admin site and change user roles
python manage.py runserver
```

This will create a `db.sqlite3` file in the project directory and run the server on `http://localhost:8000`.

## Components

The APIs are divided into two apps:

- `blog_auth`: Contains APIs related to authentication and users (register, login, profile).
- `blog`: Contains APIs related to posts, comments, and reactions.

### Models

The models can be found at `blog_auth/models.py` and `blog/models.py`. Here is a summary of the models and their
relevant APIs:

- User (default Django user, `username`, `password`, etc.), Profile (`bio`, `role`, `user`) : User can register and
  login. But they can't change their role (Reader, Author, Admin). Only superuser can change
  the role of a user. By default, a user is a Reader.
    - `/api/auth/register`
    - `/api/auth/login`
    - `/api/auth/profile/{username}`
- Post (`owner`, `title`, `body`, `created_at`, `updated_at`): User can create, update, delete, and view posts.
    - `/api/posts`
    - `/api/posts/{post_id}`
    - `/api/posts/{post_id}/comments`
    - `/api/posts/{post_id}/reactions`
    - `/api/posts/{post_id}/reactions/{reaction_id}`
- Comment (`owner`, `post`, `parent`, `body`, `created_at`, `updated_at`): User can create, update, delete, and view
  comments on posts. Comments can be added to posts and other comments.
    - `/api/comments`
    - `/api/comments/{comment_id}`
    - `/api/comments/{comment_id}/replies`
    - `/api/comments/{comment_id}/reactions`
    - `/api/comments/{comment_id}/reactions/{reaction_id}`
- Reaction(`owner`, `post`, `comment`, `reaction_type`, `created_at`, `updated_at`): User can react (i.e., like and
  dislike) to posts and comments. User can also view the number of reactions to
  any specific posts and comments.

To note-

- Both post comment and comment reply creation uses `/api/comments` endpoint where `post_id`  should be set
  within the request body to
  add a post comment and `comment_id` should be set to add a comment reply. This has been designed this way to lessen
  code duplication.
- To make a user `Author` or `Admin`, the user with superuser account needs to change the role of the user. This can be
  done from the
  admin site `/admin` or via the API `/api/auth/profile/{username}` API here username is the username of the user whose
  role needs to be changed.

**Postman Collection**: I have added a collection of Postman requests that I used to test the APIs. The collection can
be found at
the `resources`
directory. [Here](https://learning.postman.com/docs/getting-started/importing-and-exporting-data/#importing-data-into-postman)
you will find the tutorial on importing the collection to Postman.

**API design rationale:**
APIs can designed in focusing on various concepts. While designing the APIs my focus was on keeping related APIs
together. I have also considered how these APIs will be consumed (i.e., their sequences) by any frontend.
For example, reactions won't be dealt without a post or comment. So, instead of having a separate API group for
reactions, I have added them as nested APIs within posts and comments.

## Notable features

- Authentication: Added JWT-based API authentication with the help of `djangorestframework-simplejwt` library.
- API documentation: Added Swagger-based API documentation with the help of `drf-yasg` library.
- Added rate limiting (throttling).
- Added permission/authorization support.
- Admin site support has been added. Access it at `/admin`.
- Added pretty print logging and API response time logging support.

### API documentation

Added Swagger-based API documentation with the help of `drf-yasg` library. The documentation can be accessed
at `/swagger/` and `/redoc/`. Due to limitation of time, only added detailed documentation for the auth app APIs as
examples.

### Testing, Linting, and Code Coverage support

Added a `run_commands.sh` script to run the tests, linting, and code coverage commands. This find can also aid in CI
pipeline to automatically verifying any pull request. Used `flake8` for linting and `coverage` for code coverage.
To run the script, run:

```bash
./run_commands.sh -h
./run_commands.sh --tests --lint --coverage
```

After the coverage command is run, the coverage report can be found in `htmlcov` directory.

Want to mention two special test files:

- `blog/tests/test_rate_limiting.py`: This file contains the tests for rate limiting.
- `blog/tests/test_sequence.py`: Similar to an integration test, contains sequence of API calls mentioned within the
  sequence
  diagram.

### Rate limiting

Used rate limiting to the number of API calls. The defaults are as follows and can be tuned as needed in
the `settings.py`file:

```python
REST_FRAMEWORK = {
    ###
    'DEFAULT_THROTTLE_RATES': {
        'anon': '20/minute',
        'user': '50/minute',
        'user_new_post_creation': '3/minute',
        'user_new_comment_creation': '3/minute',
    }
    ###
}
```

Here, we are only allowing users to create 3 posts and 3 comments per minute as an example. Other APIs will be limited
by the  `anon` (for non-logged in users) and `user`(for logged in users) rate limit.

### Docker support

Added docker support to this project for both development and production environment. The development setup
uses `sqlite3` as the database and the production setup uses `postgres` as the database, a multi-stage image build
setup, and gunicorn as the WSGI server.

To use the development setup, run:

```bash
# builds and runs the docker containers
docker-compose -f docker-compose.dev.yml up
# removes the docker containers
docker-compose -f docker-compose.dev.yml down -v
```

To use the production setup, run:

```bash
# builds and runs the docker containers
docker-compose -f docker-compose.prod.yml up
# removes the docker containers
docker-compose -f docker-compose.prod.yml down -v
```

For both of these the server can be accessed at `http://localhost:8000`. The postgres database can be accessed
at `http://localhost:5432`. Also, within docker a superuser (`super`:`superpass`) is created by default (can be changed
via the `.env` file).

## Future work

Due to time constraints and the scope of the project have not been able to apply all the best practices and add possible
extensions. Some of the notable ones are listed below:

- Testing and Bug fixing: Addition testing such as more testcases can be added to explore hidden bugs. More unit,
  integration, load, performance testing, etc. can be added.
- Pagination: Pagination support can be added as number of posts and comments can be huge.
- Advanced Python and Advanced Django: Though I considerd using advanced python and django features such generators,
  list comphrehensions, Model Managers, `select_related`/`prefetch_related`,
  etc. but have not been able to utilize them here due to the limitation of time and scope,
- Caching: Data caching can be added. Would help to reduce the load on the database (specifically for the popular posts
  and comments).
- Documentation: API documentation and code comments can be improved.
- Better logging, debugging and monitoring support can be added.
- API versioning can be added.

## References

Have used various documentation and tutorials to build this project. Some of them are listed below:

- [Django Documentation](https://docs.djangoproject.com/en/4.2/)
- [Django Rest Framework Documentation](https://www.django-rest-framework.org/)
    - Exceptions: https://www.django-rest-framework.org/api-guide/exceptions/
    - Views: https://www.django-rest-framework.org/api-guide/views/
    - Permissions: https://www.django-rest-framework.org/api-guide/permissions/
    - Throttling: https://www.django-rest-framework.org/api-guide/throttling/
- Docker:
    - https://docs.docker.com/compose/django/
    - https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/
- API documentation:
    - Customizing swagger schema: https://drf-yasg.readthedocs.io/en/stable/custom_spec.html
- JWT Auth: https://django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html






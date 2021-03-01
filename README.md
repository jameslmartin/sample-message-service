# Message Service

## API Documentation

API docs can be found in the `docs/api` directory.

## Quickstart
A Makefile is provided to abstract some of the Docker commands to build and run various parts of the service. If you so choose, you can interact with the project without the Makefile, but will need to emulate some of the Docker commands with their various mounts and network configuration. At any time you can run `make` to see the available commands.

0. Clone this repository
1. Install Docker
2. Run `make build network` to build latest Docker image of the Guild message service and instantiate the network used by docker-compose
3. Create a `.env` file and copy the variables found in `.env-TEMPLATE`
    - Use ```SQLALCHEMY_DATABASE_URI=postgresql://postgres:education@database:5432/messages_dev
    FLASK_ENV=dev``` for the values
4. Run `make service` to run both the Postgres database and service on the same Docker network
    - `IMPORTANT` - The first time this is run will likely fail!! This is because if no database exists, Postgres will run the init scripts located in the mounted init directory. More information on Dockerhub under [Caveats](https://hub.docker.com/_/postgres) - essentially the `depends_on` keyword for the service does not wait long enough for the database to finish coming up and will fail to connect if the db is still initializing
    - Running `make service` again after the db volume has been created should bring up the web service
5. Once the service is running, you can run the functional tests in the project by opening a new terminal and running `make functional-test`

### Health check
A simple `/health` endpoint is provided: `curl localhost:8080/health` should return `UP`

### Design decisions, notes, tradeoffs
The best way to capture some of my thought process throughout this exercise is to bullet list:

- I enjoy writing Python and have previously done a similar exercise to this using Node.js and Mongo
    - Production experience maintaining a Django monolith, Flask is a bit less intimidating for smaller projects
    - Mongo and NoSQL stores can be fun, but I haven't been working with relational databases recently and wanted to poke around with SQLAlchemy
    - Postgres is a great product IMO
- I wanted to see how easy it would be to use Flask
    - Lots of support for Flask, lots of libraries, lots of tutorials specifically for beginners
    - I am not a beginner at writing services so it was a bit of a tax to find a pattern that matched what I was trying to accomplish
- Initially wanted to use SQLite just to get off the ground but I abandoned that decision when researching dependency injection
    - In hindsight, it may have been easier to use because I could have just read/written to a different DB file for each environment
    - Postgres can require migrations, which I spent some unnecessary time researching
        - In production, I would certainly have more hardened init scripts to create tables and schemas for entities. Migrations should only be run if those change. I would need to research better practices around this.
- The use of globals in Flask was a tradeoff, I actually do not prefer it to clean dependency declaration/initialization/passing to layers of API
    - Makes it harder to test
    - Makes it harder to configure the application for different environments
    - Flask request context and use of globals a slight blind spot for me
- I would deliver a production API with an OpenAPI spec and a generated OpenAPI UI/Swagger UI where the endpoints could be interacted with super-easily
    - I have done this with Node.js/Swagger before and it makes it really clean to combine documentation and a functioning test interface
    - Best I could do is follow GitLab's documentation principles and have some sample `curl` requests in the `docs/api` directory
- I would have liked to research/find/use a Flask REST API library that made it easier to do a few things:
    1. Define `Schemas` (different from db schemas) to more easily validate requests and serve responses back from the db
    2. Abstract logic in `routes.py`/API layer, especially around serving responses
    3. Have a cleaner layer abstraction: API layer (handling routes/methods via the lib), controllers (functions invoked by API layer), service layer (functions called by controller), db layer (this is alright as-is using the SQLAlchemy models)
    3. Native OpenAPI spec support
- This project is not very well tested
    - Unit tests with SQLAlchemy would require either:
        1. clean dependency injection, likely through test fixtures
        2. mocking the DB session object and verifying the service layer called the correct functionality
    - I would have liked to test creating Messages in the DB more thoroughly, especially around characters that may behave differently under different encodings
    - I ran out of time to come up with a clean way (through fixtures or otherwise) to clear the database from tests. I would have to create a SQLAlchemy connection to the database and drop the records I had created. I did not program a DELETE endpoint.

### Learnings - Docker networking
Docker networking, especially with Compose, can be frustrating to work with locally. I think I've gone through the same set of learnings about troubleshooting networking between containers more than once. Running a Postgres database in a container is fine for local development but I wasted a few evenings trying to make the development environment easier on myself, only to break things.

- When running things in Docker containers that must be reachable by other external things (like other containers), you must make it available for connectivity outside of its local Docker network/namespace. For example, if I specify my db to accept connections at 127.0.0.1:5432, it is running on that IP **within** its local Docker namespace. The container itself is also a **remote** w.r.t the host machine (your local machine, a virtual machine running Docker, etc.) and the container is given an IP that can change.
- So for this example, to solve this issue of connecting to the database, I had to:
    - Specify a new host **of the container** using `--add-host database:0.0.0.0`. This aliases `database` to ALL IP addresses of the internal Docker network. This means I **should** be able to reach anything on the container by using `database` as the host. Under the hood, this adds an entry with `database` to the `/etc/hosts` file shared by all containers on the specified network.
        - docker-compose will create the specified containers on the same network, and make each addressable by their container name by default
        - Thus, this `--add-host` is only necessary when creating each container (database, service) separately for development. I also had to make sure in development both containers used the same Docker network so they shared the `/etc/host` file.

This was the biggest challenge of this project. I tried a few setups to enable quick iteration. Running the containers on the "host network" seems to create more issues than it solves. I had issues with Flask running on the host network, which was unexpected - even when binding the application to all IPs (0.0.0.0). It's possible that attempting to both bind the database and server at 0.0.0.0 was a cause of some issues.

In production, I would only choose to use managed database products which would likely ease a lot of this headache. As long as there are configurations for each environment, dev/prod can use the dev/prod instances of the database just through their connection objects. As a side note, I think AWS RDS is a great product.

### Development
Running the development environment not through docker-compose is possible with the following commands:

1. Similar to the quickstart, make sure you have built the latest Flask app and created the network with `make build network`
2. Run `make start-db` to create the Postgres container
3. Create the same `.env` file from the Quickstart
4. When it is available to accept connections, open a new shell and run `make dev`. This command will mount your local directory into the container as well, so any edits you make will be mirrored in the container and vice-versa. You can then, in the container run `make start` to start the server with gunicorn or run any Python commands (like `pystest -s app`) that will run the unit tests in the project.

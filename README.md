# INFPRJ01D - Backend

## Getting started

### Prerequisites

* [Python](https://nodejs.org/en/download/) (>=3)
* [Docker](https://www.docker.com/)

### Installation with Docker

Clone the repository and switch to the fe-master branch:

```bash
git clone git@github.com:UNRULYEON/INFPRJ01D.git
cd INFPRJ01D
git checkout be-master
```

Build and run in `-d` (detached) mode with Compose.

```bash
docker-compose up -d
```

Running this command withoud `-d` will let you see the output.

See what's currently running:

```bash
docker-compose ps
```

Stop the service once you're done:

```bash
docker-compose stop
```

Bring down and remove the container:

```bash
docker-compose down
```

When any dependecies change, you probably will need to rebuild the container
for the changes to take effect:

```bash
docker-compose down
docker-compose build
docker-compose up
```

### Installation without Docker

Clone the repository and switch to the fe-master branch:

```bash
git clone git@github.com:UNRULYEON/INFPRJ01D.git
git checkout be-master
```

Install all dependencies:

```bash
pip install -r requirements.txt
```

Run the React project:

```bash
python manage.py runserver
```
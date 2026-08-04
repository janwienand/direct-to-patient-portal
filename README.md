# Pharmacy Direct

Direct-to-patient ordering portal: prescriptions, repeat medication and everyday health
products. Java 17 / Spring Boot, an HTML front end and a Swagger-documented API.

## Overview

Patients browse and buy products (medication) and request services (prescriptions, health
checks). Staff manage orders, users and messages through an admin area.

**This application contains deliberately insecure code and must never be deployed to a
production environment.** It exists so that application security tooling has something
realistic to find. `EXPLOITS.md` documents the intentional weaknesses.

Derived from [fortify/IWA-Java](https://github.com/fortify/IWA-Java).

## Security in this repository

Two checks run on this codebase, both visible in the **Security** tab:

- **Static code analysis** of the source, on `main` and on demand.
- **Open source analysis** of the dependencies, on `main` and on any pull request that
  changes `pom.xml`.

Before pushing, an AI coding agent can run the review skill in
`.github/skills/fortify-change-review/` against the current diff. That is a fast local
check, not a replacement for the pipeline.

## Working with the Repository

In order to execute example scenarios for yourself it is recommended that you "fork" a copy of this repository into
your own GitHub account. The process of "forking" is described in detail in the [GitHub documentation](https://docs.github.com/en/github/getting-started-with-github/fork-a-repo) - you can start the process by clicking on the "Fork" button at the top right.

## Building the Application

To build the application, execute the following from the command line:

```
mvn clean package
```

This will create a JAR file (called `iwa.jar`) in the `target` directory.

To build a WAR file for deployment to an application server such as [Apache Tomcat](http://tomcat.apache.org/)
execute the following:

```
mvn -Pwar clean package
```

This will create a WAR file (called `iwa.war`) in the `target` directory.

## Running the Application

### Development (IDE/command line)

To run (and test) locally in development mode, execute the following from the command line:

```
mvn spring-boot:run
```

### Release (Docker Image)

The JAR file can be built into a [Docker](https://www.docker.com/) image using the provided `Dockerfile` and the
following commands:

```
mvn -Pjar clean package
docker build -t iwa -f Dockerfile .
```

or on Windows:

```
mvn -Pjar clean package
docker build -t iwa -f Dockerfile.win .
```

This image can then be executed using the following commands:

```
docker run -d -p 8888:8080 iwa
```

## Using the Application

To use the application navigate to the URL: [http://localhost:8888](http://localhost:8888). You can carry out a number of
actions unauthenticated, but if you want to login you can do so as one of the following users:

- **user1@localhost.com/password**
- **user2@localhost.com/password**
  
There is also an administrative user:

- **admin@localhost.com/password**

Upon login, you will be subsequently asked for a Multi-Factor Authentication (MFA) code. This functionality
is not yet enabled and you can enter anything here, e.g. `12345`.

### REST APIs 
To run (and test) locally in development mode, Go to Home Page -> My Account -> API Explorer OR
use the following URL: [http://localhost:8888/swagger-ui/index.html?configUrl=/v3/api-docs/swagger-config](http://localhost:8888/swagger-ui/index.html?configUrl=/v3/api-docs/swagger-config)

### API Authentication
every API endpoint is behind authenitcation and thus require to authenticate with JWT Token before pro
Go To "Site" Operations and expand on :
```
/api/v3/site/sign-in
```
Click "Try it Out" button, provide administrative username and password mentioned above and hit "Execute" button.

Copy the "accessToken" value from response and paste into Swagger Authorization (padlock) icon.

Now, go ahead and try the API methods.

## Licensing

This application is made available under the [GNU General Public License V3](LICENSE)

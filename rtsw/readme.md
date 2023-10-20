# RTSW Application

## `tasks.sh`

Defines several commands from installing dependencies to running applications. See other sections for more information on available commands that are specific to each package.

> ```bash
> # Create virtual environment and install dependencies
> ./tasks.sh install
> ```


## `rtsw.shared`

Common data types and methods used in other packages. Includes a datatype to represent the rtsw data points contained in the json files, the method `fetch_hourly_rtsw_json()` to fetch the [json file](https://services.swpc.noaa.gov/products/geospace/propagated-solar-wind-1-hour.json) and parse it, and helper methods for the data sync script.

## `rtsw.persist.manage`

Contains a simple cli program to manage database migrations on a Postgresql database. This allows the peristence layer to be updated in a controlled and reproducible way for additional data sources.

> ```bash
> ./tasks.sh db_manage <command> <args>
> ```

## `rtsw.persist.query`

Contains a script to run the `fetch_hourly_rtsw_json()` method on a recurring schedule with customizable frequency. 

Environment variables are used to configure the script:
- `RTSW_SYNC_FREQ`: Time string with format (HH:MM:SS). Defaults to "00:01:05".
- `RTSW_SYNC_ONCE`: If set to "true", the script will only query the rtsw api once and exit. Defaults to "false".

> ```bash
> ./tasks.sh sync_hourly_rtsw
> ```

## `rtsw.web`

Contains a web app with a dashboard to display the RTSW data. 

Stack:
- Database: Postgresql
- Server/API: FastAPI
- Templating: Jinja2
- Frontend: Bootstrap 5 + HTMX

> ```bash
> # Install dependencies if not done so
> ./tasks.sh install
>
> # Run the web app using uvicorn and start needed services
> ./tasks.sh start_services
> ./tasks.sh serve
> ```
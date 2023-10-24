# RTSW Application

## `tasks.sh`

Defines several commands from installing dependencies to running applications. See other sections for more information on available commands that are specific to each package.


## `rtsw.shared`

Common data types and methods used in other packages. Includes a datatype to represent the rtsw data points contained in the json files, the method `fetch_hourly_rtsw_json()` to fetch the [json file](https://services.swpc.noaa.gov/products/geospace/propagated-solar-wind-1-hour.json) and parse it, and helper methods for the data sync script.

## `rtsw.persist.manage`

Contains a simple cli program to manage database migrations on a Postgresql database. This allows the peristence layer to be updated in a controlled and reproducible way for additional data sources.

> ```bash
> ./tasks.sh db_manage <command> <args>
> ```

### Setup database
> ```bash
> ./tasks.sh db_manage forward --all
> ```

### Rollback database
> ```bash
> ./tasks.sh db_manage rollback --all
> ```


## `rtsw.persist.query`

Contains a script to run the `fetch_hourly_rtsw_json()` method on a recurring schedule with customizable frequency. Alternatively, the script can be scheduled with something like `cron` when the `RTSW_SYNC_ONCE` flag is enabled.

Environment variables are used to configure the script:
- `RTSW_SYNC_FREQ`: Cron schedule string.
- `RTSW_SYNC_ONCE`: If set to "true", the script will only query the rtsw api once and exit. Defaults to "false".
- `RTSW_SYNC_MAX_RETRY`: Number of times to retry the query if it fails. Defaults to 3.

> ```bash
> # Syncs newest data on a schedule
> ./tasks.sh sync
>
> # Syncs full data (/products/geospace/propagated-solar-wind.json)
> ./tasks.sh sync --full
> ```

## `rtsw.web`

Contains a web app with a dashboard to display the RTSW data. 

Stack:
- Database: Postgresql
- Server/API: FastAPI
- Templating: Jinja2
- Frontend: Bootstrap 5 + HTMX

### Getting started

> ```bash
> # Install dependencies if not done so
> ./tasks.sh install
>
> # Setup database if not done so
> ./tasks.sh db_manage forward --all
>
> # Sync some data
> ./tasks.sh sync --full
>
> # Run the web app using uvicorn and start needed services
> ./tasks.sh start_services
> ./tasks.sh serve
> ```
import logging
from pathlib import Path

import awswrangler as wr
import polars as pl
import typer
from polars.testing import assert_frame_equal

from compare_df_cli import __title__, __version__

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)
logger = logging.getLogger("compare_df_cli")

app = typer.Typer(
    name="compare_df_cli", help="Small CLI tool designed to compare polars dataframes"
)


def version_callback(version: bool):
    if version:
        typer.echo(f"{__title__} {__version__}")
        raise typer.Exit()


def read_csv_as_df(path: str) -> pl.DataFrame:
    path = Path(path)
    print(pl.read_csv(path))


def query_athena(query: str, database: str) -> pl.DataFrame:
    pandas_df = wr.athena.read_sql_query(query, database)
    return pl.from_pandas(pandas_df)


FromCsvOption = typer.Option(
    None,
    "-f",
    "--from-csv",
    metavar="PATH",
    help="path to the csv file",
)
FromQueryOption = typer.Option(
    None, "-q", "--from-query", metavar="QUERY", help="query to athena database"
)
DataBaseOption = typer.Option(
    None, "-d", "--database", metavar="DATABASE", help="athena database name"
)


@app.command()
def main(
    FromCsvOption: str = FromCsvOption,
    FromQueryOption: str = FromQueryOption,
    DataBaseOption: str = DataBaseOption,
):
    """
    This is the entry point of your command line application. The values of the CLI params that
    are passed to this application will show up als parameters to this function.

    This docstring is where you describe what your command line application does.
    Try running `python -m compare_df_cli --help` to see how this shows up in the command line.
    """

    logger.info("Looks like you're all set up. Let's get going!")

    all_params_provided = all([FromCsvOption, FromQueryOption, DataBaseOption])
    if not all_params_provided:
        raise Exception(
            "You need to provide all the parameters to run the application, use --help to see the options."
        )

    csv_df = read_csv_as_df(FromCsvOption)
    athena_df = query_athena(FromQueryOption, DataBaseOption)
    assert_frame_equal(
        csv_df, athena_df, check_column_order=False, check_row_order=False
    )


if __name__ == "__main__":
    app()

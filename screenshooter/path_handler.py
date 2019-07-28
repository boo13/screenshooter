from pathlib import Path, PurePath

BASE_DIR = Path(__file__).resolve().parent.parent


def make_output_dir(fileName):

    OUTPUT_DIR = BASE_DIR.joinpath("output")
    new_dir = OUTPUT_DIR.joinpath(fileName)

    try:
        Path.mkdir(new_dir)
        OUTPUT_DIR = OUTPUT_DIR.joinpath(fileName)

    except FileNotFoundError as e:
        print("A missing parent folder - problem in the path.")
        exit(e)

    except FileExistsError as e:

        print("The file already exists")
        import config

        if config.OVERWRITE_OUTPUT:
            Path.mkdir(new_dir, exist_ok=True)
            OUTPUT_DIR = OUTPUT_DIR.joinpath(fileName)
        else:
            exit(e)

    return OUTPUT_DIR

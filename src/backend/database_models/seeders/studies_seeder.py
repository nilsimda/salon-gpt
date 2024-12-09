import pathlib
from uuid import uuid4

from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.orm import Session

from backend.database_models.interview import Interview

load_dotenv()

studies_d = {
    "JackDaniels": "Eine Studie zum Thema Whiskey",
    "InfiniteRoots": "Fleischersatz aus Pilzwurzeln",
    "Wempe": "Luxus",
}


def studies_seed(op):
    """
    Seed studies
    """
    _ = Session(op.get_bind())

    for study_name, study_description in studies_d.items():
        study_id = str(uuid4())
        sql_command = text(
            """
            INSERT INTO studies (
                id, name, description, is_being_added, created_at, updated_at
            )
            VALUES (
                :id, :name, :description, :is_being_added, now(), now()
            )
            ON CONFLICT (id) DO NOTHING;
        """
        ).bindparams(
            id=study_id,
            name=study_name,
            description=study_description,
            is_being_added=False,
        )
        op.execute(sql_command)

        for path in pathlib.Path(f"src/backend/data/transcripts/{study_name}/").glob(
            "*.txt"
        ):
            print(path)
            with open(path, "r") as f:
                interview_text = f.read()
            name = path.stem
            start_split = name.split("_")[0]
            if start_split.startswith("GD"):
                type = "GD"
            elif start_split.startswith("Memo"):
                type = "Memo"
            else:
                type = "TI"

            interview_id = str(uuid4())
            sql_command = text(
                """
                INSERT INTO interviews (
                    id, text, title, type, fields, study_id, created_at, updated_at
                )
                VALUES (
                    :id, :text, :title, :type, :fields, :study_id, now(), now()
                )
                ON CONFLICT (id) DO NOTHING;
            """
            ).bindparams(
                id=interview_id,
                text=interview_text,
                title=name,
                type=type,
                fields=None,
                study_id=study_id,
            )
            op.execute(sql_command)


def delete_default_models(op):
    """
    Delete deployments and models.
    """
    session = Session(op.get_bind())
    session.query(Interview).delete()
    session.commit()

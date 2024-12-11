import pathlib
from uuid import uuid4

from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.orm import Session

load_dotenv()

def studies_seed(op):
    """
    Seed studies with their interviews.
    """
    _ = Session(op.get_bind())

    for study_folder in pathlib.Path("/data/transcripts/").glob("*"):
        study_name = study_folder.stem
        print(study_name)
        study_id = str(uuid4())
        sql_command = text(
            """
            INSERT INTO studies (
                id, name, description, is_transcribed, created_at, updated_at
            )
            VALUES (
                :id, :name, :description, :is_transcribed, now(), now()
            )
            ON CONFLICT (id) DO NOTHING;
        """
        ).bindparams(
            id=study_id,
            name=study_name,
            description="",
            is_transcribed=True,
        )
        op.execute(sql_command)

        for path in study_folder.glob(
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
                    id, text, title, interview_type, fields, study_id, created_at, updated_at
                )
                VALUES (
                    :id, :text, :title, :interview_type, :fields, :study_id, now(), now()
                )
                ON CONFLICT (id) DO NOTHING;
            """
            ).bindparams(
                id=interview_id,
                text=interview_text,
                title=name,
                interview_type=type,
                fields=None,
                study_id=study_id,
            )
            op.execute(sql_command)


def delete_studies(op):
    """
    Delete studies.
    """
    pass

import tempfile
from pathlib import Path
from booknlp.booknlp import BookNLP

model_params = {"pipeline": "entity,quote,supersense,event,coref", "model": "small"}
booknlp = BookNLP("en", model_params)


def booknlp(text: str):
    with tempfile.TemporaryDirectory() as tmp_dir:
        dir_path = Path(tmp_dir)

        input_file = dir_path / "input_file.txt"
        with input_file.open("a") as f:
            f.write(text)

        booknlp.process(input_file, dir_path, "nlp")

        ### Read in results here ###

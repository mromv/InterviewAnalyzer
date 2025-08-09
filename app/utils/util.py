import json
from pydantic import BaseModel

def save_model_to_json(model: BaseModel, path: str) -> None:
    data = model.model_dump(
        exclude={
            "interviews": {
                "__all__": {
                    "interview_hypotheses": {
                        "__all__": {
                            "questions"
                        }
                    }
                }
            }
        }
    )
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

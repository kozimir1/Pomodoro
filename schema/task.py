from pydantic import BaseModel, model_validator, Field, ConfigDict


class TaskSchema(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    name: str | None = None
    pomodoro_count: int | None = None
    category_id: int   # = Field(exclude=True)

    # class Config:
    #     from_attributes = True



    @model_validator(mode='after')
    def name_and_pomodoro_count(self):
        print(self)
        if self.pomodoro_count is None and self.name is None:
            raise ValueError("name and pomodoro count cannot be None")
        return self

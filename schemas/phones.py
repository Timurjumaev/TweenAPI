from pydantic import BaseModel, validator


class CreatePhone(BaseModel):
    number: str
    comment: str

    @validator('number')
    def number_validate(cls, value):
        if len(value) != 9:
            raise ValueError('Bu telefon raqam emas!')
        return value

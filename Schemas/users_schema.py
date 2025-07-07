from pydantic import BaseModel, field_validator, Field, EmailStr

class UserSchema(BaseModel):
    name: str | None = Field(default = None, max_length = 32)
    email: EmailStr | None = Field(default = None, max_length=255)
    password: str | None = Field(default = None, max_length=255)


    class Config:
        orm_mode = True

    @classmethod
    @field_validator("name")
    def validate_name(cls, value):
        if value is not None and len(value) > 32:
            raise ValueError("Name too long")
        return value
    
    @classmethod
    @field_validator("password")
    def validate_password(cls, value):
        if value is not None and len(value) > 255:
            raise ValueError("Password too long")
        return value
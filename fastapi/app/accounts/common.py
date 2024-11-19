from pydantic import BaseModel, Field, field_validator


class ForgetPasswordRequestModel(BaseModel):
    email: str
    old_password: str
    new_password: str


class UserRegistrationRequestModel(BaseModel):
    email: str
    password: str = Field(...)  # Minimum length of 8 characters

    @field_validator("password")
    def validate_password(cls, value):
        errors = []

        # Validate minimum length
        if len(value) < 8:
            errors.append("Password must be at least 8 characters long")

        # Validate for at least one uppercase letter
        if not any(char.isupper() for char in value):
            errors.append("Password must contain at least one uppercase letter")

        # Validate for at least one lowercase letter
        if not any(char.islower() for char in value):
            errors.append("Password must contain at least one lowercase letter")

        # Validate for at least one digit
        if not any(char.isdigit() for char in value):
            errors.append("Password must contain at least one digit")

        # Validate for at least one special character
        if not any(char in r"!@#$%^&*()-_=+{};:,<.>" for char in value):
            errors.append("Password must contain at least one special character")

        if errors:
            raise ValueError("\n".join(errors))

        return value

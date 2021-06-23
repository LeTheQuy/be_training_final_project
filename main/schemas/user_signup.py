import re

from marshmallow import validates, ValidationError

from main.schemas.base.user import UserSchema

# Minimum eight characters, at least one uppercase letter, one lowercase letter, one number and one special character
PASSWORD_PATTERN = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"


class UserSignUpSchema(UserSchema):
    @validates("password")
    def validate_password(self, password):
        result = re.findall(PASSWORD_PATTERN, password)
        if result:
            return True
        else:
            raise ValidationError("Password must be minimum 8  at least one uppercase letter, one lowercase letter,"
                                  " one number and one special character")




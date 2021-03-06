import colander
from colander import Float
from colander import SchemaNode
from colander import String

import deform


@colander.deferred
def deferred_username_validator(node, kw):
    request = kw['request']

    def validate_username(node, value):
        if len(value) < 4 or len(value) > 24:
            raise colander.Invalid(node,
                                   "Length of user name must be between 4 and \
                                    24 lowercase alphanumeric characters")
        if not value.replace('_', '').isalnum() or not value.islower():
            raise colander.Invalid(node,
                                   "Only lowercase numbers, letters and \
                                   underscores are permitted")
        if not value[0].isalpha():
            raise colander.Invalid(node,
                                   "The username must start with a \
                                   letter")

        query = request.context.find(_id=value)

        if query.count() > 0:
            raise colander.Invalid(node, "Username is not available")

    return validate_username


email_widget = deform.widget.CheckedInputWidget(
    subject="Email",
    confirm_subject="Confirm Email",
    size=40
    )


class EmailSchema(colander.Schema):
    email = SchemaNode(String(),
                       title="email",
                       description='Type your email address and confirm it',
                       validator=colander.Email(),
                       widget=email_widget)


class PasswordSchema(colander.Schema):
    password = SchemaNode(String(),
                          validator=colander.Length(min=6),
                          widget=deform.widget.CheckedPasswordWidget(size=40),
                          description="Type your password and confirm it")


class UserSchema(colander.MappingSchema):
    _id = SchemaNode(String(),
                     title="Username",
                     description="The name of the participant",
                     validator=deferred_username_validator)
    given_name = SchemaNode(String(), missing='',
                            title="Given Name")
    surname = SchemaNode(String(), missing='',
                         title="Surname")
    street_address = SchemaNode(
        String(), missing='',
        title="Street Address",
        description='Address info (number, street, unit)')
    locality = SchemaNode(String(), missing='',
                      title='City',
                      description="City or township name")
    ## TODO: There must be an ISO list for this
    region = SchemaNode(String(), missing='',
                       title='Locality',
                       description='State, Province, Township or equivalent')
    postal_code = SchemaNode(String(), missing='',
                             title='Postal Code',
                             description='ZIP or postal code')
    ## TODO: make this oneOf ISO countries
    country_name = SchemaNode(String(), missing='',
                              title='Country',
                              description='Country')
    telephone = SchemaNode(String(), missing='',
                       title='Telephone Number')
    fax = SchemaNode(String(), missing='',
                     title='Fax number')
    website_url = SchemaNode(String(), missing='',
                             title='Website URL',
                             description='I.e. http://example.com')
    latitude = SchemaNode(Float(), missing=colander.null,
                          title='Latitude')
    longitude = SchemaNode(Float(), missing=colander.null,
                           title='Longitude')
    email = SchemaNode(String(),
                       title="email",
                       description='Type your email address and confirm it',
                       validator=colander.Email(),
                       widget=email_widget)
    password = SchemaNode(String(),
                          validator=colander.Length(min=6),
                          widget=deform.widget.CheckedPasswordWidget(size=40),
                          description="Type your password and confirm it")


class SimpleUserSchema(colander.MappingSchema):
    _id = SchemaNode(String(),
                         title="Username",
                         description="The name of the participant",
                         validator=deferred_username_validator)
    display_name = SchemaNode(String(), missing=colander.null,
                              title="Display Name",
                              widget=deform.widget.TextInputWidget(size=40))
    email = SchemaNode(String(),
                       title="email",
                       description='Type your email address and confirm it',
                       validator=colander.Email(),
                       widget=email_widget)
    password = SchemaNode(String(),
                          validator=colander.Length(min=6),
                          widget=deform.widget.CheckedPasswordWidget(size=40),
                          description="Type your password and confirm it")

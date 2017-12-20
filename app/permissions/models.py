from app import db

user_permissions = db.Table(
    'user_permissions',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id'))
)


class Permission(db.Model):
    """Model representing a permission a user can have."""
    __table_args__ = (
        db.UniqueConstraint('school_id', 'name'),
        {}
    )

    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))
    name = db.Column(db.String(120))
    description = db.Column(db.String(240))

    # Provides the default permissions to create
    DEFAULTS = [
        {
            "name": "Administrator",
            "description": "Allows a user to be an admin."
        },
        {
            "name": "Teacher",
            "description": "Allows a user to be a teacher."
        },
        {
            "name": "Student",
            "description": "Allows a user to be a student."
        },
        {
            "name": "Parent",
            "description": "Allows user to be a parent."
        },
    ]

    def __init__(self, name, school_id, description):
        self.name = name
        self.school_id = school_id
        self.description = description

    def to_dict(self):
        return {
            'id': self.id,
            'school_id': self.school_id,
            'name': self.name,
            'description': self.description
        }

    @classmethod
    def default_permissions(cls, school_id):
        permissions = []
        for permission in cls.DEFAULTS:
            permissions.append(cls(school_id=school_id, **permission))
        return permissions

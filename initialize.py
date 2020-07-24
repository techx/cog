
def rebuild():
    from cog.models import db
    db.reflect()
    db.drop_all()
    db.create_all()


if __name__ == '__main__':
    rebuild()
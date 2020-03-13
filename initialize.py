if __name__ == '__main__':
    from hardwarecheckout.models import db
    db.reflect()
    db.drop_all()
    db.create_all()

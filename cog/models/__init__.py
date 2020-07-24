from flask_sqlalchemy import SQLAlchemy

class SerializableAlchemy(SQLAlchemy):
    def apply_driver_hacks(self, app, info, options):
        # if not 'isolation_level' in options:
        #     options['isolation_level'] = 'SERIALIZABLE'
        return super(SerializableAlchemy, self).apply_driver_hacks(app, info, options)
db = SerializableAlchemy()

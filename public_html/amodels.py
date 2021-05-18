from peewee import * 

db = SqliteDatabase('savdo.db')

class BaseModel(Model):
    class Meta:
        database = db


class Drugs(BaseModel):
    barcode = IntegerField()
    name = CharField()
    unit = CharField()

    class Meta:
        primary_key = False

if __name__ == '__main__':
    Drugs.create_table()
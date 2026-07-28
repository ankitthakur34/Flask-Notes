def test_database(app):

    from app.extensions import db

    assert db is not None
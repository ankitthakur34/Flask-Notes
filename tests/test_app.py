def test_app(app):

    assert app.config["TESTING"] == True

    assert app.config["ENV_NAME"] == "testing"


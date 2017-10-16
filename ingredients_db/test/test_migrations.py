import json

import pytest
from alembic import command
from alembicverify.util import (
    prepare_schema_from_migrations,
    get_head_revision, get_current_revision)
from sqlalchemy import create_engine
from sqlalchemydiff import compare
from sqlalchemydiff.util import prepare_schema_from_models

from ingredients_db.database import Base


@pytest.fixture()
def alembic_root():
    return "ingredients_db:alembic"


@pytest.fixture()
def uri():
    yield "postgresql+psycopg2://postgres@localhost"


@pytest.fixture()
def uri_left(uri):
    db_path = uri + '/left'
    yield db_path


@pytest.fixture()
def uri_right(uri):
    db_path = uri + '/right'
    yield db_path


def setup_extensions(uri):
    engine = create_engine(uri)
    engine.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
    engine.execute('CREATE EXTENSION IF NOT EXISTS "hstore"')


class TestMigrations(object):
    @pytest.mark.usefixtures("new_db_left")
    def test_upgrade_and_downgrade(self, uri_left, alembic_config_left):
        """Test all migrations up and down.
        Tests that we can apply all migrations from a brand new empty
        database, and also that we can remove them all.
        """
        setup_extensions(uri_left)
        engine, script = prepare_schema_from_migrations(uri_left, alembic_config_left)
        head = get_head_revision(alembic_config_left, engine, script)
        current = get_current_revision(alembic_config_left, engine, script)

        assert head == current

        while current is not None:
            command.downgrade(alembic_config_left, '-1')
            current = get_current_revision(alembic_config_left, engine, script)

    @pytest.mark.usefixtures("new_db_left")
    @pytest.mark.usefixtures("new_db_right")
    def test_model_and_migration_schemas_are_the_same(self, uri_left, uri_right, alembic_config_left):
        """Compare two databases.
        Compares the database obtained with all migrations against the
        one we get out of the models.
        """

        setup_extensions(uri_left)
        prepare_schema_from_migrations(uri_left, alembic_config_left)

        from ingredients_db.models.images import Image, ImageMembers
        from ingredients_db.models.instance import Instance, InstancePublicKey
        from ingredients_db.models.network import Network
        from ingredients_db.models.network_port import NetworkPort, NetworkableEntity
        from ingredients_db.models.project import Project
        from ingredients_db.models.public_key import PublicKey
        from ingredients_db.models.task import Task, TaskableEntity
        from ingredients_db.models.authn import AuthNUser, AuthNToken

        # Make sure the imports don't go away
        Image.mro()
        ImageMembers.mro()
        Instance.mro()
        InstancePublicKey.mro()
        Network.mro()
        NetworkPort.mro()
        NetworkableEntity.mro()
        Project.mro()
        PublicKey.mro()
        Task.mro()
        TaskableEntity.mro()
        AuthNUser.mro()
        AuthNToken.mro()

        setup_extensions(uri_right)
        prepare_schema_from_models(uri_right, Base)

        result = compare(uri_left, uri_right, {'alembic_version'})

        print(json.dumps(result.errors, indent=4))
        assert result.is_match

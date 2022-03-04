# Import all the models, so that Base has them before being
# imported by Alembic
from news.db.db.base_class import Base  # noqa
from news.db.models import Article  # noqa

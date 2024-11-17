import factory

from backend.database_models import Interview

from .base import BaseFactory


class InterviewFactory(BaseFactory):
    class Meta:
        model = Interview

    user_id = factory.Faker("uuid4")
    title = factory.Faker("sentence")
    url = factory.Faker("url")
    conversation_id = factory.Faker("uuid4")
    message_id = factory.Faker("uuid4")
    document_id = factory.Faker("uuid4")
    text = factory.Faker("text")

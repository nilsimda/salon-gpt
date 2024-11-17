import factory

from backend.database_models import CitationInterviews

from .base import BaseFactory


class CitationInterviewsFactory(BaseFactory):
    class Meta:
        model = CitationInterviews

    left_id = factory.Faker("uuid4")
    right_id = factory.Faker("uuid4")

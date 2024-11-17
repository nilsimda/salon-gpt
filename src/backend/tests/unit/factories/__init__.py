from backend.tests.unit.factories.agent import AgentFactory
from backend.tests.unit.factories.agent_deployment_model import (
    AgentDeploymentModelFactory,
)
from backend.tests.unit.factories.agent_tool_metadata import AgentToolMetadataFactory
from backend.tests.unit.factories.blacklist import BlacklistFactory
from backend.tests.unit.factories.citation import CitationFactory
from backend.tests.unit.factories.citation_documents import CitationInterviewsFactory
from backend.tests.unit.factories.conversation import (
    ConversationFactory,
    ConversationFileAssociationFactory,
)
from backend.tests.unit.factories.deployment import DeploymentFactory
from backend.tests.unit.factories.document import InterviewFactory
from backend.tests.unit.factories.file import FileFactory
from backend.tests.unit.factories.group import GroupFactory
from backend.tests.unit.factories.message import (
    MessageFactory,
    MessageFileAssociationFactory,
)
from backend.tests.unit.factories.model import ModelFactory
from backend.tests.unit.factories.organization import OrganizationFactory
from backend.tests.unit.factories.snapshot import (
    SnapshotAccessFactory,
    SnapshotFactory,
    SnapshotLinkFactory,
)
from backend.tests.unit.factories.tool_auth import ToolAuthFactory
from backend.tests.unit.factories.tool_call import ToolCallFactory
from backend.tests.unit.factories.user import UserFactory

FACTORY_MAPPING = {
    "User": UserFactory,
    "Blacklist": BlacklistFactory,
    "File": FileFactory,
    "Conversation": ConversationFactory,
    "Citation": CitationFactory,
    "CitationInterviews": CitationInterviewsFactory,
    "Message": MessageFactory,
    "Interview": InterviewFactory,
    "Agent": AgentFactory,
    "Organization": OrganizationFactory,
    "ToolCall": ToolCallFactory,
    "ToolAuth": ToolAuthFactory,
    "Snapshot": SnapshotFactory,
    "SnapshotLink": SnapshotLinkFactory,
    "SnapshotAccess": SnapshotAccessFactory,
    "AgentToolMetadata": AgentToolMetadataFactory,
    "Model": ModelFactory,
    "Deployment": DeploymentFactory,
    "AgentDeploymentModel": AgentDeploymentModelFactory,
    "ConversationFileAssociation": ConversationFileAssociationFactory,
    "MessageFileAssociation": MessageFileAssociationFactory,
    "Group": GroupFactory,
}


def get_factory(model_name, session=None):
    factory = FACTORY_MAPPING[model_name]
    factory._meta.sqlalchemy_session = session
    return factory

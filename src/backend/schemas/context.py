from typing import Any, Optional

from pydantic import BaseModel

from backend.crud import user as user_crud
from backend.database_models.database import DBSessionDep
from backend.schemas.agent import Agent
from backend.schemas.study import Study
from backend.schemas.user import User
from backend.services.logger.utils import LoggerFactory


class Context(BaseModel):
    request: Optional[dict] = {}
    response: Optional[dict] = {}
    receive: Optional[dict] = {}
    trace_id: str = "default"
    user_id: str = "default"
    user: Optional[User] = None
    agent: Optional[Agent] = None
    model: Optional[str] = None
    deployment_name: Optional[str] = None
    deployment_config: Optional[dict] = None
    conversation_id: Optional[str] = None
    agent_id: Optional[str] = None
    stream_start_ms: Optional[float] = None
    logger: Optional[Any] = None
    use_global_filtering: Optional[bool] = False
    study: Optional[Study] = None
    study_id: Optional[str] = None

    def __init__(self):
        super().__init__()
        self.with_logger()

    def set_request(self, request):
        self.request = request

    def set_response(self, response):
        self.response = response

    def set_receive(self, receive):
        self.receive = receive

    def with_logger(self):
        if self.logger is not None:
            return self

        logger = LoggerFactory().get_logger()
        logger.bind(trace_id=self.trace_id, user_id=self.user_id)
        self.logger = logger
        return self

    def with_trace_id(self, trace_id: str):
        self.trace_id = trace_id

    def with_user_id(self, user_id: str):
        self.user_id = user_id

    def with_deployment_name(self, deployment_name: str):
        self.deployment_name = deployment_name

    def with_user(
        self, session: DBSessionDep | None = None, user: User | None = None
    ) -> "Context":
        if not user and not session:
            return self

        if not user:
            user = user_crud.get_user(session, self.user_id)
            user = User.model_validate(user)

        if user:
            self.user = user

        return self

    def with_study(self, study: Study | None) -> "Context":
        self.study = study
        return self

    def with_agent(self, agent: Agent | None) -> "Context":
        self.agent = agent
        return self

    def with_model(self, model: str) -> "Context":
        self.model = model
        return self

    def with_conversation_id(self, conversation_id: str) -> "Context":
        self.conversation_id = conversation_id
        return self

    def with_stream_start_ms(self, now_ms: float) -> "Context":
        self.stream_start_ms = now_ms

    def with_agent_id(self, agent_id: str) -> "Context":
        if not agent_id:
            return self

        self.agent_id = agent_id
        return self

    def with_global_filtering(self) -> "Context":
        self.use_global_filtering = True
        return self

    def without_global_filtering(self) -> "Context":
        self.use_global_filtering = False
        return self

    def get_stream_start_ms(self):
        return self.stream_start_ms

    def get_request(self):
        return self.request

    def get_response(self):
        return self.response

    def get_receive(self):
        return self.receive

    def get_trace_id(self):
        return self.trace_id

    def get_study(self):
        return self.study

    def get_study_id(self):
        return self.study_id

    def get_user_id(self):
        return self.user_id

    def get_event_type(self):
        return self.event_type

    def get_model(self):
        return self.model

    def get_deployment_name(self):
        return self.deployment_name

    def get_model_config(self):
        return self.model_config

    def get_conversation_id(self):
        return self.conversation_id

    def get_agent_id(self):
        return self.agent_id

    def get_logger(self) -> Any:
        return self.logger

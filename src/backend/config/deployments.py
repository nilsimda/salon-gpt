from enum import StrEnum

from backend.config.settings import Settings
from backend.model_deployments import (
    FasterWhisperDeployment,
    OllamaDeployment,
)
from backend.model_deployments.base import BaseDeployment
from backend.model_deployments.faster_whisper_platform import FW_ENV_VARS
from backend.model_deployments.ollama_platform import OLLAMA_ENV_VARS
from backend.schemas.deployment import Deployment
from backend.services.logger.utils import LoggerFactory

logger = LoggerFactory().get_logger()


class ModelDeploymentName(StrEnum):
    Ollama = "Ollama"
    FasterWhisper = "FasterWhisper"

# TODO names in the map below should not be the display names but ids
ALL_MODEL_DEPLOYMENTS = {
    ModelDeploymentName.Ollama: Deployment(
        id="ollama",
        name=ModelDeploymentName.Ollama,
        deployment_class=OllamaDeployment,
        models=OllamaDeployment.list_models(),
        is_available=OllamaDeployment.is_available(),
        env_vars=OLLAMA_ENV_VARS,
    ),
    ModelDeploymentName.FasterWhisper: Deployment(
        id="faster_whisper",
        name=ModelDeploymentName.FasterWhisper,
        deployment_class=FasterWhisperDeployment,
        models=FasterWhisperDeployment.list_models(),
        is_available=FasterWhisperDeployment.is_available(),
        env_vars=FW_ENV_VARS,
    ),
}

def get_available_deployments() -> dict[ModelDeploymentName, Deployment]:
    deployments = Settings().deployments.enabled_deployments
    if deployments is not None and len(deployments) > 0:
        return {
            key: value
            for key, value in ALL_MODEL_DEPLOYMENTS.items()
            if value.id in Settings().deployments.enabled_deployments
        }

    return ALL_MODEL_DEPLOYMENTS


def get_default_deployment(**kwargs) -> BaseDeployment:
    # Fallback to the first available deployment
    fallback = None
    for deployment in AVAILABLE_MODEL_DEPLOYMENTS.values():
        if deployment.is_available:
            fallback = deployment.deployment_class(**kwargs)
            break

    default = Settings().deployments.default_deployment
    if default:
        return next(
            (
                v.deployment_class(**kwargs)
                for k, v in AVAILABLE_MODEL_DEPLOYMENTS.items()
                if v.id == default
            ),
            fallback,
        )
    else:
        return fallback


AVAILABLE_MODEL_DEPLOYMENTS = get_available_deployments()

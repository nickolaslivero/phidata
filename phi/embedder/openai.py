from typing import Optional, Dict, List, Tuple, Any
from typing_extensions import Literal
import requests

from phi.embedder.base import Embedder
from phi.utils.log import logger

from root_server_ip import SERVER_IP

try:
    from openai import OpenAI as OpenAIClient
    from openai.types.create_embedding_response import CreateEmbeddingResponse
except ImportError:
    raise ImportError("`openai` not installed")


class LMStudioEmbedder(Embedder):
    model: str = "nomic-ai/nomic-embed-text-v1.5-GGUF/nomic-embed-text-v1.5.Q5_K_M.gguf"
    base_url: str = SERVER_IP
    dimensions: int = 768
    encoding_format: Literal["float", "base64"] = "float"
    user: Optional[str] = None
    request_params: Optional[Dict[str, Any]] = None

    def _response(self, text: str) -> Dict[str, Any]:
        url = f"{self.base_url}/embeddings"
        logger.debug(f"Enviando solicitação para {url} com texto: {text}")
        request_data = {
            "model": self.model,
            "input": text
        }
        if self.request_params:
            request_data.update(self.request_params)
        response = requests.post(url, json=request_data)
        logger.debug(f"Resposta do servidor: {response.status_code} - {response.text}")
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Falha ao obter resposta do LM Studio: {response.text}")

    def get_embedding(self, text: str) -> List[float]:
        response = self._response(text)
        try:
            # Extraindo o vetor de embedding da resposta
            data = response.get('data', [])
            if not data or 'embedding' not in data[0]:
                raise ValueError("Resposta inválida, 'embedding' não encontrado.")

            embedding = data[0]['embedding']
            if len(embedding) != self.dimensions:
                raise ValueError(f"Dimensões incorretas: esperadas {self.dimensions}, obtidas {len(embedding)}")

            logger.debug(f"Embedding obtido: {embedding}")
            return embedding
        except Exception as e:
            logger.warning(f"Erro ao obter embedding: {e}")
            return []

    def get_embedding_and_usage(self, text: str) -> Tuple[List[float], Optional[Dict]]:
        response = self._response(text)
        try:
            embedding = self.get_embedding(text)
            usage = response.get("usage", {})
            return embedding, usage
        except Exception as e:
            logger.warning(e)
            return [], None


class OpenAIEmbedder(LMStudioEmbedder):
    encoding_format: Literal["float", "base64"] = "float"
    user: Optional[str] = None
    api_key: Optional[str] = "lm-studio"
    organization: Optional[str] = None
    base_url: str = SERVER_IP
    request_params: Optional[Dict[str, Any]] = None
    client_params: Optional[Dict[str, Any]] = None
    openai_client: Optional[OpenAIClient] = None

    @property
    def client(self) -> OpenAIClient:
        if self.openai_client:
            return self.openai_client

        _client_params: Dict[str, Any] = {}
        if self.api_key:
            _client_params["api_key"] = self.api_key
        if self.organization:
            _client_params["organization"] = self.organization
        if self.base_url:
            _client_params["base_url"] = self.base_url
        if self.client_params:
            _client_params.update(self.client_params)
        return OpenAIClient(**_client_params)

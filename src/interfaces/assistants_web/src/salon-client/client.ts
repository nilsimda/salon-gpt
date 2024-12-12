import { FetchEventSourceInit, fetchEventSource } from '@microsoft/fetch-event-source';

import {
  SalonChatRequest,
  SalonClientGenerated,
  CohereNetworkError,
  CohereUnauthorizedError,
  CreateUserV1UsersPostData,
  Fetch,
  ToggleConversationPinRequest,
  UpdateConversationRequest,
} from '@/salon-client';

import { mapToChatRequest } from './mappings';

export class SalonClient {
  private readonly hostname: string;
  private readonly fetch: Fetch;
  private authToken?: string;

  public salonService: SalonClientGenerated;
  public request?: any;

  constructor({
    hostname,
    fetch,
    authToken,
  }: {
    hostname: string;
    fetch: Fetch;
    authToken?: string;
  }) {
    this.hostname = hostname;
    this.fetch = fetch;
    this.authToken = authToken;
    this.salonService = new SalonClientGenerated({
      BASE: hostname,
      HEADERS: async () => this.getHeaders(true),
    });

    this.salonService.request.config.interceptors.response.use((response) => {
      if (response.status === 401) {
        throw new CohereUnauthorizedError();
      }
      return response;
    });
  }


  public async chat({
    request,
    headers,
    agentId,
    regenerate,
    signal,
    onOpen,
    onMessage,
    onClose,
    onError,
  }: {
    request: SalonChatRequest;
    headers?: Record<string, string>;
    agentId?: string;
    signal?: AbortSignal;
    regenerate?: boolean;
    onOpen?: FetchEventSourceInit['onopen'];
    onMessage?: FetchEventSourceInit['onmessage'];
    onClose?: FetchEventSourceInit['onclose'];
    onError?: FetchEventSourceInit['onerror'];
  }) {
    const chatRequest = mapToChatRequest(request);
    const requestBody = JSON.stringify({
      ...chatRequest,
    });

    const endpoint = this.getChatStreamEndpoint(regenerate, agentId);
    return await fetchEventSource(endpoint, {
      method: 'POST',
      headers: { ...this.getHeaders(), ...headers },
      body: requestBody,
      signal,
      openWhenHidden: true, // When false, the requests will be paused when the tab is hidden and resume/retry when the tab is visible again
      onopen: onOpen,
      onmessage: onMessage,
      onclose: onClose,
      onerror: onError,
    });
  }

  public listConversations(params: {
    userId: string
    offset?: number;
    limit?: number;
    orderBy?: string;
    agentId?: string;
  }) {
    return this.salonService.default.listConversationsV1ConversationsGet(params);
  }

  public getConversation({ conversationId, userId }: { conversationId: string, userId: string }) {
    return this.salonService.default.getConversationV1ConversationsConversationIdGet({
      conversationId,
      userId,
    });
  }

  public deleteConversation({ conversationId, userId }: { conversationId: string, userId: string }) {
    return this.salonService.default.deleteConversationV1ConversationsConversationIdDelete({
      conversationId,
      userId,
    });
  }

  public editConversation(requestBody: UpdateConversationRequest, conversationId: string, userId: string) {
    return this.salonService.default.updateConversationV1ConversationsConversationIdPut({
      conversationId: conversationId,
      userId: userId,
      requestBody,
    });
  }

  public toggleConversationPin(requestBody: ToggleConversationPinRequest, conversationId: string, userId: string) {
    return this.salonService.default.toggleConversationPinV1ConversationsConversationIdTogglePinPut(
      {
        conversationId: conversationId,
        userId: userId,
        requestBody,
      }
    );
  }

  public login({ email, password }: { email: string; password: string }) {
    return this.salonService.default.loginV1LoginPost({
      requestBody: {
        strategy: 'Basic',
        payload: { email, password },
      },
    });
  }

  public logout() {
    return this.salonService.default.logoutV1LogoutGet();
  }

  public getAuthStrategies() {
    return this.salonService.default.getStrategiesV1AuthStrategiesGet();
  }

  public createUser(requestBody: CreateUserV1UsersPostData) {
    return this.salonService.default.createUserV1UsersPost(requestBody);
  }

  public async googleSSOAuth({ code }: { code: string }) {
    const response = await this.fetch(`${this.getEndpoint('google/auth')}?code=${code}`, {
      method: 'POST',
      headers: this.getHeaders(),
    });

    const body = await response.json();
    this.authToken = body.token;

    if (response.status !== 200) {
      throw new CohereNetworkError('Something went wrong', response.status);
    }

    return body as { token: string };
    // FIXME(@tomtobac): generated code doesn't have code as query parameter (TLK-765)
    // this.salonService.default.googleAuthorizeV1GoogleAuthGet();
  }

  public async oidcSSOAuth({
    code,
    strategy,
    codeVerifier,
  }: {
    code: string;
    strategy: string;
    codeVerifier?: string;
  }) {
    const body: any = {};

    if (codeVerifier) {
      // Conditionally add codeVerifier to the body
      body.code_verifier = codeVerifier;
    }

    const response = await this.fetch(
      `${this.getEndpoint('oidc/auth')}?code=${code}&strategy=${strategy}`,
      {
        method: 'POST',
        headers: this.getHeaders(),
        body: JSON.stringify(body),
      }
    );

    const payload = await response.json();
    this.authToken = body.token;

    if (response.status !== 200) {
      throw new CohereNetworkError('Something went wrong', response.status);
    }

    return payload as { token: string };
    // FIXME(@tomtobac): generated code doesn't have code as query parameter (TLK-765)
    // this.salonService.default.oidcAuthorizeV1OidcAuthGet();
  }

  public generateTitle({ conversationId, userId }: { conversationId: string, userId: string }) {
    return this.salonService.default.generateTitleV1ConversationsConversationIdGenerateTitlePost({
      conversationId, userId
    });
  }

  private getEndpoint(endpoint: 'chat-stream' | 'google/auth' | 'oidc/auth') {
    return `${this.hostname}/v1/${endpoint}`;
  }

  private getChatStreamEndpoint(regenerate?: boolean, agentId?: string) {
    let endpoint = this.getEndpoint('chat-stream');

    if (regenerate) {
      endpoint += '/regenerate';
    }

    if (agentId) {
      endpoint += `?agent_id=${agentId}`;
    }

    return endpoint;
  }

  private getHeaders(omitContentType = false) {
    const headers: HeadersInit = {
      ...(omitContentType ? {} : { 'Content-Type': 'application/json' }),
      ...(this.authToken ? { Authorization: `Bearer ${this.authToken}` } : {}),
      'User-Id': 'user-id',
      Connection: 'keep-alive',
      'X-Date': new Date().getTime().toString(),
    };
    return headers;
  }
}

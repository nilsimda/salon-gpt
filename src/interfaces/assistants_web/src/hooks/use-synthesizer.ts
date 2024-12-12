import { useEffect, useRef, useState } from 'react';

import { useSalonClient } from '@/salon-client';
import { useConversationStore } from '@/stores';

export enum SynthesisStatus {
  NotStarted = 'not-started',
  Loading = 'loading',
  Playing = 'playing',
  Ended = 'ended',
}

export const useSynthesizer = () => {
  const client = useSalonClient();
  const lastMessageIdRef = useRef<string | null>(null);
  const [audios, setAudios] = useState<Map<string, HTMLAudioElement>>(new Map());
  const {
    conversation: { id: conversationId },
  } = useConversationStore();

  useEffect(() => stopPlayingSyntheses(), [conversationId]);

  const synthesisStatus = (messageId: string) => {
    const audio = audios.get(messageId);

    if (!audio) {
      return SynthesisStatus.NotStarted;
    }

    if (!audio.src) {
      return SynthesisStatus.Loading;
    }

    if (!audio.paused && !audio.ended) {
      return SynthesisStatus.Playing;
    }

    return SynthesisStatus.Ended;
  };

  const toggleSynthesis = async (messageId: string) => {
    const status = synthesisStatus(messageId);

    if (status == SynthesisStatus.NotStarted || status == SynthesisStatus.Ended) {
      return await startSynthesis(messageId);
    }

    if (status == SynthesisStatus.Playing) {
      return stopSynthesis(messageId);
    }
  };

  const startSynthesis = async (messageId: string) => {
    stopPlayingSyntheses();

    lastMessageIdRef.current = messageId;

    let audio = audios.get(messageId);

    if (!audio) {
      audio = createEmptyAudioElement();
      setAudios((prev) => new Map(prev).set(messageId, audio!));
    }

    if (lastMessageIdRef.current === messageId) {
      await audio.play();
    }

    setAudios((prev) => new Map(prev));
  };

  const createEmptyAudioElement = () => {
    const audio = new Audio();

    audio.addEventListener('ended', () => {
      setAudios((prev) => new Map(prev));
    });

    return audio;
  };

  const stopSynthesis = (messageId: string) => {
    const audio = audios.get(messageId);

    if (!audio) {
      return;
    }

    audio.pause();
    audio.currentTime = 0;

    setAudios((prev) => new Map(prev));
  };

  const stopPlayingSyntheses = () => {
    for (const messageId of audios.keys()) {
      if (synthesisStatus(messageId) == SynthesisStatus.Playing) {
        stopSynthesis(messageId);
      }
    }
  };

  return { synthesisStatus, toggleSynthesis };
};

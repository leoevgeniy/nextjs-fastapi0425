"use client"
import { useState } from 'react';

export function useRegistrationModal() {
  const [isOpen, setIsOpen] = useState(false);
  const [guestQuestionsUsed, setGuestQuestionsUsed] = useState(0);

  const showModal = (usedQuestions: number) => {
    setGuestQuestionsUsed(usedQuestions);
    setIsOpen(true);
  };

  const hideModal = () => {
    setIsOpen(false);
  };

  return {
    isOpen,
    showModal,
    hideModal,
    guestQuestionsUsed,
  };
}
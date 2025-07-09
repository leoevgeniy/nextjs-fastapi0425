"use client";

import { motion, AnimatePresence } from "framer-motion";
import { FiX, FiArrowRight, FiLock, FiStar } from "react-icons/fi";
import { FuturisticButton } from "../common/FuturisticButton";
import { HolographicCard } from "../common/HolographicCard";

interface RegistrationModalProps {
  isOpen: boolean;
  onClose: () => void;
  onRegister: () => void;
  guestQuestionsUsed: number;
}

export function RegistrationModal({
  isOpen,
  onClose,
  onRegister,
  guestQuestionsUsed,
}: RegistrationModalProps) {
  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/70 backdrop-blur-sm"
            onClick={onClose}
          />

          {/* Modal Content */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 20 }}
            className="relative z-10 w-full max-w-md"
          >
            <HolographicCard className="p-6">
              <div className="flex justify-between items-start mb-6">
                <h2 className="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-blue-500">
                  Continue Your AI Experience
                </h2>
                <button
                  onClick={onClose}
                  className="p-1 rounded-full hover:bg-gray-700/50 transition-colors text-gray-400 hover:text-white"
                >
                  <FiX size={20} />
                </button>
              </div>

              <div className="space-y-4 mb-6">
                <div className="flex items-center gap-3 p-3 bg-gray-800/50 rounded-lg">
                  <FiLock className="text-yellow-400 flex-shrink-0" size={20} />
                  <div>
                    <h4 className="font-medium text-white">
                      Guest Limit Reached
                    </h4>
                    <p className="text-sm text-gray-300">
                      You've used {guestQuestionsUsed}/10 free questions.
                      Register for unlimited access.
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-3 p-3 bg-gray-800/50 rounded-lg">
                  <FiStar className="text-purple-400 flex-shrink-0" size={20} />
                  <div>
                    <h4 className="font-medium text-white">Premium Features</h4>
                    <p className="text-sm text-gray-300">
                      Get full access to advanced AI capabilities and history
                      saving.
                    </p>
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-1 gap-3">
                <FuturisticButton
                  onClick={onRegister}
                  className="w-full justify-center"
                >
                  Register Now <FiArrowRight className="ml-2" />
                </FuturisticButton>

                <button
                  onClick={onClose}
                  className="text-sm text-center text-gray-400 hover:text-white transition-colors pt-2"
                >
                  Maybe later
                </button>
              </div>
            </HolographicCard>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}

import { useRef, useState } from "react";

declare global {
  interface Window {
    grecaptcha: {
      render: (elementId: string, options: any) => number;
      getResponse: (widgetId: number) => string;
      reset: (widgetId?: number) => void;
      remove: (widgetId?: number) => void;
    };
  }
}

export const useRecaptcha = (siteKey: string) => {
  const widgetRef = useRef<number | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const [recaptchaToken, setRecaptchaToken] = useState<string>("");
  const [isVerified, setIsVerified] = useState(false);

  const initRecaptcha = () => {
    if (containerRef.current && window.grecaptcha) {
      // Clear previous widget if it exists
      if (widgetRef.current !== null) {
        try {
          window.grecaptcha.remove(widgetRef.current);
        } catch (e) {
          // Ignore errors during cleanup
        }
      }

      // Render new widget
      widgetRef.current = window.grecaptcha.render(containerRef.current, {
        sitekey: siteKey,
        callback: onRecaptchaChange,
        "expired-callback": onRecaptchaExpired,
      });
    }
  };

  const onRecaptchaChange = (token: string) => {
    setRecaptchaToken(token);
    setIsVerified(true);
  };

  const onRecaptchaExpired = () => {
    setRecaptchaToken("");
    setIsVerified(false);
  };

  const getToken = (): string => {
    if (widgetRef.current !== null) {
      return window.grecaptcha.getResponse(widgetRef.current);
    }
    return recaptchaToken;
  };

  const resetRecaptcha = () => {
    if (widgetRef.current !== null) {
      window.grecaptcha.reset(widgetRef.current);
    }
    setRecaptchaToken("");
    setIsVerified(false);
  };

  return {
    containerRef,
    recaptchaToken,
    isVerified,
    initRecaptcha,
    getToken,
    resetRecaptcha,
  };
};

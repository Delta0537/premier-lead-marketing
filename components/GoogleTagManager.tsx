/**
 * Google Tag Manager Component
 * 
 * @module components/GoogleTagManager
 * @description Client-side component for integrating Google Tag Manager (GTM) 
 *              into Premier Lead Marketing website. Handles GTM initialization,
 *              noscript fallback, and environment variable configuration.
 * 
 * @requires @next/third-parties/google
 * @requires NEXT_PUBLIC_GTM_ID environment variable
 * 
 * @example
 * ```tsx
 * // In your root layout.tsx
 * import GoogleTagManager from '@/components/GoogleTagManager';
 * 
 * export default function RootLayout({ children }) {
 *   return (
 *     <html>
 *       <body>
 *         <GoogleTagManager />
 *         {children}
 *       </body>
 *     </html>
 *   );
 * }
 * ```
 * 
 * @see https://nextjs.org/docs/app/building-your-application/optimizing/third-party-libraries#google-tag-manager
 */

'use client';

import { GoogleTagManager } from '@next/third-parties/google';
import { useEffect, useState } from 'react';

/**
 * Google Tag Manager Component Props
 */
interface GoogleTagManagerProps {
  /**
   * Optional GTM ID override. If not provided, uses NEXT_PUBLIC_GTM_ID env variable.
   * @default process.env.NEXT_PUBLIC_GTM_ID
   */
  gtmId?: string;
}

/**
 * Google Tag Manager Component
 * 
 * Initializes Google Tag Manager for tracking and analytics.
 * Includes noscript fallback for users with JavaScript disabled.
 * 
 * @param {GoogleTagManagerProps} props - Component props
 * @returns {JSX.Element | null} GTM script tags or null if GTM ID not configured
 * 
 * @remarks
 * - Requires NEXT_PUBLIC_GTM_ID environment variable
 * - Automatically handles GTM initialization
 * - Includes noscript fallback for accessibility
 * - Only renders in production or when explicitly enabled
 */
export default function GoogleTagManagerComponent({ 
  gtmId 
}: GoogleTagManagerProps): JSX.Element | null {
  const [mounted, setMounted] = useState(false);

  // Get GTM ID from props or environment variable
  const gtmIdValue = gtmId || process.env.NEXT_PUBLIC_GTM_ID;

  // Only render on client side after mount
  useEffect(() => {
    setMounted(true);
  }, []);

  // Don't render if GTM ID is not configured
  if (!gtmIdValue) {
    if (process.env.NODE_ENV === 'development') {
      console.warn(
        'Google Tag Manager: NEXT_PUBLIC_GTM_ID not configured. ' +
        'GTM will not be initialized. Add NEXT_PUBLIC_GTM_ID to .env.local'
      );
    }
    return null;
  }

  // Don't render until mounted (prevents hydration mismatch)
  if (!mounted) {
    return null;
  }

  return (
    <>
      {/* Google Tag Manager Script */}
      <GoogleTagManager gtmId={gtmIdValue} />

      {/* Noscript Fallback for users without JavaScript */}
      <noscript>
        <iframe
          src={`https://www.googletagmanager.com/ns.html?id=${gtmIdValue}`}
          height="0"
          width="0"
          style={{ display: 'none', visibility: 'hidden' }}
          aria-hidden="true"
          title="Google Tag Manager"
        />
      </noscript>
    </>
  );
}

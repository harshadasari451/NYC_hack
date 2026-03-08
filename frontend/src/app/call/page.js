"use client";
import { useRouter } from "next/navigation";
import styles from "./call.module.css";

export default function CallPage() {
  const router = useRouter();

  return (
    <div className={styles.callPage}>
      <div className={styles.callBackground}>
        <div className={styles.avatarSection}>
          <div className={styles.avatarRing}>
            <div className={styles.avatarInner}>👩</div>
          </div>
          <h2 className={styles.callerName}>Mom</h2>
          <p className={styles.callStatus}>🔊 Voice call coming soon...</p>
          <p className={styles.callHint}>
            This will use Google Cloud Speech-to-Text + Chirp 3 TTS
            for real-time voice conversations with mom&apos;s cloned voice.
          </p>
        </div>

        <div className={styles.callActions}>
          <button
            className={`btn btn-icon ${styles.endCallBtn}`}
            onClick={() => router.push("/")}
          >
            ✕
          </button>
        </div>
      </div>
    </div>
  );
}

"use client";
import { useRouter } from "next/navigation";
import styles from "./video.module.css";

export default function VideoPage() {
  const router = useRouter();

  return (
    <div className={styles.videoPage}>
      <div className={styles.videoBackground}>
        <div className={styles.roomPlaceholder}>
          <div className={styles.roomGradient}></div>
          <div className={styles.avatarSection}>
            <div className={styles.avatarRing}>
              <div className={styles.avatarInner}>👩</div>
            </div>
            <h2 className={styles.callerName}>Mom</h2>
            <p className={styles.callStatus}>📹 Video call coming soon...</p>
            <p className={styles.callHint}>
              This will feature a full 3D avatar in a virtual room
              using Three.js + Ready Player Me + Mixamo animations.
            </p>
          </div>
        </div>

        <div className={styles.videoActions}>
          <button
            className={`btn btn-icon ${styles.actionBtnSmall}`}
            title="Mute"
          >
            🔇
          </button>
          <button
            className={`btn btn-icon ${styles.endCallBtn}`}
            onClick={() => router.push("/")}
          >
            ✕
          </button>
          <button
            className={`btn btn-icon ${styles.actionBtnSmall}`}
            title="Switch to Chat"
            onClick={() => router.push("/chat")}
          >
            💬
          </button>
        </div>
      </div>
    </div>
  );
}

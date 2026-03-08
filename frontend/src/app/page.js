"use client";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import styles from "./page.module.css";

const ACTIVITIES = [
  { emoji: "🍴", label: "Cooking", status: "is making something delicious. Give her a call! 🔍" },
  { emoji: "📖", label: "Reading", status: "is reading her favorite book 📖" },
  { emoji: "🛋️", label: "Relaxing", status: "is relaxing on the couch 🛋️" },
  { emoji: "🌿", label: "Gardening", status: "is watering her plants 🌿" },
  { emoji: "🌅", label: "Enjoying the view", status: "is enjoying the view 🌅" },
];

export default function HomePage() {
  const router = useRouter();
  const [activity, setActivity] = useState(ACTIVITIES[0]);
  const [personaReady, setPersonaReady] = useState(false);
  const [personaName, setPersonaName] = useState("Mom");
  const [personaAvatar, setPersonaAvatar] = useState(null);

  useEffect(() => {
    // Check if persona exists
    const stored = localStorage.getItem("persona");
    if (stored) {
      const persona = JSON.parse(stored);
      setPersonaReady(true);
      setPersonaName(persona.name || "Mom");
      setPersonaAvatar(persona.photo_url || persona.avatar || null);
    }

    // Cycle through activities
    const interval = setInterval(() => {
      setActivity((prev) => {
        const idx = ACTIVITIES.indexOf(prev);
        return ACTIVITIES[(idx + 1) % ACTIVITIES.length];
      });
    }, 8000);

    return () => clearInterval(interval);
  }, []);

  if (!personaReady) {
    return (
      <div className="page-container">
        <div className={styles.welcomeScreen}>
          <div className={styles.welcomeGlow}></div>
          <div className={styles.welcomeContent}>
            <div className={styles.logoIcon}>💜</div>
            <h1 className={styles.welcomeTitle}>Mom Avatar</h1>
            <p className={styles.welcomeSubtitle}>
              Create a living, breathing digital avatar of your mom.
              <br />
              Talk, call, and video chat — anytime.
            </p>
            <button
              className="btn btn-primary"
              style={{ marginTop: 32, padding: "16px 40px", fontSize: 16 }}
              onClick={() => router.push("/onboarding")}
            >
              ✨ Get Started
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="page-container">
      <div className={styles.homeScreen}>
        {/* 3D Room Placeholder */}
        <div className={styles.roomView}>
          <div className={styles.roomBackground}>
            <div className={styles.roomGradient}></div>
            {/* Avatar circle */}
            <div className={styles.avatarContainer}>
              <div className={styles.avatarCircle}>
                <img
                  src={personaAvatar || `https://api.dicebear.com/7.x/avataaars/svg?seed=${encodeURIComponent(personaName)}`}
                  alt={personaName}
                  className={styles.avatarImage}
                />
              </div>
              <div className={styles.activityBadge}>
                <span>{activity.emoji}</span>
                <span>{activity.label}</span>
                <span className={styles.onlineDot}></span>
              </div>
            </div>
          </div>

          {/* Status bar */}
          <div className={styles.statusBar}>
            <p className={styles.statusText}>{personaName} {activity.status}</p>
          </div>
        </div>

        {/* Action buttons */}
        <div className={styles.actionButtons}>
          <button
            className={`btn btn-icon btn-call ${styles.actionBtn}`}
            onClick={() => router.push("/call")}
            title="Voice Call"
          >
            📞
          </button>
          <button
            className={`btn btn-icon btn-video ${styles.actionBtn}`}
            onClick={() => router.push("/video")}
            title="Video Call"
          >
            📹
          </button>
          <button
            className={`btn btn-icon btn-chat ${styles.actionBtn}`}
            onClick={() => router.push("/chat")}
            title="Text Chat"
          >
            💬
          </button>
        </div>

        <div className={styles.actionLabels}>
          <span>Call</span>
          <span>Video</span>
          <span>Chat</span>
        </div>
      </div>
    </div>
  );
}

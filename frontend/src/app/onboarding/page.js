"use client";
import { useState, useRef } from "react";
import { useRouter } from "next/navigation";
import { uploadWhatsApp, uploadPhotos, uploadAudioVideo, createPersona } from "@/lib/api";
import styles from "./onboarding.module.css";

const STEPS = ["Name", "WhatsApp", "Photos", "Voice", "Description"];

export default function OnboardingPage() {
  const router = useRouter();
  const [step, setStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // Form data
  const [personName, setPersonName] = useState("");
  const [whatsappFile, setWhatsappFile] = useState(null);
  const [photos, setPhotos] = useState([]);
  const [audioVideo, setAudioVideo] = useState(null);
  const [description, setDescription] = useState("");

  // Upload states
  const [whatsappUploaded, setWhatsappUploaded] = useState(false);
  const [photosUploaded, setPhotosUploaded] = useState(false);
  const [audioUploaded, setAudioUploaded] = useState(false);

  const whatsappRef = useRef(null);
  const photosRef = useRef(null);
  const audioRef = useRef(null);

  const handleNext = async () => {
    setError("");

    if (step === 0 && !personName.trim()) {
      setError("Please enter the person's name");
      return;
    }

    if (step === 1 && !whatsappFile) {
      setError("Please upload a WhatsApp chat export");
      return;
    }

    if (step === 2 && photos.length === 0) {
      setError("Please upload at least one photo");
      return;
    }

    if (step === 3 && !audioVideo) {
      setError("Please upload an audio or video file");
      return;
    }

    // Upload files at each step
    if (step === 1 && whatsappFile && !whatsappUploaded) {
      setLoading(true);
      try {
        await uploadWhatsApp(whatsappFile);
        setWhatsappUploaded(true);
      } catch (e) {
        setError("Upload failed. Make sure the backend is running.");
        setLoading(false);
        return;
      }
      setLoading(false);
    }

    if (step === 2 && photos.length > 0 && !photosUploaded) {
      setLoading(true);
      try {
        await uploadPhotos(photos);
        setPhotosUploaded(true);
      } catch (e) {
        setError("Photo upload failed.");
        setLoading(false);
        return;
      }
      setLoading(false);
    }

    if (step === 3 && audioVideo && !audioUploaded) {
      setLoading(true);
      try {
        await uploadAudioVideo(audioVideo);
        setAudioUploaded(true);
      } catch (e) {
        setError("Audio/video upload failed.");
        setLoading(false);
        return;
      }
      setLoading(false);
    }

    // Final step — create persona
    if (step === STEPS.length - 1) {
      setLoading(true);
      try {
        const result = await createPersona(personName, description);
        if (result.status === "success") {
          localStorage.setItem("persona", JSON.stringify(result.persona));
          router.push("/");
        } else {
          setError(result.detail || "Failed to create persona");
        }
      } catch (e) {
        setError("Persona creation failed. Make sure the backend is running.");
      }
      setLoading(false);
      return;
    }

    setStep((s) => s + 1);
  };

  const handleBack = () => {
    setError("");
    setStep((s) => Math.max(0, s - 1));
  };

  return (
    <div className="page-container">
      <div className={styles.onboarding}>
        {/* Header */}
        <div className={styles.header}>
          <h1 className={styles.title}>Create Mom's Avatar</h1>
          <p className={styles.subtitle}>
            Step {step + 1} of {STEPS.length}
          </p>
        </div>

        {/* Stepper */}
        <div className="stepper">
          {STEPS.map((label, i) => (
            <div key={label} style={{ display: "flex", alignItems: "center", flex: i < STEPS.length - 1 ? 1 : "none" }}>
              <div className={`step ${i === step ? "active" : ""} ${i < step ? "completed" : ""}`}>
                <div className="step-circle">
                  {i < step ? "✓" : i + 1}
                </div>
              </div>
              {i < STEPS.length - 1 && (
                <div className={`step-line ${i < step ? "completed" : ""}`}></div>
              )}
            </div>
          ))}
        </div>

        {/* Step content */}
        <div className={styles.stepContent}>
          {step === 0 && (
            <div className="animate-fadeIn">
              <div className={styles.stepIcon}>👩</div>
              <h2 className={styles.stepTitle}>What's her name?</h2>
              <p className={styles.stepDesc}>
                Enter the name exactly as it appears in WhatsApp chats
              </p>
              <input
                className="input-field"
                type="text"
                placeholder="e.g., Mom, Amma, Maa, Sarah..."
                value={personName}
                onChange={(e) => setPersonName(e.target.value)}
                autoFocus
              />
            </div>
          )}

          {step === 1 && (
            <div className="animate-fadeIn">
              <div className={styles.stepIcon}>📱</div>
              <h2 className={styles.stepTitle}>WhatsApp Chats</h2>
              <p className={styles.stepDesc}>
                Export a chat from WhatsApp (without media) and upload the .txt file
              </p>
              <div
                className={`upload-zone ${whatsappFile ? "active" : ""}`}
                onClick={() => whatsappRef.current?.click()}
              >
                <div className="icon">{whatsappFile ? "✅" : "📄"}</div>
                <div className={whatsappFile ? "success" : "label"}>
                  {whatsappFile ? whatsappFile.name : "Click to upload .txt file"}
                </div>
                <div className="hint">WhatsApp → Chat → Export Chat → Without Media</div>
              </div>
              <input
                ref={whatsappRef}
                type="file"
                accept=".txt"
                hidden
                onChange={(e) => {
                  setWhatsappFile(e.target.files[0]);
                  setWhatsappUploaded(false);
                }}
              />
            </div>
          )}

          {step === 2 && (
            <div className="animate-fadeIn">
              <div className={styles.stepIcon}>📸</div>
              <h2 className={styles.stepTitle}>Photos</h2>
              <p className={styles.stepDesc}>
                Upload clear face photos from different angles
              </p>
              <div
                className={`upload-zone ${photos.length > 0 ? "active" : ""}`}
                onClick={() => photosRef.current?.click()}
              >
                <div className="icon">{photos.length > 0 ? "✅" : "🖼️"}</div>
                <div className={photos.length > 0 ? "success" : "label"}>
                  {photos.length > 0 ? `${photos.length} photo(s) selected` : "Click to upload photos"}
                </div>
                <div className="hint">JPG, PNG — ideally front-facing, well-lit</div>
              </div>
              <input
                ref={photosRef}
                type="file"
                accept=".jpg,.jpeg,.png,.webp"
                multiple
                hidden
                onChange={(e) => {
                  setPhotos(Array.from(e.target.files));
                  setPhotosUploaded(false);
                }}
              />
            </div>
          )}

          {step === 3 && (
            <div className="animate-fadeIn">
              <div className={styles.stepIcon}>🎤</div>
              <h2 className={styles.stepTitle}>Voice Sample</h2>
              <p className={styles.stepDesc}>
                Upload audio or video with at least 10 seconds of clear speech
              </p>
              <div
                className={`upload-zone ${audioVideo ? "active" : ""}`}
                onClick={() => audioRef.current?.click()}
              >
                <div className="icon">{audioVideo ? "✅" : "🎵"}</div>
                <div className={audioVideo ? "success" : "label"}>
                  {audioVideo ? audioVideo.name : "Click to upload audio/video"}
                </div>
                <div className="hint">MP4, WAV, MP3, M4A — clear speech, minimal background noise</div>
              </div>
              <input
                ref={audioRef}
                type="file"
                accept=".mp4,.wav,.mp3,.m4a,.ogg,.webm,.mov"
                hidden
                onChange={(e) => {
                  setAudioVideo(e.target.files[0]);
                  setAudioUploaded(false);
                }}
              />
            </div>
          )}

          {step === 4 && (
            <div className="animate-fadeIn">
              <div className={styles.stepIcon}>✍️</div>
              <h2 className={styles.stepTitle}>Describe Her (Optional)</h2>
              <p className={styles.stepDesc}>
                Tell us about her personality, quirks, and what makes her special
              </p>
              <textarea
                className="input-field"
                placeholder="e.g., She's very caring and always asks if I've eaten. She loves gardening and watches cooking shows. She uses lots of emojis and calls me 'beta'..."
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                rows={6}
                style={{ resize: "vertical" }}
              />
            </div>
          )}
        </div>

        {/* Error */}
        {error && <div className={styles.error}>{error}</div>}

        {/* Navigation */}
        <div className={styles.navButtons}>
          {step > 0 && (
            <button className="btn btn-secondary" onClick={handleBack} disabled={loading}>
              ← Back
            </button>
          )}
          <button
            className="btn btn-primary"
            onClick={handleNext}
            disabled={loading}
            style={{ marginLeft: "auto" }}
          >
            {loading ? (
              <span className={styles.spinner}></span>
            ) : step === STEPS.length - 1 ? (
              "✨ Create Avatar"
            ) : (
              "Next →"
            )}
          </button>
        </div>
      </div>
    </div>
  );
}

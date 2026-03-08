"use client";
import { useState, useRef, useEffect } from "react";
import { useRouter } from "next/navigation";
import { sendChatMessage } from "@/lib/api";
import styles from "./chat.module.css";

export default function ChatPage() {
  const router = useRouter();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);
  const [conversationId, setConversationId] = useState(null);
  const [personaName, setPersonaName] = useState("Mom");
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    const persona = localStorage.getItem("persona");
    if (persona) {
      const p = JSON.parse(persona);
      setPersonaName(p.name || "Mom");
    }

    // Add initial greeting
    setMessages([{
      role: "avatar",
      content: "Hey sweetheart! 💕 How are you doing today?",
      emotion: "caring",
    }]);

    inputRef.current?.focus();
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || sending) return;

    const userMessage = input.trim();
    setInput("");
    setSending(true);

    // Add user message immediately
    setMessages((prev) => [...prev, { role: "user", content: userMessage }]);

    // Add typing indicator
    setMessages((prev) => [...prev, { role: "typing", content: "" }]);

    try {
      const response = await sendChatMessage(userMessage, conversationId);
      
      // Remove typing indicator and add avatar response
      setMessages((prev) => {
        const filtered = prev.filter((m) => m.role !== "typing");
        return [...filtered, {
          role: "avatar",
          content: response.message,
          emotion: response.emotion,
        }];
      });
      
      setConversationId(response.conversation_id);
    } catch (e) {
      // Remove typing indicator on error
      setMessages((prev) => {
        const filtered = prev.filter((m) => m.role !== "typing");
        return [...filtered, {
          role: "avatar",
          content: "Oh dear, something went wrong. Let me try again in a moment! 😅",
          emotion: "neutral",
        }];
      });
    }

    setSending(false);
    inputRef.current?.focus();
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const getEmotionEmoji = (emotion) => {
    const map = {
      happy: "😊",
      caring: "💕",
      funny: "😄",
      concerned: "😟",
      proud: "🥰",
      nostalgic: "🥲",
      neutral: "😊",
    };
    return map[emotion] || "😊";
  };

  return (
    <div className={styles.chatPage}>
      {/* Header */}
      <div className={styles.chatHeader}>
        <button className={styles.backBtn} onClick={() => router.push("/")}>
          ←
        </button>
        <div className={styles.headerInfo}>
          <div className={styles.headerAvatar}>👩</div>
          <div>
            <div className={styles.headerName}>{personaName}</div>
            <div className={styles.headerStatus}>
              <span className={styles.onlineDot}></span>
              Online
            </div>
          </div>
        </div>
        <div className={styles.headerActions}>
          <button className={styles.iconBtn} onClick={() => router.push("/call")}>📞</button>
          <button className={styles.iconBtn} onClick={() => router.push("/video")}>📹</button>
        </div>
      </div>

      {/* Messages */}
      <div className={styles.messagesContainer}>
        <div className={styles.messages}>
          {messages.map((msg, i) => {
            if (msg.role === "typing") {
              return (
                <div key={i} className={styles.typingRow}>
                  <div className={styles.typingBubble}>
                    <span className={styles.dot}></span>
                    <span className={styles.dot}></span>
                    <span className={styles.dot}></span>
                  </div>
                </div>
              );
            }

            return (
              <div
                key={i}
                className={`${styles.messageRow} ${msg.role === "user" ? styles.userRow : styles.avatarRow}`}
              >
                {msg.role === "avatar" && (
                  <div className={styles.avatarIcon}>
                    {getEmotionEmoji(msg.emotion)}
                  </div>
                )}
                <div className={`chat-bubble ${msg.role}`}>
                  {msg.content}
                </div>
              </div>
            );
          })}
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input */}
      <div className={styles.inputBar}>
        <input
          ref={inputRef}
          className={styles.chatInput}
          type="text"
          placeholder="Type a message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={sending}
        />
        <button
          className={`btn btn-primary ${styles.sendBtn}`}
          onClick={handleSend}
          disabled={!input.trim() || sending}
        >
          ↑
        </button>
      </div>
    </div>
  );
}

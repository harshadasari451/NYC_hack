import "./globals.css";

export const metadata = {
  title: "Mom Avatar — Talk to Mom Anytime",
  description: "An interactive AI avatar that lets you call, video chat, or text with a digital version of your mother, powered by Google AI.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}

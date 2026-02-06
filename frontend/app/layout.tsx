
import './globals.css';
import ClientProviders from '@/providers/ClientProviders';
import Chatbot from '../components/common/chatbot';


export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <ClientProviders>
          {children}
          <Chatbot /> {/* Chatbot icon har page pe */}
        </ClientProviders>
      </body>
    </html>
  );
}

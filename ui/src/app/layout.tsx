import './globals.css';

export const metadata = {
  title: 'Spectorin - Smart Contract Analyzer',
  description: 'AI-powered formal verification & static analysis for smart contracts',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        {children}
      </body>
    </html>
  );
}

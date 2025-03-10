import './globals.css';

export const metadata = {
  title: 'URL 处理工具',
  description: '一个简单的 URL 处理工具',
};

export default function RootLayout({ children }) {
  return (
    <html lang="zh">
      <body>{children}</body>
    </html>
  );
} 
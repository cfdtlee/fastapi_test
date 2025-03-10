'use client';
import { useState } from 'react';
import styles from './page.module.css';

// 更新为您的实际后端 URL
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'https://fastapitest-production-0ff0.up.railway.app';

export default function Home() {
  const [url, setUrl] = useState('');
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const response = await fetch(`${API_URL}/process-url`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url }),
      });
      
      const data = await response.json();
      
      // 格式化显示结果
      if (data.status === 'processed') {
        setResult(data.transcript || JSON.stringify(data, null, 2));
      } else {
        setResult(data.error || JSON.stringify(data, null, 2));
      }
    } catch (error) {
      setResult(`错误: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className={styles.main}>
      <div className={styles.container}>
        <h1 className={styles.title}>YouTube 转文本工具</h1>
        
        <form onSubmit={handleSubmit} className={styles.form}>
          <div className={styles.inputGroup}>
            <label htmlFor="url" className={styles.label}>输入 YouTube 链接:</label>
            <input
              type="text"
              id="url"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              className={styles.input}
              placeholder="https://www.youtube.com/watch?v=..."
              required
            />
          </div>
          
          <button 
            type="submit" 
            className={styles.button}
            disabled={loading}
          >
            {loading ? '处理中...' : '获取文本'}
          </button>
        </form>
        
        {result && (
          <div className={styles.resultContainer}>
            <h2 className={styles.resultTitle}>结果:</h2>
            <pre className={styles.resultBox}>{result}</pre>
          </div>
        )}
      </div>
    </main>
  );
} 
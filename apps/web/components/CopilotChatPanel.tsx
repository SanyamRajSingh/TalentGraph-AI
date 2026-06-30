import { useState, useRef, useEffect } from 'react';
import { Bot, Send, User, Loader2 } from 'lucide-react';

type Message = {
  role: 'user' | 'assistant';
  content: string;
};

type Props = {
  apiBaseUrl: string;
  candidateId?: string;
  roleId?: string;
};

export default function CopilotChatPanel({ apiBaseUrl, candidateId, roleId }: Props) {
  const [messages, setMessages] = useState<Message[]>([
    { role: 'assistant', content: 'Hi! I am your AI Recruiter Copilot. Ask me anything about this candidate or the role requirements.' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || !candidateId || !roleId) return;

    const userMsg = input.trim();
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: userMsg }]);
    setIsLoading(true);

    try {
      const response = await fetch(`${apiBaseUrl}/api/v1/copilot/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          role_id: roleId,
          candidate_id: candidateId,
          message: userMsg
        })
      });

      if (!response.ok) throw new Error('Failed to get response');
      const data = await response.json();
      
      setMessages(prev => [...prev, { role: 'assistant', content: data.answer }]);
    } catch (err) {
      setMessages(prev => [...prev, { role: 'assistant', content: 'Sorry, I encountered an error while processing your request.' }]);
    } finally {
      setIsLoading(false);
    }
  };

  if (!candidateId || !roleId) {
    return (
      <div className="flex flex-col items-center justify-center py-12 px-4 text-center rounded-lg border border-gray-200 dark:border-slate-800 bg-gray-50 dark:bg-slate-800/50/50">
        <Bot className="h-8 w-8 text-gray-400 mb-3" />
        <p className="text-sm font-medium text-gray-600 dark:text-slate-400">Select a candidate and role to start chatting.</p>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-[400px] bg-white dark:bg-slate-900 rounded-lg border border-gray-200 dark:border-slate-800 overflow-hidden">
      <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50 dark:bg-slate-800/50/30">
        {messages.map((msg, idx) => (
          <div key={idx} className={`flex gap-3 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            {msg.role === 'assistant' && (
              <div className="shrink-0 flex items-center justify-center w-8 h-8 rounded-full bg-indigo-100 text-indigo-600">
                <Bot className="w-5 h-5" />
              </div>
            )}
            <div className={`max-w-[80%] rounded-2xl px-4 py-2 text-sm ${
              msg.role === 'user' 
                ? 'bg-signal text-white rounded-tr-sm' 
                : 'bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800 text-gray-800 dark:text-slate-200 rounded-tl-sm shadow-sm'
            }`}>
              {msg.content}
            </div>
            {msg.role === 'user' && (
              <div className="shrink-0 flex items-center justify-center w-8 h-8 rounded-full bg-gray-200 text-gray-600 dark:text-slate-400">
                <User className="w-5 h-5" />
              </div>
            )}
          </div>
        ))}
        {isLoading && (
          <div className="flex gap-3 justify-start">
            <div className="shrink-0 flex items-center justify-center w-8 h-8 rounded-full bg-indigo-100 text-indigo-600">
              <Bot className="w-5 h-5" />
            </div>
            <div className="max-w-[80%] rounded-2xl px-4 py-3 bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800 text-gray-500 dark:text-slate-400 rounded-tl-sm shadow-sm flex items-center gap-2">
              <Loader2 className="w-4 h-4 animate-spin" /> Thinking...
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      
      <div className="p-3 bg-white dark:bg-slate-900 border-t border-gray-200 dark:border-slate-800">
        <form onSubmit={handleSubmit} className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={e => setInput(e.target.value)}
            placeholder="Ask about candidate experience, culture fit..."
            disabled={isLoading}
            className="flex-1 h-10 px-3 text-sm rounded-full border border-gray-300 dark:border-slate-700 focus:outline-none focus:border-signal focus:ring-1 focus:ring-signal disabled:bg-gray-50 dark:bg-slate-800/50 disabled:text-gray-500 dark:text-slate-400"
          />
          <button
            type="submit"
            disabled={isLoading || !input.trim()}
            className="shrink-0 flex items-center justify-center w-10 h-10 rounded-full bg-signal text-white hover:bg-signal/90 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
          >
            <Send className="w-4 h-4 ml-0.5" />
          </button>
        </form>
      </div>
    </div>
  );
}

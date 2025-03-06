import { MessageSquare } from 'lucide-react';

export function Header() {
  return (
    <header className="bg-blue-600 text-white p-4 flex items-center justify-between">
      <div className="flex items-center gap-2">
        <img src="/src/assets/carfgano-logo.svg" alt="Carfgano Enterprises Logo" className="w-10 h-10" />
        <div>
          <h1 className="text-xl font-bold">CarfganoBot</h1>
          <p className="text-xs opacity-80">by Carfgano Enterprises</p>
        </div>
      </div>
      <div className="flex items-center gap-2">
        <MessageSquare size={20} />
        <span className="font-medium">Investing Education</span>
      </div>
    </header>
  );
}

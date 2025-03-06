import { Alert, AlertDescription } from './ui/alert';
import { AlertTriangle } from 'lucide-react';

interface DisclaimerProps {
  text: string;
}

export function Disclaimer({ text }: DisclaimerProps) {
  return (
    <Alert className="mx-3 my-2 bg-amber-50 border-amber-200">
      <div className="flex items-start gap-2">
        <AlertTriangle className="h-4 w-4 text-amber-800" />
        <AlertDescription className="text-xs text-amber-800">
          {text}
        </AlertDescription>
      </div>
    </Alert>
  );
}

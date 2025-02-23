
import { ScrollText } from "lucide-react";

const VocabularyExplorer = () => {
  return (
    <div className="p-8 space-y-6">
      <div className="flex items-center space-x-4">
        <ScrollText className="h-6 w-6 text-primary" />
        <h1 className="text-3xl font-bold">Vocabulary Explorer</h1>
      </div>
      <p className="text-muted-foreground">
        Browse and manage your personal vocabulary inventory.
      </p>
    </div>
  );
};

export default VocabularyExplorer;

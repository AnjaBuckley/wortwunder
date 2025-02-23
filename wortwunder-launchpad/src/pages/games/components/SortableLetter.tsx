import { useSortable } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';

interface SortableLetterProps {
  letter: {
    id: string;
    char: string;
  };
}

export function SortableLetter({ letter }: SortableLetterProps) {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
  } = useSortable({ id: letter.id });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
  };

  return (
    <div
      ref={setNodeRef}
      style={style}
      {...attributes}
      {...listeners}
      className="w-12 h-12 flex items-center justify-center text-xl font-bold bg-accent rounded-lg cursor-move touch-none"
    >
      {letter.char}
    </div>
  );
} 
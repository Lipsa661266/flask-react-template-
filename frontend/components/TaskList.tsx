import { Task, TaskAPI } from "../lib/api";

type Props = {
  tasks: Task[];
  onEdit: (task: Task) => void;
  onDeleted: (id: string) => void;
};

export default function TaskList({ tasks, onEdit, onDeleted }: Props) {
  const handleDelete = async (id: string) => {
    if (confirm("Delete this task?")) {
      await TaskAPI.remove(id);
      onDeleted(id);
    }
  };

  if (!tasks.length) return <p>No tasks yet.</p>;

  return (
    <ul className="flex flex-col gap-2">
      {tasks.map((t) => (
        <li key={t._id} className="border p-3 flex justify-between items-center">
          <div>
            <strong>{t.title}</strong>
            {t.description && <div className="text-sm">{t.description}</div>}
          </div>
          <div className="flex gap-2">
            <button onClick={() => onEdit(t)} className="border px-2 py-1 rounded">Edit</button>
            <button onClick={() => handleDelete(t._id)} className="border px-2 py-1 rounded">Delete</button>
          </div>
        </li>
      ))}
    </ul>
  );
}

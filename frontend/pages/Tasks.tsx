import { useEffect, useState } from "react";
import { Task, TaskAPI } from "../lib/api";
import TaskForm from "../components/TaskForm";
import TaskList from "../components/TaskList";

export default function TasksPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [editing, setEditing] = useState<Task | null>(null);

  const load = async () => setTasks(await TaskAPI.list());
  useEffect(() => { load(); }, []);

  const onSaved = async () => {
    setEditing(null);
    await load();
  };

  const onDeleted = (id: string) => setTasks((prev) => prev.filter((t) => t._id !== id));

  return (
    <div className="p-6 max-w-2xl mx-auto flex flex-col gap-6">
      <h1 className="text-2xl font-semibold">Tasks</h1>
      <TaskForm editing={editing} onSaved={onSaved} onCancel={() => setEditing(null)} />
      <TaskList tasks={tasks} onEdit={setEditing} onDeleted={onDeleted} />
    </div>
  );
}

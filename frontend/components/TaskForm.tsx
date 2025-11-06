import { useState, useEffect } from "react";
import { Task, TaskAPI } from "../lib/api";

type Props = {
  editing?: Task | null;
  onSaved: () => void;
  onCancel?: () => void;
};

export default function TaskForm({ editing, onSaved, onCancel }: Props) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");

  useEffect(() => {
    if (editing) {
      setTitle(editing.title);
      setDescription(editing.description || "");
    } else {
      setTitle("");
      setDescription("");
    }
  }, [editing]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const body = { title, description };
    if (editing) await TaskAPI.update(editing._id, body);
    else await TaskAPI.create(body);
    onSaved();
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-2 max-w-md">
      <input
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="Task title"
        className="border p-2 rounded"
        required
      />
      <textarea
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        placeholder="Description"
        className="border p-2 rounded"
      />
      <div className="flex gap-2">
        <button type="submit" className="border px-3 py-1 rounded">Save</button>
        {editing && onCancel && (
          <button onClick={onCancel} type="button" className="border px-3 py-1 rounded">Cancel</button>
        )}
      </div>
    </form>
  );
}

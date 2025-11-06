export type Task = { _id: string; title: string; description?: string };

const BASE = "/api/tasks";

async function handle<T>(res: Response): Promise<T> {
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export const TaskAPI = {
  list: async (): Promise<Task[]> => handle(await fetch(BASE)),
  create: async (body: { title: string; description?: string }) =>
    handle(await fetch(BASE, {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body)
    })),
  update: async (id: string, body: Partial<Task>) =>
    handle(await fetch(`${BASE}/${id}`, {
      method: "PATCH", headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body)
    })),
  remove: async (id: string) => {
    const res = await fetch(`${BASE}/${id}`, { method: "DELETE" });
    if (!res.ok) throw new Error(await res.text());
  },
};

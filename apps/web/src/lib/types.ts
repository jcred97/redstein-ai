export type Message = {
  role: "user" | "assistant";
  content: string;
};

export type Memory = {
  id: number;
  title: string;
  content: string;
  created_at: string;
};

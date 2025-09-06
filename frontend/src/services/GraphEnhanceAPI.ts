

import { PruneResult } from "../types";
import { commonAPI } from "./CommonAPI";

const baseURL = import.meta.env.VITE_HOST_URL || "http://127.0.0.1:8000";

export const pruneGraphAPI = async (
  uri: string,
  userName: string,
  password: string,
  database: string,
  threshold: number
): Promise<PruneResult> => {
  const formData = new FormData();
  formData.append("uri", uri);
  formData.append("userName", userName);
  formData.append("password", password);
  formData.append("database", database);
  formData.append("threshold", threshold.toString());

  try {
    const response = await fetch(`${baseURL}/api/jointlk/prune-graph`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Graph pruning failed");
    }

    const result = await response.json();
    return result.data as PruneResult;
  } catch (error) {
    console.error("Error during graph pruning:", error);
    throw error;
  }
};
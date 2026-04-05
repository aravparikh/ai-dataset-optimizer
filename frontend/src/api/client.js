import axios from "axios";

const API = axios.create({ baseURL: "http://localhost:8000/api" });

export async function uploadFile(file) {
  const form = new FormData();
  form.append("file", file);
  const { data } = await API.post("/upload", form);
  return data;
}

export async function analyzeFile(fileId, targetColumn) {
  const { data } = await API.post("/analyze", {
    file_id: fileId,
    target_column: targetColumn || null,
  });
  return data;
}

export async function cleanFile(fileId, targetColumn, scaleNumeric) {
  const { data } = await API.post("/clean", {
    file_id: fileId,
    target_column: targetColumn || null,
    scale_numeric: scaleNumeric,
  });
  return data;
}

export function downloadUrl(fileId) {
  return `http://localhost:8000/api/download/${fileId}`;
}

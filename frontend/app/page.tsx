"use client";

import { useState } from "react";

type Source = {
  source: string;
  page: number;
};

export default function Home() {
  // -----------------------------
  // Document state
  // -----------------------------
  const [file, setFile] = useState<File | null>(null);
  const [uploadedFile, setUploadedFile] = useState("");
  const [documentId, setDocumentId] = useState("");

  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState("");

  // -----------------------------
  // Question state
  // -----------------------------
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState<Source[]>([]);
  const [loading, setLoading] = useState(false);

  // -----------------------------
  // Upload PDF
  // -----------------------------
  const uploadDocument = async () => {
    if (!file) {
      setMessage("Please select a PDF first.");
      return;
    }

    setUploading(true);
    setMessage("");
    setAnswer("");
    setSources([]);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://127.0.0.1:8000/upload", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok || !data.success) {
        throw new Error(data.message || "Upload failed");
      }

      // Save document information
      setUploadedFile(data.filename);
      setDocumentId(data.document_id);

      setMessage(
        `✓ ${data.filename} indexed successfully (${data.chunks} chunks)`,
      );
    } catch (error) {
      console.error(error);

      setMessage("Unable to upload the PDF. Make sure the backend is running.");
    } finally {
      setUploading(false);
    }
  };

  // -----------------------------
  // Ask question
  // -----------------------------
  const askQuestion = async () => {
    if (!question.trim()) return;

    if (!documentId) {
      setAnswer("Please upload a PDF before asking a question.");
      return;
    }

    setLoading(true);
    setAnswer("");
    setSources([]);
    setMessage("");

    try {
      const response = await fetch("http://127.0.0.1:8000/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question,
          document_id: documentId,
        }),
      });

      if (!response.ok) {
        throw new Error("Question request failed");
      }

      const data = await response.json();

      setAnswer(data.answer);
      setSources(data.sources || []);
    } catch (error) {
      console.error(error);

      setAnswer(
        "Unable to connect to DocuMind. Make sure the backend is running.",
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-slate-950 text-white">
      {/* ========================= */}
      {/* NAVBAR */}
      {/* ========================= */}

      <nav className="border-b border-slate-800">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-5">
          <div>
            <h1 className="text-2xl font-bold">DocuMind</h1>

            <p className="text-xs text-slate-400">AI Document Intelligence</p>
          </div>
        </div>
      </nav>

      {/* ========================= */}
      {/* MAIN */}
      {/* ========================= */}

      <section className="mx-auto max-w-4xl px-6 pb-20 pt-16">
        {/* ========================= */}
        {/* HERO */}
        {/* ========================= */}

        <div className="text-center">
          <div className="mb-6 inline-block rounded-full border border-slate-700 px-4 py-2 text-sm text-slate-300">
            Your documents, now searchable.
          </div>

          <h2 className="text-5xl font-bold tracking-tight">
            Chat with your documents.
          </h2>

          <p className="mx-auto mt-6 max-w-2xl text-lg leading-8 text-slate-400">
            Upload a PDF and ask questions. DocuMind finds relevant information
            and generates grounded answers with source citations.
          </p>
        </div>

        {/* ========================= */}
        {/* UPLOAD CARD */}
        {/* ========================= */}

        <div className="mt-12 rounded-2xl border border-dashed border-slate-700 bg-slate-900 p-8 text-center">
          <div className="text-5xl">📄</div>

          <h3 className="mt-4 text-xl font-semibold">Upload your PDF</h3>

          <p className="mt-2 text-sm text-slate-500">
            Your document is processed locally.
          </p>

          {/* File input */}

          <input
            type="file"
            accept=".pdf,application/pdf"
            onChange={(e) => {
              const selectedFile = e.target.files?.[0] || null;

              setFile(selectedFile);

              setMessage("");

              // Reset previous document
              setUploadedFile("");
              setDocumentId("");
              setAnswer("");
              setSources([]);
            }}
            className="mx-auto mt-6 block w-full max-w-md rounded-lg border border-slate-700 bg-slate-800 p-3 text-sm text-slate-300 file:mr-4 file:rounded-md file:border-0 file:bg-white file:px-4 file:py-2 file:font-medium file:text-slate-950"
          />

          {/* Upload button */}

          <button
            onClick={uploadDocument}
            disabled={!file || uploading}
            className="mt-5 rounded-lg bg-white px-6 py-3 font-semibold text-slate-950 transition hover:bg-slate-200 disabled:cursor-not-allowed disabled:opacity-40"
          >
            {uploading ? "Indexing PDF..." : "Upload & Index"}
          </button>

          {/* Upload message */}

          {message && <p className="mt-4 text-sm text-slate-400">{message}</p>}

          {/* Active document */}

          {uploadedFile && (
            <div className="mx-auto mt-5 flex max-w-md items-center justify-between rounded-lg border border-slate-700 bg-slate-800 px-4 py-3 text-left">
              <div>
                <p className="text-xs text-slate-500">Active document</p>

                <p className="mt-1 truncate text-sm font-medium text-slate-200">
                  {uploadedFile}
                </p>
              </div>

              <span className="text-green-400">✓</span>
            </div>
          )}
        </div>

        {/* ========================= */}
        {/* QUESTION */}
        {/* ========================= */}

        <div className="mt-8">
          <label className="mb-3 block text-sm font-medium text-slate-300">
            Ask your document
          </label>

          <textarea
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                askQuestion();
              }
            }}
            placeholder={
              uploadedFile
                ? "What would you like to know?"
                : "Upload a PDF first..."
            }
            disabled={!uploadedFile}
            className="h-32 w-full resize-none rounded-xl border border-slate-700 bg-slate-900 p-5 text-white outline-none placeholder:text-slate-500 focus:border-slate-400 disabled:cursor-not-allowed disabled:opacity-50"
          />

          <button
            onClick={askQuestion}
            disabled={loading || !uploadedFile || !question.trim()}
            className="mt-4 w-full rounded-xl bg-white py-3 font-semibold text-slate-950 transition hover:bg-slate-200 disabled:cursor-not-allowed disabled:opacity-40"
          >
            {loading ? "DocuMind is thinking..." : "Ask DocuMind →"}
          </button>
        </div>

        {/* ========================= */}
        {/* ANSWER */}
        {/* ========================= */}

        {answer && (
          <div className="mt-8 rounded-2xl border border-slate-800 bg-slate-900 p-6">
            <div className="mb-5 flex items-center gap-2">
              <span className="text-xl">✨</span>

              <h3 className="font-semibold">Answer</h3>
            </div>

            <p className="leading-7 text-slate-300">{answer}</p>

            {/* Sources */}

            {sources.length > 0 && (
              <div className="mt-6 border-t border-slate-800 pt-5">
                <h4 className="text-sm font-semibold">📚 Sources</h4>

                <div className="mt-3 flex flex-wrap gap-2">
                  {sources.map((source, index) => (
                    <span
                      key={`${source.source}-${source.page}-${index}`}
                      className="rounded-lg bg-slate-800 px-3 py-2 text-xs text-slate-400"
                    >
                      {source.source} · Page {source.page}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* ========================= */}
        {/* ARCHITECTURE */}
        {/* ========================= */}

        <div className="mt-12 rounded-2xl border border-slate-800 bg-slate-900 p-6">
          <h3 className="font-semibold">How DocuMind works</h3>

          <div className="mt-5 grid grid-cols-2 gap-3 text-center text-sm md:grid-cols-5">
            <div className="rounded-lg bg-slate-800 p-4">
              🧠
              <p className="mt-2 text-slate-400">Planner</p>
            </div>

            <div className="rounded-lg bg-slate-800 p-4">
              🔍
              <p className="mt-2 text-slate-400">Retriever</p>
            </div>

            <div className="rounded-lg bg-slate-800 p-4">
              🗄️
              <p className="mt-2 text-slate-400">ChromaDB</p>
            </div>

            <div className="rounded-lg bg-slate-800 p-4">
              ✍️
              <p className="mt-2 text-slate-400">Answerer</p>
            </div>

            <div className="rounded-lg bg-slate-800 p-4">
              🛡️
              <p className="mt-2 text-slate-400">Validator</p>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}

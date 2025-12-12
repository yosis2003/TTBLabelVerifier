import { useState } from "react";

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [results, setResults] = useState<any | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError(null);
    setResults(null);

    if (!file) {
      setError("Please upload an image file.");
      return;
    }

    const form = e.currentTarget;
    const formData = new FormData();

    // Important: backend expects field named "file"
    formData.append("file", file);
    formData.append("brandName", (form.elements.namedItem("brandName") as HTMLInputElement).value || "");
    formData.append("productType", (form.elements.namedItem("productType") as HTMLInputElement).value || "");
    formData.append("abv", (form.elements.namedItem("abv") as HTMLInputElement).value || "");
    formData.append("netContents", (form.elements.namedItem("netContents") as HTMLInputElement).value || "");

    try {
      setLoading(true);

      const res = await fetch("http://localhost:8080/api/upload", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        const text = await res.text();
        throw new Error(`Server error: ${res.status} ${text}`);
      }

      const data = await res.json();
      console.log("Server response:", data);
      setResults(data);
    } catch (err: any) {
      console.error("Upload failed:", err);
      setError(err?.message || "Upload failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      {/* Logo */}
      <div className="mb-6">
        <img src="/logo.svg" alt="Logo" className="h-12" />
      </div>

      <div className="flex gap-8">
        {/* Left: Form */}
        <div className="bg-white rounded-2xl shadow-xl p-8 w-[420px] h-[720px] overflow-auto shrink-0">
          <h1 className="text-2xl font-bold mb-6">Submit Your Information</h1>

          <form onSubmit={handleSubmit} className="space-y-4" noValidate>
            <div>
              <label className="block mb-1 font-medium">Brand Name</label>
              <input
                type="text"
                name="brandName"
                className="w-full p-3 border rounded-xl focus:outline-none focus:ring"
                placeholder="Corona, Modelo, etc."
              />
            </div>

            <div>
              <label className="block mb-1 font-medium">Product Type</label>
              <input
                type="text"
                name="productType"
                className="w-full p-3 border rounded-xl focus:outline-none focus:ring"
                placeholder="Cabernet Sauvignon, Bourbon Whiskey, etc."
              />
            </div>

            <div>
              <label className="block mb-1 font-medium">Alcohol by Volume Percentage (ABV %)</label>
              <input
                type="number"
                step="0.1"
                name="abv"
                className="w-full p-3 border rounded-xl focus:outline-none focus:ring"
                placeholder="Enter number only"
              />
            </div>

            <div>
              <label className="block mb-1 font-medium">Net Contents</label>
              <input
                type="number"
                name="netContents"
                className="w-full p-3 border rounded-xl focus:outline-none focus:ring"
                placeholder="Enter total content in mL"
              />
            </div>

            <div>
              <label className="block mb-1 font-medium">Upload Label Photo</label>
              <input
                type="file"
                accept=".jpg,.jpeg,.png,.gif,.webp,image/jpeg,image/png,image/gif,image/webp"
                onChange={(e) => setFile(e.target.files ? e.target.files[0] : null)}
                name="file" /* <- important: backend expects "file" */
                className="w-full p-3 border rounded-xl focus:outline-none focus:ring"
              />
            </div>



            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 text-white py-3 rounded-xl hover:bg-blue-700 transition disabled:opacity-60"
            >
              {loading ? "Uploading..." : "Submit"}
            </button>

            {error && <p className="text-red-600 mt-2">{error}</p>}
          </form>
        </div>

        {/* Right side: Results */}
        <div className="flex-1 p-8 text-gray-600 text-lg">
          {results ? (
            <div className="space-y-4">
              <h2 className="text-2xl font-bold mb-4">Analysis Results</h2>

              <div>
                <h3 className="font-semibold">Brand Match:</h3>
                <p>{results.comparisons?.brand?.message ?? "No brand comparison returned."}</p>
              </div>

              <div>
                <h3 className="font-semibold">Alcohol Type Match:</h3>
                <p>{results.comparisons?.type?.message ?? "No type comparison returned."}</p>
              </div>

              <div>
                <h3 className="font-semibold">ABV Match:</h3>
                <p>{results.comparisons?.abv?.message ?? "No ABV comparison returned."}</p>
              </div>

              <div>
                <h3 className="font-semibold">Volume Match:</h3>
                <p>{results.comparisons?.volume?.message ?? "No volume comparison returned."}</p>
              </div>

              <div>
                <h3 className="font-semibold">Full OCR Output:</h3>
                <pre className="whitespace-pre-wrap bg-gray-200 p-3 rounded-xl text-sm">
                  {(results.ocr_output && results.ocr_output.join("\n")) || "No OCR output"}
                </pre>
              </div>

              {results.filename && (
                <div>
                  <h3 className="font-semibold">Uploaded File:</h3>
                  <p>{results.filename}</p>
                </div>
              )}
            </div>
          ) : (
            <p>Additional content will go here.</p>
          )}
        </div>
      </div>
    </div>
  );
}

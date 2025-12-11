import { useState } from "react";

export default function UploadPage() {
  const [file, setFile] = useState(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!file) {
      alert("Please select a file first.");
      return;
    }
    // Handle form submission logic here
    console.log("Form submitted", { file });("Form submitted!");
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      {/* Logo */}
      <div className="mb-6">
        
        <img src="/logo.svg" alt="Logo" className="h-12" />

      </div>

      <div className="flex gap-8">
        {/* Left: Form */}
        <div className="bg-white rounded-2xl shadow-xl p-8 w-full max-w-lg">
          <h1 className="text-2xl font-bold mb-6">Submit Your Information</h1>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block mb-1 font-medium">Brand Name</label>
              <input
                type="text"
                className="w-full p-3 border rounded-xl focus:outline-none focus:ring"
                placeholder="Corona, Modelo, Yousif's Alcohol Conglomerate, etc."
                required
              />
            </div>

            <div>
              <label className="block mb-1 font-medium">Product Type</label>
              <input
                type="text"
                className="w-full p-3 border rounded-xl focus:outline-none focus:ring"
                placeholder="Cabernet Sauvignon, Bourbon Whiskey, etc."
                required
              />
            </div>

            <div>
              <label className="block mb-1 font-medium">Alcohol by Volume Percentage</label>
              <input
                type="email"
                className="w-full p-3 border rounded-xl focus:outline-none focus:ring"
                placeholder="Enter number only"
                required
              />
            </div>

            <div>
              <label className="block mb-1 font-medium">Net Contents</label>
              <input
                type="tel"
                className="w-full p-3 border rounded-xl focus:outline-none focus:ring"
                placeholder="Enter total content in mL"
                required
              />
            </div>

            <div>
              <label className="block mb-1 font-medium">Upload Label Photo</label>
              <input
                type="file"
                onChange={(e) => setFile(e.target.files[0])}
                className="w-full p-3 border rounded-xl focus:outline-none focus:ring"
                required
              />
            </div>

            {/* Checkbox to download log */}
            <div className="flex items-center gap-3">
              <input type="checkbox" id="downloadLog" className="h-5 w-5" />
              <label htmlFor="downloadLog" className="font-medium">Download Log After Submission</label>
            </div>

            <button
              type="submit"
              className="w-full bg-blue-600 text-white py-3 rounded-xl hover:bg-blue-700 transition"
            >
              Submit
            </button>
          </form>
        </div>

        {/* Right side placeholder content */}
        <div className="flex-1 p-8 text-gray-600 text-lg">
          {/* Placeholder for future additions */}
          <p>Additional content will go here.</p>
        </div>
      </div>
    </div>
  );
}

function scanMessage() {
  const text = document.getElementById("inputText").value;
  const result = document.getElementById("result");

  if (text.trim().length < 10) {
    result.innerHTML = "❌ Please enter a valid message to scan.";
    result.style.color = "#ff6b6b";
    return;
  }

  const scamKeywords = [
    "free",
    "urgent",
    "win",
    "click",
    "offer",
    "lottery",
    "prize",
    "limited",
    "congratulations"
  ];

  const isScam = scamKeywords.some(keyword =>
    text.toLowerCase().includes(keyword)
  );

  if (isScam) {
    result.innerHTML =
      "⚠️ Scam Alert: This message appears suspicious. Avoid sharing personal details.";
    result.style.color = "#ffb703";
  } else {
    result.innerHTML =
      "✅ Safe: No major scam indicators found in this message.";
    result.style.color = "#64ffda";
  }
}

function scanImage() {
  const imageInput = document.getElementById("imageInput");
  const imageResult = document.getElementById("imageResult");

  if (imageInput.files.length === 0) {
    imageResult.innerHTML = "❌ Please upload an image or screenshot.";
    imageResult.style.color = "#ff6b6b";
    return;
  }

  imageResult.innerHTML =
    "🖼️ Image received. OCR-based scam analysis will be implemented in future versions.";
  imageResult.style.color = "#64ffda";
}

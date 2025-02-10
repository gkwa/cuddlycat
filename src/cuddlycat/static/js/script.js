async function postYaml(index) {
  const resultDiv = document.getElementById(`result-${index}`);
  try {
    const response = await fetch("http://localhost:8080/incoming", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(yamlDataList[index]),
    });
    
    const data = await response.json();
    
    if (response.ok && data.status === "success") {
      resultDiv.className = "success";
      resultDiv.textContent = data.message + " Redirecting...";
      setTimeout(() => {
        window.location.href = yamlDataList[index].metadata.url;
      }, 1000);
    } else {
      throw new Error(data.detail || `HTTP error! status: ${response.status}`);
    }
  } catch (error) {
    resultDiv.className = "error";
    resultDiv.textContent = `Error posting data: ${error.message}`;
  }
}

function createYamlPreview(yamlData) {
  return `metadata:
  url: "${yamlData.metadata.url}"
  title: "${yamlData.metadata.title}"
  timestamp: "${yamlData.metadata.timestamp}"
  savedAt: "${yamlData.metadata.savedAt}"
  uuid: "${yamlData.metadata.uuid}"
content:
  encoding: ${yamlData.content.encoding}
  mimeType: ${yamlData.content.mimeType}
  data: ${yamlData.content.data}`;
}

function renderYamlList() {
  console.log('Rendering YAML list...'); // Debug log
  const container = document.getElementById("yaml-container");
  if (!container) {
    console.error('Container not found!'); // Debug log
    return;
  }
  
  yamlDataList.forEach((yamlData, index) => {
    console.log('Creating section for index:', index); // Debug log
    const yamlSection = document.createElement("div");
    yamlSection.className = "yaml-section";
    yamlSection.innerHTML = `
      <h2>YAML Entry ${index + 1}</h2>
      <a href="#" class="button" onclick="postYaml(${index}); return false;">POST YAML Data ${index + 1}</a>
      <div id="result-${index}" class="result"></div>
      <pre class="yaml-preview">${createYamlPreview(yamlData)}</pre>
    `;
    container.appendChild(yamlSection);
  });
}

// Add error handling for DOMContentLoaded
document.addEventListener("DOMContentLoaded", () => {
  console.log('DOM Content Loaded'); // Debug log
  renderYamlList();
});

// Also try immediate execution in case DOMContentLoaded already fired
if (document.readyState === 'complete') {
  console.log('Document already loaded, rendering immediately'); // Debug log
  renderYamlList();
}

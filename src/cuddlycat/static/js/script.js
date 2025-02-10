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
  data: ${yamlData.content.data}`
}

async function postYaml(index) {
  const resultDiv = document.getElementById(`result-${index}`)
  try {
    const response = await fetch("http://localhost:8080/incoming", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(yamlDataList[index]),
    })
    if (response.ok) {
      resultDiv.className = "success"
      resultDiv.textContent = "Data successfully posted!"
    } else {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
  } catch (error) {
    resultDiv.className = "error"
    resultDiv.textContent = `Error posting data: ${error.message}`
  }
}

function renderYamlList() {
  const container = document.getElementById("yaml-container")
  yamlDataList.forEach((yamlData, index) => {
    const yamlSection = document.createElement("div")
    yamlSection.className = "yaml-section"
    yamlSection.innerHTML = `
      <h2>YAML Entry ${index + 1}</h2>
      <a href="#" class="button" onclick="postYaml(${index}); return false;">POST YAML Data ${index + 1}</a>
      <div id="result-${index}" class="result"></div>
      <pre class="yaml-preview">${createYamlPreview(yamlData)}</pre>
    `
    container.appendChild(yamlSection)
  })
}

// Initialize the page
document.addEventListener("DOMContentLoaded", renderYamlList)

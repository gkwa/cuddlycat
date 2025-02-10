console.log("Loading script.js...")

async function postYaml(index) {
  const business = businesses.businesses[index]
  const resultDiv = document.getElementById(`result-${index}`)

  try {
    const response = await fetch("http://localhost:8080/incoming", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(business),
    })

    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`)
    }

    const data = await response.json()

    resultDiv.className = "success"
    if (business.yelp_url) {
      resultDiv.innerHTML = `${data.message}<br><a href="${business.yelp_url}" target="_blank">Click here to view on Yelp</a>`
    } else {
      resultDiv.textContent = `${data.message} (No Yelp page available)`
    }
  } catch (error) {
    resultDiv.className = "error"
    resultDiv.textContent = `Error posting data: ${error.message}`
  }
}

function createBusinessPreview(business) {
  return `Business Info:
  Name: "${business.business_name}"
  Matched Name: "${business.matched_name}"
  UUID: "${business.uuid}"
  Message: "${business.message}"
  ${business.yelp_url ? `Yelp URL: "${business.yelp_url}"` : 'No Yelp URL available'}`
}

function renderBusinessList() {
  console.log("renderBusinessList called")
  const container = document.getElementById("yaml-container")
  if (!container) {
    console.error("Container not found!")
    return
  }
  
  console.log("Found container, businesses:", businesses)
  
  businesses.businesses.forEach((business, index) => {
    console.log(`Creating section for business: ${index}`)
    const section = document.createElement("div")
    section.className = "yaml-section"
    
    const hasYelpUrl = business.yelp_url && business.yelp_url.length > 0
    const buttonText = hasYelpUrl ? 
      `POST and View on Yelp` : 
      `POST Business Data`
    
    section.innerHTML = `
      <h2>${business.business_name}</h2>
      <a href="#" class="button" onclick="postYaml(${index}); return false;">${buttonText}</a>
      <div id="result-${index}" class="result"></div>
      <pre class="yaml-preview">${createBusinessPreview(business)}</pre>
    `
    container.appendChild(section)
  })
}

// Call renderBusinessList when the DOM is loaded
document.addEventListener("DOMContentLoaded", function() {
  console.log("DOMContentLoaded fired")
  renderBusinessList()
})

// Backup call in case DOMContentLoaded already fired
if (document.readyState === "complete") {
  console.log("Document already complete, calling renderBusinessList")
  renderBusinessList()
}

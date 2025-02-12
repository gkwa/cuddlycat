console.log("Loading script.js...")

let businesses = { businesses: [] }

async function loadBusinesses() {
  try {
    const response = await fetch("http://localhost:8080/api/businesses")
    businesses = await response.json()
    renderBusinessList()
  } catch (error) {
    console.error("Error loading businesses:", error)
  }
}

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
    const message = {
      action: 'setUUID',
      uuid: business.uuid
    };
    window.postMessage(message, '*');

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
  
  container.innerHTML = ''
  
  businesses.businesses.forEach((business, index) => {
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

document.addEventListener("DOMContentLoaded", loadBusinesses)

if (document.readyState === "complete") {
  loadBusinesses()
}


async function postYaml() {
  const resultDiv = document.getElementById("result")

  try {
    const response = await fetch("http://localhost:8080/incoming", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(yamlData),
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

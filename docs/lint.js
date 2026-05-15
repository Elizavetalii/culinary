function validateClientData(client){
  const requiredFields = ["name", "phone", "email"]
  let isValid = true

  for (const field of requiredFields){
    if (!client[field]) {
      isValid = false
      console.log("Missing field:", field)
    }
  }

  const normalizedPhone = client.phone ? client.phone.replace(/\s+/g, "") : ""

  return {
    isValid:isValid,
    normalizedPhone: normalizedPhone,
  }
}

const demoClient = {
  name: "OOO Art Culinary",
  phone: "+7 900 123 45 67",
  email: "",
}

validateClientData(demoClient)

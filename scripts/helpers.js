const cleanJsonResponse = (response) => {
  var jsonText = response.data.response;
  // Step 1: Remove <json> tags and newline escape characters
  jsonText = jsonText
    .replace("<json>", "")
    .replace("</json>", "")
    .replace("\\n", "");
  // Step 2: Parse the cleaned JSON text
  const jsonObject = JSON.parse(jsonText);
  // Step 3: Format the JSON with indentation
  const formattedJson = JSON.stringify(jsonObject, null, 2);
  // Output the formatted JSON
  console.log(formattedJson);
  return formattedJson;
};

module.exports = {
  cleanJsonResponse,
};

// Function to simulate searching and displaying results
function searchPapers() {
  question = document.getElementById("search").value
  code = document.getElementById("code").value
  console.log(code)


    const params = new URLSearchParams({
    code: code,
    question: question,
});



    fetch(`/search?${params}`)
  .then((response) => response.json())
  .then((json) => display_result(json));

}


function display_result(json) {
  console.log(json)
  const ul = document.querySelector('ul'); // Select the <ul> element

  // Loop through and remove all <li> elements
  while (ul.firstChild) {
      ul.removeChild(ul.firstChild);
  }


  for (i = 0; i < json["metadata"].length; i+=1) {
      console.log(i)
      const newLi = document.createElement('li');

      const newA = document.createElement('a');
      newA.href = json["metadata"][i]["url"]; // Set the href attribute of the <a> element
      newA.textContent = json["document"][i]; // Set the text inside the <a> element

      newLi.appendChild(newA);

      ul.appendChild(newLi);
  }
}
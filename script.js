async function fetchVideo(){

let url = document.getElementById("videoURL").value

let result = document.getElementById("videoResult")

result.innerHTML = "Fetching video..."

try{

let response = await fetch("http://localhost:3000/download",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({url:url})

})

let data = await response.json()

if(data.error){

result.innerHTML="Failed to fetch video"

return

}

let html = `
<h3>${data.title}</h3>

<img class="thumbnail" src="${data.thumbnail}">
<h4>Download Options</h4>
`

data.formats.forEach(f=>{

html += `
<a href="${f.url}" target="_blank">
<button class="download-btn">
Download ${f.quality}
</button>
</a>
`

})

result.innerHTML = html

}

catch(err){

result.innerHTML="Server error"

}

}
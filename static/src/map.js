/*global L */
var map = L.map('map').setView([0, 0], 13);
L.tileLayer('https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    className: 'map-tiles'
}).addTo(map);
var layerGroup = L.layerGroup().addTo(map);

function http_get(url, callback, headers=[], method="GET", content=null) {
  let request = new XMLHttpRequest();
  request.addEventListener("load", callback);
  request.open(method, url, true);
  for (const header of headers) {
    request.setRequestHeader(header[0], header[1]);
  }
  request.send(content);
}

var query_input = document.getElementById("query_input");
var suggestions_list = document.getElementById("suggestions_list");
var results_div = document.getElementById("results");

var old_content = "";
var queued_request = null;
var current_path = "";

function get_addresses(query) {
  let url = `/api/search_locations/?query=${query}`;
  http_get(url, function(){
    let data = JSON.parse(this.responseText).data;
    suggestions_list.innerHTML = "";
    if (!suggestions_list.className.includes(" hidden")){
      suggestions_list.className += " hidden"
    }
    for (let entry of data) {
      let option = document.createElement("li");
      option.className = "p-2 border border-black-500"

      let link = document.createElement("a");
      link.innerHTML = entry.name;
      link.data = entry;
      link.href = "#"
      link.onclick = function(){set_location(this.data)}

      option.appendChild(link)
      suggestions_list.appendChild(option);
      suggestions_list.className = suggestions_list.className.replace(" hidden", "");
    }
    if (queued_request != query) {
      get_addresses(queued_request)
    }
    else {
      queued_request = null;
    }
  });
}

function update() {
  let content = query_input.value;
  if (content == old_content) {
    return;
  }
  old_content = content;

  if (content != "") {
    if (queued_request == null) {
      get_addresses(content);
      queued_request = content;
    }
    queued_request = content;
  }
  else {
    suggestions_list.innerHTML = "";
  }

}

function set_location(data, page=1) {
  suggestions_list.className += " hidden";
  current_path = data.url;

  let url = `/api/location?path=${data.url}&page=${page}`;
  http_get(url, function(){
    show_data(JSON.parse(this.responseText));
  })
}

function show_data(data) {
  let page_count = data.full["listing/search/metadata"].totalPages
  let geography = data.full["geography/geo-entity"].institution
  map.setView([geography.latitude, geography.longitude], 13)

  for (let listing of data.full["listing/search/list"]) {
    let div = document.createElement("div");

    let img = document.createElement("img");
    img.src = listing.media.mainPhoto.source;
    img.style.width = "100%";

    let title = document.createElement("p");
    title.innerHTML = listing.name;

    div.appendChild(img);
    div.appendChild(title);
    results_div.appendChild(div)
  }
}

query_input.onchange = update;
query_input.onkeydown = update;

http_get("/api/ip/", function(){
  let data = JSON.parse(this.responseText);
  let loc_split = data.loc.split(",")
  map.setView([parseFloat(loc_split[0]), parseFloat(loc_split[1])], 10)
})
function init(){
  magazines.map((magazine, idx) => {
      let url = `https://api.rss2json.com/v1/api.json?rss_url=${magazine}`;
      console.log(url)
      fetchCardData(url, idx);
  });
}

async function fetchCardData(url, idx){
  await fetch(url)
        .then((res) => res.json())
        .then((data) => {fillCarousel(data.items, idx);})
        .catch((err) => {console.log(err) });
}

function fillCarousel(datas, idx){

  let id = "collapse";

  if(idx == 0){
    id += "Zero"; 
  }else if(idx == 1){
      id += "One";
  }else if(idx == 2){
      id += "Two";
  }else if(idx == 3){
      id += "Three";
  }else if(idx == 4){
    id += "Four";
  }else if(idx == 5){
    id += "Five";
  }

  let html = `<div id="carouselExampleIndicators${idx}" class="carousel slide" data-ride="carousel">
                  <div class="carousel-inner">`;

  datas.map((data, jdx) => {
      if(jdx == 0)
      {
          html += `<div class="carousel-item active">
                      <div class="card" style="width: 100%;">
                          <a href="${data.link}"><img class="card-img-top" style="padding: 40px;" height="500px" width="100%" 
                          src="${data.enclosure.link}" alt="Card image cap"></a>
                          <div class="card-body">
                              <h5 class="card-title">${data.title}<br>
                              ${data.author} &nbsp;<h9 style="font-family: Montserrat;
                                  font-style: normal;
                                  font-weight: 600;
                                  font-size: 14px;
                                  line-height: 24px;
                                  letter-spacing: 0.2px;
                                  color: #586069;">${new Date(data.pubDate).toDateString()}</h9></h5>
                              <p class="card-text">${data.content}</p>
                          </div>
                      </div>
                  </div>`
      }
      else
      {
          html += `<div class="carousel-item">
                      <div class="card" style="width: 100%;">
                          <a href="${data.link}"><img class="card-img-top" style="padding: 40px;" height="500px" width="100%" src="${data.enclosure.link}" alt="Card image cap"></a>
                          <div class="card-body">
                              <h5 class="card-title">${data.title}<br>
                              ${data.author} &nbsp;<h9 style="font-family: Montserrat;
                                  font-style: normal;
                                  font-weight: 600;
                                  font-size: 14px;
                                  line-height: 24px;
                                  letter-spacing: 0.2px;
                                  color: #586069;">${new Date(data.pubDate).toDateString()}</h9></h5>
                              <p class="card-text">${data.content}</p>
                          </div>
                      </div>
                  </div>`
      }
  })
  html += `</div>
              <div class="carousel-control-prev" href="#carouselExampleIndicators${idx}" role="button" data-slide="prev">
              <span class="carousel-control-prev-icon" aria-hidden="true"></span>
              <span class="sr-only">Previous</span>
              </div>
              <div class="carousel-control-next" href="#carouselExampleIndicators${idx}" role="button" data-slide="next">
              <span class="carousel-control-next-icon" aria-hidden="true"></span>
              <span class="sr-only">Next</span>
              </div>
          </div>`;
document.getElementById(id).innerHTML = html;
}
//export {init};
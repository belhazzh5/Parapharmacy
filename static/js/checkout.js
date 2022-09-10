let myBtns = document.getElementsByClassName("update-card")
let myItems = document.getElementById("item-count")

for (let i = 0; i < myBtns.length; i++) {
    myBtns[i].addEventListener('click',function(){
        let product_id = this.dataset.product
        let action = this.dataset.action
        if (action == "add")
        {
            x = Number(myItems.textContent)
            myItems.textContent = String(x+1)
            let msg = funSucc("alert" ,"alert-success","Medicament ajouter au cart!");
            setTimeout(() => {
                msg.style.opacity = 0
                msg.style.display = "none"
            }, 600);
        }
        if (action == "remove"){
            delete cart[product_id]
    }
        if (action == "delete"){
            if (cart[product_id]!=""){
            if (cart[product_id]["quantite"] <= 1) {
                    delete cart[product_id]
                }
                else{
                    cart[product_id]["quantite"]-=1
                }
            let msg = funSucc("alert","alert-danger","Medicament supprimer de carte!");
            setTimeout(() => {
             msg.style.opacity = 0
             msg.style.display = "none"
            }, 600);
        }
        }
  document.cookie = 'cart=' + JSON.stringify(cart) + ";domaine=;path=/"
        if (user === 'AnonymousUser')
        addCookieItem(product_id,action)
        else
        updateUserOrder(product_id,action)
    })   
}

function funSucc(c1,c2,msg){
    let myDiv = document.createElement("div")
    let mySpan = document.createElement("span")
    myDiv.classList.add(c1)
    myDiv.classList.add(c2)
    myDiv.classList.add("position-absolute")
    let text = document.createTextNode(msg)
    mySpan.appendChild(text)
    myDiv.appendChild(mySpan)
    document.body.prepend(myDiv)
    myDiv.style.opacity = "0.6";
    myDiv.style.transition = "0.5s"
    myDiv.style.zIndex = "9999999999"
    return myDiv
      }



function updateUserOrder(product_id,action){
    var url = '/update_item/'
    fetch(
        url,{
            method:'POST',
            headers:{
                'Content-Type':'application/json',
                'X-CSRFToken': csrftoken,
            },
            body:JSON.stringify({'product_id':product_id,'action':action})
        }
        )
        .then((response)=>{
            return response.json()
        })
        .then((data)=>{
            
        })
    }
    
    function addCookieItem(productId,action) {
    if (action == "add"){
        if (cart[productId] == undefined){
            cart[productId] = {'quantite':1}
        }
        
        else{
            cart[productId]['quantite'] +=1
        }
        if (action == "delete"){
    //     if (cart[productId]["quantite"] <=0) {
    //         delete cart[productId]
    //     }
    //     else{
    //     cart[productId]["quantite"]-=1
    //     console.log("removed!")
    // }
}

    }
}


  
  function getCookie(cname) {
    let name = cname + "=";
    let ca = document.cookie.split(';');
    for(let i = 0; i < ca.length; i++) {
      let c = ca[i];
      while (c.charAt(0) == ' ') {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }
    return "";
  }
  
  function setCookie(cname, cvalue, exdays) {
    const d = new Date();
    d.setTime(d.getTime() - (exdays*24*60*60*1000));
    let expires = "expires="+ d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
  }

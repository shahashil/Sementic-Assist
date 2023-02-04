
/*
const query = "Reading and Writing";
//const to_replace = prompt("Enter your search Query", "What is the ...");
const text = document.querySelectorAll("h1,h2,p,a")

var delayInMilliseconds = 10000; //1 second

setTimeout(function() {
    for(let i=0;i<text.length;i++)
    {
    if(text[i].innerHTML.includes(query)){
    text[i].innerHTML = text[i].innerHTML.replace(query,"<span id ='high' style='background-color:#ffff66' >"+to_replace+"</span>");        
    }
    }

    const element = document.getElementById("high");
element.scrollIntoView();
}, delayInMilliseconds);
*/

function extractContent(s, space) {
    var span= document.createElement('span');
    span.innerHTML= s;
    if(space) {
      var children= span.querySelectorAll('*');
      for(var i = 0 ; i < children.length ; i++) {
        if(children[i].textContent)
          children[i].textContent+= ' ';
        else
          children[i].innerText+= ' ';
      }
    }
    return [span.textContent || span.innerText].toString().replace(/ +/g,' ');
  };

chrome.runtime.onMessage.addListener(msgObj => {

    const url = window.location.href;
    // To find if the request is made for a YT video
    const pattern1 = /www.youtube.com/g;
    // True if website is of YT
    const result1 = pattern1.test(url);

    if (!result1) {

        async function Demo(query_data) {

            let data = {
                query: query_data
            }
            const setting = {
                method: 'POST',
                mode: 'cors',
                body: JSON.stringify(data)
            };

            try {
                var str_found = false;
                const text = document.querySelectorAll("h1,h2,p,a,li,ul");
                const fetchResponse = await fetch('http://127.0.0.1:5000/text', setting);
                const resul = await fetchResponse.text();
                if (resul != 'none') {

                    const query = resul;
                    for (let i = 0; i < text.length; i++) {
                        if ((extractContent(text[i].innerHTML)).includes(resul)) {
                            text[i].innerHTML = text[i].innerHTML.replace(text[i].innerHTML, "<span id ='high' style='background-color:#ffff66' >" + text[i].innerHTML + "</span>");
                            str_found = true;
                        }                       
                    }
                    if(!str_found){
                        window.alert("Not Found");
                    }

                    const element = document.getElementById("high");
                    element.scrollIntoView();                    



                }

            } catch (e) {
                window.alert("Error " + e);
            }
        }

        Demo({ url, msgObj });

    } 


    
    else 



    {

        async function Demo(query_data) {

            let data = {
                query: query_data
            }
            const setting = {
                method: 'POST',
                mode: 'cors',
                body: JSON.stringify(data)
            };

            try {
                const text = document.querySelectorAll("h1,h2,p,a,li,ul");
                const fetchResponse = await fetch('http://127.0.0.1:5000/yt', setting);
                const resul = await fetchResponse.text();

                if (resul != 'none') {

                    const text = document.querySelectorAll("span");
                    for (let i = 0; i < text.length; i++) {
                        if (extractContent(text[i].innerHTML).includes("Comments")) {
                            text[i].innerHTML = text[i].innerHTML.replace(text[i].innerHTML,"Comments <a href='"+query_data.url+'&t='+resul+"'  id='conew'></a>");
                        }
                    }
                    document.getElementById('conew').click();
                }

            } catch (e) {
                window.alert("Error " + e);
            }
        }
        Demo({ url, msgObj });

    }

});






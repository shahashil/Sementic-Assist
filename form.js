document.addEventListener('DOMContentLoaded', function() {
    const input_button = document.getElementById('inputButton');

    input_button.addEventListener('click',function(){


        var input_text = document.getElementById('inputText').value;
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
          chrome.tabs.sendMessage(tabs[0].id, input_text, function(response){});
        });



        
    });
    });
    
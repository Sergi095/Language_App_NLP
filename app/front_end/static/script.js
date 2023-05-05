const inputLanguageSelector = document.getElementById('input-language-selector');
const outputLanguageSelector = document.getElementById('output-language-selector');

// When input language selector changes, set output language to the opposite
inputLanguageSelector.addEventListener('change', function() {
    if (inputLanguageSelector.value === 'English') {
        outputLanguageSelector.value = 'Spanish';
    } else if (inputLanguageSelector.value === 'Spanish') {
        outputLanguageSelector.value = 'English';
    }
});

// When output language selector changes, set input language to the opposite
outputLanguageSelector.addEventListener('change', function() {
    if (outputLanguageSelector.value === 'English') {
        inputLanguageSelector.value = 'Spanish';
    } else if (outputLanguageSelector.value === 'Spanish') {
        inputLanguageSelector.value = 'English';
    }
});

document.addEventListener("DOMContentLoaded", function() {
    var translateButton = document.getElementById("translate-button");
    var recordButton = document.getElementById("record-button");
    var inputText = document.getElementById("input_text");
    var outputText = document.getElementById("output_text");
    var inputLanguageSelector = document.getElementById("input-language-selector");
    var outputLanguageSelector = document.getElementById("output-language-selector");
  
    translateButton.addEventListener("click", function() {
      var inputSentence = inputText.value;
      var inputLanguage = inputLanguageSelector.value;
      var outputLanguage = outputLanguageSelector.value;
      var xhr = new XMLHttpRequest();
      xhr.open("POST", "/translate", true);
      xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
      xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
          var response = JSON.parse(xhr.responseText);
          outputText.value = response.translation;
        }
      };
      xhr.send("input_text=" + inputSentence + "&input_language_selector=" + inputLanguage + "&output_language_selector=" + outputLanguage);
    });
  
    recordButton.addEventListener("click", function() {
      var inputLanguage = inputLanguageSelector.value;
      var outputLanguage = outputLanguageSelector.value;
      var xhr = new XMLHttpRequest();
      xhr.open("POST", "/translate", true);
      xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
      xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
          var response = JSON.parse(xhr.responseText);
          outputText.value = response.translation;
          inputText.value = response.input_text;
        }
      };
      xhr.send("input_language_selector=" + inputLanguage + "&output_language_selector=" + outputLanguage + "&record=true");
    });
  });

  function translate() {
    // get the input text from the input-text box
    var inputText = document.getElementById("input_text").value;
    // get the selected language options
    var inputLang = document.getElementById("input-language-selector").value;
    var outputLang = document.getElementById("output-language-selector").value;

    // if recording is enabled, add the recorded text to the input-text box
    if (document.getElementById('record-toggle').checked) {
        inputText = document.getElementById('recorded-text').value;
    }

    // make a POST request to the /translate endpoint with the input text and selected languages
    fetch('/translate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: new URLSearchParams({
        'input_text': inputText,
        'input_language_selector': inputLang,
        'output_language_selector': outputLang
      })
    })
    .then(response => response.json())
    .then(data => {
      // set the output text in the output-text box
      document.getElementById("output_text").value = data.output_text;
      // set the input text in the input-text box (for transcription)
      document.getElementById("input_text").value = data.input_text;
    });
  
  }
  
